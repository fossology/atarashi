#!/usr/bin/env python3
"""Decide `-only` against `-or-later` where the references cannot.

All 17 `X-only` / `X-or-later` pairs in the merged license list carry **byte-identical
reference text** — the distinction is not in the license, it is in how a file adopts
it ("either version 2 of the License, or (at your option) any later version"). So a
matcher scoring query against reference is choosing between them on no evidence, and
loses roughly half the time. Measured on the Software Heritage tail sample, all four
`-only` licenses were answered as `-or-later`; on the head corpora 35 of 122 raw
top-1 errors are this one distinction.

**The obvious rule is the wrong one, and it was measured before being kept.** Reading
"or (at your option) any later version" out of the query predicts the correct side on
93.6% of DEP-5 notice queries where it fires — but wiring it in changed DEP-5 by
nothing at all (the notice layer already carries *separate* rules for the two sides, so
the matcher can tell them apart there) and made the Software Heritage tail *worse*,
0.682 -> 0.652. A whole license body quotes that exact wording in its "How to apply"
appendix, so every GPL body reads as or-later, including the ones that are not.

What is left is the case that actually fails: a **bare license body**, where the two
references are identical and the file contains no election at all. "Or later" is
something an author opts into, so a body on its own is `-only` — which is how SPDX,
ScanCode and the Software Heritage annotators all label it. That rule needs no
threshold: the matched unit is the body exactly when its length equals the license's
full text.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import re

# "or (at your option) any later version" and its common spellings, plus the SPDX and
# FOSSology suffixes a file may carry directly.
_LATER = re.compile(r"""
    (?:any\s+later\s+version)
  | (?:or\s*\(\s*at\s+your\s+option\s*\)\s*any\s+later)
  | (?:either\s+version\s+[\d.]+\s*,?\s*or)
  | (?:version\s+[\d.]+\s+or\s+(?:any\s+)?later)
  | (?:[\w.-]+-or-later\b)
  | (?:\b[al]?gpl[-\s]?[\d.]+\+)
""", re.IGNORECASE | re.VERBOSE | re.DOTALL)

# An explicit refusal of later versions. Checked first, and only honoured when no
# later-signal is present: a file that says both is quoting the license body and
# declaring its own choice, and the declaration is the "or later" one.
_ONLY = re.compile(r"""
    (?:version\s+[\d.]+\s+only\b)
  | (?:[\w.-]+-only\b)
  | (?:of\s+the\s+License\s*,?\s*(?:but\s+)?not\s+(?:any\s+)?later)
""", re.IGNORECASE | re.VERBOSE | re.DOTALL)

_ONLY_SUFFIX = "-only"
_LATER_SUFFIX = "-or-later"


def later_signal(text: str) -> bool | None:
    """``True`` for or-later, ``False`` for only, ``None`` when the text does not say.

    ``None`` is the common case and must stay a real answer: guessing a side on a file
    that never states one is how this distinction got lost in the first place.
    """
    joined = " ".join(text.split())
    if _ONLY.search(joined) and not _LATER.search(joined):
        return False
    if _LATER.search(joined):
        return True
    return None


def sibling(shortname: str) -> str | None:
    """The other side of an only/or-later pair, or None if the name is not one side."""
    if shortname.endswith(_ONLY_SUFFIX):
        return shortname[: -len(_ONLY_SUFFIX)] + _LATER_SUFFIX
    if shortname.endswith(_LATER_SUFFIX):
        return shortname[: -len(_LATER_SUFFIX)] + _ONLY_SUFFIX
    return None


def corrected(shortname: str, matched_body: bool,
              known: frozenset[str] | set[str]) -> str:
    """``-only`` when a bare license body matched, otherwise ``shortname`` untouched.

    ``matched_body`` says the unit that won is the license's own full text, which is
    the only situation where the two siblings are indistinguishable by evidence.
    Anywhere else the notice layer has distinct rules for the two sides and its answer
    stands.
    """
    if not matched_body or not shortname.endswith(_LATER_SUFFIX):
        return shortname
    other = shortname[: -len(_LATER_SUFFIX)] + _ONLY_SUFFIX
    return other if other in known else shortname
