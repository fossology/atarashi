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
import plac
import os
import json
import os
import errno
from pkg_resources import resource_filename

from atarashi.agents.cosineSimNgram import NgramAgent
from atarashi.agents.dameruLevenDist import DameruLevenDist
from atarashi.agents.tfidf import TFIDF
from atarashi.agents.wordFrequencySimilarity import WordFrequencySimilarity

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"
__version__ = "0.0.11"




def atarashii_runner(inputFile, agent_name, processedLicense, similarity="CosineSim", ngram_json=None, verbose=None):
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
    scanner = NgramAgent(processedLicense, ngramJson=ngram_json)
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
  if (os.path.isfile(inputFile)):
    result = scanner.scan(inputFile)
    return result
  else:    
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), inputFile)


@plac.annotations(
  agent_name = plac.Annotation("Name of the agent that needs to be run", "option", "a", str, ["wordFrequencySimilarity", "DLD", "tfidf", "Ngram"], metavar="{wordFrequencySimilarity,DLD,tfidf,Ngram}"),  
  inputFile = plac.Annotation("Specify the input file path to scan", "positional", None, str, metavar="inputFile"),
  processedLicense = plac.Annotation("Specify the location of processed license list file", "option", "l", str, metavar="PROCESSEDLICENSELIST"),
  ngram_json = plac.Annotation("Specify the location of Ngram JSON (for Ngram agent only)", "option", "j"),
  similarity = plac.Annotation("Specify the similarity algorithm that you want. First 2 are for TFIDF and last 3 are for Ngram", "option", "s", str, ["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"], metavar="{ScoreSim,CosineSim,DiceSim,BigramCosineSim}"),
  verbose = plac.Annotation("increase output verbosity", "flag", "v")  
)

def evaluate(inputFile, processedLicense, ngram_json, agent_name="wordFrequencySimilarity", similarity="CosineSim", verbose=False):
  '''
  Calls atarashii_runner for each file in the folder/ repository specified by user
  Prints the Input file path and the JSON output from atarashii_runner
  '''
  defaultProcessed = resource_filename("atarashi", "data/licenses/processedLicenses.csv")
  defaultJSON = resource_filename("atarashi", "data/Ngram_keywords.json")

  if processedLicense is None:
    processedLicense = defaultProcessed
  if ngram_json is None:
    ngram_json = defaultJSON
  if similarity is None:
    similarity = "CosineSim"

  try:
    result = atarashii_runner(inputFile, agent_name, processedLicense, similarity, ngram_json, verbose)
    if result != -1:
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
  except FileNotFoundError as e:
    print("Error: " + e.strerror+ ": '" + e.filename + "'")


def main():
  plac.call(evaluate)


if __name__ == '__main__':
  plac.call(evaluate)