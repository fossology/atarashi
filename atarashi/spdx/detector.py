#!/usr/bin/env python3
"""First-class SPDX-License-Identifier detection for Atarashi.

Author-declared `SPDX-License-Identifier:` tags are the strongest, highest-precision
license signal in real source files. Atarashi resolves them directly instead of
routing to text similarity, and returns nothing (abstains) when no tag is present.

Parses the SPDX license expression that follows the tag into its component license
ids and `WITH` exceptions, tolerating comment terminators, quotes, parentheses,
`AND`/`OR`/`WITH` operators and `+` (or-later) forms.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# The tag keyword is matched case-insensitively for recall; the expression follows.
_TAG = re.compile(r"SPDX-License-Identifier\s*:\s*(.+)", re.IGNORECASE)
# Trailing comment terminators that can follow the expression on the same line.
_COMMENT_CLOSE = re.compile(r"\s*(?:\*/|-->|--}}|#}|\?>|'''|\"\"\").*$")
_OPERATORS = frozenset({"AND", "OR"})
# A valid SPDX id token (license or exception), incl. `+` and LicenseRef/DocumentRef.
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+:-]*$")


@dataclass(frozen=True)
class SpdxMatch:
    """One detected SPDX-License-Identifier tag."""

    expression: str  # cleaned SPDX license expression, as written
    licenses: tuple[str, ...]  # component license ids, order-preserving, unique
    exceptions: tuple[str, ...]  # `WITH` exception ids, order-preserving, unique
    line: int  # 1-based line number of the tag


def _clean(raw: str) -> str:
    return _COMMENT_CLOSE.sub("", raw).strip().strip("\"'`").strip()


def _parse(expr: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Split an SPDX expression into (license ids, exception ids)."""
    tokens = expr.replace("(", " ").replace(")", " ").split()
    licenses: list[str] = []
    exceptions: list[str] = []
    expect_exception = False
    for tok in tokens:
        upper = tok.upper()
        if upper == "WITH":
            expect_exception = True
            continue
        if upper in _OPERATORS:
            expect_exception = False
            continue
        if not _ID.match(tok):
            continue  # drop stray comment/punctuation tokens
        if expect_exception:
            exceptions.append(tok)
            expect_exception = False
        else:
            licenses.append(tok)
    # order-preserving de-duplication
    return tuple(dict.fromkeys(licenses)), tuple(dict.fromkeys(exceptions))


def detect(text: str) -> list[SpdxMatch]:
    """Return every SPDX-License-Identifier tag in ``text``; empty list if none."""
    matches: list[SpdxMatch] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        found = _TAG.search(line)
        if not found:
            continue
        expression = _clean(found.group(1))
        licenses, exceptions = _parse(expression)
        if not licenses:
            continue  # a tag with no parseable license is not a confident match
        matches.append(SpdxMatch(expression, licenses, exceptions, lineno))
    return matches
