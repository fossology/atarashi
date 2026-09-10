#!/usr/bin/env python3
"""Tests for only/or-later disambiguation.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.libs.orlater import corrected, later_signal, sibling

KNOWN = frozenset({"GPL-3.0-only", "GPL-3.0-or-later", "MIT"})


def test_sibling_pairs_both_ways():
    assert sibling("GPL-3.0-only") == "GPL-3.0-or-later"
    assert sibling("GPL-3.0-or-later") == "GPL-3.0-only"
    assert sibling("MIT") is None


def test_a_bare_license_body_is_only():
    """"Or later" is an election an author makes; a body on its own contains none."""
    assert corrected("GPL-3.0-or-later", True, KNOWN) == "GPL-3.0-only"


def test_a_cited_license_keeps_the_matchers_answer():
    """Outside the body case the notice layer has distinct rules for the two sides."""
    assert corrected("GPL-3.0-or-later", False, KNOWN) == "GPL-3.0-or-later"


def test_only_is_never_promoted_to_or_later():
    assert corrected("GPL-3.0-only", True, KNOWN) == "GPL-3.0-only"


def test_unknown_sibling_leaves_the_name_alone():
    assert corrected("GPL-2.0-or-later", True, KNOWN) == "GPL-2.0-or-later"


def test_later_signal_reads_the_election_but_not_the_appendix():
    """Kept because the signal is real; it is the *body* that makes it unusable —
    a GPL body quotes this wording in its "How to apply" appendix."""
    assert later_signal("either version 3 of the License, or (at your option) "
                        "any later version") is True
    assert later_signal("version 3 only") is False
    assert later_signal("Permission is hereby granted, free of charge") is None
