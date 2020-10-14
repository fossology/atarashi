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
import os
import json
from pkg_resources import resource_filename

from atarashi.agents.cosineSimNgram import NgramAgent
from atarashi.agents.dameruLevenDist import DameruLevenDist
from atarashi.agents.tfidf import TFIDF
from atarashi.agents.wordFrequencySimilarity import WordFrequencySimilarity

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"
__version__ = "0.0.11"


def atarashii_runner(inputFile, processedLicense, agent_name, similarity="CosineSim", ngramJsonLoc=None, verbose=None):
  '''
  :param inputFile: Input File for scanning of license
  :param processedLicense: Processed License List (CSV) path (Default path already provided)
  :param agent_name: Specify the agent that you want to use for scanning
  :param similarity: Specify the similarity type to be used for the particular agent
  :param ngramJsonLoc: Specify N-Gram Json File location
  :param verbose: Specify if verbose mode is on or not (Default is Off/ None)
  :return: Returns the array of JSON with scan results

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
  scanner = ""
  if agent_name == "wordFrequencySimilarity":
    scanner = WordFrequencySimilarity(processedLicense)
  elif agent_name == "DLD":
    scanner = DameruLevenDist(processedLicense)
  elif agent_name == "tfidf":
    scanner = TFIDF(processedLicense)
    if similarity == "CosineSim":
      scanner.setSimAlgo(TFIDF.TfidfAlgo.cosineSim)
    elif similarity == "ScoreSim":
      scanner.setSimAlgo(TFIDF.TfidfAlgo.scoreSim)
    else:
      print("Please choose similarity from {CosineSim,ScoreSim}")
      return -1
  elif agent_name == "Ngram":
    scanner = NgramAgent(processedLicense, ngramJson=ngramJsonLoc)
    if similarity == "CosineSim":
      scanner.setSimAlgo(NgramAgent.NgramAlgo.cosineSim)
    elif similarity == "DiceSim":
      scanner.setSimAlgo(NgramAgent.NgramAlgo.diceSim)
    elif similarity == "BigramCosineSim":
      scanner.setSimAlgo(NgramAgent.NgramAlgo.bigramCosineSim)
    else:
      print("Please choose similarity from {CosineSim,DiceSim,BigramCosineSim}")
      return -1

  scanner.setVerbose(verbose)
  result = scanner.scan(inputFile)
  return result


def main():
  '''
  Calls atarashii_runner for each file in the folder/ repository specified by user
  Prints the Input file path and the JSON output from atarashii_runner
  '''
  defaultProcessed = resource_filename("atarashi", "data/licenses/processedLicenses.csv")
  defaultJSON = resource_filename("atarashi", "data/Ngram_keywords.json")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file path to scan")
  parser.add_argument("-l", "--processedLicenseList", required=False,
                      help="Specify the location of processed license list file")
  parser.add_argument("-a", "--agent_name", required=True,
                      choices=['wordFrequencySimilarity', 'DLD', 'tfidf', 'Ngram'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("-s", "--similarity", required=False, default="CosineSim",
                      choices=["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the similarity algorithm that you want."
                           " First 2 are for TFIDF and last 3 are for Ngram")
  parser.add_argument("-j", "--ngram_json", required=False,
                      help="Specify the location of Ngram JSON (for Ngram agent only)")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="count", default=0)
  parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
  args = parser.parse_args()
  inputFile = args.inputFile
  agent_name = args.agent_name
  similarity = args.similarity
  verbose = args.verbose
  processedLicense = args.processedLicenseList
  ngram_json = args.ngram_json

  if processedLicense is None:
    processedLicense = defaultProcessed
  if ngram_json is None:
    ngram_json = defaultJSON

  result = atarashii_runner(inputFile, processedLicense, agent_name, similarity, ngram_json, verbose)
  if agent_name == "wordFrequencySimilarity":
    result = [{
            "shortname": str(result),
            "sim_score": 1,
            "sim_type": "wordFrequencySimilarity",
            "description": ""
        }]
  elif agent_name == "DLD":
    result = [{
            "shortname": str(result),
            "sim_score": 1,
            "sim_type": "dld",
            "description": ""
        }]
  result = list(result)
  result = {"file": os.path.abspath(inputFile), "results": result}
  result = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=4)
  print(result + "\n")


if __name__ == '__main__':
  main()
