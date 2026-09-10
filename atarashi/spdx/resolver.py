#!/usr/bin/env python3
"""Resolve detected SPDX license ids to FOSSology license shortnames.

Bridges the SPDX detector to Atarashi's result contract: a resolved tag is a
high-precision match (``sim_score`` 1.0, ``sim_type`` ``SPDXIdentifier``). Ids that
do not correspond to a known shortname are dropped, so the caller abstains rather
than inventing a license.

Each result also carries ``expression``: the whole SPDX expression the tag declared,
with known ids rewritten to their canonical shortname. A flat list of shortnames
cannot represent what the author actually said — ``MIT AND Apache-2.0`` and
``MIT OR Apache-2.0`` collapse to the same pair, and ``GPL-2.0 WITH
Classpath-exception-2.0`` loses the exception entirely, which changes what the
license permits. AND/OR/WITH is legally decisive, so it travels with the result.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import re
from collections.abc import Iterable

from atarashi.spdx.detector import SpdxMatch, detect

# Identifier-shaped tokens; everything else in the expression (spaces, parentheses)
# is left exactly as written so the declaration keeps its original shape.
_ID_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+:-]*")
_OPERATORS = frozenset({"AND", "OR", "WITH"})


def shortname_index(shortnames: Iterable[str]) -> dict[str, str]:
    return {s.lower(): s for s in shortnames if isinstance(s, str)}


def lookup_shortname(license_id: str, index: dict[str, str]) -> str | None:
    """Resolve an SPDX id against a license list, bridging the GPL renaming.

    SPDX 3.0 split `GPL-2.0` into `GPL-2.0-only` and `GPL-2.0-or-later`. FOSSology's
    list predates that and writes `GPL-2.0` and `GPL-2.0+`. Without the bridge the
    two vocabularies never meet: the notice index keys on SPDX ids, so every GPL,
    LGPL and AGPL rule — about 3,700 of them — resolved to nothing and was dropped,
    leaving the GPL family matchable only against its own multi-thousand-token body.
    """
    key = license_id.lower()
    if key in index:
        return index[key]
    if key.endswith("+") and key[:-1] in index:  # `GPL-2.0+` -> `GPL-2.0`
        return index[key[:-1]]
    if key.endswith("-or-later"):
        stem = key[: -len("-or-later")]
        for candidate in (stem + "+", stem):     # prefer the or-later spelling
            if candidate in index:
                return index[candidate]
    if key.endswith("-only"):
        stem = key[: -len("-only")]
        if stem in index:
            return index[stem]
    return None


def canonical_expression(expression: str, index: dict[str, str]) -> str:
    """The expression with known ids rewritten to their canonical shortname.

    Operators are upper-cased; ids that do not resolve — exceptions, ``LicenseRef``s,
    licenses outside the list — are kept as written rather than dropped. Dropping a
    component would silently rewrite the author's declaration into a different one.
    """
    def replace(found: re.Match) -> str:
        token = found.group(0)
        if token.upper() in _OPERATORS:
            return token.upper()
        return lookup_shortname(token, index) or token

    return _ID_TOKEN.sub(replace, expression)


def resolve(matches: Iterable[SpdxMatch], shortnames: Iterable[str]) -> list[dict]:
    """Map SPDX matches to result dicts for ids present in ``shortnames``.

    One dict per resolvable component license, each carrying the whole expression it
    came from. Deduplication is per (shortname, expression), not per shortname: the
    same license declared under two different expressions is two different facts.
    """
    index = shortname_index(shortnames)
    results: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for match in matches:
        expression = canonical_expression(match.expression, index)
        for license_id in match.licenses:
            shortname = lookup_shortname(license_id, index)
            if shortname is None or (shortname, expression) in seen:
                continue
            seen.add((shortname, expression))
            results.append({
                "shortname": shortname,
                "sim_type": "SPDXIdentifier",
                "sim_score": 1.0,
                "description": "",
                "expression": expression,
            })
    return results


def detect_and_resolve(data: str, shortnames: Iterable[str]) -> list[dict]:
    """Detect SPDX tags in ``data`` and resolve them against ``shortnames``."""
    return resolve(detect(data), shortnames)
