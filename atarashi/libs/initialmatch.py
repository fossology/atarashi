#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

import itertools


def HeadersNgramSim(header, processedData):
  '''
  Creates array of ngrams
  Check with the processed data how much are matching
  sim_score = matches/ count of ngrams

  :param header: License Header
  :param processedData: Input file extracted and processed data
  :return: Array of JSON with scanning results
  '''
  header = header.split(" ")
  ngrams = []
  for i in range(3, 8):
    ngrams += [header[j:j + i] for j in range(len(header) - i + 1)]
  count = 0
  for ngram in ngrams:
    if ' '.join(ngram) in processedData:
      count += 1
  sim = 0
  if len(ngrams) > 0:
    sim = float(count) / float(len(ngrams))
  return sim


def spdx_identifer(data, shortnames):
  '''
  Identify SPDX-License-Identifier tags via the first-class SPDX detector.

  Parses full SPDX expressions (AND/OR/WITH, `+`, LicenseRef) and resolves each
  component to a Fossology shortname; unresolved ids are dropped. Unlike the
  legacy scan this does not treat bare `license:` lines as tags.

  :param data: Input File data
  :param shortnames: Array of shortnames (SPDX-ID)
  :return: Array of JSON with scanning results
  '''
  from atarashi.spdx.resolver import detect_and_resolve
  return detect_and_resolve(data, shortnames)


def initial_match(filePath, processedData, licenses):
  '''
  :param inputFile: Input file path
  :param licenseList: Processed License List path
  :return: Array of JSON with scanning results from spdx_identifer and HeadersNgramSim
  '''

  with open(filePath) as file:
    raw_data = file.read()

  # Match SPDX identifiers
  spdx_identifiers = spdx_identifer(raw_data, licenses['shortname'])

  # match with headers
  # similarity with headers
  exact_match_header = []
  header_sim_match = []
  for idx in range(len(licenses)):
    header = licenses.iloc[idx]['processed_header']
    if len(header) > 0:
      if header in processedData:
        exact_match_header.append({
          'shortname': licenses.iloc[idx]['shortname'],
          'sim_type': 'ExactHeader',
          'sim_score': 1.0,
          'description': ''
        })
      ngram_sim = HeadersNgramSim(header, processedData)
      if ngram_sim >= 0.7:
        header_sim_match.append({
          'shortname': licenses.iloc[idx]['shortname'],
          'sim_type': 'HeaderNgramSimilarity',
          'sim_score': ngram_sim,
          'description': ''
        })

  # match with full text
  exact_match_fulltext = []
  for idx in range(len(licenses)):
    full_text = licenses.iloc[idx]['processed_text']
    if full_text in processedData:
      exact_match_fulltext.append({
        'shortname': licenses.iloc[idx]['shortname'],
        'sim_type': 'ExactFullText',
        'sim_score': 1.0,
        'description': ''
      })

  matches = list(itertools.chain(spdx_identifiers, exact_match_header, exact_match_fulltext, header_sim_match[:5]))
  return matches
