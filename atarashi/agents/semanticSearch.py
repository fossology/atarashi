#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2024 Abdelrahman Jamal (abdelrahmanjamal5565@gmail.com)

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
import argparse
import os
import nirjas
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


from atarashi.agents.atarashiAgent import AtarashiAgent, exactMatcher

__author__ = "Abdelrahman Jamal"
__email__ = "abdelrahmanjamal5565@gmail.com"

class SemanticSearchAgent(AtarashiAgent):
    """
    An agent that performs semantic search to identify potential licenses within files.
    """

    def __init__(self, licenseList):
        super().__init__(licenseList)
        
    def extract_comments(self, filePath: str):
        """
        Extracts comments from a file using the 'nirjas' library, falling back to reading the entire file if comment extraction fails.
        """
        if not os.path.exists(filePath):
           raise Exception(f"File path '{filePath}' does not exist")
        try: 
            # * Manually extracting comments using nirjas and not the commentPreprocessor class
            # * Because I prefer to do my own preprocessing and I also need accurate comment reading,
            # * Normal nirjas works by appending comments together.
            nirjas_comments = nirjas.extract(filePath)
            if nirjas_comments.total_lines_of_comments == 0:
                # Go to the except case to read all the file, even if it has no comments
                # ! This is debatable, and I might remove it.
                raise Exception()
            all_comments = []
            # Go through each comment type, and read the comment itself given it's starting and ending lines
            # This is necessary because nirjas by default appends multi-line or continous single-line comments
            # together, and for semantic search purposes, I want to read the comments exactly as they were in the file.
            with open(filePath, "r") as f:
                all_lines = f.readlines()
            for single_line_comment in nirjas_comments['single_line_comment']:
                all_comments.append(single_line_comment['comment'])
            for cont_single_line_comment in nirjas_comments['cont_single_line_comment']:
                start = cont_single_line_comment['start_line'] - 1
                end = cont_single_line_comment['end_line']
                for line_idx in range(start, end):
                    comment = all_lines[line_idx]
                    all_comments.append(comment)
            for multi_line_comment in nirjas_comments['multi_line_comment']:
                start = multi_line_comment['start_line'] - 1
                end = multi_line_comment['end_line']
                for line_idx in range(start, end):
                    line = all_lines[line_idx]
                    all_comments.append(line) 
            comments = "".join(all_comments)
        except:
            with open(filePath, "r") as f:
                comments = f.read()
        return comments

    def scan(self, filePath): 
        '''
        Scans a file for potential licenses using semantic search and fuzzy string matching.
        '''

        # Quick check if an exact match exists, if it does then return that.
        temp = exactMatcher(super().loadFile(filePath), self.licenseList)
        if temp != -1:
            result = []
            for shortname in temp:
                result.append({
                "shortname": str(shortname),
                "sim_score": 1,
                "sim_type": "SemanticSearch-LVD",
                "description": "exact match"
                })
            return result
        
        # Append The Fulll License Name, Short License Name, and SPDX-License-Identifier to the license text
        # Some files only contain 'SPDX-License-Identifier: 0BSD' or 'License: 0BSD' and since this agent attempts
        # To match based on license text matching, those will not be identified. Appending those lines
        # To the license text helps this agent identify those cases more often
        def convert(row):
            row['text'] = f"License Name: {row['fullname']} \n License: {row['shortname']} \n SPDX-License-Identifier: {row['shortname']} \n{row['text']}"
            return row
        
        self.licenseList = self.licenseList.apply(convert, axis=1)

        file_comments = self.extract_comments(filePath)

        # Remove characters not found in license texts
        chars_to_remove = ['—', '…', '•', '§', '«', '»', '„', '・', '−', '*', '>', '<']
        for char_to_remove in chars_to_remove:
            file_comments = file_comments.replace(char_to_remove, '')

        # Separate the comments into single line comments
        file_comments = file_comments.split('\n')

        # Separate each license text line by line and append them to one big list (used for matching)
        # The license_index_map maps each line to the correct license index in the licenseList dataframe
        license_index_map = {}
        all_license_texts = []
        for license_index, license_text in enumerate(self.licenseList['text']):
            for line in license_text.split('\n'):
                all_license_texts.append(line)
                license_index_map[len(all_license_texts) - 1] = license_index
        
        # Perform first level fuzzy matching for all lines in the comments
        results = []
        fuzzy_similarity_matrix = np.zeros((len(file_comments), len(all_license_texts)))
        for index, comment in enumerate(file_comments):
            for i in range(len(all_license_texts)):
                fuzzy_similarity_matrix[index][i] = fuzz.ratio(comment, all_license_texts[i]) 
            max_score_index = np.argmax(fuzzy_similarity_matrix[index]) 
            results.append(
                        (
                            fuzzy_similarity_matrix[index][max_score_index], 
                            comment
                        )
                    ) 

        # Try to append lines that match with a similarity score of more than 40% with one of the lines in 
        # Any of the licenses. The goal is to get a bigger and bigger text chunk that matches to a bigger 
        # text chunk in one of the license texts - The bigger the chunk, the more likely that this match is 
        # correct.
        appended_comments = []
        appended_comment = []
        for result in results:
            if result[0] >= 40:
                if appended_comment == [] and result[1] == '':
                    continue
                appended_comment.append(result[1])
            else:
                appended_comments.append(appended_comment)
                appended_comment = []
        
        if len(appended_comment) > 0 and appended_comment not in appended_comments:
            appended_comments.append(appended_comment)

        # Attempt the final - second level license match with all the bigger text chunks
        # In some licenses, the license header is used instead of the license text
        # In case that a license has a license header, we match all chunks with both and take 
        # the match with the highest similarity score
        results = []
        for appended_comment in appended_comments:
            appended_comment = "\n".join(appended_comment)
            fuzzy_similarity_matrix_2 = np.zeros(len(self.licenseList))
            for i in range(len(self.licenseList)):
                fuzzy_similarity_matrix_2[i] = fuzz.ratio(appended_comment, self.licenseList.loc[i, 'text'])
                if pd.notna(licenseList.loc[i, 'license_header']):
                    license_header_sim_score = fuzz.ratio(appended_comment, self.licenseList.loc[i, 'license_header'].replace('\n\n', '\n'))
                    fuzzy_similarity_matrix_2[i] = license_header_sim_score if license_header_sim_score > fuzzy_similarity_matrix_2[i] else fuzzy_similarity_matrix_2[i]
                if self.verbose > 0:
                    print('Comment: ' + appended_comment + " - License: " + self.licenseList.iloc[i]['shortname'] + " Similarity Score: " + str(fuzzy_similarity_matrix_2[i]))
            top_5_license_text_indices = np.argsort(fuzzy_similarity_matrix_2)[-5:][::-1]
        
            if fuzzy_similarity_matrix_2[top_5_license_text_indices[0]] >= 50:
                results.append({
                "shortname": self.licenseList.loc[top_5_license_text_indices[0], 'shortname'],
                "sim_score": fuzzy_similarity_matrix_2[top_5_license_text_indices[0]],
                "sim_type": "SemanticSearch-LVD",
                "description": ""
                })
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("processedLicenseList", help="Specify the processed license list file")
    parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action='count', default=0)
    args = parser.parse_args()

    inputFile = args.inputFile
    licenseList = args.processedLicenseList
    verbose = args.verbose

    scanner = SemanticSearchAgent(licenseList, verbose=verbose)

    results = scanner.scan(inputFile)
    if len(results) == 0:
        print("Result is nothing")
    for result in results:
        print("License Detected using Semantic Search: " + result[0]['shortname'])


