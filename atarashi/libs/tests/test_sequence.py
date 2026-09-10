#!/usr/bin/env python3
"""Tests for the token-sequence license matcher.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.libs.sequence import tied_with_leader, LicenseMatcher

MIT = ("Permission is hereby granted, free of charge, to any person obtaining a copy "
       "of this software and associated documentation files, to deal in the Software "
       "without restriction.")
BSD = ("Redistribution and use in source and binary forms, with or without "
       "modification, are permitted provided that the following conditions are met.")
REFS = [("MIT", MIT), ("BSD-3-Clause", BSD)]


def test_exact_full_text():
    m = LicenseMatcher(REFS)
    assert m.exact(MIT) == "MIT"
    assert m.exact("  PERMISSION is hereby granted, free of charge...") is None


def test_embedded_notice_matches_with_span():
    m = LicenseMatcher(REFS)
    doc = "/*\n * Copyright 2020 Acme\n * " + MIT + "\n */\nint main(){}"
    hits = m.match(doc)
    assert hits and hits[0].shortname == "MIT"
    assert hits[0].score >= 0.9
    # matched span points into the query token stream
    assert 0 <= hits[0].start < hits[0].end


def test_picks_matching_reference():
    m = LicenseMatcher(REFS)
    assert m.match(BSD)[0].shortname == "BSD-3-Clause"


def test_no_license_text_returns_empty():
    m = LicenseMatcher(REFS)
    assert m.match("int main() { return 0; } // just code, no license") == []


def test_partial_presence_scores_below_full():
    m = LicenseMatcher(REFS)
    half = "Permission is hereby granted, free of charge, to any person"
    hits = m.match(half)
    assert hits and hits[0].shortname == "MIT"
    assert hits[0].score < 1.0  # coverage of the reference is partial


def test_min_run_filters_short_contiguous_matches():
    m = LicenseMatcher(REFS)
    half = "Permission is hereby granted, free of charge, to any person"  # ~10-token run
    assert m.match(half, min_run=20) == []


def test_longest_run_ranking_beats_higher_raw_coverage():
    # SHORT ref shares scattered words with the query (higher coverage), LONG ref
    # shares one distinctive contiguous run — the long contiguous run must win.
    query = ("this software is provided under the following distinctive license grant "
             "clause alpha beta gamma delta epsilon zeta eta theta as written here")
    short_scattered = "this software the following license clause as here provided under"
    long_run = ("distinctive license grant clause alpha beta gamma delta epsilon zeta "
                "eta theta")
    m = LicenseMatcher([("SCATTERED", short_scattered), ("RUN", long_run)])
    assert m.match(query)[0].shortname == "RUN"


AGPL = ("This program is free software you can redistribute it under the terms of the "
        "GNU Affero General Public License as published by the Free Software Foundation.")
GPL = ("This program is free software you can redistribute it under the terms of the "
       "GNU General Public License as published by the Free Software Foundation.")


def test_required_phrase_gates_out_wrong_variant():
    refs = [("AGPL-3.0", AGPL), ("GPL-3.0", GPL)]
    required = [("AGPL-3.0", ["affero general public license"])]
    m = LicenseMatcher(refs, required=required)
    names = [h.shortname for h in m.match(GPL)]
    assert "AGPL-3.0" not in names
    assert "GPL-3.0" in names


def test_required_phrase_present_allows_match():
    refs = [("AGPL-3.0", AGPL)]
    m = LicenseMatcher(refs, required=[("AGPL-3.0", ["affero general public license"])])
    assert m.match(AGPL)[0].shortname == "AGPL-3.0"


def test_multiple_units_per_license_header_matches():
    full = ("Apache License Version 2.0 January 2004 terms and conditions for use "
            "reproduction and distribution as defined by sections below")
    header = ("Licensed under the Apache License Version 2.0 you may not use this file "
              "except in compliance with the License")
    m = LicenseMatcher([("Apache-2.0", full), ("Apache-2.0", header)])
    doc = "# " + header + "\nimport os\n"
    hits = m.match(doc)
    assert [h.shortname for h in hits] == ["Apache-2.0"]
    assert hits[0].score >= 0.9


# --- seed-and-extend core -----------------------------------------------------

def test_repetitive_reference_does_not_inflate_coverage():
    """A repeated phrase must be counted once, not once per place it occurs.

    Alignment seeds on shared n-grams and groups them by diagonal, so a single
    query phrase matching a reference that repeats it produces one run per
    occurrence. Summing those would report most of the reference as present when
    only a fraction of it is — the query token must be spent once.
    """
    phrase = "redistribution and use in source and binary forms are permitted"
    ref = " ".join([phrase] * 8)
    matcher = LicenseMatcher([("Repeat-1.0", ref)])
    hit = matcher.match(phrase, min_run=8)[0]
    assert hit.longest_run == len(phrase.split())
    # One of eight repetitions is present, so coverage must sit near an eighth —
    # emphatically not near 1.0, which is what unchained runs would report.
    assert hit.score < 0.2


def test_span_locates_the_notice_inside_surrounding_noise():
    notice = "permission is hereby granted free of charge to any person obtaining a copy"
    matcher = LicenseMatcher([("MIT", notice)])
    lead = "int main void return zero "
    hit = matcher.match(lead + notice + " more unrelated trailing code here", min_run=8)[0]
    assert hit.start == len(lead.split())
    assert hit.end == hit.start + len(notice.split())


def test_unseen_query_tokens_cannot_match():
    """Tokens absent from every reference share an id; they must never align."""
    matcher = LicenseMatcher([("MIT", "permission is hereby granted free of charge to any person")])
    assert matcher.match("zzz qqq vvv www xxx yyy", min_run=4) == []


# --- short references ---------------------------------------------------------

def test_short_reference_matches_only_when_present_in_full():
    """"Licensed under the Apache License, Version 2.0" is seven tokens. Requiring a
    run of `min_run` made the whole short-reference register unmatchable; such a
    reference is admitted, but only when the query contains all of it."""
    ref = "licensed under the apache license version 2.0"
    matcher = LicenseMatcher([("Apache-2.0", ref)])
    hits = matcher.match("this file is " + ref + " see license for details", min_run=8)
    assert [h.shortname for h in hits] == ["Apache-2.0"]
    assert hits[0].score == 1.0


def test_partial_short_reference_is_rejected():
    """Half a short reference is generic wording, not evidence."""
    matcher = LicenseMatcher([("Apache-2.0", "licensed under the apache license version 2.0")])
    assert matcher.match("licensed under the apache foundation grant terms", min_run=8) == []


def test_long_reference_still_requires_the_full_min_run():
    """The exemption applies only below min_run; long references are unaffected."""
    ref = " ".join(f"clause{i} of the agreement" for i in range(20))
    matcher = LicenseMatcher([("Long-1.0", ref)])
    assert matcher.match("clause3 of the agreement", min_run=8) == []


# --- per-unit required phrases ------------------------------------------------

def test_unit_required_phrase_separates_close_variants():
    """MPL-2.0 and MPL-2.0-no-copyleft-exception differ by one clause. Without the
    gate the shared body matches both and the variant is a coin flip."""
    body = ("this source code form is subject to the terms of the mozilla public "
            "license v 2.0 if a copy of the mpl was not distributed with this file")
    refs = [
        ("MPL-2.0", body, []),
        ("MPL-2.0-no-copyleft-exception", body, ["no copyleft exception"]),
    ]
    matcher = LicenseMatcher(refs, unit_gating=True)
    assert [h.shortname for h in matcher.match(body, min_run=8)] == ["MPL-2.0"]


def test_unit_required_phrase_admits_the_variant_when_present():
    body = "this source code form is subject to the terms of the mozilla public license"
    refs = [("MPL-2.0-no-copyleft-exception", body, ["no copyleft exception"])]
    matcher = LicenseMatcher(refs, unit_gating=True)
    assert matcher.match(body, min_run=8) == []
    assert [h.shortname for h in
            matcher.match(body + " no copyleft exception", min_run=8)] == \
        ["MPL-2.0-no-copyleft-exception"]


def test_two_tuple_references_still_work():
    """The 3-tuple form is an extension; plain (name, text) must keep working."""
    matcher = LicenseMatcher([("MIT", "permission is hereby granted free of charge to any person")])
    assert matcher.match("permission is hereby granted free of charge to any person",
                         min_run=8)[0].shortname == "MIT"


def test_unit_gating_is_off_by_default():
    """Measured as a net loss on real queries; the phrases ship, the hard gate does
    not. See the note in LicenseMatcher.__init__."""
    body = "this source code form is subject to the terms of the mozilla public license"
    refs = [("MPL-2.0-no-copyleft-exception", body, ["no copyleft exception"])]
    assert LicenseMatcher(refs).match(body, min_run=8)[0].shortname == \
        "MPL-2.0-no-copyleft-exception"


# --- reported result set ------------------------------------------------------

def test_only_genuine_ties_are_reported_alongside_the_leader():
    """Acceptance is per-candidate, so several close variants clear the bar on the
    same text. Reporting them all put four wrong licenses next to the right one on
    97% of files, invisible to any top-1 metric."""
    notice = "permission is hereby granted free of charge to any person obtaining a copy"
    refs = [("MIT", notice),
            ("Weaker-1.0", notice + " and to sublicense under further conditions")]
    hits = LicenseMatcher(refs).match(notice, min_run=8)
    assert len(hits) == 2, "both should match; the cut is what removes the weaker one"
    assert [h.shortname for h in tied_with_leader(hits)] == ["MIT"]


def test_a_true_tie_is_still_reported():
    """Identical evidence for two licenses is real ambiguity, not noise to hide."""
    notice = "redistribution and use in source and binary forms are permitted provided"
    hits = LicenseMatcher([("A-1.0", notice), ("B-1.0", notice)]).match(notice, min_run=8)
    assert sorted(h.shortname for h in tied_with_leader(hits)) == ["A-1.0", "B-1.0"]


def test_empty_input_is_handled():
    assert tied_with_leader([]) == []


# --- ranker family gate -------------------------------------------------------

def test_ranker_declines_outside_its_trained_families():
    """Held-out families are actively harmed (-0.051, GPL alone -0.134), so the model
    must not act on a license family it never trained on."""
    from atarashi.libs.ranker import rerank

    class Boom:
        def predict_proba(self, _):
            raise AssertionError("model must not be consulted for an unseen family")

    hits = LicenseMatcher([("NCSA", "permission is hereby granted free of charge to any"),
                           ("MIT", "permission is hereby granted free of charge to any person")]
                          ).match("permission is hereby granted free of charge to any", min_run=8)
    bundle = {"model": Boom(), "scaler": None, "families": ["MIT", "GPL"]}
    assert rerank(hits, bundle) is hits


def test_ranker_declines_on_the_unrecognised_family_bucket():
    """OTHER is a bucket for unrecognised names; it cannot vouch for coverage."""
    from atarashi.libs.ranker import family, rerank

    class Boom:
        def predict_proba(self, _):
            raise AssertionError("model must not be consulted for OTHER")

    hits = LicenseMatcher([("Weird-Vendor-EULA", "permission is hereby granted free of charge"),
                           ("MIT", "permission is hereby granted free of charge to any person")]
                          ).match("permission is hereby granted free of charge", min_run=8)
    assert family(hits[0].shortname) == "OTHER"
    assert rerank(hits, {"model": Boom(), "scaler": None,
                         "families": ["OTHER", "MIT"]}) is hits
