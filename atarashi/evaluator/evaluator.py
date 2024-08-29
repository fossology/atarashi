#!/usr/bin/env python3
"""
Copyright 2019 Ayush Bhardwaj (classicayush@gmail.com)

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

__author__ = "Ayush Bhardwaj"
__email__ = "classicayush@gmail.com"

from pkg_resources import resource_filename
import argparse
import zipfile
import shutil
import time
import sys
import os

from tqdm.contrib.concurrent import process_map
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')

from atarashii import build_scanner_obj

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'TestFiles.zip')
with zipfile.ZipFile(CONFIG_PATH, 'r') as zip:
  zip.extractall()


# To generate colored Text
def prGreen(text): tqdm.write("\033[92m {}\033[00m" .format(text))


def prCyan(text): tqdm.write("\033[96m {}\033[00m" .format(text))


filesScanned = 0
match = 0


def processFile(scan_input):
  '''
  processFile function runs the agent command on the bash/terminal and gets the
  result for the given file

  :param filepath: The path of the file to be scanned
  :param similarity: Similarity type of the agent
  :return: Returns 1 if the result found by agent is correct and otherwise returns false
  :rtype: int
  '''
  scanner = scan_input[0]
  filepath = scan_input[1]
  if filepath:
    # Extract Filename from the Path
    base = os.path.basename(filepath)
    filename = os.path.splitext(base)[0]
    # Run Scanner
    try:
      temp = scanner.scan(filepath)
      if temp == -1 or len(temp) == 0:
        temp = [{'shortname': 'NULL'}]
      result = temp[0]['shortname']
      result = result.strip("['']")
      prCyan("\n" + " ====> " + 'On File: ' + filename)
      tqdm.write("The Obtained result by agent is: " + result)
      if filename == result:
        return 1
      return 0
    except Exception:
      return 0


def evaluate(scanner):
  '''
  The Function runs the agent command on the bash/terminal and gets the result.
  The license name is then parsed from the result and matched with the actual
  name. Successful matched % is then returned as accuracy.

  :param scanner: Scanner object prepared to run scans
  :return: Time elapsed in the evaluation & the accuracy
  :rtype: float, int
  '''
  start_time = time.time()
  fileList = []
  for (root, dirs, files) in os.walk("TestFiles", topdown=True):
    for file in files:
      filepath = root + os.sep + file
      fileList.append((scanner, filepath))

  result = process_map(processFile, fileList, max_workers=os.cpu_count())

  # success_count is the count of successfully matched files
  success_count = sum(result)
  accuracy = success_count * 100 / len(result)
  prCyan('Total files scanned = ' + str(len(fileList)))
  prGreen('Successfully matched = ' + str(success_count))
  timeElapsed = time.time() - start_time
  return (timeElapsed, accuracy)


if __name__ == "__main__":
  defaultProcessed = resource_filename("atarashi",
                                       "data/licenses/processedLicenses.csv")
  defaultJSON = resource_filename("atarashi", "data/Ngram_keywords.json")
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--agent_name", required=True,
                      choices=['wordFrequencySimilarity', 'DLD', 'tfidf', 'Ngram', 'SemanticSearch'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("-s", "--similarity", required=False, default="CosineSim",
                      choices=["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the similarity algorithm that you want."
                           " First 2 are for TFIDF and last 3 are for Ngram")
  parser.add_argument("-l", "--processedLicenseList", required=False,
                      help="Specify the location of processed license list file")
  parser.add_argument("-j", "--ngram_json", required=False,
                      help="Specify the location of Ngram JSON (for Ngram agent only)")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="count", default=0)
  args = parser.parse_args()
  agent_name = args.agent_name
  similarity = args.similarity
  verbose = args.verbose
  processedLicense = args.processedLicenseList
  ngram_json = args.ngram_json

  if processedLicense is None:
    processedLicense = defaultProcessed
  if ngram_json is None:
    ngram_json = defaultJSON
  agent_name = args.agent_name
  similarity = args.similarity

  scanner = build_scanner_obj(processedLicense, agent_name, similarity,
                              ngram_json, verbose)
  timeElapsed, accuracy = evaluate(scanner)

  print('\n' + '      ++++++++++++++++++ Result ++++++++++++++++++')
  print('      ' + '+' * 44)
  prGreen("     ---> Total time elapsed: " + str(round(timeElapsed, 2)) + " Seconds  <---")
  prGreen("     ---> Accuracy: " + str(round(accuracy, 2)) + "%                     <---")
  print('      ' + '+' * 44)
  print('      ' + '+' * 44)

  shutil.rmtree('TestFiles')

