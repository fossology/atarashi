#!/usr/bin/env python3
"""Token-sequence license matcher with matched-span and coverage scoring.

The core of the native cascade: identify which reference license text is present in
an input by aligning normalized token sequences and scoring by how much of the
reference is covered. This is the algorithm class production scanners (ScanCode,
askalono) use — bag-of-words similarity was shown to plateau on this task.

Two paths:
  * ``exact`` — O(1) hash lookup when the whole input is a known license text.
  * ``match`` — span alignment with coverage in [0, 1] for embedded notices/text.

Alignment is seed-and-extend over shared shingles, not a general diff. A shared
n-gram is a *seed*; seeds on the same diagonal (equal ``query_pos - ref_pos``) are
consecutive pieces of one contiguous run, so walking the reference once and grouping
seeds by diagonal recovers every common run of >= ``shingle`` tokens in roughly
O(len(reference)). The previous implementation ran a full ``difflib.SequenceMatcher``
per candidate, which is O(n*m) and dominated scan time by an order of magnitude.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace

from atarashi.libs.normalize import normalize, token_spans, tokens


# A match must contain at least one contiguous run of this many tokens — a
# distinctive license phrase — so scattered common-word overlap does not match.
# References shorter than this are exempt but must match in full; see `match`.
DEFAULT_MIN_RUN = 8

# Alignment seeds on n-grams, so this is the shortest reference that can be matched
# at all. Also the floor for indexing a reference unit: anything shorter is unusable.
DEFAULT_SHINGLE = 3

# Shingles are packed positionally into one int key. The base must be fixed before
# indexing starts — deriving it from vocabulary size would re-key every unit as the
# vocabulary grew — so it is a constant comfortably above any license vocabulary.
_BASE = 1 << 21

# Only the strongest candidates are aligned. Candidates are ranked by how many
# distinct shingles they share with the query, which upper-bounds the run length
# they can produce, so a unit far down that ranking cannot win. Generous by design:
# alignment is now cheap enough that the cap is a safety rail, not a tuning knob.
DEFAULT_MAX_CANDIDATES = 200

# How many ranked candidates leave the matcher. Five was never swept: measured on the
# Software Heritage tail, five of the six queries whose correct licence was "missing
# from retrieval" in fact sat at ranks 15-46, so most of what looked like an index gap
# was this truncation. The ranker normalises features *within* the candidate list, so
# this cannot be raised at inference alone — the model has to be refit at the same
# depth. See the engine report.
DEFAULT_TOP_K = 5


@dataclass(frozen=True)
class SpanMatch:
    """One reference matched within the query token stream."""

    shortname: str
    score: float  # coverage of the reference (matched / ref_tokens), in [0, 1]
    longest_run: int  # longest contiguous matched token run — the ranking signal
    matched_tokens: int
    ref_tokens: int
    start: int  # matched span start token index in the query (inclusive)
    end: int  # matched span end token index in the query (exclusive)
    char_start: int  # matched span start, character offset into the query text
    char_end: int  # matched span end, character offset into the query text
    required_ok: bool = True  # every phrase the rule marks as required is present

    # Signals below are computed on the way to the fields above and were previously
    # discarded. They are what separates close variants: two candidates can tie on
    # run and coverage while disagreeing completely on *how* they failed to match.
    # Evidence from the license's OTHER units, which selecting one winner discards.
    # A license whose best-covered unit the query fills completely is better
    # supported than one covering 70% of a shorter unit, even when the retained
    # unit's longest run is a token shorter — that is exactly how
    # mpl-2.0-no-copyleft-exception was beating MPL-2.0.
    best_unit_coverage: float = 0.0  # highest coverage any unit of this license reached
    units_matched: int = 1  # how many of its units matched at all

    run_count: int = 1  # matched runs after chaining; 1 = one clean block
    ref_gap: int = 0  # reference tokens between runs that the query does not have
    query_gap: int = 0  # query tokens between runs that the reference does not have
    ref_head: int = 0  # reference tokens before the first run
    ref_tail: int = 0  # reference tokens after the last run
    shingle_ratio: float = 0.0  # shared shingles / this unit's distinct shingles
    query_coverage: float = 0.0  # matched tokens / query length

    @property
    def substitution(self) -> int:
        """Tokens where query and reference both have text, and it differs.

        A pure deletion (`ref_gap` with no `query_gap`) means the reference says
        something the query never does — an or-later clause the file omits. A pure
        insertion is the reverse. Both differing at once is a substitution, which is
        what a changed version digit looks like.
        """
        return min(self.ref_gap, self.query_gap)


class LicenseMatcher:
    """Match input text against a fixed set of reference license texts."""

    def __init__(self, references: Iterable[tuple[str, str]],
                 shingle: int = DEFAULT_SHINGLE,
                 required: Iterable[tuple[str, list[str]]] | None = None,
                 max_candidates: int = DEFAULT_MAX_CANDIDATES,
                 unit_gating: bool = False):
        self.shingle = shingle
        self.max_candidates = max_candidates
        self.unit_gating = unit_gating
        # Tokens are interned to ints once, so alignment compares machine integers
        # rather than strings and shingles pack into a single int key.
        self._vocab: dict[str, int] = {}
        # A license may have several reference units (full text, header/notice, …),
        # so units are stored by index and mapped back to a shortname.
        self._unit_name: list[str] = []
        self._unit_ids: list[list[int]] = []
        # Shingle keys per unit, cached at index time. Recomputing them per candidate
        # was the single largest remaining cost once alignment stopped being O(n*m).
        self._unit_keys: list[list[int]] = []
        self._index: dict[int, set[int]] = {}
        self._exact: dict[str, str] = {}
        # Key phrases that MUST appear in the input for a reference to match — the
        # lever that keeps generic boilerplate from matching and separates close
        # variants (e.g. an "Affero"/version clause). Empty => no gating.
        self._required: dict[str, list[str]] = {
            name: [" ".join(tokens(p)) for p in phrases if tokens(p)]
            for name, phrases in (required or [])
        }
        # Per-unit required phrases, from the `{{...}}` spans ScanCode marks in its
        # rules. Off by default: measured on 246 notice queries, gating on them cost
        # precision 0.9289 -> 0.9121 and R@1 0.9024 -> 0.8862. It does separate close
        # variants — it fixed three EPL-1.0/EPL-2.0 confusions — but it broke five
        # more, because dropping a license's strongest unit hands the query to a
        # competing license rather than to abstention. Kept, tested, and available:
        # the phrases are the right signal, a hard per-unit filter is the wrong use
        # of it. Enable with `unit_gating=True`.
        self._unit_required: list[list[str]] = []
        for reference in references:
            name, text = reference[0], reference[1]
            phrases = reference[2] if len(reference) > 2 else ()
            toks = tokens(text)
            if not toks:
                continue
            self._exact.setdefault(normalize(text), name)
            ids = [self._intern(t) for t in toks]
            keys = self._keys(ids)
            uid = len(self._unit_name)
            self._unit_name.append(name)
            self._unit_ids.append(ids)
            self._unit_keys.append(keys)
            self._unit_required.append(
                [" ".join(tokens(p)) for p in phrases if tokens(p)])
            for key in set(keys):
                self._index.setdefault(key, set()).add(uid)

    def _intern(self, token: str) -> int:
        ident = self._vocab.get(token)
        if ident is None:
            ident = len(self._vocab)
            if ident >= _BASE:
                raise ValueError(f"vocabulary exceeded {_BASE} terms; raise _BASE")
            self._vocab[token] = ident
        return ident

    def _keys(self, ids: list[int]) -> list[int]:
        """Pack each ``shingle``-gram into one int key, positionally.

        Positional encoding in base ``_BASE``, so distinct n-grams get distinct
        keys — exact, not a hash, so there are no collisions to guard against.
        """
        n, out = self.shingle, []
        for i in range(len(ids) - n + 1):
            key = 0
            for j in range(i, i + n):
                key = key * _BASE + ids[j] + 1
            out.append(key)
        return out

    def _query_ids(self, toks: list[str]) -> list[int]:
        """Query tokens as ids; unseen tokens get -1, which no reference contains."""
        return [self._vocab.get(t, -1) for t in toks]

    def _has_required(self, name: str, q_joined: str) -> bool:
        phrases = self._required.get(name)
        if not phrases:
            return True
        return all(f" {p} " in q_joined for p in phrases)

    def _unit_has_required(self, uid: int, q_joined: str) -> bool:
        """Every phrase the rule marks as required must appear in the query."""
        return all(f" {p} " in q_joined for p in self._unit_required[uid])

    def exact(self, query: str) -> str | None:
        """Return a shortname when the whole normalized input equals a reference."""
        return self._exact.get(normalize(query))

    def _runs(self, ref_keys: list[int], qpos: dict[int, list[int]]):
        """Every common run of >= ``shingle`` tokens, as (ref_start, q_start, length).

        Walks the reference once. A seed at reference position ``i`` matching query
        position ``j`` lies on diagonal ``j - i``; a run is a maximal stretch of
        consecutive seeds on one diagonal, so the previous step's diagonals are all
        that must be carried forward.
        """
        n = self.shingle
        prev: dict[int, tuple[int, int, int]] = {}
        runs: list[tuple[int, int, int]] = []
        for i, key in enumerate(ref_keys):
            cur: dict[int, tuple[int, int, int]] = {}
            for j in qpos.get(key, ()):
                d = j - i
                seed = prev.get(d)
                cur[d] = (seed[0], seed[1], seed[2] + 1) if seed else (i, j, 1)
            for d, run in prev.items():
                if d not in cur:
                    runs.append(run)
            prev = cur
        runs.extend(prev.values())
        # A run of c consecutive shingles spans c + n - 1 tokens.
        return [(si, sj, c + n - 1) for si, sj, c in runs]

    def match(self, query: str, min_run: int = DEFAULT_MIN_RUN,
              top_k: int = DEFAULT_TOP_K) -> list[SpanMatch]:
        """The best reference matches within ``query``; see ``match_with_evidence``."""
        return self.match_with_evidence(query, min_run, top_k)[0]

    def match_with_evidence(
            self, query: str, min_run: int = DEFAULT_MIN_RUN,
            top_k: int = DEFAULT_TOP_K) -> tuple[list[SpanMatch], dict[str, float]]:
        """Return the best reference matches, plus per-key evidence for all of them.

        The second value maps every key the matcher aligned — plain license or whole
        expression — to the best coverage any of its units reached, including the keys
        that did not make ``top_k``. A compound candidate needs it: reporting
        ``GPL-2.0-only OR BSD-2-Clause`` means naming both licenses, and which of them
        to name *first* is answered by which one the query supports on its own units,
        not by the order somebody wrote the expression in.

        Ranked by the longest contiguous matched run.

        Ranking by the longest run (not coverage) rewards a distinctive license
        phrase over scattered common-word overlap, and is robust to references of
        different lengths. A license with several units (full text + header/notice)
        is reported once, keeping its strongest unit.

        ``score`` is the fraction of *distinct* reference tokens covered by some run
        of at least ``shingle`` tokens. Isolated common words do not contribute, so
        it reads lower than a general-diff coverage would, and means something
        sharper: how much of the reference literally appears in the query.
        """
        spans = token_spans(query)
        q_tokens = [tok for tok, _, _ in spans]
        if len(q_tokens) < self.shingle:
            return [], {}
        q_ids = self._query_ids(q_tokens)
        q_joined = f" {' '.join(q_tokens)} "

        qpos: dict[int, list[int]] = {}
        counts: dict[int, int] = {}
        for j, key in enumerate(self._keys(q_ids)):
            qpos.setdefault(key, []).append(j)
        for key in qpos:
            for uid in self._index.get(key, ()):
                counts[uid] = counts.get(uid, 0) + 1
        if not counts:
            return [], {}
        # Shared-shingle count bounds the achievable run, so the tail cannot win.
        candidates = sorted(counts, key=counts.get, reverse=True)[:self.max_candidates]

        best: dict[str, SpanMatch] = {}
        corroboration: dict[str, tuple[float, int]] = {}
        for uid in candidates:
            name = self._unit_name[uid]
            if not self._has_required(name, q_joined):
                continue
            required_ok = self._unit_has_required(uid, q_joined)
            if self.unit_gating and not required_ok:
                continue
            ref = self._unit_ids[uid]
            runs = self._runs(self._unit_keys[uid], qpos)
            if not runs:
                continue
            longest = max(size for _, _, size in runs)
            # A reference shorter than min_run cannot produce a qualifying run, which
            # made the whole short-reference register unmatchable — "Licensed under
            # the Apache License, Version 2.0" is seven tokens, and 700 of the 1,339
            # apache-2.0 rules are shorter than eight. Such a reference is admitted
            # only when the query contains it *in full*: the run must span the entire
            # reference, which is the same bar ScanCode sets with per-rule coverage.
            if longest < min(min_run, len(ref)):
                continue
            chained = _chain(runs)
            covered = sum(size for _, _, size in chained)
            start = min(sj for _, sj, _ in chained)
            end = max(sj + size for _, sj, size in chained)
            gaps = _gaps(chained, len(ref))
            cand = SpanMatch(
                name, covered / len(ref), longest, covered, len(ref),
                start, end, spans[start][1], spans[end - 1][2], required_ok,
                run_count=len(chained), ref_gap=gaps[0], query_gap=gaps[1],
                ref_head=gaps[2], ref_tail=gaps[3],
                shingle_ratio=counts[uid] / max(len(set(self._unit_keys[uid])), 1),
                query_coverage=covered / len(q_tokens))
            corroboration[name] = (max(corroboration.get(name, (0.0, 0))[0], cand.score),
                                   corroboration.get(name, (0.0, 0))[1] + 1)
            prev = best.get(name)
            if prev is None or _rank(cand) > _rank(prev):
                best[name] = cand
        # Longest contiguous run first (distinctive phrase); ties broken by coverage
        # so the reference the query most fully fills (e.g. MIT over an MIT-superset
        # like Xnet/X11) wins over a looser superset match.
        merged = [replace(m, best_unit_coverage=corroboration[name][0],
                          units_matched=corroboration[name][1])
                  for name, m in best.items()]
        results = sorted(merged, key=_rank, reverse=True)
        evidence = {name: cov for name, (cov, _) in corroboration.items()}
        return results[:top_k], evidence


def _rank(match: SpanMatch) -> tuple[int, float, bool]:
    """Ranking key: longest run, then coverage, then required phrases satisfied.

    Longest run first: a distinctive license phrase beats scattered common-word
    overlap, and it is independent of reference length. Coverage second, so the
    reference the query most fully fills wins over a looser superset — MIT over an
    MIT-superset like Xnet/X11.

    Coverage's preference for shorter references is load-bearing, not a defect.
    Replacing it with "prefer the larger reference on equal evidence" — on the theory
    that resolving toward the broader license is the safer way to be wrong — was
    measured and is much worse: precision 0.929 → 0.775. It costs far more than the
    narrow-variant confusions it fixes.

    Required-phrase satisfaction is last: it only breaks exact ties, which were
    previously resolved arbitrarily. As a hard filter it measured as a net loss —
    see the note in ``LicenseMatcher.__init__``.
    """
    return (match.longest_run, match.score, match.required_ok)


def _gaps(chained: list[tuple[int, int, int]], ref_len: int) -> tuple[int, int, int, int]:
    """(ref_gap, query_gap, ref_head, ref_tail) over the chained runs.

    Walked in reference order. Between consecutive runs, the reference may skip
    tokens the query does not supply and the query may carry tokens the reference
    does not — the two are different facts and the pair of them is where a variant
    clause lives, so they are counted separately rather than as one edit distance.
    """
    ordered = sorted(chained)  # by reference start
    ref_gap = query_gap = 0
    for (ri, qi, size), (rj, qj, _) in zip(ordered, ordered[1:]):
        ref_gap += max(0, rj - (ri + size))
        query_gap += max(0, qj - (qi + size))
    head = ordered[0][0]
    tail = ref_len - (ordered[-1][0] + ordered[-1][2])
    return ref_gap, query_gap, head, max(0, tail)


def tied_with_leader(matches: list[SpanMatch]) -> list[SpanMatch]:
    """The best match, plus any the matcher genuinely cannot distinguish from it.

    Acceptance is per-candidate: a match is confident if its own run or coverage
    clears a bar. Nothing compares it to the leader. Because close variants are near
    token-supersets of each other, several clear the bar at once on the same text —
    an unambiguous EPL-1.0 notice reported EPL-1.0, BSD-3-Clause, Apache-2.0,
    GPL-2.0 and LGPL-2.1, all "confident". Measured on the DEP-5 corpus, 97% of
    answered files carried at least one license that was not theirs, at 4.72
    licenses reported per file.

    Reporting only exact ties on the ranking key keeps genuine ambiguity — where the
    evidence really is identical — and drops everything the ranking already
    separated. Exact-set accuracy goes 0.024 -> 0.763 on that corpus; top-1 is
    unchanged, which is why every earlier measurement missed this.
    """
    if not matches:
        return []
    key = _rank(matches[0])
    return [m for m in matches if _rank(m) == key]


def _chain(runs: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Select runs that overlap in neither the reference nor the query.

    Coverage must mean "how much of the reference is present in the query", which
    requires each query token to be spent once. Without that, a repetitive reference
    inflates: one query phrase matches at many reference offsets, each on its own
    diagonal, and summing them reports far more of the reference as present than is.

    Longest-first is the same greedy order ``difflib`` uses, so the selection stays
    close to the alignment this replaced. Run counts are small, so the quadratic
    overlap check costs nothing.
    """
    taken: list[tuple[int, int, int]] = []
    for run in sorted(runs, key=lambda r: -r[2]):
        si, sj, size = run
        if any(si < tsi + tsize and tsi < si + size or
               sj < tsj + tsize and tsj < sj + size
               for tsi, tsj, tsize in taken):
            continue
        taken.append(run)
    return taken
