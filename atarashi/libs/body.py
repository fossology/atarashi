#!/usr/bin/env python3
"""Split a licence body into its grant and its instructional trailer.

Eighteen licences in the merged list — Apache-2.0, ECL-2.0, the SHL pair, and the
whole GPL/LGPL/AGPL family — end with a section addressed to the *licensor* rather
than the licensee: "APPENDIX: How to apply the Apache License to your work",
"How to Apply These Terms to Your New Programs". It tells an author how to attach the
licence to their code. It is not part of the grant, and SPDX marks where it starts
with the line ``END OF TERMS AND CONDITIONS``.

Indexing it as part of the body is a measurable defect, because real ``LICENSE``
files often stop at that line. Then the licence's own reference is *longer* than the
file that is verbatim that licence, and coverage — matched reference tokens over
reference tokens — reads far below 1.0:

    query: a real Apache-2.0 LICENSE file with no appendix
      Apache-2.0   run 764  coverage 0.889  ref_tail 177   <- 177 unmatched
      Pixar        run 752  coverage 0.984  ref_tail 0     <- wins

``Pixar`` is "Modified Apache 2.0", which is Apache-2.0's terms *without* the
appendix, so it fits the file exactly and takes the answer. That cost 19 of
Apache-2.0's 37 errors on the prevalence pool, and the same shape runs through the
GPL family, where the trailer is up to 20.7% of the body (GPL-1.0).

The appendix is kept as a *separate* unit rather than discarded: a file that does
carry it should still match, and the boilerplate it contains ("Licensed under the
Apache License, Version 2.0 … you may not use this file except in compliance") is a
real notice register in its own right. Splitting rather than truncating also means no
evidence leaves the index, so the change can only move which unit wins.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import re

# The SPDX-conventional end-of-grant marker. Matched on raw text with flexible
# whitespace, because the reference bodies keep their original line wrapping.
_END_OF_TERMS = re.compile(r"end\s+of\s+terms\s+and\s+conditions", re.IGNORECASE)

# A trailer shorter than this is not worth its own unit — it is a sign-off line, not
# an appendix, and a reference below the matcher's shingle floor cannot match anyway.
MIN_TRAILER_TOKENS = 40


def split_terms(text: str) -> tuple[str, str | None]:
    """``(grant, appendix)`` — the appendix is ``None`` when there is no real trailer.

    Splits at the *last* ``END OF TERMS AND CONDITIONS``; the marker itself stays with
    the grant, since it is the closing line of the terms. Text that does not carry the
    marker, or whose trailer is too short to index, comes back unchanged as
    ``(text, None)``, so every other licence in the list is untouched.
    """
    if not text:
        return text, None
    matches = list(_END_OF_TERMS.finditer(text))
    if not matches:
        return text, None
    cut = matches[-1].end()
    trailer = text[cut:]
    if len(trailer.split()) < MIN_TRAILER_TOKENS:
        return text, None
    return text[:cut], trailer
