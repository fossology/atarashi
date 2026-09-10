#!/usr/bin/env python3
"""Optional Nirjas-gate front-end: skip Atarashi on non-license text.

Nirjas ships a recall-first binary gate ("is this text worth identifying?"). Used
as a pre-filter it spares Atarashi from scanning obvious non-license comments. The
gate is an optional Nirjas extra; when it is not installed ``should_scan`` fails
open (returns True) so Atarashi still runs.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache

Classifier = Callable[[list[str]], list[bool]]


@lru_cache(maxsize=1)
def _default_classifier() -> Classifier | None:
    """Load the Nirjas gate once, or None if the gate extra is unavailable."""
    try:
        from nirjas.gate import classify, load_gate  # pyright: ignore[reportMissingImports]
    except Exception:
        return None
    pipe, threshold = load_gate()
    return lambda texts: classify(pipe, texts, threshold)


def should_scan(text: str, classifier: Classifier | None = None) -> bool:
    """True if ``text`` looks license-bearing (worth scanning by Atarashi).

    Fails open (True) when the Nirjas gate extra is not installed. ``classifier``
    may be injected for testing or to reuse a preloaded gate.
    """
    clf = classifier if classifier is not None else _default_classifier()
    if clf is None:
        return True
    return bool(clf([text])[0])
