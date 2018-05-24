#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv
from preprocessing import preprocess
from CommentExtractor import CommentExtract

'''Python Module to classify license using histogram similarity algorithm
Input: File from which license needs to be scanned and license list (CSV)
Output: License which is contained in the file.
Description: It extract comments from the file and after preprocessing,
              it creates a frequency array of words and then classify if
              by finding the best match.
              python wordFrequencySimilarity.py <filename> <licenseList>
'''

# Input
filename = sys.argv[1]
licenseList = sys.argv[2]

commentFile = CommentExtract(filename)
processedData = preprocess(commentFile)

def wordFrequency(data):
  # Find word frequency
  match_pattern = re.findall(r'\b[a-z]{3,15}\b', data)
  frequency = {}
  for word in match_pattern:
    count = frequency.get(word,0)
    frequency[word] = count + 1
  return frequency

def classifyLicense(processedLicense, licensesFrequencyArray):
  # Histogram Similarity Algorithm
  globalCount = -1
  result = 0
  for idx in range(len(licensesFrequencyArray)):
    tempCount = 0
    for word, processedLicenseWordFreq in processedLicense.items():
      licenseWordFreq = licensesFrequencyArray[idx].get(word, 0)
      if min(licenseWordFreq, processedLicenseWordFreq) > 0:
        tempCount = tempCount + min(licenseWordFreq, processedLicenseWordFreq)
    if globalCount < tempCount:
      result = idx
      globalCount = tempCount
  return result

# Fetch license name and description from the License List (CSV)
licenses = []
with open(licenseList, 'r') as licenseFile:
  licenseReader = csv.reader(licenseFile)
  count = 0
  for row in licenseReader:
    if count > 0: 
      licenses.append(row[1:3])
    count = count + 1

licensesFrequencyArray = []
for idx in range(len(licenses)):
  license = licenses[idx][1]
  licensesFrequencyArray.append(wordFrequency(license))

processedLicense = wordFrequency(processedData)
result = classifyLicense(processedLicense, licensesFrequencyArray)
print("License Detected: " + licenses[result][0])