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
import gensim
import os
import argparse
import code_comment
from gensim.models.doc2vec import Doc2Vec
from atarashi.libs.commentPreprocessor import CommentPreprocessor

__author__ = "Ayush Bhardwaj"
__email__ = "classicayush@gmail.com"

temp = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(temp, 'spdxDoc2Vec.model')

def semanticTextSim(filePath):
  '''
  The function loads the trained model and returns the most similar doc to the input doc.
  It preprocess the files and extract the comments out of it i.e. License statements.
  The doc is converted to vector and most similar doc (highest cosine sim) is returned.

  :param filePath: Input file path to scan
  :return: result with license name, sim score, sim type and description
  :rtype: list (JSON Format)
  '''
  commentFile = CommentPreprocessor.extract(filePath)
  with open(commentFile) as file:
    doc = file.read()
  matches = []

  # Load the trained model
  model = Doc2Vec.load(path)

  # To find the vector of a document 
  data = ((doc).lower()).split()
  vector = model.infer_vector(data)

  # to find most similar docs 
  similar_doc = model.docvecs.most_similar([vector])

  matches.append({
      'shortname': similar_doc[0][0],
      'sim_score': similar_doc[0][1],
      'sim_type': "semanticTextSim",
      'description': ""
      })

  return matches

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")

  args = parser.parse_args()
  filename = args.inputFile

  scanner = semanticTextSim(filename)
