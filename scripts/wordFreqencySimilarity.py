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

Author: Aman Jain (amanjain5221@gmail.com)
'''

import re
import sys

from CommentExtractor import CommentExtract
from getLicenses import fetch_licenses
from CommentPreprocessor import preprocess

'''Python Module to classify license using histogram similarity algorithm
Input: File from which license needs to be scanned and license list (CSV)
Output: License which is contained in the file.
Description: It extract comments from the file and after preprocessing,
              it creates a frequency array of words and then classify it
              by finding the best match.
              python wordFrequencySimilarity.py <filename> <licenseList>
'''

# Input
filename = sys.argv[1]
licenseList = sys.argv[2]

commentFile = CommentExtract(filename)
with open(commentFile) as file:
  data = file.read().replace('\n', ' ')
processedData = preprocess(data)

def wordFrequency(data):
  # Find word frequency
  match_pattern = re.findall(r'\b[a-z]{3,15}\b', data)
  frequency = {}
  for word in match_pattern:
    count = frequency.get(word,0)
    frequency[word] = count + 1
  return frequency

def classifyLicenseFreqMatch(processedLicense, licensesFrequency):
  # Histogram Similarity Algorithm
  globalCount = 0
  result = 0
  for idx in range(len(licensesFrequency)):
    tempCount = 0
    for word, processedLicenseWordFreq in processedLicense.items():
      licenseWordFreq = licensesFrequency[idx].get(word, 0)
      if min(licenseWordFreq, processedLicenseWordFreq) > 0:
        tempCount = tempCount + min(licenseWordFreq, processedLicenseWordFreq)
    if globalCount < tempCount:
      result = idx
      globalCount = tempCount
  return result

# fetch preprocessed licenses
licenses = fetch_licenses(licenseList)

# create array of frequency array of licenses
licensesFrequency = []
for idx in range(len(licenses)):
  license = licenses[idx][1]
  licensesFrequency.append(wordFrequency(license))

processedLicense = wordFrequency(processedData)
result = classifyLicenseFreqMatch(processedLicense, licensesFrequency)
print("License Detected: " + licenses[result][0])
