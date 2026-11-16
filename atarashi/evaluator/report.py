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

Helpers that turn the per-file records produced by evaluator.processFile()
into summaries, comparison tables and confusion data.
"""


def is_correct(record):
  '''
  A record is correct when the scan succeeded and the predicted license
  matches the expected one.
  '''
  return record['status'] == 'ok' and record['predicted'] == record['expected']


def summarize(records):
  '''
  Count the outcomes of an evaluation run.

  :param records: List of dicts returned by processFile()
  :return: Dict with total, correct, wrong, null, errors and accuracy (%)
  :rtype: dict
  '''
  total = len(records)
  correct = sum(1 for r in records if is_correct(r))
  null = sum(1 for r in records if r['status'] == 'null')
  errors = sum(1 for r in records if r['status'] == 'error')
  wrong = total - correct - null - errors
  accuracy = correct * 100 / total if total else 0.0
  return {
    'total': total,
    'correct': correct,
    'wrong': wrong,
    'null': null,
    'errors': errors,
    'accuracy': accuracy
  }


def misclassifications(records):
  '''
  List the files whose predicted license differs from the expected one.

  :param records: List of dicts returned by processFile()
  :return: Sorted list of (expected, predicted) tuples. Failed scans are
           reported with the prediction 'ERROR'.
  :rtype: list
  '''
  pairs = []
  for r in records:
    if is_correct(r):
      continue
    predicted = 'ERROR' if r['status'] == 'error' else r['predicted']
    pairs.append((r['expected'], predicted))
  return sorted(pairs)


def format_table(rows):
  '''
  Build a plain text comparison table.

  :param rows: List of dicts, each with agent, similarity, time and the
               keys returned by summarize()
  :return: The table as a string
  :rtype: str
  '''
  header = "{:<25}{:<17}{:>9}{:>9}{:>7}{:>6}{:>8}{:>10}".format(
    'Agent', 'Similarity', 'Accuracy', 'Correct', 'Wrong', 'NULL',
    'Errors', 'Time(s)')
  lines = [header, '-' * len(header)]
  for row in rows:
    lines.append("{:<25}{:<17}{:>8.1f}%{:>9}{:>7}{:>6}{:>8}{:>10.2f}".format(
      row['agent'], row['similarity'] or '-', row['accuracy'],
      row['correct'], row['wrong'], row['null'], row['errors'],
      row['time']))
  return '\n'.join(lines)


def confusion_matrix(records):
  '''
  Build a confusion matrix of expected (rows) vs predicted (columns)
  licenses.

  :param records: List of dicts returned by processFile()
  :return: pandas DataFrame with counts
  '''
  import pandas as pd
  expected = [r['expected'] for r in records]
  predicted = ['ERROR' if r['status'] == 'error' else r['predicted']
               for r in records]
  return pd.crosstab(pd.Series(expected, name='expected'),
                     pd.Series(predicted, name='predicted'))
