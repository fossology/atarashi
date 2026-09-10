#!/usr/bin/env python3
"""Tests for the Phase-0 cascade agent (SPDX-first, else UNKNOWN).

SPDX-License-Identifier: GPL-2.0-only
"""
import pandas as pd

from atarashi.agents.cascade import Cascade

MIT_TEXT = ("Permission is hereby granted, free of charge, to any person obtaining a "
            "copy of this software and associated documentation files, to deal in the "
            "Software without restriction.")
APACHE_HEADER = ("Licensed under the Apache License Version 2.0 you may not use this "
                 "file except in compliance with the License you may obtain a copy")
LICENSES = pd.DataFrame({
    "shortname": ["MIT", "Apache-2.0", "GPL-2.0"],
    "processed_text": [MIT_TEXT, "Apache License Version 2.0 full body text here", ""],
    "processed_header": ["", APACHE_HEADER, ""],
})


def _scan(tmp_path, content):
    f = tmp_path / "src.py"
    f.write_text(content)
    return Cascade(LICENSES).scan(str(f))


def test_spdx_tag_resolved(tmp_path):
    out = _scan(tmp_path, "# SPDX-License-Identifier: MIT\nprint(1)\n")
    assert out[0]["shortname"] == "MIT"
    assert out[0]["sim_type"] == "SPDXIdentifier"
    assert out[0]["sim_score"] == 1.0


def test_exact_full_text(tmp_path):
    out = _scan(tmp_path, MIT_TEXT)
    assert out[0]["shortname"] == "MIT"
    assert out[0]["sim_type"] == "ExactFullText"


def test_embedded_license_text_sequence_match(tmp_path):
    out = _scan(tmp_path, "/*\n * Copyright 2020 Acme\n * " + MIT_TEXT + "\n */\nint main(){}")
    assert out[0]["shortname"] == "MIT"
    assert out[0]["sim_type"] == "SequenceCoverage"
    assert out[0]["sim_score"] >= 0.9


def test_no_license_abstains(tmp_path):
    out = _scan(tmp_path, "# Copyright 2020 ACME Corp\nprint(1)\n")
    assert out[0]["shortname"] == "UNKNOWN"


def test_unknown_spdx_id_abstains(tmp_path):
    out = _scan(tmp_path, "# SPDX-License-Identifier: Nonexistent-9.9\n")
    assert out[0]["shortname"] == "UNKNOWN"


def test_notice_header_matches_via_header_unit(tmp_path):
    # The comment block must carry more than the bare header: on its own the header
    # is a reference unit verbatim, so the exact-hash stage answers first and the
    # sequence path this test exists to cover is never reached.
    out = _scan(tmp_path, "# Copyright 2020 Acme Corp\n# " + APACHE_HEADER + "\nimport os\n")
    assert out[0]["shortname"] == "Apache-2.0"
    assert out[0]["sim_type"] == "SequenceCoverage"


# --- abstention: weak evidence must not be reported as a match ----------------

LONG_BODY = " ".join(f"clause{i} term text follows here" for i in range(40))
WEAK = pd.DataFrame({
    "shortname": ["Long-1.0"],
    "processed_text": [LONG_BODY],
    "processed_header": [""],
})


def test_weak_span_match_abstains(tmp_path):
    """A short run covering little of the reference is not evidence of a license."""
    f = tmp_path / "src.py"
    # 10 contiguous reference tokens: over the matcher's min_run floor (8), under
    # the acceptance bar (20), and ~5% coverage of the body.
    f.write_text("int main(){} " + " ".join(LONG_BODY.split()[:10]) + " more code")
    out = Cascade(WEAK).scan(str(f))
    assert out[0]["shortname"] == "UNKNOWN"
    assert out[0]["sim_type"] == "Abstain"


def test_weak_match_reported_when_bar_is_lowered(tmp_path):
    """The same input matches once the run threshold is relaxed — proving the
    abstention is what suppressed it, not a failure to match at all."""
    f = tmp_path / "src.py"
    f.write_text("int main(){} " + " ".join(LONG_BODY.split()[:10]) + " more code")
    out = Cascade(WEAK, strong_run=5).scan(str(f))
    assert out[0]["shortname"] == "Long-1.0"
    assert out[0]["sim_type"] == "SequenceCoverage"


def test_long_run_accepted_despite_low_coverage(tmp_path):
    """A verbatim notice covers little of a long body but is still identifying."""
    f = tmp_path / "src.py"
    f.write_text("code\n" + " ".join(LONG_BODY.split()[:25]) + "\nmore code")
    out = Cascade(WEAK).scan(str(f))
    assert out[0]["shortname"] == "Long-1.0"
    assert out[0]["sim_score"] < 0.5, "accepted on run length, not coverage"


def test_abstain_result_carries_the_best_rejected_score(tmp_path):
    f = tmp_path / "src.py"
    f.write_text("int main(){} " + " ".join(LONG_BODY.split()[:10]) + " more code")
    out = Cascade(WEAK).scan(str(f))
    assert 0.0 < out[0]["sim_score"] < 0.5


# --- gate front-end ----------------------------------------------------------

def test_gate_rejection_abstains_without_matching(tmp_path, monkeypatch):
    monkeypatch.setattr("atarashi.agents.cascade.should_scan", lambda text: False)
    f = tmp_path / "src.py"
    f.write_text(MIT_TEXT)
    out = Cascade(LICENSES).scan(str(f))
    assert out[0]["shortname"] == "UNKNOWN"


def test_gate_can_be_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr("atarashi.agents.cascade.should_scan", lambda text: False)
    f = tmp_path / "src.py"
    f.write_text(MIT_TEXT)
    assert Cascade(LICENSES, use_gate=False).scan(str(f))[0]["shortname"] == "MIT"


def test_spdx_tag_wins_over_a_rejecting_gate(tmp_path, monkeypatch):
    """The tag is read from raw text before the gate, so it is never gated away."""
    monkeypatch.setattr("atarashi.agents.cascade.should_scan", lambda text: False)
    f = tmp_path / "src.py"
    f.write_text("# SPDX-License-Identifier: MIT\nprint(1)\n")
    assert Cascade(LICENSES).scan(str(f))[0]["shortname"] == "MIT"


# --- comment extraction ------------------------------------------------------

def test_falls_back_to_raw_when_extraction_unavailable(tmp_path, monkeypatch):
    def boom(_):
        raise ImportError("nirjas not installed")
    monkeypatch.setattr(
        "atarashi.libs.commentPreprocessor.CommentPreprocessor.extract", boom)
    f = tmp_path / "src.py"
    f.write_text(MIT_TEXT)
    assert Cascade(LICENSES).scan(str(f))[0]["shortname"] == "MIT"


def test_extracted_comment_is_used_for_matching(tmp_path, monkeypatch):
    """Matching runs on the extracted comment, not the raw file."""
    seen = {}

    def fake_extract(path):
        seen["called"] = True
        out = tmp_path / "comment.txt"
        out.write_text(MIT_TEXT)
        return str(out)

    monkeypatch.setattr(
        "atarashi.libs.commentPreprocessor.CommentPreprocessor.extract", fake_extract)
    f = tmp_path / "src.py"
    f.write_text("int main(){ return 0; }")   # raw file has no license at all
    out = Cascade(LICENSES).scan(str(f))
    assert seen.get("called")
    assert out[0]["shortname"] == "MIT"


def test_empty_extraction_falls_back_to_raw(tmp_path, monkeypatch):
    def empty_extract(path):
        out = tmp_path / "empty.txt"
        out.write_text("   \n")
        return str(out)

    monkeypatch.setattr(
        "atarashi.libs.commentPreprocessor.CommentPreprocessor.extract", empty_extract)
    f = tmp_path / "src.py"
    f.write_text(MIT_TEXT)
    assert Cascade(LICENSES).scan(str(f))[0]["shortname"] == "MIT"


def test_compound_match_reports_every_license_it_attests_to(tmp_path):
    """A compound unit matched one span but names several licenses, and the exception
    is what makes the grant what it is — reporting only the leader states a different
    license than the file declares. Same contract the SPDX-tag path already emits."""
    import json

    licenses = pd.DataFrame({
        "shortname": ["Apache-2.0", "LLVM-exception"],
        "processed_text": ["Apache License Version 2.0 full body text here", "x"],
        "processed_header": ["", ""],
    })
    notice = tmp_path / "notice_rules.json"
    notice.write_text(json.dumps({"source": "test", "units": [
        ["Apache-2.0 WITH LLVM-exception",
         "The LLVM Project is under the Apache License v2.0 with LLVM Exceptions"]]}))
    f = tmp_path / "src.c"
    f.write_text("// Part of the LLVM Project, under the Apache License v2.0 "
                 "with LLVM Exceptions.\nint main(){}")
    out = Cascade(licenses, notice_path=str(notice), use_ranker=False,
                  strong_run=8).scan(str(f))

    assert [r["shortname"] for r in out] == ["Apache-2.0", "LLVM-exception"]
    assert {r["expression"] for r in out} == {"Apache-2.0 WITH LLVM-exception"}
    assert all(r["matched_text"] for r in out)


def test_compound_names_the_license_the_file_supports_first(tmp_path):
    """Which component leads is decided by the query, not by the rule's wording.

    A plain BSD-2-Clause file that matched a `GPL-2.0-only OR BSD-2-Clause` rule was
    reported as GPL-2.0-only with BSD-2-Clause second, because that is the order the
    rule's author wrote it in. The file carries BSD text and no GPL text, so
    BSD-2-Clause is what it supports. The reported set is identical either way; only
    the order a top-1 consumer reads changes.
    """
    import json

    bsd = ("Redistribution and use in source and binary forms, with or without "
           "modification, are permitted provided that the following conditions are "
           "met: Redistributions of source code must retain the above copyright "
           "notice, this list of conditions and the following disclaimer.")
    licenses = pd.DataFrame({
        "shortname": ["GPL-2.0-only", "BSD-2-Clause"],
        "processed_text": [
            "This program is free software you can redistribute it under the terms "
            "of the GNU General Public License version 2 as published by the Free "
            "Software Foundation",
            # Longer than the compound unit, so the compound wins on coverage while
            # this unit still supplies BSD-2-Clause's independent evidence.
            bsd + " Neither the name of the holder may be used to endorse products."],
        "processed_header": ["", ""],
    })
    notice = tmp_path / "notice_rules.json"
    notice.write_text(json.dumps({"source": "test", "units": [
        ["GPL-2.0-only OR BSD-2-Clause", bsd]]}))
    f = tmp_path / "LICENSE"
    f.write_text("Copyright (c) 2020 Acme Corporation. All rights reserved.\n" + bsd)

    out = Cascade(licenses, notice_path=str(notice), use_ranker=False,
                  strong_run=8).scan(str(f))
    names = [r["shortname"] for r in out]
    assert set(names) == {"BSD-2-Clause", "GPL-2.0-only"}, names
    assert names[0] == "BSD-2-Clause", names


def test_single_license_match_still_reports_one_license(tmp_path):
    """The expansion must not multiply results for a plain reference."""
    out = _scan(tmp_path, "/*\n * Copyright 2020 Acme\n * " + MIT_TEXT + "\n */\nint main(){}")
    assert [r["shortname"] for r in out] == ["MIT"]
    assert out[0]["expression"] == "MIT"


def test_license_dot_txt_is_not_mangled_by_comment_extraction(tmp_path):
    """`LICENSE.txt` is prose, not code. Nirjas maps `.txt` to a "text" language and
    ran comment extraction over it, dropping content: a verbatim GPL-3.0 body lost
    1,315 characters and the cascade abstained, while the same bytes named `LICENSE`
    resolved. Measured on the Software Heritage annotated sample."""
    body = MIT_TEXT + " " + MIT_TEXT
    as_txt = tmp_path / "LICENSE.txt"
    as_txt.write_text(body)
    agent = Cascade(LICENSES, use_gate=False)
    assert agent._comment_text(str(as_txt), "FALLBACK").strip() == body.strip()
