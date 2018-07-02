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
import os
import json
from numpy import dot
from CommentPreprocessor import preprocess
from CommentExtractor import CommentExtract
from getLicenses import fetch_licenses
from nltk.tokenize import word_tokenize
import textdistance

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


def wordFrequency(a):
  arr = word_tokenize(a)
  frequency = {}
  for word in arr:
    if word in frequency:
      frequency[word] += 1
    else:
      frequency[word] = 1
  return frequency


def Ngram_guess(processedData):
  dir = os.path.dirname(os.path.abspath(__file__))
  with open(dir + '/database_keywordsNoStemSPDX.json', 'r') as file:
    unique_keywords = json.loads(file.read())

  initial_guess = []

  for keywords in unique_keywords:
    # print(keywords)
    matched_keys = 0
    for key in keywords['ngrams']:
      if key in processedData:
        matched_keys += 1
    if matched_keys > 0:
      initial_guess.append({
        'shortname': keywords['shortname'],
        'match': matched_keys / len(keywords['ngrams'])
      })
  if args is not None and args.verbose:
    print("Length of guess using ngram identifers ", len(initial_guess))
    initial_guess.sort(key=lambda x: x['match'], reverse=True)
    print(initial_guess)
  return initial_guess


def CosineSimNgram(inputFile, licenseList):
  commentFile = CommentExtract(inputFile)
  with open(commentFile) as file:
    data = file.read().replace('\n', ' ')
  processedData = preprocess(data)

  licenses = fetch_licenses(licenseList)
  matches = []
  initial_guess = Ngram_guess(processedData)
  for license in [x for x in licenses if x[0] in [y['shortname'] for y in initial_guess]]:
    # cosineSim = cosine_similarity(wordFrequency(license[1]), wordFrequency(processedData))
    cosineSim = textdistance.sorensen(license[1], processedData)
    if cosineSim >= 0:
      matches.append({
        'shortname': license[0],
        'cosineSim': cosineSim
      })
      if args is not None and args.verbose:
        print(str(cosineSim), license[0])

  if len(matches) > 0:
    if args is not None and args.verbose:
      print("Length of matches ", len(matches))
    matches.sort(key=lambda x: x['cosineSim'], reverse=True)
    return matches
  return None


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  inputFile = args.inputFile
  licenseList = args.licenseList

  result = CosineSimNgram(inputFile, licenseList)
  if result is not None:
    print("N-Gram identifier and Vector space search ", str(result))
  else:
    print("Result is nothing")
