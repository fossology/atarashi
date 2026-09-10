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

from collections.abc import Sequence

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


def unknown_result(top_score: float = 0.0, considered: Sequence[tuple] = ()) -> dict:
    """Abstention, carrying what was considered and rejected.

    An abstention that says only UNKNOWN gives a reviewer nothing to act on, and on
    the DEP-5 corpus 11 of 15 abstentions had the correct licence sitting among the
    rejected candidates. Naming them turns "we do not know" into "we could not
    confirm any of these", which is the difference between a dead end and a starting
    point for review.
    """
    hint = ", ".join(f"{name} ({score:.2f})" for name, score in considered[:3])
    return {
        "shortname": UNKNOWN_SHORTNAME,
        "sim_type": "Abstain",
        "sim_score": top_score,
        "candidates": [{"shortname": n, "score": round(s, 4)} for n, s in considered[:5]],
        "description": f"no confident license match; closest: {hint}" if hint
                       else "no confident license match",
    }

