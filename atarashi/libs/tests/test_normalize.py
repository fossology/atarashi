#!/usr/bin/env python3
"""Tests for SPDX-style normalization.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.libs.normalize import normalize, token_spans, tokens


def test_case_and_whitespace_collapsed():
    assert normalize("Permission   is\nHEREBY  granted") == "permission is hereby granted"


def test_punctuation_neutralized():
    assert normalize('"MIT", (the License);') == "mit the license"


def test_curly_quotes_and_dashes_folded():
    # smart quotes and en/em dashes must not create distinct tokens
    assert normalize("“BSD” — style") == normalize('"BSD" - style')


def test_tokens_split():
    assert tokens("Apache License, Version 2.0") == ["apache", "license", "version", "2", "0"]


def test_empty_is_empty():
    assert tokens("   \n  ") == []
    assert normalize("") == ""


# --- source offsets -----------------------------------------------------------

def test_token_spans_offsets_index_the_original_text():
    text = 'Licensed under the Apache License, Version 2.0 (the "License");'
    for token, start, end in token_spans(text):
        assert text[start:end].lower() == token


def test_token_spans_agree_with_tokens():
    """`tokens` is derived from `token_spans`; a drift would misalign every span."""
    text = "  Copyright (c) 2020 ACME  --  ALL rights\treserved.\n\nMIT licence!!  "
    assert [t for t, _, _ in token_spans(text)] == tokens(text)


def test_offsets_survive_punctuation_and_whitespace_collapse():
    """Normalization changes length, so offsets cannot come from the normalized form."""
    text = "a***b   \n  c"
    assert [(s, e) for _, s, e in token_spans(text)] == [(0, 1), (4, 5), (11, 12)]
