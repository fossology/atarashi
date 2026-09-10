#!/usr/bin/env python3
"""Tests for splitting a licence body from its instructional appendix.

SPDX-License-Identifier: GPL-2.0-only
"""
import unittest

from atarashi.libs.body import MIN_TRAILER_TOKENS, split_terms


def _trailer(words: int = MIN_TRAILER_TOKENS + 10) -> str:
    return " ".join(["boilerplate"] * words)


class SplitTermsTest(unittest.TestCase):
    def test_text_without_the_marker_is_unchanged(self):
        text = "Permission is hereby granted, free of charge, to any person"
        self.assertEqual(split_terms(text), (text, None))

    def test_empty_text(self):
        self.assertEqual(split_terms(""), ("", None))

    def test_splits_at_the_marker_and_keeps_it_with_the_grant(self):
        grant, appendix = split_terms(f"terms here END OF TERMS AND CONDITIONS {_trailer()}")
        self.assertTrue(grant.endswith("END OF TERMS AND CONDITIONS"))
        self.assertIsNotNone(appendix)
        assert appendix is not None
        self.assertIn("boilerplate", appendix)

    def test_match_is_case_insensitive_and_tolerates_wrapping(self):
        grant, appendix = split_terms(
            f"terms\n\nEnd of Terms\nand   Conditions\n\n{_trailer()}")
        self.assertIsNotNone(appendix)
        self.assertIn("terms", grant)

    def test_a_short_trailer_is_not_worth_a_unit(self):
        # A sign-off line is not an appendix, and a reference this short cannot match.
        text = "terms here END OF TERMS AND CONDITIONS thanks for reading"
        self.assertEqual(split_terms(text), (text, None))

    def test_splits_at_the_last_marker(self):
        text = ("first END OF TERMS AND CONDITIONS middle "
                "END OF TERMS AND CONDITIONS " + _trailer())
        grant, appendix = split_terms(text)
        self.assertIn("middle", grant)
        assert appendix is not None
        self.assertNotIn("middle", appendix)

    def test_the_two_halves_reconstruct_the_original(self):
        text = f"terms END OF TERMS AND CONDITIONS {_trailer()}"
        grant, appendix = split_terms(text)
        self.assertEqual(grant + (appendix or ""), text)


class RealLicenceShapeTest(unittest.TestCase):
    """The shape the split exists for: an Apache-style grant plus a how-to-apply tail."""

    APACHE_TAIL = (
        "APPENDIX: How to apply the Apache License to your work. To apply the Apache "
        "License to your work, attach the following boilerplate notice, with the "
        "fields enclosed by brackets replaced with your own identifying information. "
        "Copyright [yyyy] [name of copyright owner] Licensed under the Apache "
        "License, Version 2.0 (the \"License\"); you may not use this file except in "
        "compliance with the License."
    )

    def test_appendix_leaves_the_grant(self):
        grant, appendix = split_terms(
            "1. Definitions. License shall mean the terms and conditions for use. "
            "END OF TERMS AND CONDITIONS " + self.APACHE_TAIL)
        self.assertIn("Definitions", grant)
        self.assertNotIn("APPENDIX", grant)
        assert appendix is not None
        self.assertIn("boilerplate notice", appendix)


if __name__ == "__main__":
    unittest.main()
