#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scipy
import string
import re

filename = sys.argv[1]

"""Rules to apply:
All whitespace should be treated as a single blank space
The words in the following columns are considered equivalent and interchangeable. e.g.Analog = analogue 
All upper case and lower case letters should be treated as lower case letters
"(c)", or "Copyright" should be considered equivalent and interchangeable
Any hyphen, dash, en dash, em dash, or other variation should be considered equivalent. 
Ignore the list item for matching purposes (eg. bullets, numbered lists)

"""

replacements = {
  'Acknowledgement':'Acknowledgment',
  'Analog':'Analogue',
  'Analyze':'Analyse',
  'Artifact':'Artefact',
  'Authorization':'Authorisation',
  'Authorized':'Authorised',
  'Caliber':'Calibre',
  'Canceled':'Cancelled',
  'Capitalizations':'Capitalisations',
  'Catalog':'Catalogue',
  'Categorize':'Categorise',
  'Center':'Centre',
  'Emphasized':'Emphasised',
  'Favor':'Favour',
  'Favorite':'Favourite',
  'Fulfill':'Fulfil',
  'Fulfillment':'Fulfilment',
  'Initialize':'Initialise',
  'Judgement':'Judgment',
  'Labeling':'Labelling',
  'Labor':'Labour',
  'License':'Licence',
  'Maximize':'Maximise',
  'Modeled':'Modelled',
  'Modeling':'Modelling',
  'Offense':'Offence',
  'Optimize':'Optimise',
  'Organization':'Organisation',
  'Organize':'Organise',
  'Practice':'Practise',
  'Program':'Programme',
  'Realize':'Realise',
  'Recognize':'Recognise',
  'Signaling':'Signalling',
  'Sublicense':'Sub-license',
  'Sub-license':'Sub license',
  'Utilization':'Utilisation',
  'While':'Whilst',
  'Wilfull':'Wilful',
  'Noncommercial':'Non-commercial',
  'Percent':'Per cent',
  'Copyright holder':'Copyright owner'
}

def replace(match):
  return replacements[match.group(0)]

with open(filename) as file:
  data = file.read().replace('\n', ' ')
  data = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, data)
  data = data.lower()
  data = re.sub(r'\s\s*', ' ', data)
  data = re.sub(r'\u00A9|copyright|\(c\)', 'copyright', data)
  data = re.sub(r'[{}]'.format(string.punctuation), '.', data)
  data = re.sub(r'[\u2022,\u2023,\u25E6,\u2043,\u2219]', '', data)

print(data)
