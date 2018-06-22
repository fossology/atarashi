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
import string
import re

"""Rules to apply:
All whitespace should be treated as a single blank space
The words in the following columns are considered equivalent and interchangeable. e.g.Analog = analogue 
All upper case and lower case letters should be treated as lower case letters
"(c)", or "Copyright" should be considered equivalent and interchangeable
Any hyphen, dash, en dash, em dash, or other variation should be considered equivalent. 
Ignore the list item for matching purposes (eg. bullets, numbered lists)

"""

replacements = {
  'acknowledgement': 'acknowledgment',
  'analog': 'analogue',
  'analyze': 'analyse',
  'artifact': 'artefact',
  'authorization': 'authorisation',
  'authorized': 'authorised',
  'caliber': 'calibre',
  'canceled': 'cancelled',
  'capitalizations': 'capitalisations',
  'catalog': 'catalogue',
  'categorize': 'categorise',
  'center': 'centre',
  'emphasized': 'emphasised',
  'favor': 'favour',
  'favorite': 'favourite',
  'fulfill': 'fulfil',
  'fulfillment': 'fulfilment',
  'initialize': 'initialise',
  'judgement': 'judgment',
  'labeling': 'labelling',
  'labor': 'labour',
  'license': 'licence',
  'maximize': 'maximise',
  'modeled': 'modelled',
  'modeling': 'modelling',
  'offense': 'offence',
  'optimize': 'optimise',
  'organization': 'organisation',
  'organize': 'organise',
  'practice': 'practise',
  'program': 'programme',
  'realize': 'realise',
  'recognize': 'recognise',
  'signaling': 'signalling',
  'sublicense': 'sub-license',
  'sub-license': 'sub license',
  'utilization': 'utilisation',
  'while': 'whilst',
  'wilfull': 'wilful',
  'noncommercial': 'non-commercial',
  'percent': 'per cent',
  'copyright holder': 'copyright owner'
}

args = None


def replace(match):
  return replacements[match.group(0)]


def preprocess(data):
  data = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, data)
  data = data.lower()
  data = re.sub(r'\s\s*', ' ', data)
  data = re.sub(r'copyright|\(c\)', 'copyright', data)
  data = re.sub(r'[{}]'.format(string.punctuation), '.', data)
  # data = re.sub(r'[\u2022,\u2023,\u25E6,\u2043,\u2219]', '', data)
  return data


if __name__ == "__main__":
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  inputFile = args.inputFile
  with open(inputFile) as file:
    data = file.read().replace('\n', ' ')
  print("Preprocessed data is --", str(preprocess(data)))
