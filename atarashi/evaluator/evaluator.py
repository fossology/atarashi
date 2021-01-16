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
import subprocess
import zipfile,os
import time
import json
from tqdm import tqdm
import shutil
import sys
import argparse
from multiprocessing import Pool

__author__ = "Ayush Bhardwaj"
__email__ = "classicayush@gmail.com"

with zipfile.ZipFile('TestFiles.zip', 'r') as zip:
  zip.extractall()

# To generate colored Text
def prGreen(text): tqdm.write("\033[92m {}\033[00m" .format(text))


def prCyan(text): tqdm.write("\033[96m {}\033[00m" .format(text))


def getCommand(agent_name, similarity):
  '''
  getCommand function helps us to find the command needed to be run on the bash. The command is obtained from the combination of agent name and the sim type.

  :param agent_name: The scanner agent going to be evaluated
  :param similarity: Similarity type of the agent
  :return: Command obtained using the agent name and the sim type
  :rtype: str
  '''
  if agent_name == "wordFrequencySimilarity":
    command = "atarashi -a wordFrequencySimilarity"
  elif agent_name == "DLD":
    command = "atarashi -a DLD"
  elif agent_name == "lr_classifier":
    command = "atarashi -a lr_classifier"
  elif agent_name == "nb_classifier":
    command = "atarashi -a nb_classifier"
  elif agent_name == "svc_classifier":
    command = "atarashi -a svc_classifier"
  elif agent_name == "tfidf":
    command = "atarashi -a tfidf"
    if similarity == "CosineSim":
      command = "atarashi -a tfidf -s CosineSim"
    elif similarity == "ScoreSim":
      command = "atarashi -a tfidf -s ScoreSim"
    elif similarity == " ":
      command = "atarashi -a tfidf"
    else:
      print("Please choose similarity from {CosineSim,ScoreSim}")
      return -1
  elif agent_name == "Ngram":
    command = "atarashi -a Ngram"
    if similarity == "CosineSim":
      command = "atarashi -a Ngram -s CosineSim"
    elif similarity == "DiceSim":
      command = "atarashi -a Ngram -s DiceSim"
    elif similarity == "BigramCosineSim":
      command = "atarashi -a Ngram -s BigramCosineSim"
    elif similarity == " ":
      command = "atarashi -a Ngram"
    else:
      print("Please choose similarity from {CosineSim,ScoreSim}")
      return -1
  return command

filesScanned = 0
match = 0

def processFile(filepath):
  '''
  processFile function runs the agent command on the bash/terminal and gets the result for the given file

  :param filepath: The path of the file to be scanned
  :param similarity: Similarity type of the agent
  :return: Returns 1 if the result found by agent is correct and otherwise returns false
  :rtype: int
  '''
  if filepath:
    # Extract Filename from the Path
    base = os.path.basename(filepath)
    filename = os.path.splitext(base)[0]
    tqdm.write("\n" + " ====> "+'On File: ' + filename)
    # Run Scanner command from bash
    runCommand = command + " " + filepath
    tqdm.write('Command Running: ' + runCommand + '\n')
    try:
      output = subprocess.check_output(
          runCommand, shell=True, stderr=subprocess.STDOUT)
      output = output.decode("utf-8")
      temp = json.loads(output)
      if len(temp['results']) == 0:
        temp['results'].append({'shortname': 'NULL'})
      result = temp['results'][0]['shortname']
      result = result.strip("['']")
      tqdm.write("The Obtained result by agent is: " + result)
      prCyan('Scanned the file ' + str(filepath) + '\n')
      if filename == result:
        return 1
      else:
        return 0
    except Exception:
      return 0

def evaluate(command):
  '''
  The Function runs the agent command on the bash/terminal and gets the result. The license name is then parsed from the result and matched with the actual name. Successful matched % is then returned as accuracy.

  :param command: The Scanner agent command with agent name and sim
  :type command: str
  :return: Time elapsed in the evaluation & the accuracy
  :rtype: float, int
  '''
  start_time = time.time()
  fileList = []
  for (root, dirs, files) in os.walk("TestFiles", topdown=True):
    for file in files:
      filepath = root + os.sep + file
      fileList.append(filepath)

  with Pool(os.cpu_count()) as p:
    result = list(tqdm(p.imap_unordered(processFile, fileList), total=len(fileList), unit="files"))

  # success_count is the count of successfully matched files
  success_count = sum(result)
  accuracy = success_count * 100 / len(result)
  prCyan('Total files scanned = ' + str(len(fileList)))
  prGreen('Successfully matched = ' + str(success_count))
  timeElapsed = time.time() - start_time
  return (timeElapsed, accuracy)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--agent_name", required=True,
                      choices=['wordFrequencySimilarity', 'DLD',"lr_classifier","svc_classifier","nb_classifier", 'tfidf', 'Ngram'], help="Name of the agent that you want to evaluate")
  parser.add_argument("-s", "--similarity", required=False,
                      default=" ", choices=["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"], help="Specify the similarity algorithm that you want to evaluate"
                      " First 2 are for TFIDF and last 3 are for Ngram")
  args = parser.parse_args()
  agent_name = args.agent_name
  similarity = args.similarity


  command = getCommand(agent_name, similarity)
  timeElapsed, accuracy = evaluate(command)
  print('\n' + '      ++++++++++++++++++ Result ++++++++++++++++++')
  print('      ++++++++++++++++++++++++++++++++++++++++++++')
  prGreen("     ---> Total time elapsed: " + str(round(timeElapsed, 2)) + " Seconds  <---")
  prGreen("     ---> Accuracy: " + str(round(accuracy, 2)) + "%                     <---")
  print('      ++++++++++++++++++++++++++++++++++++++++++++')
  print('      ++++++++++++++++++++++++++++++++++++++++++++')


  zf = zipfile.ZipFile("TestFiles.zip", "w")
  for dirname, subdirs, files in os.walk("TestFiles"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
  zf.close()

  shutil.rmtree('TestFiles')

