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
from initial_match import initial_match
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


def bigram_tokenize(s):
  return [s[i:i + 2] for i in range(len(s) - 1)]


def NgramSim(inputFile, licenseList, simType):
  processedData, licenses, matches = initial_match(inputFile, licenseList)

  # Full text Bi-gram Cosine Similarity Match
  Cosine_matches = []
  Dice_matches = []
  Bigram_cosine_matches = []

  initial_guess = Ngram_guess(processedData)
  ngram_guesses = []
  for guess in initial_guess:
    for x in guess['shortname']:
      ngram_guesses.append(x)
  # print(ngram_guesses)

  all_guesses = unique([l['shortname'] for l in matches])
  for license in [x for x in licenses if x[0] in ngram_guesses or x[0] in all_guesses]:

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
    matches = list(itertools.chain(matches, Cosine_matches))

  if simType == "DiceSim" and len(Dice_matches) > 0:
    matches = list(itertools.chain(matches, Dice_matches))

  if simType == "BigramCosineSim" and len(Bigram_cosine_matches) > 0:
    matches = list(itertools.chain(matches, Bigram_cosine_matches))

  matches.sort(key=lambda x: x['sim_score'], reverse=True)
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
