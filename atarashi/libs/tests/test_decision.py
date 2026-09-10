#!/usr/bin/env python3
"""Tests for the abstention / UNKNOWN decision.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.libs.decision import (DEFAULT_MIN_COVERAGE, DEFAULT_STRONG_RUN,
                                    UNKNOWN_SHORTNAME, is_confident,
                                    unknown_result)


def test_unknown_result_shape():
    out = unknown_result(0.42)
    assert out["shortname"] == UNKNOWN_SHORTNAME
    assert out["sim_type"] == "Abstain"
    assert out["sim_score"] == 0.42


# --- span-match acceptance ---------------------------------------------------

def test_long_run_accepted_even_at_negligible_coverage():
    """A verbatim notice covers ~1% of a long license body but identifies it."""
    assert is_confident(coverage=0.01, longest_run=DEFAULT_STRONG_RUN)


def test_high_coverage_accepted_even_with_short_runs():
    """A whole short license, matched in fragments, is still the license."""
    assert is_confident(coverage=DEFAULT_MIN_COVERAGE, longest_run=1)


def test_short_run_and_low_coverage_rejected():
    assert not is_confident(coverage=0.05, longest_run=10)


def test_thresholds_are_inclusive():
    assert is_confident(coverage=0.0, longest_run=DEFAULT_STRONG_RUN)
    assert is_confident(coverage=DEFAULT_MIN_COVERAGE, longest_run=0)


def test_thresholds_are_overridable():
    assert is_confident(0.05, 10, strong_run=10)
    assert is_confident(0.05, 1, min_coverage=0.05)
    assert not is_confident(0.4, 19, strong_run=20, min_coverage=0.5)


def test_abstention_names_what_it_rejected():
    """An abstention saying only UNKNOWN gives a reviewer nothing. On the DEP-5 corpus
    11 of 15 abstentions had the correct licence among the rejected candidates."""
    out = unknown_result(0.22, [("GPL-3.0-only", 0.2229), ("GPL-2.0-only", 0.1451)])
    assert out["shortname"] == UNKNOWN_SHORTNAME
    assert [c["shortname"] for c in out["candidates"]] == ["GPL-3.0-only", "GPL-2.0-only"]
    assert "GPL-3.0-only (0.22)" in out["description"]


def test_abstention_without_candidates_is_still_valid():
    out = unknown_result(0.0)
    assert out["candidates"] == []
    assert out["description"] == "no confident license match"
