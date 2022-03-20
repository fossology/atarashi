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
import re
import string
import tempfile

from nirjas import extract as commentExtract, LanguageMapper

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

args = None

def licenseComment(data):
  match_list = ['source', 'free', 'under','use',  'copyright', 'grant', 'software', 'license','licence', 'agreement', 'distribute', 'redistribution', 'liability', 'rights', 'reserved', 'general', 'public', 'modify', 'modified', 'modification', 'permission','permitted' 'granted', 'distributed', 'notice', 'distribution', 'terms', 'freely', 'licensed', 'merchantibility','redistributed', 'see', 'read', '(c)', 'copying', 'legal', 'licensing', 'spdx']

  MLmapCount, CSLmapCount, SLmapCount = [], [], []
  comment = ""
  tempCount = 0
  if "multi_line_comment" in data:
    for id, item in enumerate(data["multi_line_comment"]):
      count = 0
      if 'spdx-license-identifier' in item['comment'].lower():
        return item['comment']

      for i in match_list:
        if i in item['comment'].lower():
          count+=1

      if count > tempCount:
        tempCount = count
        comment = item['comment']

  if "cont_single_line_comment" in data:
    for id, item in enumerate(data["cont_single_line_comment"]):
      count = 0
      if 'spdx-license-identifier' in item['comment'].lower():
        return item['comment']

      for i in match_list:
        if i in item['comment'].lower():
          count+=1

      if count > tempCount:
        tempCount = count
        comment = item['comment']

  if "single_line_comment" in data:
    for id, item in enumerate(data["single_line_comment"]):
      count = 0
      if 'spdx-license-identifier' in item['comment'].lower():
        return item['comment']

      for i in match_list:
        if i in item['comment'].lower():
          count+=1

      if count > tempCount:
        tempCount = count
        comment = item['comment']

  return comment


class CommentPreprocessor(object):

  @staticmethod
  def preprocess(data):
    '''
    - All whitespace should be treated as a single blank space
    - All upper case and lower case letters should be treated as lower case letters "(c)", or "Copyright" should be
      considered equivalent and interchangeable
    - Any hyphen, dash, en dash, em dash, or other variation should be considered equivalent.
    - Remove the exceptional characters

    :param data: Input file in string format
    :return: Pre-process the data according to the rules mentioned above
    '''
    data = data.lower()
    data = re.sub(r'copyright|\(c\)|\u00a9', 'copyright', data)
    data = re.sub(r'[{}]'.format(string.punctuation), ' ', data)
    data = re.sub(
        r'[\u2013\u2014\u2015\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u2026\u2032\u2033]',
        '', data)
    data = re.sub(r'\s{2,}', ' ', data)
    return data.strip()

  @staticmethod
  def extract(inputFile):
    '''
    Extract comments from given input file and return a temp file stored in OS.
    This reads all comments from the different files types.

    :param inputFile: Location of Input file from which comments needs to be extracted
    :return: Temp file path from the OS
    '''

    supportedFileExtensions = list(LanguageMapper.LANG_MAP.keys())

    fd, outputFile = tempfile.mkstemp()
    fileType = os.path.splitext(inputFile)[1]

    with open(outputFile, 'w') as outFile:
      # if the file extension is supported
      if fileType in supportedFileExtensions:
        data_file = commentExtract(inputFile)
        data = licenseComment(data_file)
        outFile.write(data)
      else:
        # if file extension is not supported
        with open(inputFile) as inFile:
          lines = inFile.read().split('\n')
          for line in lines:
            outFile.write(line + '\n')

    os.close(fd)
    return outputFile


if __name__ == "__main__":
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--process", required=True,
                      choices=['preprocess', 'extract'],
                      help="Which process you want to run")
  parser.add_argument("inputFile", help="Specify the input file which needs to be processed")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="count", default=0)
  args = parser.parse_args()
  process = args.process
  inputFile = args.inputFile
  verbose = args.verbose

  if process == "extract":
    tempLoc = str(CommentPreprocessor.extract(inputFile))
    print("Temporary output file path: ", tempLoc)
    if verbose > 0:
      print(open(tempLoc, 'r').read())
  else:
    with open(inputFile) as file:
      data = file.read().replace('\n', ' ')
      print("Preprocessed data is: ", str(CommentPreprocessor.preprocess(data)))
