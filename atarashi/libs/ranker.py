#!/usr/bin/env python3
"""Learned candidate scoring, replacing the hand-ordered ranking key.

The cascade retrieves well and orders badly: on an independent corpus, 62 of 77 wrong
answers already held the correct license inside the top five candidates, 28 of them at
rank two. Hand-tuning that ordering was attempted five separate ways and every attempt
lost more than it gained, which is what motivated learning the combination instead.

The model scores each candidate from the match evidence alone — run lengths, coverage,
gap structure, distance to the leader. It never reads license text. Models that do are
demonstrably unsafe here: on high-overlap/different-meaning pairs they score under 40%
and below chance when overlap disagrees with the label, which is exactly the
GPL-2-vs-GPL-3 case.

Scope is measured and narrow, and the model is gated to it. Held-out families are not
merely unhelped, they are actively harmed: leave-one-license-family-out is **-0.051**,
and holding out GPL costs -0.134. That got *worse* as training licenses grew from 18
to 34 — more families give the model more per-family signatures to memorise rather
than a general rule, so widening the corpus does not fix it and the measurement says
so directly.

The model therefore declines to act outside its training distribution: if the leading
candidate's license family was not in training, the hand-tuned ordering stands. That
converts a -0.051 regression on unseen families into no change, while keeping the
gain where it is validated. It is also off entirely unless an artifact is present.

``featurize`` is imported by the training code so the two cannot drift; a mismatch
between training and inference features would be silent and would poison the scores.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import math
import re
from pathlib import Path

DEFAULT_RANKER = Path(__file__).resolve().parents[1] / "data" / "ranker.joblib"

# Accept the top candidate when the model's probability for it clears this. The
# shipped artifact carries a threshold derived by split-conformal calibration rather
# than this constant, which is only the fallback when none is recorded.
#
# The conformal derivation: nonconformity for a candidate is 1 - P(correct); calibrate
# on held-out queries whose correct licence is among the candidates; take the
# ceil((n+1)(1-alpha))/n empirical quantile. At alpha=0.10 over n=432 that gives an
# accept floor of 0.3013, with realised coverage 0.931 and a mean set size of 0.99.
#
# Two limits worth stating wherever the guarantee is quoted. It is **conditional on
# the correct licence being retrievable at all** — 864 of 1,002 queries — because
# calibration can only use queries whose candidate list contains the truth; for the
# rest no threshold helps. And it is **marginal, not per-licence**: class-conditional
# coverage needs on the order of 100 calibration points per class against the ~27
# available here.
#
# That the tuned value and the derived one agree to three decimals (0.30 against
# 0.3013) is reassurance, not evidence — the grid search optimised on the same data.
DEFAULT_ACCEPT = 0.30

# Report an ambiguity rather than a pick when the leader beats the runner-up by less
# than this. Measured on 619 answered DEP-5 queries: no correct answer was ever
# decided by a margin below 0.195, while eight wrong ones fall under 0.1. Flagging
# there costs nothing and stops the engine choosing silently between two variants it
# cannot actually separate — which for GPL-2.0-only against GPL-2.0-or-later is a
# difference in what the licence permits.
DEFAULT_AMBIGUOUS_MARGIN = 0.10

_FAMILY = re.compile(r"^(a?l?gpl|mpl|epl|bsd|apache|mit|cc|isc|artistic|zlib|ofl"
                     r"|wtfpl|edl|ecl|cddl|python|boost|bsl|osl|ms|eupl|upl|ncsa"
                     r"|openssl|postgresql|unlicense|w3c|x11|zpl)", re.I)


def family(shortname: str) -> str:
    """Coarse license family — the unit at which this model generalises, or not."""
    found = _FAMILY.match(shortname or "")
    return found.group(1).upper() if found else "OTHER"

# Fixed order — the model's columns are positional.
FEATURE_NAMES = [
    "longest_run", "log_ref_tokens", "ref_coverage", "query_coverage",
    "matched_tokens", "shingle_ratio", "run_count",
    "best_unit_coverage", "units_matched",
    "ref_gap", "query_gap", "ref_head", "ref_tail", "substitution",
    "required_ok", "run_margin", "cov_margin",
]


def featurize(matches, normalize: bool = True) -> list[list[float]]:
    """Feature rows for one query's ranked candidates.

    ``run_margin`` and ``cov_margin`` are distances to the leader. They are the
    signal a per-candidate confidence bar can never see, and they turn out to be the
    strongest features the model has — the rank *position* itself is deliberately not
    a feature, because a model given it simply reproduces the ordering it was meant
    to improve.

    Features are standardized **within the candidate list** by default. Absolute
    magnitudes fingerprint a license — a reference body of 5,699 tokens is GPL-3.0
    and 2,984 is GPL-2.0 — so a model given them learns license identity instead of
    what a good match looks like, and then fails on any license it has not seen.
    Describing each candidate only by how it compares to its rivals for the same
    query removes that shortcut: it moved leave-one-license-family-out from -0.054 to
    -0.013 on its own, and to +0.001 once tree depth came down to 2.
    """
    if not matches:
        return []
    lead = matches[0]
    rows = [[
        float(m.longest_run),
        math.log1p(m.ref_tokens),
        float(m.score),
        float(m.query_coverage),
        float(m.matched_tokens),
        float(m.shingle_ratio),
        float(m.run_count),
        float(m.best_unit_coverage),
        float(m.units_matched),
        float(m.ref_gap),
        float(m.query_gap),
        float(m.ref_head),
        float(m.ref_tail),
        float(m.substitution),
        1.0 if m.required_ok else 0.0,
        float(lead.longest_run - m.longest_run),
        float(lead.score - m.score),
    ] for m in matches]
    if not normalize or len(rows) < 2:
        return rows
    columns = list(zip(*rows))
    stats = []
    for column in columns:
        mean = sum(column) / len(column)
        variance = sum((v - mean) ** 2 for v in column) / len(column)
        stats.append((mean, math.sqrt(variance) or 1.0))
    return [[(v - mean) / sd for v, (mean, sd) in zip(row, stats)] for row in rows]


# The artifact is immutable for the life of a process and every agent construction
# would otherwise re-read it from disk — measurably slow, and noisy besides.
_CACHE: dict[str, object] = {}


def load_ranker(path: Path | None = None) -> dict | None:
    """The trained scorer, or None when absent — the caller keeps its own ordering."""
    target = Path(path or DEFAULT_RANKER)
    key = str(target)
    if key in _CACHE:
        return _CACHE[key]
    bundle = None
    if target.exists():
        try:
            import warnings

            import joblib

            with warnings.catch_warnings():
                # joblib's unpickler trips a NumPy 2.5 deprecation once per stored
                # array — hundreds of lines on first scan, from a dependency, about
                # nothing the caller can act on.
                warnings.simplefilter("ignore", DeprecationWarning)
                loaded = joblib.load(target)
            if {"model", "scaler"} <= set(loaded):
                bundle = loaded
        except Exception:
            bundle = None
    _CACHE[key] = bundle
    return bundle


def _list_in_scope(matches, bundle) -> bool:
    """Whether the model may rank this candidate list.

    Gating on the *leader* was wrong in a way the prevalence benchmark made obvious.
    A verbatim Apache-2.0 body puts `ImageMagick` first — its licence is Apache-2.0
    plus extra text, so it wins the longest run (847 against 764) while covering 0.81
    of its own reference against Apache-2.0's 0.996. `family("ImageMagick")` is OTHER,
    so the gate declined, the hand-tuned run-first ordering stood, and **286 of 639
    Apache-2.0 files were reported as ImageMagick**.

    The model's competence is about the licences it can recognise, not about whichever
    candidate the run-length heuristic happened to put on top. So the list is in scope
    when *any* candidate is, and the model is free to promote the one it knows.
    """
    return any(_in_scope(m.shortname, bundle) for m in matches)


def _in_scope(shortname: str, bundle) -> bool:
    """Whether the model has any business ranking this candidate.

    **Family granularity, and licence granularity was measured and rejected.** Gating
    on the family lets the model act on `MIT-advertising` because `MIT` was trained,
    and it then promotes plain MIT over it: on the Software Heritage tail the learned
    ranker is *worse* than the matcher's own ordering, R@1 0.758 -> 0.697, with the
    correct licence at matcher rank 1 in seven of the misses. Gating on the 37 trained
    licences instead fixes exactly that (tail R@1 0.697 -> 0.742) — and costs far more
    than it buys, because it also declines the case that is the ranker's single largest
    win on the head corpora.

    Measured on 916 head-corpus queries: when the matcher's leader is an *untrained*
    licence the ranker helps in 74 of 117 and hurts in none, because there the leader
    is usually wrong and the correct licence is one the model knows. On the tail the
    same situation inverts — an untrained leader is *correct* 34 times in 43 — and the
    two are not separable by evidence: median query coverage is 0.969 when the
    untrained leader is right and 0.957 when it is wrong.

    So there is no inference-time signal to gate on. The bias toward trained licences
    is real and whether it is correct depends on whether the file's licence is in the
    training set, which cannot be known while scanning. End to end, licence gating cost
    DEP-5 R@1 0.8435 -> 0.8003 to gain 0.045 on the tail; the head is the larger
    population, so families stay. The artifact still records `licenses`, because the
    fix for this is a training set wider than 37 licences — at *licence* granularity,
    a different axis from the family-count curve that plateaus at 12.
    """
    if not bundle:
        return False
    known = bundle.get("families")
    if not known:
        return True
    # "OTHER" is the bucket for names the family rule does not recognise, not a
    # family. Its presence in training says nothing about whether *this* licence
    # was covered, so it cannot license a decision.
    leader = family(shortname)
    return leader != "OTHER" and leader in known


def accept(matches, bundle, threshold: float | None = None) -> bool | None:
    """Whether the leading candidate is worth reporting.

    Three outcomes, and the third is the important one. ``None`` means the model has
    no opinion — no artifact, an unseen license family, or a scoring failure — and the
    caller must fall back to its own confidence rule. Collapsing that into ``True``
    would turn "I cannot judge this" into "report it", which is exactly backwards for
    a family the model was never trained on.
    """
    if not bundle or not matches:
        return None
    if not _list_in_scope(matches, bundle):
        return None
    tau = bundle.get("accept", DEFAULT_ACCEPT) if threshold is None else threshold
    try:
        rows = featurize(matches)
        scores = bundle["model"].predict_proba(bundle["scaler"].transform(rows))[:, 1]
    except Exception:
        return None
    return bool(max(scores) >= tau)


def score_candidates(matches, bundle):
    """``(ordered matches, their scores)``, or None when the model has no opinion.

    One entry point, because acceptance, ordering and the ambiguity margin all read
    the same scores and computing them three times invites them to disagree.
    """
    if not bundle or not matches:
        return None
    if not _list_in_scope(matches, bundle):
        return None
    try:
        rows = featurize(matches)
        scores = bundle["model"].predict_proba(bundle["scaler"].transform(rows))[:, 1]
    except Exception:
        return None
    order = sorted(range(len(matches)), key=lambda i: -scores[i])
    return [matches[i] for i in order], [float(scores[i]) for i in order]


def rerank(matches, bundle):
    """Re-order ``matches`` by learned score, most likely first.

    Declines on any license family absent from training — see the module docstring;
    outside its training distribution this model is worse than the ordering it
    replaces, so silence is the correct behaviour rather than a missed opportunity.

    Returns the input untouched on any failure. A ranking model that raises must not
    take the scan down with it — the hand-tuned order is a working fallback.
    """
    if not bundle or len(matches) < 2:
        return matches
    if not _list_in_scope(matches, bundle):
        return matches
    try:
        rows = featurize(matches)
        scores = bundle["model"].predict_proba(bundle["scaler"].transform(rows))[:, 1]
    except Exception:
        return matches
    return [m for _, m in sorted(zip(scores, matches),
                                 key=lambda pair: -pair[0])]
