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

import argparse
import json
import math
import os
import itertools

import textdistance
from CommentExtractor import CommentExtract
from CommentPreprocessor import preprocess
from getLicenses import fetch_licenses
from nltk.tokenize import word_tokenize
from numpy import dot, unique

args = None


def l2_norm(a):
  a = [value for key, value in a.items()]
  return math.sqrt(dot(a, a))


def cosine_similarity(a, b):
  dot_product = 0
  for key, count in a.items():
    if key in b:
      dot_product += b[key] * count
  temp = l2_norm(a) * l2_norm(b)
  if temp == 0:
    return 0
  else:
    return dot_product / temp


def wordFrequency(arr):
  frequency = {}
  for word in arr:
    if word in frequency:
      frequency[word] += 1
    else:
      frequency[word] = 1
  return frequency


def Ngram_guess(processedData):
  dir = os.path.dirname(os.path.abspath(__file__))
  with open(dir + '/../database_keywordsNoStemSPDX1.json', 'r') as file:
    unique_keywords = json.loads(file.read())

  initial_guess = []

  for keywords in unique_keywords:
    matched_keys = 0
    for key in keywords['ngrams']:
      if key in processedData:
        matched_keys += 1
    if matched_keys > 0:
      initial_guess.append({
        'shortname': keywords['shortname'],
        'sim_type': 'Ngram guess',
        'sim_score': matched_keys / len(keywords['ngrams']),
        'description': ' '
      })
  if args is not None and args.verbose:
    print("Length of guess using ngram identifers ", len(initial_guess))
    initial_guess.sort(key=lambda x: x['sim_score'], reverse=True)
    print("INITIAL GUESS WITH NGRAM IDENTIFIER", initial_guess)
  return initial_guess


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


def bigram_tokenize(s):
  return [s[i:i + 2] for i in range(len(s) - 1)]


def spdx_identifer(data, shortnames):
  """
  Identify SPDX-License-Identifier
  Make sure the identifier must be present in Fossology merged license list
  """
  tokenized_data = data.split(" ")
  possible_spdx = []
  max_licenses = 5
  for idx in range(len(tokenized_data)):
    if tokenized_data[idx] == "SPDX-License-Identifier:":
      possible_spdx.append(tokenized_data[idx + 1:idx + 1 + max_licenses])
  spdx_identifiers = []
  for arr in possible_spdx:
    if len(arr) > 0:
      for word in arr:
        if word in shortnames:
          spdx_identifiers.append({
            'shortname': word,
            'sim_type': 'SPDXIdentifier',
            'sim_score': 1.0,
            'description': ''
          })

  return spdx_identifiers


def NgramSim(inputFile, licenseList, simType):
  commentFile = CommentExtract(inputFile)
  with open(commentFile) as file:
    data = file.read().replace('\n', ' ')
  processedData = preprocess(data)

  licenses = fetch_licenses(licenseList)

  # Match SPDX identifiers
  spdx_identifiers = spdx_identifer(data, [license[0] for license in licenses])

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
  header_sim_match.sort(key=lambda x: x['sim_score'], reverse=True)

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

  # Full text Bi-gram Cosine Similarity Match
  Cosine_matches = []
  Dice_matches = []
  Bigram_cosine_matches = []

  initial_guess = Ngram_guess(processedData)
  all_guesses = unique([l['shortname'] for l in matches])
  for license in [x for x in licenses if x[0] in [y['shortname'] for y in initial_guess] or x[0] in all_guesses]:

    if simType == "CosineSim":
      # cosine similarity with unigram
      cosineSim = cosine_similarity(wordFrequency(word_tokenize(license[1])),
                                    wordFrequency(word_tokenize(processedData)))
      if cosineSim >= 0.6:
        Cosine_matches.append({
          'shortname': license[0],
          'sim_type': 'CosineSim',
          'sim_score': cosineSim,
          'description': ''
        })
      if args is not None and args.verbose:
        print("Cosine Sim ", str(cosineSim), license[0])

    elif simType == "DiceSim":
      # dice similarity
      diceSim = textdistance.sorensen(word_tokenize(license[1]), word_tokenize(processedData))
      if diceSim >= 0.6:
        Dice_matches.append({
          'shortname': license[0],
          'sim_type': 'DiceSim',
          'sim_score': diceSim,
          'description': ''
        })
      if args is not None and args.verbose:
        print("Dice Sim ", str(diceSim), license[0])

    elif simType == "BigramCosineSim":
      bigram_cosine_sim = cosine_similarity(wordFrequency(bigram_tokenize(license[1])),
                                            wordFrequency(bigram_tokenize(processedData)))
      if bigram_cosine_sim >= 0.8:
        Bigram_cosine_matches.append({
          'shortname': license[0],
          'sim_type': 'BigramCosineSim',
          'sim_score': bigram_cosine_sim,
          'description': ''
        })
      if args is not None and args.verbose:
        print("Bigram Cosine Sim ", str(bigram_cosine_sim), license[0])

  if simType == "CosineSim" and len(Cosine_matches) > 0:
    Cosine_matches.sort(key=lambda x: x['sim_score'], reverse=True)
    matches = list(itertools.chain(matches, Cosine_matches))

  if simType == "DiceSim" and len(Dice_matches) > 0:
    Dice_matches.sort(key=lambda x: x['sim_score'], reverse=True)
    matches = list(itertools.chain(matches, Dice_matches))

  if simType == "BigramCosineSim" and len(Bigram_cosine_matches) > 0:
    Bigram_cosine_matches.sort(key=lambda x: x['sim_score'], reverse=True)
    matches = list(itertools.chain(matches, Bigram_cosine_matches))
  return matches


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("Similarity", choices=["CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the similarity algorithm that you want")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  inputFile = args.inputFile
  licenseList = args.licenseList
  simType = args.Similarity

  result = NgramSim(inputFile, licenseList, simType)
  if len(result) > 0:
    print("N-Gram identifier and " + str(simType) + " is " + str(result))
  else:
    print("Result is nothing")
