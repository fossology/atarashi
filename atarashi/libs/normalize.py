#!/usr/bin/env python3
"""SPDX-style text normalization and tokenization for license matching.

Normalization follows the spirit of the SPDX license matching guidelines: fold
case, neutralize punctuation/quote/bullet variation, and collapse whitespace, so
that cosmetically different renderings of the same license text produce the same
token sequence. Used by the exact-hash and sequence matchers.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import re

# Curly quotes / dashes -> ASCII so quotes and hyphens don't split matches.
_TRANSLATE = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", " ": " ",
})
_PUNCT = re.compile(r"[^\w\s]+")
_WS = re.compile(r"\s+")
# A token is a maximal run of word characters: normalization turns everything that
# is neither word nor whitespace into a separator, so these runs are exactly what
# survives it. Matching them directly is what lets a token keep its source offsets.
_WORD = re.compile(r"\w+")


def normalize(text: str) -> str:
    """Return a case-folded, punctuation-stripped, whitespace-collapsed form."""
    text = text.translate(_TRANSLATE).lower()
    text = _PUNCT.sub(" ", text)
    return _WS.sub(" ", text).strip()


def token_spans(text: str) -> list[tuple[str, int, int]]:
    """``(token, start, end)`` for each token, offsets into ``text`` itself.

    Auditors need the span in the file, not an index into a normalized token
    stream, and normalization cannot supply it: collapsing punctuation and
    whitespace changes length, so offsets into the normalized form do not map
    back. The character translation applied first is one-for-one, so word-run
    offsets measured on it are offsets into the original.
    """
    prepared = text.translate(_TRANSLATE)
    return [(found.group(0).lower(), found.start(), found.end())
            for found in _WORD.finditer(prepared)]


def tokens(text: str) -> list[str]:
    """Normalized whitespace-delimited tokens of ``text``.

    Derived from :func:`token_spans` rather than from :func:`normalize` so the two
    cannot drift: a mismatch would silently misalign every reported span.
    """
    return [token for token, _, _ in token_spans(text)]
