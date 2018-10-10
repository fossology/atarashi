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

  def __cosine_similarity(self, a, b):
    '''
    https://blog.nishtahir.com/2015/09/19/fuzzy-string-matching-using-cosine-similarity/

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

    # unique words from tokenized input file
    processedData = unique(processedData1.split(" "))

    all_documents = self.licenseList['processed_text'].tolist()
    all_documents.append(processedData1)
    sklearn_tfidf = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=True,
                                    sublinear_tf=True, tokenizer=tokenize,
                                    vocabulary=processedData)

    sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

    score_arr = []
    result = 0
    for counter, value in enumerate(sklearn_representation.toarray()[:len(sklearn_representation.toarray()) - 1],
                                    start=0):
      sim_score = sum(value)
      score_arr.append({
        'shortname': self.licenseList.iloc[result]['shortname'],
        'sim_type': "Sum of TF-IDF score",
        'sim_score': sim_score,
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

    all_documents = self.licenseList['processed_text'].tolist()
    all_documents.append(processedData1)
    sklearn_tfidf = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True, tokenizer=tokenize)

    sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

    for counter, value in enumerate(sklearn_representation.toarray()[:len(sklearn_representation.toarray()) - 1],
                                    start=0):
      sim_score = self.__cosine_similarity(value, sklearn_representation.toarray()[-1])
      if sim_score >= 0.8:
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
