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

import argparse
from enum import Enum
import itertools
import time

from numpy import unique, sum, dot
from sklearn.feature_extraction.text import TfidfVectorizer

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.initialmatch import initial_match
from atarashi.libs.utils import l2_norm


def tokenize(data): return data.split(" ")


class TFIDF(AtarashiAgent):

  class TfidfAlgo(Enum):
    scoreSim = 1
    cosineSim = 2

  def __init__(self, licenseList, algo=TfidfAlgo.cosineSim):
    super().__init__(licenseList)
    self.algo = algo
    self.__precompute_tfidf()

  def __precompute_tfidf(self):
    '''
    Precompute TF-IDF vectors for the license corpus.
    '''
    all_documents = self.licenseList['processed_text'].tolist()

    # Precompute for Cosine Similarity (standard params)
    self.cosine_vectorizer = TfidfVectorizer(min_df=1, max_df=0.10, use_idf=True,
                                             smooth_idf=True, sublinear_tf=True,
                                             tokenizer=tokenize, token_pattern=None)
    self.cosine_license_matrix = self.cosine_vectorizer.fit_transform(all_documents).toarray()

    # Precompute for Score Similarity (no max_df, no vocabulary restriction yet)
    self.score_vectorizer = TfidfVectorizer(min_df=1, use_idf=True, smooth_idf=True,
                                            sublinear_tf=True, tokenizer=tokenize,
                                            token_pattern=None)
    self.score_license_matrix = self.score_vectorizer.fit_transform(all_documents).toarray()

  def __cosine_similarity(self, a, b):
    '''
    https://blog.nishtahir.com/fuzzy-string-matching-using-cosine-similarity/

    :return: Cosine similarity value of two word frequency arrays
    '''
    dot_product = dot(a, b)
    temp = l2_norm(a) * l2_norm(b)
    if temp == 0:
      return 0
    else:
      return dot_product / temp

  def __tfidfsumscore(self, inputFile):
    '''
    TF-IDF Sum Score Algorithm. Used TfidfVectorizer to implement it.

    :param inputFile: Input file path
    :return: Sorted array of JSON of scanner results with sim_type as __tfidfsumscore
    '''
    processedData1 = super().loadFile(inputFile)
    matches = initial_match(self.commentFile, processedData1, self.licenseList)

    startTime = time.time()

    # The original implementation restricted vocabulary to unique words in input file.
    # To maintain semantic parity while being efficient, we use the precomputed matrix
    # but only sum the elements corresponding to words present in the input file.
    input_words = set(processedData1.split(" "))
    feature_names = self.score_vectorizer.get_feature_names_out()
    # Indices of features (words) that are present in the input file
    valid_indices = [i for i, word in enumerate(feature_names) if word in input_words]

    score_arr = []
    if valid_indices:
        # subset of matrix with only valid word columns
        subset_matrix = self.score_license_matrix[:, valid_indices]
        sums = subset_matrix.sum(axis=1)
        for counter, sim_score in enumerate(sums):
            score_arr.append({
                'shortname': self.licenseList.iloc[counter]['shortname'],
                'sim_type': "Sum of TF-IDF score",
                'sim_score': sim_score,
                'desc': "Score can be greater than 1 also"
            })
    else:
        # No words match
        for counter in range(len(self.licenseList)):
            score_arr.append({
                'shortname': self.licenseList.iloc[counter]['shortname'],
                'sim_type': "Sum of TF-IDF score",
                'sim_score': 0.0,
                'desc': "Score can be greater than 1 also"
            })

    score_arr.sort(key=lambda x: x['sim_score'], reverse=True)
    matches = list(itertools.chain(matches, score_arr[:5]))
    matches.sort(key=lambda x: x['sim_score'], reverse=True)
    if self.verbose > 0:
      print("time taken is " + str(time.time() - startTime) + " sec")
    return matches

  def __tfidfcosinesim(self, inputFile):
    '''
    TF-IDF Cosine Similarity Algorithm. Used TfidfVectorizer to implement it.

    :param inputFile: Input file path
    :return: Sorted array of JSON of scanner results with sim_type as __tfidfcosinesim
    '''
    processedData1 = super().loadFile(inputFile)
    matches = initial_match(self.commentFile, processedData1, self.licenseList)

    startTime = time.time()

    search_matrix = self.cosine_vectorizer.transform([processedData1]).toarray()[0]

    for counter, value in enumerate(self.cosine_license_matrix, start=0):
      sim_score = self.__cosine_similarity(value, search_matrix)
      if sim_score >= 0.16:
        matches.append({
          'shortname': self.licenseList.iloc[counter]['shortname'],
          'sim_type': "TF-IDF Cosine Sim",
          'sim_score': sim_score,
          'desc': ''
        })
    matches.sort(key=lambda x: x['sim_score'], reverse=True)
    if self.verbose > 0:
      print("time taken is " + str(time.time() - startTime) + " sec")
    return matches

  def scan(self, filePath):
    if self.algo == self.TfidfAlgo.cosineSim:
      return self.__tfidfcosinesim(filePath)
    elif self.algo == self.TfidfAlgo.scoreSim:
      return self.__tfidfsumscore(filePath)
    else:
      return -1

  def getSimAlgo(self):
    return self.algo

  def setSimAlgo(self, newAlgo):
    if isinstance(newAlgo, self.TfidfAlgo):
      self.algo = newAlgo


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--tfidf_similarity", required=False,
                      default="ScoreSim",
                      choices=["CosineSim", "ScoreSim"],
                      help="Specify the similarity algorithm that you want")
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("processedLicenseList",
                      help="Specify the processed license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="count", default=0)
  args = parser.parse_args()

  tfidf_similarity = args.tfidf_similarity
  filename = args.inputFile
  licenseList = args.processedLicenseList
  verbose = args.verbose

  scanner = TFIDF(licenseList, verbose=verbose)
  if tfidf_similarity == "CosineSim":
    scanner.setSimAlgo(TFIDF.TfidfAlgo.cosineSim)
    print("License Detected using TF-IDF algorithm + cosine similarity " + str(scanner.scan(filename)))
  else:
    scanner.setSimAlgo(TFIDF.TfidfAlgo.scoreSim)
    print("License Detected using TF-IDF algorithm + sum score " + str(scanner.scan(filename)))
