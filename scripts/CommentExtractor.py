#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
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

Author: Aman Jain (amanjain5221@gmail.com)
'''

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