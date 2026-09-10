#!/usr/bin/env python3
"""Tests for the notice/short-form reference layer.

SPDX-License-Identifier: GPL-2.0-only
"""
import json

from atarashi.libs.references import DEFAULT_INDEX, load_notice_units


def _artifact(tmp_path, units):
    p = tmp_path / "notice_rules.json"
    p.write_text(json.dumps({"source": "test", "units": units}))
    return p


LONG = "licensed under the apache license version two point zero you may not use"


def test_maps_spdx_ids_to_caller_shortnames(tmp_path):
    path = _artifact(tmp_path, [["Apache-2.0", LONG]])
    assert list(load_notice_units(["Apache-2.0"], path=path)) == [("Apache-2.0", LONG, [])]


def test_mapping_is_case_insensitive(tmp_path):
    """The artifact keys on SPDX ids; a license list may case them differently."""
    path = _artifact(tmp_path, [["apache-2.0", LONG]])
    assert list(load_notice_units(["Apache-2.0"], path=path)) == [("Apache-2.0", LONG, [])]


def test_drops_licenses_the_caller_does_not_know(tmp_path):
    path = _artifact(tmp_path, [["Apache-2.0", LONG], ["Nonexistent-9.9", LONG]])
    assert [u[0] for u in load_notice_units(["Apache-2.0"], path=path)] == ["Apache-2.0"]


def test_drops_units_too_short_to_ever_match(tmp_path):
    """A unit shorter than the minimum run can never produce a match."""
    path = _artifact(tmp_path, [["Apache-2.0", "licensed under a ."], ["Apache-2.0", LONG]])
    assert list(load_notice_units(["Apache-2.0"], path=path, min_tokens=8)) == [("Apache-2.0", LONG, [])]


def test_missing_artifact_yields_nothing_rather_than_raising(tmp_path):
    """Fails open: an agent built before the index exists still runs full-text only."""
    assert list(load_notice_units(["MIT"], path=tmp_path / "absent.json")) == []


def test_shipped_artifact_is_present_and_substantial():
    """The committed index is the whole point of the layer; guard against a stub."""
    payload = json.loads(DEFAULT_INDEX.read_text())
    assert payload["source"] == "scancode-toolkit"
    assert payload["schema"] == 2
    assert len(payload["units"]) > 20000
    assert len({u[0] for u in payload["units"]}) > 900


def test_shipped_artifact_keeps_required_phrase_text_in_the_body():
    """Regression: `{{...}}` marks a required phrase, not a wildcard. Stripping the
    span deleted the most identifying wording and left generic filler indexed — it
    cost 32 points of coverage and 0.33 R@1 before it was caught."""
    payload = json.loads(DEFAULT_INDEX.read_text())
    texts = [u[1] for u in payload["units"] if u[0] == "Apache-2.0"]
    assert any("apache license" in t.lower() for t in texts)
    assert not any("{{" in t or "}}" in t for t in texts)
    assert sum(1 for u in payload["units"] if len(u) > 2 and u[2]) > 5000


def test_required_phrases_travel_with_the_unit(tmp_path):
    """`{{...}}` spans gate close variants apart; they must reach the matcher."""
    path = _artifact(tmp_path, [["MPL-2.0", LONG, ["no copyleft exception"]]])
    assert list(load_notice_units(["MPL-2.0"], path=path)) == [
        ("MPL-2.0", LONG, ["no copyleft exception"])]
