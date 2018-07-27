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

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

import argparse
import os
import json
from tqdm import tqdm

from getLicenses import fetch_licenses
from multiprocessing import Pool as ThreadPool
from license_clustering import cluster_licenses
from utils import unpack_json_tar
import csv


def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])


def load_database(licenseList):
  licenses = fetch_licenses(licenseList)
  if 'processed_text' not in licenses.columns:
    raise ValueError('The license list does not contain processed_text column.')

  uniqueNGrams = []

  cluster_arr = cluster_licenses(licenseList)
  for cluster in cluster_arr:
    license_text = licenses[licenses['shortname'] == cluster[0]].iloc[0]['processed_text']
    ngrams = []
    ngramrange = [2, 5, 6, 7, 8]
    for x in ngramrange:
      ngrams += list(find_ngrams(license_text.split(), x))
    obj = {
      'shortname': cluster,  # add all shortnames
      'ngrams': ngrams
    }
    uniqueNGrams.append(obj)
  return uniqueNGrams, cluster_arr, licenses


def unique_ngrams(uniqueNGram):
  matches = []

  for ngram in uniqueNGram['ngrams']:
    find = ' '.join(ngram)
    ismatch = True
    # check with all license text except for licenses in cluster
    filtered = [x for x in licenses if x[0] not in uniqueNGram['shortname']]
    for lic in filtered:
      if find in lic[1]:
        ismatch = False
        break

    if ismatch:
      matches.append(find)
  # print("Matches", matches)
  return matches


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("processedLicenseList", help="Specify the processed license list file")
  parser.add_argument("-t", "--threads", required=False, default=os.cpu_count(),
                      type=int,
                      help="No of threads to use for download. Default: CPU count")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  licenseList = args.processedLicenseList
  threads = args.threads
  uniqueNGrams, cluster_arr, licenses = load_database(licenseList)
  no_keyword_matched = []
  matched_output = []
  ngram_keywords = []

  cpuCount = os.cpu_count()
  threads = cpuCount * 2 if threads > cpuCount * 2 else threads
  pool = ThreadPool(threads)
  zip_ngrams = zip(list(range(len(cluster_arr))), uniqueNGrams)

  for idx, row in enumerate(tqdm(pool.imap_unordered(unique_ngrams, uniqueNGrams),
                                 desc="Licenses processed", total=len(cluster_arr),
                                 unit="license")):

    matched_output.append([str(uniqueNGrams[idx]['shortname']), len(row)])
    if len(row) == 0:
      no_keyword_matched.append(uniqueNGrams[idx]['shortname'])

    ngram_keywords.append({
      'shortname': uniqueNGrams[idx]['shortname'],
      'ngrams': row
    })

  unpack_json_tar()

  dir = os.path.dirname(os.path.abspath(__file__))
  dir = os.path.abspath(dir + "/../data/")

  with open(dir + '/Ngram_keywords.json', 'w') as myfile:
    myfile.write(json.dumps(ngram_keywords))

  with open(dir + "/NGram_DataFrame.csv", 'w') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerows(matched_output)

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
