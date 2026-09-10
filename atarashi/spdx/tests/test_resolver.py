#!/usr/bin/env python3
"""Tests for SPDX id -> shortname resolution and the upgraded spdx_identifer.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.libs.initialmatch import spdx_identifer
from atarashi.spdx.resolver import detect_and_resolve, resolve
from atarashi.spdx.detector import detect

SHORTNAMES = ["MIT", "Apache-2.0", "GPL-2.0", "BSD-3-Clause", "LGPL-2.1"]


def test_resolve_exact():
    r = resolve(detect("SPDX-License-Identifier: MIT"), SHORTNAMES)
    assert r == [{"shortname": "MIT", "sim_type": "SPDXIdentifier",
                  "sim_score": 1.0, "description": "", "expression": "MIT"}]


def test_resolve_case_insensitive_to_canonical_shortname():
    # detected id differs in case; result uses the canonical shortname casing
    assert resolve(detect("SPDX-License-Identifier: apache-2.0"), SHORTNAMES)[0]["shortname"] == "Apache-2.0"


def test_resolve_or_later_plus_falls_back():
    assert resolve(detect("SPDX-License-Identifier: GPL-2.0+"), SHORTNAMES)[0]["shortname"] == "GPL-2.0"


def test_unknown_id_dropped():
    assert resolve(detect("SPDX-License-Identifier: Nonexistent-9.9"), SHORTNAMES) == []


def test_compound_resolves_known_drops_unknown():
    out = resolve(detect("SPDX-License-Identifier: MIT OR Nonexistent-9.9"), SHORTNAMES)
    assert [d["shortname"] for d in out] == ["MIT"]


def test_dedupes_repeated_license():
    text = "SPDX-License-Identifier: MIT\nSPDX-License-Identifier: MIT"
    assert len(detect_and_resolve(text, SHORTNAMES)) == 1


def test_spdx_identifer_schema():
    """The legacy keys are unchanged; `expression` is an addition, not a rename."""
    out = spdx_identifer("// SPDX-License-Identifier: BSD-3-Clause", SHORTNAMES)
    assert out == [{"shortname": "BSD-3-Clause", "sim_type": "SPDXIdentifier",
                    "sim_score": 1.0, "description": "",
                    "expression": "BSD-3-Clause"}]


def test_spdx_identifer_ignores_bare_license_line():
    # regression: the legacy scan matched "license:" lines; the tag path must not
    assert spdx_identifer("license: MIT is used here", SHORTNAMES) == []


# --- expression composition ---------------------------------------------------
# A flat list of shortnames cannot say what the author declared: AND and OR collapse
# to the same pair, and a WITH exception disappears. Each is legally decisive.


def test_with_exception_survives_resolution():
    """The regression this section exists for: the exception used to be parsed and
    then silently discarded, turning a narrower grant into a plain GPL-2.0."""
    out = resolve(detect("SPDX-License-Identifier: GPL-2.0 WITH Classpath-exception-2.0"),
                  SHORTNAMES)
    assert [d["shortname"] for d in out] == ["GPL-2.0"]
    assert out[0]["expression"] == "GPL-2.0 WITH Classpath-exception-2.0"


def test_and_and_or_are_distinguishable():
    conj = resolve(detect("SPDX-License-Identifier: MIT AND Apache-2.0"), SHORTNAMES)
    disj = resolve(detect("SPDX-License-Identifier: MIT OR Apache-2.0"), SHORTNAMES)
    assert [d["shortname"] for d in conj] == [d["shortname"] for d in disj] == ["MIT", "Apache-2.0"]
    assert conj[0]["expression"] == "MIT AND Apache-2.0"
    assert disj[0]["expression"] == "MIT OR Apache-2.0"


def test_expression_canonicalizes_known_ids_and_operators():
    out = resolve(detect("SPDX-License-Identifier: mit or apache-2.0"), SHORTNAMES)
    assert out[0]["expression"] == "MIT OR Apache-2.0"


def test_expression_keeps_unresolvable_components_verbatim():
    """Dropping a component would rewrite the declaration into a different one."""
    out = resolve(detect("SPDX-License-Identifier: MIT OR Nonexistent-9.9"), SHORTNAMES)
    assert [d["shortname"] for d in out] == ["MIT"]
    assert out[0]["expression"] == "MIT OR Nonexistent-9.9"


def test_expression_preserves_parentheses():
    out = resolve(detect("SPDX-License-Identifier: (MIT OR Apache-2.0) AND GPL-2.0"),
                  SHORTNAMES)
    assert out[0]["expression"] == "(MIT OR Apache-2.0) AND GPL-2.0"


def test_same_license_under_two_expressions_is_two_results():
    text = ("SPDX-License-Identifier: GPL-2.0\n"
            "SPDX-License-Identifier: GPL-2.0 WITH Classpath-exception-2.0")
    out = detect_and_resolve(text, SHORTNAMES)
    assert [d["expression"] for d in out] == [
        "GPL-2.0", "GPL-2.0 WITH Classpath-exception-2.0"]


# --- SPDX 3.0 renaming of the GPL family --------------------------------------
# The notice index keys on SPDX ids while FOSSology's list predates the split, so
# without this bridge every GPL/LGPL/AGPL rule resolves to nothing and is dropped.

GPL_NAMES = ["GPL-2.0", "GPL-2.0+", "GPL-3.0", "GPL-3.0+", "MIT"]


def test_or_later_spdx_id_resolves_to_the_plus_shortname():
    assert resolve(detect("SPDX-License-Identifier: GPL-2.0-or-later"),
                   GPL_NAMES)[0]["shortname"] == "GPL-2.0+"


def test_only_spdx_id_resolves_to_the_bare_shortname():
    assert resolve(detect("SPDX-License-Identifier: GPL-2.0-only"),
                   GPL_NAMES)[0]["shortname"] == "GPL-2.0"


def test_or_later_falls_back_when_no_plus_spelling_exists():
    assert resolve(detect("SPDX-License-Identifier: GPL-3.0-or-later"),
                   ["GPL-3.0", "MIT"])[0]["shortname"] == "GPL-3.0"


def test_bridge_does_not_invent_licenses():
    assert resolve(detect("SPDX-License-Identifier: AGPL-9.9-or-later"), GPL_NAMES) == []
