#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import string
import code_comment # https://github.com/amanjain97/code_comment/
import tempfile

'''
Input: filePath in arguments
Output: temporary file
Description: This reads all comments from the files types c, cpp, py, go, php, js
              and put in a temporary file in users OS.
              python CommentExtractor.py <filePath>
'''

# input
# inputFile = sys.argv[1]
def CommentExtract(inputFile):
  # output file
  fd, outputFile = tempfile.mkstemp()

  fileType = inputFile.split('.')[-1]
  supportedFileExtensions = ['c', 'cpp', 'py', 'go', 'php', 'js']

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

  # print("Output temporary file - " + outputFile)
  os.close(fd)
  return outputFile