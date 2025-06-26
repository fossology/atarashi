#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2025 Rajul-Jha <rajuljha49@gmail.com>

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
import re
import argparse
import os
import pandas as pd

from atarashi.agents.atarashiAgent import AtarashiAgent


class KeywordAgent(AtarashiAgent):
    """
    A scanning agent that quickly identifies potential license files
    by searching for a set of predefined keywords. This agent is
    inspired by the FOSSology nomos scanner.
    """
    _keyword_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'license_keywords.txt')
    _refs_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'licenses', 'license_refs_combined.csv')

    def __init__(self, licenseList=None, verbose=0):
        """
        Initializes the KeywordAgent.

        :param licenseList: This parameter is ignored by this agent,
                            but kept for compatibility with the factory method.
        :param verbose: Verbosity level.
        """
        self.verbose = verbose
        self.keywords = self.load_keywords(self._keyword_file_path)
        self.license_shortnames_and_refs = self.load_license_shortnames_and_refs(self._refs_file_path)
    
    def load_keywords(self, file_path):
        """
        Keywords are based on FOSSology's nomos scanner's STRINGS.in
        https://github.com/fossology/fossology/blob/master/src/nomos/agent/generator/STRINGS.in

        :param: file_path: Path of the license_keywords.txt file
        :return: List of license keyword regex patterns.
        """
        patterns = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    keyword = line.strip()
                    if keyword:
                        patterns.append(re.compile(keyword, re.IGNORECASE))
        except Exception as e:
            if self.verbose > 0:
                print(f"Failed to load keywords from {file_path}: {e}")
        return patterns

    def load_license_shortnames_and_refs(self, file_path):
        """
        Load the license shortnames and refs using LicenseDownloader as regex patterns.

        :return: List of license keyword regex patterns.
        """
        patterns = []
        try:
            df = pd.read_csv(file_path)
            for keyword in df['key'].dropna():
                patterns.append(re.compile(r'\b' + re.escape(str(keyword)) + r'\b', re.IGNORECASE))
        except Exception as e:
            if self.verbose > 0:
                print(f"Failed to load keywords from {file_path}: {e}")
        return patterns

    def loadFile(self, filePath):
        ## DECIDE: To use comment preprocessor or not? Currently not using it for speed.
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            # Fallback for different encodings if needed
            with open(filePath, 'r', encoding='latin-1') as f:
                return f.read()

    def scan(self, filePath):
        """
        Scans a file for keywords.

        :param filePath: Path to the file to be scanned.
        :return: A list of dictionaries with scan results.
        """
        try:
            processed_data = self.loadFile(filePath)
        except Exception as e:
            if self.verbose > 0:
                print(f"Could not process file {filePath}: {e}")
            return []

        if not processed_data.strip():
            return []

        results = []
        # Scan for license keywords
        matched_keywords = []
        for keyword_re in self.keywords:
            if keyword_re.search(processed_data):
                matched_keywords.append(keyword_re.pattern)

        if matched_keywords:
            if self.verbose > 0:
                print(f"Found license-related keywords in {filePath}: {', '.join(matched_keywords)}")
            results.append({
                "shortname": "License-Possibility",
                "sim_score": 1.0,
                "sim_type": "Keyword-Scan",
                "description": f"Matched keywords: {', '.join(matched_keywords)}"
            })

        # # Scan for license shortnames and refs
        # matched_refs = []
        # for license_ref_or_shortname in self.license_shortnames_and_refs:
        #     if license_ref_or_shortname.search(processed_data):
        #         matched_refs.append(license_ref_or_shortname.pattern)

        # if matched_refs:
        #     if self.verbose > 0:
        #         print(f"Found license shortnames in {filePath}: {', '.join(matched_refs)}")
        #     results.append({
        #         "shortname": "License-Identifier",
        #         "sim_score": 1.0,
        #         "sim_type": "Shortname-Scan",
        #         "description": f"Matched shortnames/refs: {', '.join(matched_refs)}"
        #     })

        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan a file or directory for license keywords.")
    parser.add_argument("input_path", help="Path to the file or directory to scan.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity.")
    args = parser.parse_args()

    agent = KeywordAgent(verbose=args.verbose)
    input_path = os.path.expanduser(args.input_path)

    if os.path.isfile(input_path):
        results = agent.scan(input_path)
        if results:
            print(f"Keyword Scan results for {input_path}:")
            for result in results:
                print(result)
    elif os.path.isdir(input_path):
        print(f"Scanning directory: {input_path}")
        for root, _, files in os.walk(input_path):
            for file in files:
                file_path = os.path.join(root, file)
                results = agent.scan(file_path)
                if results:
                    print(f"Scan results for {file_path}:")
                    for result in results:
                        print(result)
    else:
        print(f"Error: Invalid path '{args.input_path}'")
