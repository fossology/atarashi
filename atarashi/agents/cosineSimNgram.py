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
import argparse
from enum import Enum
import itertools
import json
import os

from numpy import unique
import textdistance

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.initialmatch import initial_match
from atarashi.libs.utils import wordFrequency, cosine_similarity

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"


class NgramAgent(AtarashiAgent):
  class NgramAlgo(Enum):
    cosineSim = 1
    diceSim = 2
    bigramCosineSim = 3

  def __init__(self, licenseList, ngramJson, algo=NgramAlgo.bigramCosineSim):
    super().__init__(licenseList)
    self.simType = algo
    if isinstance(ngramJson, str):
      with open(os.path.abspath(ngramJson), 'r') as file:
        self.ngramJson = json.load(file)
    elif isinstance(ngramJson, list):
      self.ngramJson = ngramJson
    else:
      raise ValueError("Set the ngramJson as either file path or json object")
    self.__precompute_data()

  def __precompute_data(self):
    '''
    Precompute word frequencies and tokens for the full license corpus.
    '''
    self.fullLicenseList = self.licenseList.copy()
    self.licenseUnigramFreq = []
    self.licenseBigramFreq = []
    self.licenseUnigramTokens = []

    for idx in range(len(self.fullLicenseList)):
      text = self.fullLicenseList.iloc[idx]['processed_text']
      unigrams = text.split(" ")
      self.licenseUnigramTokens.append(unigrams)
      self.licenseUnigramFreq.append(wordFrequency(unigrams))
      self.licenseBigramFreq.append(wordFrequency(self.__bigram_tokenize(text)))

  def __Ngram_guess(self, processedData):
    '''
    :param processedData: Processed Data form input file
    :return: Returns possible licenses contained in the input file based
              on matching unique N-grams from Ngram_keywords.json
    '''
    initial_guess = []

    for keywords in self.ngramJson:
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
    if self.verbose > 0:
      print("Length of guess using ngram identifers ", len(initial_guess))
      initial_guess.sort(key=lambda x: x['sim_score'], reverse=True)
      print("INITIAL GUESS WITH NGRAM IDENTIFIER", initial_guess)
    return initial_guess

  def __bigram_tokenize(self, s):
    '''
    :param string: Input string to create tokens
    :return: Array of bi-gram tokens
    '''
    return [s[i:i + 2] for i in range(len(s) - 1)]

  def scan(self, inputFile):
    '''
    :param inputFile: Input file path that needs to be scanned
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
    processedData = super().loadFile(inputFile)
    try:
      matches = initial_match(self.commentFile, processedData, self.licenseList)

      # Full text Bi-gram Cosine Similarity Match
      Cosine_matches = []
      Dice_matches = []
      Bigram_cosine_matches = []

      initial_guess = self.__Ngram_guess(processedData)
      ngram_guesses = []
      for guess in initial_guess:
        for x in guess['shortname']:
          ngram_guesses.append(x)

      all_guesses = unique([l['shortname'] for l in matches])
      filteredLicenseList = self.fullLicenseList[(self.fullLicenseList.shortname.isin(ngram_guesses)) |
                                                  (self.fullLicenseList.shortname.isin(all_guesses))]
      filteredLicenseList = filteredLicenseList.sort_values('shortname').reset_index(drop=False)

      processedUnigrams = processedData.split(" ")
      processedUnigramFreq = wordFrequency(processedUnigrams)
      processedBigrams = self.__bigram_tokenize(processedData)
      processedBigramFreq = wordFrequency(processedBigrams)

      for idx in range(len(filteredLicenseList)):
        # Get the original index to access precomputed data
        original_idx = filteredLicenseList.iloc[idx]['index']
        shortname = filteredLicenseList.iloc[idx]['shortname']

        if self.simType == self.NgramAlgo.cosineSim:
          # cosine similarity with unigram
          cosineSim = cosine_similarity(
              self.licenseUnigramFreq[original_idx],
              processedUnigramFreq)
          if cosineSim >= 0.6:
            Cosine_matches.append({
              'shortname': shortname,
              'sim_type': 'CosineSim',
              'sim_score': cosineSim,
              'description': ''
            })
          if self.verbose > 0:
            print("Cosine Sim ", str(cosineSim), shortname)

        elif self.simType == self.NgramAlgo.diceSim:
          # dice similarity
          diceSim = textdistance.sorensen(self.licenseUnigramTokens[original_idx],
                                          processedUnigrams)
          if diceSim >= 0.6:
            Dice_matches.append({
              'shortname': shortname,
              'sim_type': 'DiceSim',
              'sim_score': diceSim,
              'description': ''
            })
          if self.verbose > 0:
            print("Dice Sim ", str(diceSim), shortname)

        elif self.simType == self.NgramAlgo.bigramCosineSim:
          bigram_cosine_sim = cosine_similarity(
              self.licenseBigramFreq[original_idx],
              processedBigramFreq)
          if bigram_cosine_sim >= 0.9:
            Bigram_cosine_matches.append({
              'shortname': shortname,
              'sim_type': 'BigramCosineSim',
              'sim_score': bigram_cosine_sim,
              'description': ''
            })
            if self.verbose > 0:
              print("Bigram Cosine Sim ", str(bigram_cosine_sim), shortname)

      if self.simType == self.NgramAlgo.cosineSim and len(Cosine_matches) > 0:
        matches = list(itertools.chain(matches, Cosine_matches))

      if self.simType == self.NgramAlgo.diceSim and len(Dice_matches) > 0:
        matches = list(itertools.chain(matches, Dice_matches))

      if self.simType == self.NgramAlgo.bigramCosineSim and len(Bigram_cosine_matches) > 0:
        matches = list(itertools.chain(matches, Bigram_cosine_matches))

      matches.sort(key=lambda x: x['sim_score'], reverse=True)
      return matches
    finally:
      self.cleanup()

  def getSimAlgo(self):
    return self.simType

  def setSimAlgo(self, newAlgo):
    if isinstance(newAlgo, self.NgramAlgo):
      self.simType = newAlgo


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("processedLicenseList", help="Specify the processed license list file")
  parser.add_argument("ngramJson", help="Specify the location of NGRAM JSON")
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("-s", "--similarity", required=False, default="BigramCosineSim",
                      choices=["CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the similarity algorithm that you want")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action='count', default=0)
  args = parser.parse_args()

  licenseList = args.processedLicenseList
  ngramJsonLoc = args.ngramJson
  inputFile = args.inputFile
  simType = args.similarity
  verbose = args.verbose

  scanner = NgramAgent(licenseList, ngramJson=ngramJsonLoc, verbose=verbose)
  if simType == "CosineSim":
    scanner.setSimAlgo(NgramAgent.NgramAlgo.cosineSim)
  elif simType == "DiceSim":
    scanner.setSimAlgo(NgramAgent.NgramAlgo.diceSim)
  elif simType == "BigramCosineSim":
    scanner.setSimAlgo(NgramAgent.NgramAlgo.bigramCosineSim)

  result = scanner.scan(inputFile)
  if len(result) > 0:
    print("N-Gram identifier and " + str(simType) + " is " + str(result))
  else:
    print("Result is nothing")
