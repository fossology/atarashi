#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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

import argparse
import json
import math
import os
import itertools

import textdistance
from initialmatch import initial_match
from numpy import dot, unique
from utils import unpack_json_tar

args = None


def l2_norm(a):
  '''
  :return: Scalar value of word frequency array (vector)
  '''
  a = [value for key, value in a.items()]
  return math.sqrt(dot(a, a))


def cosine_similarity(a, b):
  '''
  `https://blog.nishtahir.com/2015/09/19/fuzzy-string-matching-using-cosine-similarity/`
  :return: Cosine similarity value of two word frequency arrays
  '''
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
  '''
  Input: Array of words
  :return: Word Frequency array
  '''
  frequency = {}
  for word in arr:
    if word in frequency:
      frequency[word] += 1
    else:
      frequency[word] = 1
  return frequency


def Ngram_guess(processedData):
  '''
  :param processedData: Processed Data form input file
  :return: Returns possible licenses contained in the input file based on matching unique N-grams from Ngram_keywords.json
  '''
  unpack_json_tar()
  dir = os.path.dirname(os.path.abspath(__file__))
  with open(dir + '/../data/Ngram_keywords.json', 'r') as file:
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


def bigram_tokenize(string):
  '''
  :param string: Input string to create tokens
  :return: Array of bi-gram tokens
  '''
  return [string[i:i + 2] for i in range(len(string) - 1)]


def NgramSim(inputFile, licenseList, simType):
  '''
  :param inputFile: Input file path that needs to be scanned
  :param licenseList: Processed License List from which licenses needs to be classified
  :param simType: Specify the type of similarity to use ["CosineSim", "DiceSim", "BigramCosineSim"]
  :return: Array of JSON with the output of scan of the file.
  +------------+-----------------------------------------------------------+
  | shortname  | Short name of the license                                 |
  +------------+-----------------------------------------------------------+
  | sim_type   | Type of similarity from which the result is generated     |
  +------------+-----------------------------------------------------------+
  | sim_score  | Similarity score for the algorithm used mentioned above   |
  +------------+-----------------------------------------------------------+
  | desc       | Description/ comments for the similarity measure          |
  +------------+-----------------------------------------------------------+

  '''
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

  all_guesses = unique([l['shortname'] for l in matches])
  licenses = licenses[(licenses.shortname.isin(ngram_guesses)) |
                      (licenses.shortname.isin(all_guesses))]
  licenses.sort_values('shortname').reset_index(drop=True)

  for idx in range(len(licenses)):

    if simType == "CosineSim":
      # cosine similarity with unigram
      cosineSim = cosine_similarity(wordFrequency(licenses.iloc[idx]['processed_text'].split(" ")),
                                    wordFrequency(processedData.split(" ")))
      if cosineSim >= 0.6:
        Cosine_matches.append({
          'shortname': licenses.iloc[idx]['shortname'],
          'sim_type': 'CosineSim',
          'sim_score': cosineSim,
          'description': ''
        })
      if args is not None and args.verbose:
        print("Cosine Sim ", str(cosineSim), licenses.iloc[idx]['shortname'])

    elif simType == "DiceSim":
      # dice similarity
      diceSim = textdistance.sorensen(licenses.iloc[idx]['processed_text'].split(" "), processedData.split(" "))
      if diceSim >= 0.6:
        Dice_matches.append({
          'shortname': licenses.iloc[idx]['shortname'],
          'sim_type': 'DiceSim',
          'sim_score': diceSim,
          'description': ''
        })
      if args is not None and args.verbose:
        print("Dice Sim ", str(diceSim), licenses.iloc[idx]['shortname'])

    elif simType == "BigramCosineSim":
      bigram_cosine_sim = cosine_similarity(wordFrequency(bigram_tokenize(licenses.iloc[idx]['processed_text'])),
                                            wordFrequency(bigram_tokenize(processedData)))
      if bigram_cosine_sim >= 0.9:
        Bigram_cosine_matches.append({
          'shortname': licenses.iloc[idx]['shortname'],
          'sim_type': 'BigramCosineSim',
          'sim_score': bigram_cosine_sim,
          'description': ''
        })
        if args is not None and args.verbose:
          print("Bigram Cosine Sim ", str(bigram_cosine_sim), licenses.iloc[idx]['shortname'])

  if simType == "CosineSim" and len(Cosine_matches) > 0:
    matches = list(itertools.chain(matches, Cosine_matches))

  if simType == "DiceSim" and len(Dice_matches) > 0:
    matches = list(itertools.chain(matches, Dice_matches))

  if simType == "BigramCosineSim" and len(Bigram_cosine_matches) > 0:
    matches = list(itertools.chain(matches, Bigram_cosine_matches))

  matches.sort(key=lambda x: x['sim_score'], reverse=True)
  return matches


if __name__ == "__main__":
  curr_file_dir = os.path.abspath(os.path.dirname(__file__))
  default_processed_license = curr_file_dir + '/../licenses/processedLicenses.csv'
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("-p", "--processedLicenseList", required=False, default=default_processed_license,
                      help="Specify the processed license list file")
  parser.add_argument("-s", "--similarity", required=False, default="BigramCosineSim",
                      choices=["CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the similarity algorithm that you want")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  inputFile = args.inputFile
  licenseList = args.processedLicenseList
  simType = args.similarity

  result = NgramSim(inputFile, licenseList, simType)
  if len(result) > 0:
    print("N-Gram identifier and " + str(simType) + " is " + str(result))
  else:
    print("Result is nothing")
