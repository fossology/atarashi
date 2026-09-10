#!/usr/bin/env python3
"""Cascade agent: SPDX tag, then verbatim text, then span match, else UNKNOWN.

SPDX-License-Identifier: GPL-2.0-only
"""
import os

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.body import split_terms
from atarashi.libs.commentPreprocessor import CommentPreprocessor
from atarashi.libs.decision import (DEFAULT_MIN_COVERAGE, DEFAULT_STRONG_RUN,
                                    is_confident, unknown_result)
from atarashi.libs.gate import should_scan
from atarashi.libs.normalize import tokens
from atarashi.libs.orlater import corrected as orlater_corrected
from atarashi.libs.ranker import (DEFAULT_ACCEPT, DEFAULT_AMBIGUOUS_MARGIN,
                                  load_ranker, score_candidates)
from atarashi.libs.references import expression_components, load_notice_units
from atarashi.libs.sequence import (DEFAULT_MIN_RUN, DEFAULT_TOP_K, LicenseMatcher,
                                    tied_with_leader)
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
                 use_ranker=True, ranker_path=None, top_k=None):
        super().__init__(licenseList, verbose)
        self.min_run = min_run
        self.strong_run = strong_run
        self.min_coverage = min_coverage
        self.top_k = DEFAULT_TOP_K if top_k is None else top_k
        self.use_gate = use_gate
        self.use_notices = use_notices
        self.notice_path = notice_path
        # Absent artifact => None => the hand-tuned ordering stands.
        self.ranker = load_ranker(ranker_path) if use_ranker else None
        # The ranker standardises features *within* the candidate list, so list length
        # is part of its training distribution and an artifact is only valid at the
        # depth it was fit for. Running one at another depth is silent and severe —
        # raising top_k 5 -> 20 at inference alone cost tail R@1 0.818 -> 0.652 — so
        # the artifact carries its depth and it wins over the default. An explicit
        # `top_k=` argument still overrides, which is what the sweep needs.
        if top_k is None:
            self.top_k = int(self.ranker.get("top_k", DEFAULT_TOP_K)) if self.ranker \
                else DEFAULT_TOP_K
        self.matcher = LicenseMatcher(self._reference_units())
        # Token length of each license's own body, so a match can be recognised as
        # "the file *is* this license" rather than "the file cites it". That is the
        # only case where -only and -or-later are indistinguishable; see libs/orlater.
        # It is the *grant* that has to match, not grant-plus-appendix: the trailer is
        # instructions to the licensor, and a file that omits it is still the license.
        self._body_tokens = {
            str(row["shortname"]): len(tokens(split_terms(str(row["processed_text"]))[0]))
            for _, row in self.licenseList.iterrows()}

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
            # The grant and its "how to apply these terms" appendix are indexed as
            # separate units. Real LICENSE files routinely stop at END OF TERMS AND
            # CONDITIONS, and carrying the appendix inside the body made the license's
            # own reference longer than a file that *is* that license — which handed
            # Apache-2.0 files to `Pixar`, an Apache-2.0 copy without the appendix.
            # See libs/body.py.
            grant, appendix = split_terms(str(row["processed_text"]))
            yield (name, grant)
            if appendix:
                yield (name, appendix)
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
                     "sim_score": 1.0, "expression": exact, "description": ""}]

        hits, evidence = self.matcher.match_with_evidence(
            text, min_run=self.min_run, top_k=self.top_k)
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
            # Model-dependent, so it travels in the artifact: a flatter score
            # distribution turns the same fixed margin into false ambiguity, which
            # costs exact-set on answers that were never in doubt.
            margin = self.ranker.get("ambiguous_margin", DEFAULT_AMBIGUOUS_MARGIN)
            if len(scores) > 1 and scores[0] - scores[1] < margin:
                near = [h for h, s in zip(ranked, scores)
                        if scores[0] - s < margin]
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
            known = frozenset(str(n) for n in self.licenseList["shortname"])

            def resolve(name: str, hit) -> str:
                body = self._body_tokens.get(name) == hit.ref_tokens
                return orlater_corrected(name, body, known)

            def note_for(name: str) -> str:
                others = [n for n in ambiguous if n != name]
                return ("; ambiguous with " + ", ".join(others)
                        + " — the evidence does not separate them") if others else ""

            # A compound unit matched one span but attests to several licenses, so it
            # expands to one result per component, each carrying the whole expression
            # — the same contract the SPDX-tag path already emits. Reporting only the
            # leading license would drop the exception that makes the grant what it
            # is. Every result keeps the span of the unit that matched, because that
            # single span is the evidence for the whole expression.
            # The only/or-later siblings share a byte-identical reference text, so
            # when the *body* is what matched, the evidence cannot separate them and
            # a bare body is -only. See libs/orlater.py, including the query-side
            # rule that looks obvious and measured worse.
            def components(name: str) -> list[str]:
                """A key's licenses, best-supported first.

                An expression names several licenses and the engine reports all of
                them, but the first one is what a top-1 consumer reads. Taking it
                from the order the rule's author wrote the expression in is a coin
                flip: a plain BSD-2-Clause file matching a `GPL-2.0-only OR
                BSD-2-Clause` rule was reported as GPL-2.0-only, with BSD-2-Clause
                second, on 16 files in the prevalence pool.

                The query itself settles it. `evidence` carries, for every key the
                matcher aligned, how completely the query filled that license's own
                units — so a component the file independently supports leads, and one
                that appears only inside the compound rule follows. Order alone
                changes; the set is untouched, so this cannot alter exact-set.
                """
                parts = expression_components(name)
                if len(parts) < 2:
                    return parts
                return sorted(parts, key=lambda c: -evidence.get(c, 0.0))

            return [{"shortname": resolve(component, h),
                     "sim_type": "Ambiguous" if ambiguous else "SequenceCoverage",
                     "sim_score": round(h.score, 4),
                     "expression": h.shortname,
                     "matched_start": h.char_start, "matched_end": h.char_end,
                     "matched_text": text[h.char_start:h.char_end],
                     "description": f"matched chars {h.char_start}:{h.char_end} "
                                    f"(run {h.longest_run} tokens)"
                                    f"{note_for(h.shortname)}"}
                    for h in confident
                    for component in components(h.shortname)]

        return [unknown_result(round(hits[0].score, 4) if hits else 0.0)]
