#!/usr/bin/env python3
"""Build the notice/short-form reference index from scancode-toolkit rules.

Atarashi's reference layer was one full license text (plus an optional header) per
license. Real source files do not carry license bodies; they carry short *notices*,
and a notice sits at ~95% depth of a multi-thousand-token body, so whole-document
scoring never surfaces it. Measured on real headers, the full-text-only layer scores
R@1 ~0.004 — it cannot identify them at all. ScanCode succeeds in the wild precisely
because it indexes thousands of separate short rule texts. This script extracts that
layer so Atarashi can index it too.

scancode-toolkit is a **build-time** dependency only. The generated artifact is
committed, so installing Atarashi never pulls scancode in.

Usage (from a venv with scancode-toolkit installed):

    python scripts/build_references.py
    python scripts/build_references.py --out /tmp/notice_rules.json --max-chars 2000

On macOS scancode needs libmagic; `brew install libmagic` then set
TYPECODE_LIBMAGIC_PATH=/opt/homebrew/lib/libmagic.dylib and
TYPECODE_LIBMAGIC_DB_PATH=/opt/homebrew/share/misc/magic.mgc.

SPDX-License-Identifier: GPL-2.0-only
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DEFAULT_OUT = Path(__file__).resolve().parents[1] / "atarashi" / "data" / "licenses" / "notice_rules.json"

# `{{...}}` in a ScanCode rule marks a *required phrase* — text that must be present
# for the rule to match. It is the most identifying wording in the rule, not a
# wildcard. The braces are markup and come out; the text inside emphatically stays,
# and is also emitted separately as a gating phrase. (Checked against the shipped
# corpus: 10,624 of 36,472 rules carry braces and none is an old numeric gap
# template, so there is no wildcard case left to handle.)
_BRACE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)
# Splits an expression while keeping the operators, so a compound key can be
# rebuilt over SPDX ids: "gpl-2.0 WITH classpath-exception-2.0" -> ["gpl-2.0",
# "WITH", "classpath-exception-2.0"]. Even indices are licenses, odd are operators.
_COMPOUND = re.compile(r"\s+(AND|OR|WITH)\s+", re.IGNORECASE)

# The short-form register real files actually carry. Full license bodies are already
# covered by Atarashi's own license list, so `is_license_text` rules are not taken.
RULE_KINDS = ("is_license_notice", "is_license_reference", "is_license_tag",
              "is_license_intro")

# Below the floor a unit is generic legal filler ("licensed under a .") that cannot
# attribute to one license; above the ceiling it is a body masquerading as a notice.
MIN_CHARS = 15
MAX_CHARS = 3000


def _spdx_key(expression: str, db) -> str:
    """Rewrite a ScanCode license expression over SPDX ids, or "" if any part is unknown.

    A single-license expression comes back as a bare SPDX id, so the common case is
    unchanged. A compound one keeps its operators, upper-cased, and is keyed as the
    whole expression: ``Apache-2.0 WITH LLVM-exception``. All components must resolve
    — a half-mapped expression would name a license the rule does not attest to.
    """
    parts = _COMPOUND.split(expression.strip())
    out: list[str] = []
    for position, part in enumerate(parts):
        if position % 2:
            out.append(part.upper())
            continue
        entry = db.get(part.strip().lower())
        spdx = (getattr(entry, "spdx_license_key", "") or "").strip() if entry else ""
        if not spdx:
            return ""
        out.append(spdx)
    return " ".join(out)


def build(min_chars: int = MIN_CHARS, max_chars: int = MAX_CHARS) -> list[tuple[str, str, list[str]]]:
    """Extract short-form rules as (SPDX id or expression, text, required phrases).

    Compound (AND/OR/WITH) rules used to be skipped, on the reasoning that Atarashi
    composes expressions from the SPDX detector instead. That holds only for files
    carrying a tag. It discarded 3,941 of 29,567 short-form rules (13.3%), 1,157 of
    them ``WITH`` exceptions, and with them the register that files without a tag
    actually carry: the prose "The LLVM Project is under the Apache License v2.0 with
    LLVM Exceptions:" lives in a compound rule, while ``LLVM-exception``'s own
    single-license rules are all 1-3 tokens and fall below the indexing floor. The
    exception was therefore unreachable — 0 indexed units — for 22 of the 65 real
    ``WITH``-labelled spans in the-stack corpus.

    Measured on 292 real compound-labelled spans, indexing them takes full-expression
    R@1 from 0.000 (structurally impossible) to 0.921, and 0.788 under leave-one-out
    masking of units contained verbatim in a query. The primary license alone also
    improves, 0.490 -> 0.969 (0.370 -> 0.853 masked), because a compound rule's text
    is the register those files carry. Cost on single-license queries: -0.0015 on the
    671 DEP-5 notice queries (independent Debian labels) and -0.0070 on 5,968
    single-license spans — roughly three gained per one lost, the same trade the
    short-reference floor already accepted.

    Keys are emitted as SPDX ids so the artifact is independent of both ScanCode's
    and FOSSology's internal naming; the loader maps them to its own shortnames.
    """
    import licensedcode
    from licensedcode.cache import get_licenses_db
    from licensedcode.models import load_rules

    db = get_licenses_db()
    base = Path(licensedcode.__file__).parent / "data" / "rules"
    units: list[tuple[str, str, list[str]]] = []
    for rule in load_rules(base):
        expr = (rule.license_expression or "").strip()
        if not expr:
            continue
        if not any(getattr(rule, kind, False) for kind in RULE_KINDS):
            continue
        spdx = _spdx_key(expr, db)
        if not spdx:
            continue
        raw = rule.text() if callable(getattr(rule, "text", None)) else getattr(rule, "text", "")
        phrases = [" ".join(s.split()) for s in _BRACE.findall(raw or "")]
        text = " ".join(_BRACE.sub(r" \1 ", raw or "").split())
        if min_chars <= len(text) <= max_chars:
            units.append((spdx, text, [p for p in phrases if p]))
    return units


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--min-chars", type=int, default=MIN_CHARS)
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    args = ap.parse_args(argv)

    import scancode_config

    units = build(args.min_chars, args.max_chars)
    if not units:
        raise SystemExit("no rule units extracted — is scancode-toolkit installed?")

    payload = {
        "source": "scancode-toolkit",
        "schema": 2,  # 1 = [spdx, text]; 2 adds per-unit required phrases
        "scancode_version": scancode_config.__version__,
        "rule_kinds": list(RULE_KINDS),
        "min_chars": args.min_chars,
        "max_chars": args.max_chars,
        "units": [list(u) for u in units],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload))

    licenses = {u[0] for u in units}
    compound = {u[0] for u in units if _COMPOUND.search(u[0])}
    gated = sum(1 for u in units if u[2])
    size_mb = args.out.stat().st_size / 1e6
    print(f"wrote {len(units)} units across {len(licenses)} keys "
          f"({len(compound)} compound expressions, {gated} with required phrases) "
          f"-> {args.out} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
