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
import errno
import json
import os
import sys
from pathlib import Path

from atarashi.agents.cosineSimNgram import NgramAgent
from atarashi.agents.dameruLevenDist import DameruLevenDist
from atarashi.agents.tfidf import TFIDF
from atarashi.agents.wordFrequencySimilarity import WordFrequencySimilarity
from atarashi.agents.keywordAgent import KeywordAgent

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"
__version__ = "0.0.11"


def atarashii_runner(inputFile, processedLicense, agent_name,
                     similarity="CosineSim", ngramJsonLoc=None, verbose=None):
  '''
  :param inputFile: Input File for scanning of license
  :param processedLicense: Processed License List (CSV) path (Default path
                           already provided)
  :param agent_name: Specify the agent that you want to use for scanning
  :param similarity: Specify the similarity type to be used for the particular
                     agent
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
  scanner = build_scanner_obj(processedLicense, agent_name, similarity,
                              ngramJsonLoc, verbose)
  return run_scan(scanner, inputFile)


def build_scanner_obj(processedLicense, agent_name, similarity="CosineSim",
                      ngramJsonLoc=None, verbose=None):
  '''
  Build a scanner object with all parameters initialized.
  :param processedLicense: Processed License List (CSV) path
  :param agent_name: Agent to use for scanning
  :param similarity: Similarity type to be used for the particular agent
  :param ngramJsonLoc: N-Gram Json File location
  :param verbose: Verbosity
  :return: Returns the scanner agent object
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
  return scanner


def run_scan(scanner, inputFile):
  '''
  Perform the actual scan on input file.
  :param scanner: Scanner agent object
  :param inputFile: File to be scanned
  :return: Returns the array of JSON with scan results
  '''
  if (os.path.isfile(inputFile)):
    return scanner.scan(inputFile)
  else:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), inputFile)


def main():
  '''
  Calls atarashii_runner for each file in the folder/ repository specified by user
  Prints the Input path and the JSON output from atarashii_runner
  '''
  base_dir = Path(__file__).resolve().parent
  defaultProcessed = str(base_dir / "data" / "licenses" / "processedLicenses.csv")
  defaultJSON = str(base_dir / "data" / "Ngram_keywords.json")

  parser = argparse.ArgumentParser()
  parser.add_argument("inputPath", help="Specify the input file/directory path to scan")
  parser.add_argument("-l", "--processedLicenseList", help="Processed license list CSV")
  parser.add_argument("-a", "--agent_name", required=True,
    choices=['wordFrequencySimilarity', 'DLD', 'tfidf', 'Ngram'],
    help="Agent to run")
  parser.add_argument("-s", "--similarity", default="CosineSim",
    choices=["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"],
    help="Select the Similarity algorithm. First 2 are for TFIDF agent, last three for Ngram agent.")
  parser.add_argument("-j", "--ngram_json", help="Ngram JSON file (for Ngram agent only)")
  parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity")
  parser.add_argument("--skip-keyword", action="store_true",
    help="Skip KeywordAgent precheck before similarity scan")
  parser.add_argument("-V", "--version", action='version', version=f'%(prog)s {__version__}')
  args = parser.parse_args()

  inputPath = args.inputPath
  processedLicense = args.processedLicenseList or defaultProcessed
  ngram_json = args.ngram_json or defaultJSON
  verbose = args.verbose

  # Validate compatibility between agent and similarity
  if args.agent_name == "tfidf" and args.similarity not in ["CosineSim", "ScoreSim"]:
    print("Error: TFIDF agent supports only CosineSim or ScoreSim.", file=sys.stderr)
    return 1
  if args.agent_name == "Ngram" and args.similarity not in ["CosineSim", "DiceSim", "BigramCosineSim"]:
    print("Error: Ngram agent supports only CosineSim, DiceSim or BigramCosineSim.", file=sys.stderr)
    return 1

  scanner_obj = build_scanner_obj(processedLicense, args.agent_name, args.similarity, ngram_json, verbose)
  if scanner_obj == -1:
    return 1

  keyword_scanner = KeywordAgent(verbose=verbose)
  return_code = 0
  files_scanned = 0
  files_skipped = 0

  if os.path.isfile(inputPath):
    keyword_ok = args.skip_keyword or keyword_scanner.scan(inputPath)
    if not keyword_ok:
      files_skipped += 1
      if verbose > 0:
        print(f"File {inputPath} does not appear to contain a license, skipping.")
    else:
      try:
        result = run_scan(scanner_obj, inputPath)
        result = list(result)
      except FileNotFoundError as e:
        result = [f"Error: {e.strerror}: '{e.filename}'"]
        return_code |= 2
      except UnicodeDecodeError as e:
        result = [f"Error: Cannot encode file '{inputPath}' in '{e.encoding}'"]
        return_code |= 2
      output = {"file": os.path.abspath(inputPath), "results": result}
      print(json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4))
    print(f"Skipped {files_skipped}.\n")

  elif os.path.isdir(inputPath):
    print("[")
    printComma = False
    for dirpath, _, filenames in os.walk(inputPath):
      if "__MACOSX" in Path(dirpath).parts:
        continue
      for file in filenames:
        if file.startswith("._") or file == ".DS_Store":
          continue
        fpath = os.path.join(dirpath, file)
        keyword_ok = args.skip_keyword or keyword_scanner.scan(fpath)
        if not keyword_ok:
          files_skipped += 1
          continue
        try:
          result = run_scan(scanner_obj, fpath)
          result = list(result)
        except FileNotFoundError as e:
          result = [f"Error: {e.strerror}: '{e.filename}'"]
          return_code |= 2
        except UnicodeDecodeError as e:
          result = [f"Error: Cannot encode file '{fpath}' in '{e.encoding}'"]
          return_code |= 2
        output = {"file": os.path.abspath(fpath), "results": result}
        if printComma:
          print(",", end="")
        else:
          printComma = True
        files_scanned += 1
        print(json.dumps(output, sort_keys=True, ensure_ascii=False))
    print("]")
    if verbose > 0:
      print(f"\nScanned: {files_scanned}, Skipped: {files_skipped}")
    # print(f"Total files scanned: {files_scanned}\n")
    # print(f"Total files skipped: {files_skipped}.\n")

  else:
    print(f"Error: The path '{inputPath}' is not a valid file or directory.", file=sys.stderr)
    return_code |= 4

  return return_code


if __name__ == '__main__':
  main()
