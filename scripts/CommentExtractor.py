#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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

__author__ = "Aman Jain"

import argparse
import os
import code_comment  # https://github.com/amanjain97/code_comment/
import tempfile

'''
Input: filePath in arguments
Output: temporary file
Description: This reads all comments from the files types c, cpp, py, go, php, js
              and put in a temporary file in users OS.
              python CommentExtractor.py <filePath>
'''

args = None


def CommentExtract(inputFile):
  # output file
  fd, outputFile = tempfile.mkstemp()

  fileType = inputFile.split('.')[-1]

  supportedFileExtensions = ['c', 'cpp', 'py', 'go', 'php', 'js', 'java', 'h', 'hpp', 'cc']

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


if __name__ == '__main__':
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file from which comments needs to be extracted",
                      required=True)
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  inputFile = args.inputFile
  print("Temporary output file path --", str(CommentExtract(inputFile)))
  if args.verbose:
    print(open(CommentExtract(inputFile), 'r').read())
