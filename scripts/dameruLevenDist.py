#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
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

'''
__author__ = "Aman Jain"

import os
import sys
import re
import csv
from CommentPreprocessor import preprocess
from CommentExtractor import CommentExtract
from pyxdameraulevenshtein import damerau_levenshtein_distance
from getLicenses import fetch_licenses
import time


'''Python Module to classify license using Damerau Levenshtein distance algorithm
Input: File from which license needs to be scanned and license list (CSV)
Output: License which is contained in the file.
Description: It extract comments from the file and after preprocessing,
              it calculates the damerau_levenshtein_distance and then classify
              by finding the leadt distance.
              python dameruLevenDist.py <filename> <licenseList>
'''

def classifyLicenseDameruLevenDist(processedData, licenses):
  # Classify the license with minimum distance with scanned file
  globalDistance = sys.maxsize
  result = 0
  for idx in range(len(licenses)):
    distance = damerau_levenshtein_distance(processedData.split(' '), licenses[idx][1].split(' '))
    print(str(idx) + "  " + licenses[idx][0] + "  " + str(distance))
    if distance < globalDistance:
      globalDistance = distance
      result = idx
  return result

# Input
filename = sys.argv[1]
licenseList = sys.argv[2]

# fetch preprocessed licenses
licenses = fetch_licenses(licenseList)

# extract comments and preprocess them
commentFile = CommentExtract(filename)
with open(commentFile) as file:
  data = file.read().replace('\n', ' ')
processedData = preprocess(data)

startTime = time.time()
print("license id --- License name --- Leven Dist")
result = classifyLicenseDameruLevenDist(processedData, licenses)
print("time taken is " + str(time.time() - startTime) + " seconds")
print("License Detected using Dameru Leven Distance: " + licenses[result][0])
