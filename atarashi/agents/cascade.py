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
from atarashi.libs.references import load_notice_units
from atarashi.libs.sequence import DEFAULT_MIN_RUN, LicenseMatcher
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
                 use_gate=True, use_notices=True, notice_path=None):
        super().__init__(licenseList, verbose)
        self.min_run = min_run
        self.strong_run = strong_run
        self.min_coverage = min_coverage
        self.use_gate = use_gate
        self.use_notices = use_notices
        self.notice_path = notice_path
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
        confident = [h for h in hits
                     if is_confident(h.score, h.longest_run,
                                     self.strong_run, self.min_coverage)]
        if confident:
            # Offsets are into the text that was scanned — the extracted comment
            # block when extraction succeeded, otherwise the file itself. The
            # matched excerpt is included because that is what an auditor reads,
            # and it stays meaningful either way.
            return [{"shortname": h.shortname, "sim_type": "SequenceCoverage",
                     "sim_score": round(h.score, 4),
                     "matched_start": h.char_start, "matched_end": h.char_end,
                     "matched_text": text[h.char_start:h.char_end],
                     "description": f"matched chars {h.char_start}:{h.char_end} "
                                    f"(run {h.longest_run} tokens)"}
                    for h in confident]

        return [unknown_result(round(hits[0].score, 4) if hits else 0.0)]
