#!/usr/bin/env python3
"""Tests for the SPDX-License-Identifier detector.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.spdx import detect


def test_simple_tag():
    m = detect("# SPDX-License-Identifier: MIT")
    assert len(m) == 1
    assert m[0].licenses == ("MIT",)
    assert m[0].exceptions == ()
    assert m[0].line == 1


def test_case_insensitive_keyword():
    assert detect("// spdx-license-identifier: Apache-2.0")[0].licenses == ("Apache-2.0",)


def test_or_expression():
    assert detect("SPDX-License-Identifier: MIT OR Apache-2.0")[0].licenses == ("MIT", "Apache-2.0")


def test_and_expression_with_parens():
    m = detect("SPDX-License-Identifier: GPL-2.0-only OR (MIT AND Apache-2.0)")
    assert m[0].licenses == ("GPL-2.0-only", "MIT", "Apache-2.0")


def test_with_exception():
    m = detect("/* SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception */")
    assert m[0].licenses == ("Apache-2.0",)
    assert m[0].exceptions == ("LLVM-exception",)


def test_or_later_plus_form():
    assert detect("SPDX-License-Identifier: GPL-2.0+")[0].licenses == ("GPL-2.0+",)


def test_block_comment_terminator_stripped():
    m = detect("/* SPDX-License-Identifier: BSD-3-Clause */")
    assert m[0].expression == "BSD-3-Clause"
    assert m[0].licenses == ("BSD-3-Clause",)


def test_licenseref():
    assert detect("SPDX-License-Identifier: LicenseRef-my-license")[0].licenses == (
        "LicenseRef-my-license",
    )


def test_no_tag_abstains():
    assert detect("just some code\nint main() { return 0; }") == []


def test_loose_license_line_not_matched():
    # The old detector also matched bare "License:" lines; the tag path must not.
    assert detect("License: see the LICENSE file for details") == []


def test_multiple_tags_report_line_numbers():
    m = detect("# SPDX-License-Identifier: MIT\ncode\n# SPDX-License-Identifier: GPL-3.0-only")
    assert [(x.licenses[0], x.line) for x in m] == [("MIT", 1), ("GPL-3.0-only", 3)]


def test_trailing_quotes_stripped():
    assert detect('SPDX-License-Identifier: "MIT"')[0].licenses == ("MIT",)
