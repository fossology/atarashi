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
import json
from tqdm import tqdm
from getLicenses import fetch_licenses


def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])


def load_database(licenseList):
  licenses = fetch_licenses(licenseList)
  uniqueNGrams = []

  # print("N-Gram Range is ", ngramrange)

  for license in licenses:
    obj = {}
    ngrams = []
    # if license[0] == "AAL":
    #   print(len(license[1]))
    ngramrange = [2,3,6,7,8]
    for x in ngramrange:
      ngrams += list(find_ngrams(license[1].split(), x))
    obj['shortname'] = license[0]
    obj['ngrams'] = ngrams
    uniqueNGrams.append(obj)

  return uniqueNGrams, licenses


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  licenseList = args.licenseList
  uniqueNGrams, licenses = load_database(licenseList)
  no_keyword_matched = []
  matched_output = []
  ngram_keywords = []
  iterator = tqdm(range(len(licenses)),
                  desc="Licenses merged",
                  total=len(licenses), unit="license")
  for idx, value in enumerate(iterator):
    # print(idx)
    # join ngrams and check if they exists in any other file
    matches = []
    for ngram in uniqueNGrams[idx]['ngrams']:
      # print("ngram is ", ngram)

      # ngram = ngram['ngrams']
      find = ' '.join(ngram)
      ismatch = True

      filtered = [x for x in licenses if x[0] != licenses[idx][0]]
      for lic in filtered:
        if find in lic[1]:
          ismatch = False
          break

      if ismatch:
        matches.append(find)
    # print(matches)

    if args is not None and args.verbose:
      matched_output.append([licenses[idx][0], len(matches)])
      if len(matches) == 0:
        # print('>>>>>', licenses[idx][0], len(matches))
        no_keyword_matched.append(licenses[idx][0])



    ngram_keywords.append({
      'shortname': licenses[idx][0],
      'ngrams': matches
    })

  with open('database_keywordsNoStemSPDX.json', 'w') as myfile:
    myfile.write(json.dumps(ngram_keywords))

  if args is not None and args.verbose:
    print(matched_output)
    print("licenses with no unique keywords")
    print(no_keyword_matched)

'''
Steps:
1. Get all licenses (processed)
2. Make ngrams of it and store somewhere
3. Now check all the ngrams of each license
4. store the unique ngrams in a file (maybe csv or any file)

'''



