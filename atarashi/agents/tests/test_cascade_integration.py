#!/usr/bin/env python3
"""End-to-end cascade checks against the shipped 382-license list.

Exercises the real reference data (not synthetic texts): SPDX tags, exact full
text, embedded license text, short notices, and abstention. The shipped
``licenseList.csv`` has no header column, so notices are identifiable only via the
committed notice layer — which is exactly what ``test_notice_layer_*`` pins.

SPDX-License-Identifier: GPL-2.0-only
"""
import os
import tempfile

import pandas as pd
import pytest

from atarashi.agents.cascade import Cascade

CSV = os.path.join(os.path.dirname(__file__), "..", "..", "data", "licenses", "licenseList.csv")


@pytest.fixture(scope="module")
def agent():
    if not os.path.exists(CSV):
        pytest.skip("licenseList.csv not present")
    df = pd.read_csv(CSV).fillna("").rename(columns={"text": "processed_text"})
    df = df[["shortname", "processed_text"]]
    if "MIT" not in set(df["shortname"]):
        pytest.skip("MIT not in shipped license list")
    return Cascade(df), df


def _scan(agent, content):
    scanner, _ = agent
    fd, path = tempfile.mkstemp(suffix=".py")
    os.write(fd, content.encode())
    os.close(fd)
    try:
        return scanner.scan(path)
    finally:
        os.remove(path)


def test_spdx_tag_on_real_list(agent):
    top = _scan(agent, "# SPDX-License-Identifier: MIT\nprint(1)\n")[0]
    assert top["shortname"] == "MIT"
    assert top["sim_type"] == "SPDXIdentifier"


def test_exact_full_text_on_real_list(agent):
    _, df = agent
    mit = df.loc[df["shortname"] == "MIT", "processed_text"].iloc[0]
    assert _scan(agent, mit)[0]["shortname"] == "MIT"


def test_embedded_license_text_on_real_list(agent):
    _, df = agent
    mit = df.loc[df["shortname"] == "MIT", "processed_text"].iloc[0]
    top = _scan(agent, "/* Copyright 2020 Acme\n" + mit + "\n*/\nint main(){}\n")[0]
    assert top["shortname"] == "MIT"
    assert top["sim_type"] == "SequenceCoverage"


def test_no_license_abstains_on_real_list(agent):
    assert _scan(agent, "# Copyright 2020 Acme Corp\nimport os\n")[0]["shortname"] == "UNKNOWN"


# --- notice layer: the register real source files actually carry ---------------

# A full Apache header. Note this resolves *without* the notice layer too: the
# license body embeds its own "how to apply" notice, and a span matcher finds it
# there even though bag-of-words scoring drowned it. The layer is not what makes
# this case work.
APACHE_NOTICE = """/*
 * Copyright 2015 The Acme Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */
#include <stdio.h>
"""

# A one-line reference, taken from real source in the-stack-smol. No license body
# contains this sentence, so no full-text unit can match it at any threshold. This
# is the register the notice layer exists for.
APACHE_REFERENCE = """// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
#ifndef BOOTSTRAP_H_
#define BOOTSTRAP_H_
"""


def test_notice_layer_identifies_a_real_apache_header(agent):
    top = _scan(agent, APACHE_NOTICE)[0]
    assert top["shortname"] == "Apache-2.0"
    assert top["sim_type"] == "SequenceCoverage"


def test_notice_layer_identifies_a_short_reference(agent):
    """The case that needs the layer: too short to overlap any license body."""
    top = _scan(agent, APACHE_REFERENCE)[0]
    assert top["shortname"] == "Apache-2.0"


def test_short_reference_abstains_without_the_notice_layer(agent):
    """Pins the layer as the cause of the previous test, not the full-text index."""
    _, df = agent
    bare = Cascade(df, use_notices=False, use_gate=False)
    fd, path = tempfile.mkstemp(suffix=".c")
    os.write(fd, APACHE_REFERENCE.encode())
    os.close(fd)
    try:
        assert bare.scan(path)[0]["shortname"] == "UNKNOWN"
    finally:
        os.remove(path)


def test_notice_layer_still_abstains_on_copyright_only(agent):
    """Coverage must not come at the cost of answering the unanswerable."""
    noise = "// Copyright (c) 2012-2013, ARM Limited. All rights reserved.\n#include <a.h>\n"
    assert _scan(agent, noise)[0]["shortname"] == "UNKNOWN"


def test_result_carries_a_usable_character_span(agent):
    """Token indices into a normalized stream are not something an auditor can act
    on; the span must point into the text as written."""
    top = _scan(agent, APACHE_NOTICE)[0]
    assert top["matched_start"] < top["matched_end"]
    excerpt = top["matched_text"].lower()
    assert "apache" in excerpt
    assert APACHE_NOTICE[top["matched_start"]:top["matched_end"]] == top["matched_text"]
