#!/usr/bin/env python3
"""Cascade agent: SPDX tag, then verbatim text, then span match, else UNKNOWN.

SPDX-License-Identifier: GPL-2.0-only
"""
import os

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.commentPreprocessor import CommentPreprocessor
from atarashi.libs.decision import (DEFAULT_MIN_COVERAGE, DEFAULT_STRONG_RUN,
                                    is_confident, unknown_result)
from atarashi.libs.gate import should_scan
from atarashi.libs.ranker import (DEFAULT_ACCEPT, DEFAULT_AMBIGUOUS_MARGIN,
                                  load_ranker, score_candidates)
from atarashi.libs.references import load_notice_units
from atarashi.libs.sequence import DEFAULT_MIN_RUN, LicenseMatcher, tied_with_leader
from atarashi.spdx.resolver import detect_and_resolve


class Cascade(AtarashiAgent):
    """License identification cascade, precision first.

    Stages, each handling what the cheaper one could not, then abstaining:
      1. author-declared ``SPDX-License-Identifier`` (highest precision);
      2. exact normalized full-text match (input *is* a known license);
      3. token-sequence coverage match (license text embedded in the input);
      4. UNKNOWN — no confident match, rather than a low-confidence guess.

    Stages 2-3 run on the extracted comment block, not the raw file, so code is
    not matched as if it were license prose. Stage 1 runs on the raw text because
    a tag is a literal string that comment extraction may reformat.

    Abstention is the common outcome, not an edge case: on real source files
    carrying an SPDX tag, most have no license prose once the tag is stripped.
    """

    def __init__(self, licenseList, verbose=0, min_run=DEFAULT_MIN_RUN,
                 strong_run=DEFAULT_STRONG_RUN, min_coverage=DEFAULT_MIN_COVERAGE,
                 use_gate=True, use_notices=True, notice_path=None,
                 use_ranker=True, ranker_path=None):
        super().__init__(licenseList, verbose)
        self.min_run = min_run
        self.strong_run = strong_run
        self.min_coverage = min_coverage
        self.use_gate = use_gate
        self.use_notices = use_notices
        self.notice_path = notice_path
        # Absent artifact => None => the hand-tuned ordering stands.
        self.ranker = load_ranker(ranker_path) if use_ranker else None
        self.matcher = LicenseMatcher(self._reference_units())

    def _reference_units(self):
        """Every matchable unit: full texts, headers, and the notice layer.

        The notice layer is the decisive one. A license body is not what real source
        files carry, so indexing bodies alone identifies almost no real header
        (R@1 ~0.004 measured); the short-form rules are the register that actually
        occurs. Set ``use_notices=False`` to index only the caller's license list —
        tests with synthetic license lists want that isolation.
        """
        has_header = "processed_header" in self.licenseList.columns
        for _, row in self.licenseList.iterrows():
            name = str(row["shortname"])
            yield (name, str(row["processed_text"]))
            if has_header:
                header = row["processed_header"]
                if isinstance(header, str) and header.strip():
                    yield (name, header)
        if self.use_notices:
            yield from load_notice_units(self.licenseList["shortname"],
                                         path=self.notice_path)

    @staticmethod
    def _comment_text(filePath, fallback):
        """The license comment block, or ``fallback`` if extraction is unavailable.

        Returns the extracted text unnormalized; the matcher applies its own
        normalization to query and references alike, so the legacy
        ``CommentPreprocessor.preprocess`` transform is deliberately not used here
        (it rewrites "(c)" to "copyright", which references are not subject to).
        """
        commentFile = None
        try:
            commentFile = CommentPreprocessor.extract(filePath)
            with open(commentFile, errors="replace") as handle:
                text = handle.read()
            return text if text.strip() else fallback
        except Exception:
            return fallback
        finally:
            if commentFile and os.path.exists(commentFile):
                os.unlink(commentFile)

    def scan(self, filePath):
        """Scan ``filePath`` and return ranked result dicts (or one UNKNOWN)."""
        with open(filePath, errors="replace") as in_file:
            raw = in_file.read()

        spdx = detect_and_resolve(raw, self.licenseList["shortname"])
        if spdx:
            return spdx

        text = self._comment_text(filePath, raw)
        if self.use_gate and not should_scan(text):
            return [unknown_result()]

        exact = self.matcher.exact(text)
        if exact:
            return [{"shortname": exact, "sim_type": "ExactFullText",
                     "sim_score": 1.0, "description": ""}]

        hits = self.matcher.match(text, min_run=self.min_run)
        # The learned reject option replaces the run/coverage bar rather than stacking
        # on it: that bar reads only the retained unit, so it abstained on licenses
        # whose *other* units the query covered completely. Where the model has no
        # opinion — no artifact, or a license family it never trained on — the
        # hand-tuned rule still decides.
        scored = score_candidates(hits, self.ranker) if self.ranker else None
        ambiguous = ()
        if scored is not None:
            ranked, scores = scored
            tau = self.ranker.get("accept", DEFAULT_ACCEPT)
            if not scores or scores[0] < tau:
                return [unknown_result(round(scores[0], 4) if scores else 0.0,
                                       list(zip((h.shortname for h in ranked), scores)))]
            confident = tied_with_leader(ranked)
            # Candidates the model cannot separate are an ambiguity, not a pick, and
            # all of them are reported. Measured on the DEP-5 corpus, the correct
            # license was inside the flagged set in 8 of 8 cases while the leader
            # alone was right in none — so the set is the answer and the leader is
            # only its most likely member.
            #
            # Deliberately not collapsed to a license *family*. The pairs this catches
            # are GPL-2.0-or-later against GPL-3.0-or-later, and those are mutually
            # incompatible: "GPL" would be true of six of the eight and useful for
            # none of them.
            if len(scores) > 1 and scores[0] - scores[1] < DEFAULT_AMBIGUOUS_MARGIN:
                near = [h for h, s in zip(ranked, scores)
                        if scores[0] - s < DEFAULT_AMBIGUOUS_MARGIN]
                ambiguous = tuple(h.shortname for h in near)
                confident = near
        else:
            confident = tied_with_leader(
                [h for h in hits
                 if is_confident(h.score, h.longest_run, self.strong_run, self.min_coverage)])
        if confident:
            # Offsets are into the text that was scanned — the extracted comment
            # block when extraction succeeded, otherwise the file itself. The
            # matched excerpt is included because that is what an auditor reads,
            # and it stays meaningful either way.
            def note_for(name: str) -> str:
                others = [n for n in ambiguous if n != name]
                return ("; ambiguous with " + ", ".join(others)
                        + " — the evidence does not separate them") if others else ""

            return [{"shortname": h.shortname,
                     "sim_type": "Ambiguous" if ambiguous else "SequenceCoverage",
                     "sim_score": round(h.score, 4),
                     "matched_start": h.char_start, "matched_end": h.char_end,
                     "matched_text": text[h.char_start:h.char_end],
                     "description": f"matched chars {h.char_start}:{h.char_end} "
                                    f"(run {h.longest_run} tokens)"
                                    f"{note_for(h.shortname)}"}
                    for h in confident]

        return [unknown_result(round(hits[0].score, 4) if hits else 0.0)]
