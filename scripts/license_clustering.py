#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain

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
import time

from CosineSimNgram import wordFrequency, cosine_similarity
from getLicenses import fetch_licenses

args = None
MAX_ALLOWED_DISTANCE = 0.97


def union_and_find(arr):
  arr = map(set, arr)
  unions = []
  for item in arr:
    temp = []
    for s in unions:
      if not s.isdisjoint(item):
        item = s.union(item)
      else:
        temp.append(s)
    temp.append(item)
    unions = temp
  return unions


def refine_cluster(license_cluster):
  cluster = {}
  for key, initial_cluster in license_cluster.items():
    # for every initial_cluster, call cosine sim and union find
    for i in range(len(initial_cluster)):
      if i + 1 < len(initial_cluster):
        for j in range(i + 1, len(initial_cluster)):
          dist = cosine_similarity(wordFrequency(initial_cluster[i][1].split(" ")),
                                   wordFrequency(initial_cluster[j][1].split(" ")))
          if args is not None and args.verbose:
            print(key, initial_cluster[i][0], initial_cluster[j][0], dist)
          if dist > MAX_ALLOWED_DISTANCE:
            if args is not None and args.verbose:
              print("Pushed in cluster", key, initial_cluster[i][0], initial_cluster[j][0], dist)
            if key in cluster:
              cluster[key].append([initial_cluster[i][0], initial_cluster[j][0]])
            else:
              cluster[key] = [[initial_cluster[i][0], initial_cluster[j][0]]]
  result = []
  for key, arr in cluster.items():
    cluster[key] = union_and_find(arr)
    # convert the set to list
    for clustr in cluster[key]:
      result.append(list(clustr))

  return result


def cluster_licenses(licenseList):
  licenses = fetch_licenses(licenseList)
  initial_cluster = {}
  for license in licenses:
    license_initials = license[0].split("-")[0]
    if license_initials not in initial_cluster:
      initial_cluster[license_initials] = [license]
    else:
      initial_cluster[license_initials].append(license)

  result = refine_cluster(initial_cluster)
  flatten_result = []
  for arr in result:
    for x in arr:
      flatten_result.append(x)
  unclustered_licenses = [license[0] for license in licenses if license[0] not in flatten_result]
  for license in unclustered_licenses:
    result.append([license])
  if args is not None and args.verbose:
    print("Result", result)
  return result


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("processedLicenseList", help="Specify the processed license list file")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  licenseList = args.processedLicenseList
  start = time.time()
  cluster = cluster_licenses(licenseList)
  print("Time taken is ", str(time.time() - start))
  print(cluster)
