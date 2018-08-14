#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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
import code_comment  # https://github.com/amanjain97/code_comment/
import os
import re
import string
import tempfile

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

args = None


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
    fd, outputFile = tempfile.mkstemp()

    fileType = inputFile.split('.')[-1]

    supportedFileExtensions = ['c', 'cpp', 'py', 'go', 'php', 'js', 'java', 'h',
                               'hpp', 'cc', 'css', 'html']

    # Remove BOM UTF-8 at the beginning of file and ignore errors
    file = open(inputFile, mode='r', encoding='utf-8-sig', errors='ignore').read()
    open(inputFile, mode='w', encoding='utf-8').write(file)

    with open(outputFile, 'w') as outFile:
      # if the file extension is supported
      if fileType in supportedFileExtensions:
        for comment in code_comment.extract(inputFile):
          if comment.is_multiline:
            outFile.write('\n'.join(comment._body))
          else:
            outFile.write(''.join(comment._body))
          outFile.write('\n')
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
