#!/usr/bin/env python3
"""Abstention: return UNKNOWN instead of a low-confidence guess.

A license scanner that always emits its best guess trades precision for recall on
inputs that carry no identifiable license (e.g. a bare copyright header). This
returns an explicit UNKNOWN when the strongest match does not clear a confidence
threshold, so callers can prefer precision. Assumes scores are in [0, 1] (the new
cascade agent's contract: SPDX/exact = 1.0, sequence coverage in [0, 1]).

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

UNKNOWN_SHORTNAME = "UNKNOWN"

# Acceptance for a span match. Coverage alone is the wrong bar: a short notice
# legitimately covers only a few percent of a multi-thousand-token license body,
# so a coverage floor would reject exactly the register real files carry. The
# longest contiguous matched run is the length-independent signal — a run of this
# many tokens is a distinctive license phrase rather than shared legal boilerplate.
DEFAULT_STRONG_RUN = 20
DEFAULT_MIN_COVERAGE = 0.5


def is_confident(coverage: float, longest_run: int,
                 strong_run: int = DEFAULT_STRONG_RUN,
                 min_coverage: float = DEFAULT_MIN_COVERAGE) -> bool:
    """True if a span match is strong enough to report rather than abstain.

    Either signal suffices: a long distinctive run (a notice quoted verbatim), or
    high coverage (most of the reference is present, as in a full LICENSE file).
    """
    return longest_run >= strong_run or coverage >= min_coverage


def unknown_result(top_score: float = 0.0) -> dict:
    return {
        "shortname": UNKNOWN_SHORTNAME,
        "sim_type": "Abstain",
        "sim_score": top_score,
        "description": "no confident license match",
    }

