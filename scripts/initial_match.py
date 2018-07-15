#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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

from CommentExtractor import CommentExtract
from CommentPreprocessor import preprocess
from getLicenses import fetch_licenses
from nltk.tokenize import word_tokenize
import itertools


def HeadersNgramSim(header, processedData):
  """
  make array of ngrams
  check with the processed data how much are matching
  sim_score = matches/ count of ngrams
  """
  header = word_tokenize(header)
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
  """
  Identify SPDX-License-Identifier
  Make sure the identifier must be present in Fossology merged license list
  """
  data = data.lower()  # preprocessing of data
  shortnames = [shortname.lower() for shortname in shortnames]
  tokenized_data = data.split('\n')
  possible_spdx = []
  for idx in range(len(tokenized_data)):
    if "spdx-license-identifier:" in tokenized_data[idx] or "license:" in tokenized_data[idx]:
      possible_spdx.append(tokenized_data[idx])

  spdx_identifiers = []
  for identifiers in possible_spdx:
    for x in identifiers.split(" "):
      if x in shortnames:
        spdx_identifiers.append({
          'shortname': x,
          'sim_type': 'SPDXIdentifier',
          'sim_score': 1.0,
          'description': ''
        })

  return spdx_identifiers


def initial_match(inputFile, licenseList):
  commentFile = CommentExtract(inputFile)
  with open(commentFile) as file:
    raw_data = file.read()
    data = raw_data.replace('\n', ' ')
  processedData = preprocess(data)

  licenses = fetch_licenses(licenseList)

  # Match SPDX identifiers
  spdx_identifiers = spdx_identifer(raw_data, [license[0] for license in licenses])

  # match with headers
  # similarity with headers
  exact_match_header = []
  header_sim_match = []
  for license in licenses:
    header = license[3]
    if len(header) > 0:
      if header in processedData:
        exact_match_header.append({
          'shortname': license[0],
          'sim_type': 'ExactHeader',
          'sim_score': 1.0,
          'description': ''
        })
      ngram_sim = HeadersNgramSim(header, processedData)
      if ngram_sim >= 0.7:
        header_sim_match.append({
          'shortname': license[0],
          'sim_type': 'HeaderNgramSimilarity',
          'sim_score': ngram_sim,
          'description': ''
        })

  # match with full text
  exact_match_fulltext = []
  for license in licenses:
    full_text = license[1]
    if full_text in processedData:
      exact_match_fulltext.append({
        'shortname': license[0],
        'sim_type': 'ExactFullText',
        'sim_score': 1.0,
        'description': ''
      })

  matches = list(itertools.chain(spdx_identifiers, exact_match_header, exact_match_fulltext, header_sim_match[:5]))
  return processedData, licenses, matches