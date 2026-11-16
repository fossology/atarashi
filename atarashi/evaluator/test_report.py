#!/usr/bin/env python3
"""
SPDX-License-Identifier: GPL-2.0

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from report import summarize, misclassifications, format_table


def record(expected, predicted, status='ok'):
  return {'file': expected + '.c', 'expected': expected,
          'predicted': predicted, 'status': status, 'error': None}


RECORDS = [
  record('MIT', 'MIT'),
  record('BSD-3-Clause', 'BSD-2-Clause'),
  record('GPL-2.0-only', 'NULL', 'null'),
  record('Apache-2.0', None, 'error'),
]


class TestSummarize(unittest.TestCase):

  def test_counts_each_outcome(self):
    summary = summarize(RECORDS)
    self.assertEqual(summary['total'], 4)
    self.assertEqual(summary['correct'], 1)
    self.assertEqual(summary['wrong'], 1)
    self.assertEqual(summary['null'], 1)
    self.assertEqual(summary['errors'], 1)
    self.assertEqual(summary['accuracy'], 25.0)

  def test_empty_input_does_not_divide_by_zero(self):
    summary = summarize([])
    self.assertEqual(summary['total'], 0)
    self.assertEqual(summary['accuracy'], 0.0)

  def test_all_correct(self):
    summary = summarize([record('MIT', 'MIT'), record('Zlib', 'Zlib')])
    self.assertEqual(summary['accuracy'], 100.0)
    self.assertEqual(summary['wrong'], 0)


class TestMisclassifications(unittest.TestCase):

  def test_lists_only_mistakes(self):
    self.assertEqual(misclassifications(RECORDS), [
      ('Apache-2.0', 'ERROR'),
      ('BSD-3-Clause', 'BSD-2-Clause'),
      ('GPL-2.0-only', 'NULL'),
    ])

  def test_no_mistakes(self):
    self.assertEqual(misclassifications([record('MIT', 'MIT')]), [])


class TestFormatTable(unittest.TestCase):

  def test_contains_agent_and_accuracy(self):
    row = dict(summarize(RECORDS), agent='tfidf', similarity='CosineSim',
               time=1.5)
    table = format_table([row])
    self.assertIn('tfidf', table)
    self.assertIn('CosineSim', table)
    self.assertIn('25.0%', table)

  def test_agent_without_similarity_shows_dash(self):
    row = dict(summarize(RECORDS), agent='DLD', similarity=None, time=1.0)
    self.assertIn('DLD', format_table([row]))


if __name__ == '__main__':
  unittest.main()
