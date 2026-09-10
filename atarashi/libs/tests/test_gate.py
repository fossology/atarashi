#!/usr/bin/env python3
"""Tests for the optional Nirjas-gate front-end filter.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.libs.gate import should_scan


def test_injected_classifier_positive():
    assert should_scan("licensed under MIT", classifier=lambda texts: [True]) is True


def test_injected_classifier_negative():
    assert should_scan("just a todo comment", classifier=lambda texts: [False]) is False


def test_fails_open_when_gate_unavailable():
    # nirjas gate not installed in this env -> default classifier is None -> True
    assert should_scan("anything") is True
