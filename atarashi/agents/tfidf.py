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

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.initialmatch import initial_match


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
    Precompute representations for the license corpus.
    '''
    all_documents = self.licenseList['processed_text'].tolist()

    # Precompute for Cosine Similarity (standard params)
    self.cosine_vectorizer = TfidfVectorizer(min_df=1, max_df=0.10, use_idf=True,
                                             smooth_idf=True, sublinear_tf=True,
                                             tokenizer=tokenize, token_pattern=None)
    self.cosine_license_matrix = self.cosine_vectorizer.fit_transform(all_documents).toarray()
    self.cosine_license_norms = np.linalg.norm(self.cosine_license_matrix, axis=1)

    # Precompute for Score Similarity (baseline-compatible per-file vocab)
    self._sumscore_vectorizer = CountVectorizer(min_df=1, tokenizer=tokenize, token_pattern=None)
    count_matrix = self._sumscore_vectorizer.fit_transform(all_documents)

    # idf in baseline is computed on (licenses + input doc) for input-doc vocab only:
    # n_docs_total = N + 1, df_total = df_licenses + 1 => idf = log((N+2)/(df+2)) + 1
    doc_freq = np.bincount(count_matrix.indices, minlength=count_matrix.shape[1])
    n_docs = len(all_documents)
    idf = np.log((n_docs + 2) / (doc_freq + 2)) + 1.0

    # Store un-normalized TF-IDF for licenses: (1 + log(tf)) * idf
    tf = count_matrix.astype(np.float64)
    tf.data = 1.0 + np.log(tf.data)
    self._sumscore_license_tfidf = tf.multiply(idf).tocsr()
    self._sumscore_vocab = self._sumscore_vectorizer.vocabulary_

  def __tfidfsumscore(self, inputFile):
    '''
    TF-IDF Sum Score Algorithm. Used TfidfVectorizer to implement it.

    :param inputFile: Input file path
    :return: Sorted array of JSON of scanner results with sim_type as __tfidfsumscore
    '''
    processedData1 = super().loadFile(inputFile)
    matches = initial_match(self.commentFile, processedData1, self.licenseList)

    startTime = time.time()

    input_words_sorted = sorted(set(processedData1.split(" ")))
    valid_indices = [self._sumscore_vocab[word] for word in input_words_sorted
                     if word in self._sumscore_vocab]

    score_arr = []
    if valid_indices:
      subset = self._sumscore_license_tfidf[:, valid_indices]
      norms = np.sqrt(np.asarray(subset.multiply(subset).sum(axis=1)).ravel())
      inv_norms = np.zeros_like(norms)
      nonzero = norms != 0
      inv_norms[nonzero] = 1.0 / norms[nonzero]

      normalized = subset.multiply(inv_norms.reshape(-1, 1))
      scores = np.asarray(normalized.sum(axis=1)).ravel()
    else:
      scores = np.zeros(len(self.licenseList), dtype=np.float64)

    for counter, sim_score in enumerate(scores):
      score_arr.append({
        'shortname': self.licenseList.iloc[counter]['shortname'],
        'sim_type': "Sum of TF-IDF score",
        'sim_score': float(sim_score),
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
    search_norm = np.linalg.norm(search_matrix)
    if search_norm != 0:
      dot_products = self.cosine_license_matrix.dot(search_matrix)
      denom = self.cosine_license_norms * search_norm
      sim_scores = np.divide(dot_products, denom, out=np.zeros_like(dot_products), where=denom != 0)

      for counter in np.nonzero(sim_scores >= 0.16)[0]:
        matches.append({
          'shortname': self.licenseList.iloc[counter]['shortname'],
          'sim_type': "TF-IDF Cosine Sim",
          'sim_score': float(sim_scores[counter]),
          'desc': ''
        })
    matches.sort(key=lambda x: x['sim_score'], reverse=True)
    if self.verbose > 0:
      print("time taken is " + str(time.time() - startTime) + " sec")
    return matches

  def scan(self, filePath):
    try:
      if self.algo == self.TfidfAlgo.cosineSim:
        return self.__tfidfcosinesim(filePath)
      if self.algo == self.TfidfAlgo.scoreSim:
        return self.__tfidfsumscore(filePath)
      return -1
    finally:
      self.cleanup()

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
