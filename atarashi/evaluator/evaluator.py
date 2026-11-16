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
from report import summarize, misclassifications, format_table, \
  confusion_matrix

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'TestFiles.zip')

# Every agent and similarity combination supported by build_scanner_obj()
AGENT_COMBINATIONS = [
  ('wordFrequencySimilarity', None),
  ('DLD', None),
  ('tfidf', 'CosineSim'),
  ('tfidf', 'ScoreSim'),
  ('Ngram', 'CosineSim'),
  ('Ngram', 'DiceSim'),
  ('Ngram', 'BigramCosineSim'),
]


def extract_test_files():
  '''
  Extract the labelled test files into ./TestFiles
  '''
  with zipfile.ZipFile(CONFIG_PATH, 'r') as zip:
    zip.extractall()


# To generate colored Text
def prGreen(text): tqdm.write("\033[92m {}\033[00m" .format(text))


def prCyan(text): tqdm.write("\033[96m {}\033[00m" .format(text))


filesScanned = 0
match = 0


def processFile(scan_input):
  '''
  processFile runs the agent on the given file and records the outcome.

  :param scan_input: Tuple of (scanner object, file path)
  :return: Dict with the file name, expected license, predicted license,
           status ('ok', 'null' or 'error') and error message if any
  :rtype: dict
  '''
  scanner = scan_input[0]
  filepath = scan_input[1]
  base = os.path.basename(filepath)
  filename = os.path.splitext(base)[0]
  record = {
    'file': base,
    'expected': filename,
    'predicted': None,
    'status': 'ok',
    'error': None
  }
  try:
    temp = scanner.scan(filepath)
    if temp == -1 or len(temp) == 0:
      temp = [{'shortname': 'NULL'}]
    result = temp[0]['shortname']
    result = result.strip("['']")
    prCyan("\n" + " ====> " + 'On File: ' + filename)
    tqdm.write("The Obtained result by agent is: " + result)
    record['predicted'] = result
    if result == 'NULL':
      record['status'] = 'null'
  except Exception as e:
    record['status'] = 'error'
    record['error'] = str(e)
    tqdm.write("Error while scanning " + base + ": " + str(e))
  return record


def evaluate(scanner):
  '''
  The Function runs the agent command on the bash/terminal and gets the result.
  The license name is then parsed from the result and matched with the actual
  name. Successful matched % is then returned as accuracy.

  :param scanner: Scanner object prepared to run scans
  :return: Time elapsed in the evaluation, the accuracy and the per-file
           records returned by processFile()
  :rtype: float, float, list
  '''
  start_time = time.time()
  fileList = []
  for (root, dirs, files) in os.walk("TestFiles", topdown=True):
    for file in files:
      filepath = root + os.sep + file
      fileList.append((scanner, filepath))

  records = process_map(processFile, fileList, max_workers=os.cpu_count())

  summary = summarize(records)
  prCyan('Total files scanned = ' + str(summary['total']))
  prGreen('Successfully matched = ' + str(summary['correct']))
  timeElapsed = time.time() - start_time
  return (timeElapsed, summary['accuracy'], records)


def print_result(timeElapsed, accuracy):
  print('\n' + '      ++++++++++++++++++ Result ++++++++++++++++++')
  print('      ' + '+' * 44)
  prGreen("     ---> Total time elapsed: " + str(round(timeElapsed, 2)) + " Seconds  <---")
  prGreen("     ---> Accuracy: " + str(round(accuracy, 2)) + "%                     <---")
  print('      ' + '+' * 44)
  print('      ' + '+' * 44)


def print_details(records):
  '''
  Print the outcome breakdown and the list of misclassified files
  '''
  summary = summarize(records)
  print("\n      Correct: {correct}  Wrong: {wrong}  NULL: {null}  "
        "Errors: {errors}".format(**summary))
  mistakes = misclassifications(records)
  if mistakes:
    print("\n      Misclassified files (expected -> predicted):")
    for expected, predicted in mistakes:
      print("        " + expected + " -> " + predicted)
  for r in records:
    if r['status'] == 'error':
      print("      Error in " + r['file'] + ": " + str(r['error']))


if __name__ == "__main__":
  defaultProcessed = resource_filename("atarashi",
                                       "data/licenses/processedLicenses.csv")
  defaultJSON = resource_filename("atarashi", "data/Ngram_keywords.json")
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--agent_name", required=False,
                      choices=['wordFrequencySimilarity', 'DLD', 'tfidf', 'Ngram'],
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
  parser.add_argument("--all", action="store_true",
                      help="Evaluate every agent and similarity combination"
                           " and print a comparison table")
  parser.add_argument("--confusion-csv", dest="confusion_csv", required=False,
                      help="Save the confusion matrix (expected vs predicted)"
                           " as CSV. With --all, one file per combination"
                           " is written using this path as prefix")
  args = parser.parse_args()
  if not args.all and args.agent_name is None:
    parser.error("one of -a/--agent_name or --all is required")
  agent_name = args.agent_name
  similarity = args.similarity
  verbose = args.verbose
  processedLicense = args.processedLicenseList
  ngram_json = args.ngram_json

  if processedLicense is None:
    processedLicense = defaultProcessed
  if ngram_json is None:
    ngram_json = defaultJSON
  confusion_csv = args.confusion_csv

  extract_test_files()
  try:
    if args.all:
      rows = []
      for agent, sim in AGENT_COMBINATIONS:
        prCyan("\n ====> Evaluating " + agent + (" with " + sim if sim else ""))
        scanner = build_scanner_obj(processedLicense, agent,
                                    sim or "CosineSim", ngram_json, verbose)
        timeElapsed, accuracy, records = evaluate(scanner)
        rows.append(dict(summarize(records), agent=agent, similarity=sim,
                         time=timeElapsed))
        if confusion_csv:
          name = agent + ("_" + sim if sim else "")
          root, ext = os.path.splitext(confusion_csv)
          confusion_matrix(records).to_csv(root + "_" + name + (ext or ".csv"))
      print("\n" + format_table(rows))
    else:
      scanner = build_scanner_obj(processedLicense, agent_name, similarity,
                                  ngram_json, verbose)
      if scanner == -1:
        sys.exit(1)
      timeElapsed, accuracy, records = evaluate(scanner)
      print_result(timeElapsed, accuracy)
      print_details(records)
      if confusion_csv:
        confusion_matrix(records).to_csv(confusion_csv)
        print("\n      Confusion matrix saved to " + confusion_csv)
  finally:
    shutil.rmtree('TestFiles', ignore_errors=True)

