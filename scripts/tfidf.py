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
import itertools
import math
import time
import os

from initialmatch import initial_match
from numpy import unique, sum, dot
from sklearn.feature_extraction.text import TfidfVectorizer

args = None
tokenize = lambda data: data.split(" ")


def l2_norm(a):
  '''
  :return: Scalar value of word frequency array (vector)
  '''
  return math.sqrt(dot(a, a))


def cosine_similarity(a, b):
  '''
  `https://blog.nishtahir.com/2015/09/19/fuzzy-string-matching-using-cosine-similarity/`
  :return: Cosine similarity value of two word frequency arrays
  '''
  dot_product = dot(a, b)
  temp = l2_norm(a) * l2_norm(b)
  if temp == 0:
    return 0
  else:
    return dot_product / temp


def tfidfsumscore(inputFile, licenseList):
  '''
  TF-IDF Sum Score Algorithm. Used TfidfVectorizer to implement it.
  :param inputFile: Input file path
  :param licenseList: Processed License List
  :return: Sorted array of JSON of scanner results with sim_type as tfidfsumscore
  '''
  processedData1, licenses, matches = initial_match(inputFile, licenseList)

  startTime = time.time()
  processedData = unique(processedData1.split(" "))  # unique words from tokenized input file

  all_documents = licenses['processed_text'].tolist()
  all_documents.append(processedData1)
  sklearn_tfidf = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True, tokenizer=tokenize,
                                  vocabulary=processedData)

  sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

  score_arr = []
  result = 0
  for counter, value in enumerate(sklearn_representation.toarray()[:len(sklearn_representation.toarray()) - 1],
                                  start=0):
    sim_score = sum(value)
    score_arr.append({
      'shortname': licenses.iloc[result]['shortname'],
      'sim_type': "Sum of TF-IDF score",
      'sim_score': sim_score,
      'desc': "Score can be greater than 1 also"
    })
  score_arr.sort(key=lambda x: x['sim_score'], reverse=True)
  matches = list(itertools.chain(matches, score_arr[:5]))
  matches.sort(key=lambda x: x['sim_score'], reverse=True)
  if args is not None and args.verbose:
    print("time taken is " + str(time.time() - startTime) + " sec")
  return matches


def tfidfcosinesim(inputFile, licenseList):
  '''
  TF-IDF Cosine Similarity Algorithm. Used TfidfVectorizer to implement it.
  :param inputFile: Input file path
  :param licenseList: Processed License List
  :return: Sorted array of JSON of scanner results with sim_type as tfidfcosinesim
  '''
  processedData1, licenses, matches = initial_match(inputFile, licenseList)
  
  startTime = time.time()

  processedData = unique(processedData1.split(" "))  # unique words from tokenized input file
  all_documents = licenses['processed_text'].tolist()
  all_documents.append(processedData1)
  # sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True,
  #                                 tokenizer=tokenize, vocabulary=processedData)
  sklearn_tfidf = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True, tokenizer=tokenize)

  sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

  for counter, value in enumerate(sklearn_representation.toarray()[:len(sklearn_representation.toarray()) - 1],
                                  start=0):
    sim_score = cosine_similarity(value, sklearn_representation.toarray()[-1])
    if sim_score >= 0.8:
      matches.append({
        'shortname': licenses.iloc[counter]['shortname'],
        'sim_type': "TF-IDF Cosine Sim",
        'sim_score': sim_score,
        'desc': ''
      })
  matches.sort(key=lambda x: x['sim_score'], reverse=True)
  if args is not None and args.verbose:
    print("time taken is " + str(time.time() - startTime) + " sec")
  return matches


if __name__ == "__main__":
  print("The main file is called")
  curr_file_dir = os.path.abspath(os.path.dirname(__file__))
  default_processed_license = curr_file_dir + '/../licenses/processedLicenses.csv'
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("-p", "--processedLicenseList", required=False, default=default_processed_license,
                      help="Specify the processed license list file")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()

  filename = args.inputFile
  licenseList = args.processedLicenseList
  print("License Detected using TF-IDF algorithm + cosine similarity " + str(tfidfcosinesim(filename, licenseList)))
  print("License Detected using TF-IDF algorithm + sum score " + str(tfidfsumscore(filename, licenseList)))
