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
import math
import time

from CommentExtractor import CommentExtract
from CommentPreprocessor import preprocess
from exactMatch import exactMatcher
from getLicenses import fetch_licenses
from numpy import unique, sum, dot
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize

args = None


def initialize(filename, licenseList):
  commentFile = CommentExtract(filename)
  with open(commentFile) as file:
    data = file.read().replace('\n', ' ')
  processedData = preprocess(data)

  licenses = fetch_licenses(licenseList)

  return processedData, licenses


def l2_norm(a):
  return math.sqrt(dot(a, a))


def cosine_similarity(a, b):
  return dot(a, b) / (l2_norm(a) * l2_norm(b))


def tfidfsumscore(filename, licenseList):
  processedData1, licenses = initialize(filename, licenseList)
  if args is not None and args.verbose:
    print("PROCESSED DATA IS", processedData1)
    print("First License is ", licenses[0])

  temp = exactMatcher(processedData1, licenseList)
  if temp == -1:
    startTime = time.time()
    processedData = unique(word_tokenize(processedData1))  # unique words from tokenized input file

    all_documents = [license[1] for license in licenses]
    all_documents.append(processedData1)
    sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True,
                                    tokenizer=word_tokenize, vocabulary=processedData)

    sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

    globalmax = -1
    result = 0
    for counter, value in enumerate(sklearn_representation.toarray()[:len(sklearn_representation.toarray()) - 1],
                                    start=0):
      localmax = sum(value)
      if localmax > globalmax:
        # change the condition for all possibilities
        globalmax = localmax
        result = counter

    if args is not None and args.verbose:
      print("time taken is " + str(time.time() - startTime) + " sec")
    return licenses[result][0]
  else:
    return temp


def tfidfcosinesim(filename, licenseList):
  processedData1, licenses = initialize(filename, licenseList)
  if args is not None and args.verbose:
    print("PROCESSED DATA IS", processedData1)
    print("First License is ", licenses[0])

  temp = exactMatcher(processedData1, licenseList)
  if temp == -1:
    startTime = time.time()

    processedData = unique(word_tokenize(processedData1))  # unique words from tokenized input file
    all_documents = [license[1] for license in licenses]
    all_documents.append(processedData1)
    # sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True,
    #                                 tokenizer=word_tokenize, vocabulary=processedData)
    sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=True,
                                    tokenizer=word_tokenize)

    sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

    globalmax = -1
    result = 0
    for counter, value in enumerate(sklearn_representation.toarray()[:len(sklearn_representation.toarray()) - 1],
                                    start=0):
      localmax = cosine_similarity(value, sklearn_representation.toarray()[-1])
      if localmax > globalmax:
        # change the condition for all possibilities
        globalmax = localmax
        result = counter
    if args is not None and args.verbose:
      print("time taken is " + str(time.time() - startTime) + " sec")
    return licenses[result][0]
  else:
    return temp


if __name__ == "__main__":
  print("The main file is called")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("-s", "--stop-words", help="Set to use stop word filtering",
                      action="store_true", dest="stopWords")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()

  filename = args.inputFile
  licenseList = args.licenseList
  print("License Detected using TF-IDF algorithm + cosine similarity " + str(tfidfcosinesim(filename, licenseList)))
  print("License Detected using TF-IDF algorithm + sum score " + str(tfidfsumscore(filename, licenseList)))
