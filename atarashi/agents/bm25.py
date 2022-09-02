#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2022 Sushant kumar (sushantmishra02102002@gmail.com)

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

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.initialmatch import spdx_identifer

__author__ = "Sushant Kumar"
__email__ = "sushantmishra02102002@gmail.com"


class Bm25(AtarashiAgent):
    def __init__(self, licenseList, b=0.59, k1=1.6):
        super().__init__(licenseList)
        self.vectorizer = TfidfVectorizer(smooth_idf=False)
        self.b = b
        self.k1 = k1

    def fit_transform(self, processedData, corpus):
        '''
        This function performs the OkapiBM25 tranformation of both
        processedData and LicenseList using sklearn's TFidfVectorizer.

        Reference: https://en.wikipedia.org/wiki/Okapi_BM25/

        :param processedData: Preprocessed input file
        :param corpus: List of licenses from licenseList
        '''
        b, k1 = self.b, self.k1

        # transforming text into vector
        self.vectorizer.fit(corpus)
        corpus = super(TfidfVectorizer, self.vectorizer).transform(corpus)

        avdl = corpus.sum(1).mean()
        len_X = corpus.sum(1).A1

        # transforming processeddata into vector for similarity calc.
        processedData = super(
            TfidfVectorizer, self.vectorizer).transform([processedData])

        corpus = corpus.tocsc()[:, processedData.indices]
        self.divisor = corpus + (k1 * (1 - b + b * len_X / avdl))[:, None]

        idf = self.vectorizer._tfidf.idf_[None, processedData.indices]
        self.dividend = corpus.multiply(
            np.broadcast_to(idf-1, corpus.shape)) * (k1 + 1)

    def scores(self):
        return (self.dividend / self.divisor).sum(1).A1

    def scan(self, filePath):
        '''
        Read the content of filename, extract the comments and preprocess them.
        Find the license of the preprocessed file.

        :param filePath: Path of the file to scan
        :return: Returns the license's short name with highest similarity scores
        '''
        processedData = super().loadFile(filePath)

        with open(filePath) as file:
            raw_data = file.read()
        spdx_identifers = spdx_identifer(raw_data,
                                         self.licenseList['shortname'])

        match = []
        if spdx_identifers:
            match.extend(spdx_identifers)
        else:
            corpus = []
            corpus_identifier = []
            for idx in range(len(self.licenseList)):
                tok = self.licenseList.iloc[idx]['processed_text']
                corpus.append(tok)
                tok_identifier = self.licenseList.iloc[idx]['shortname']
                corpus_identifier.append(tok_identifier)

            self.fit_transform(
                processedData, corpus)
            doc_scores = self.scores()
            indices = np.argsort(doc_scores)[::-1][:5]

            for index in indices:
                match.append({
                    "shortname": str(corpus_identifier[index]),
                    "sim_score": doc_scores[index],
                    "sim_type": "bm25",
                    "description": ""
                })

        return match


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inputFile", help="Specify the input file which needs to be scanned")
    parser.add_argument("processedLicenseList",
                        help="Specify the processed license list file which contains licenses")
    args = parser.parse_args()
    filename = args.inputFile
    licenseList = args.processedLicenseList
    verbose = args.verbose

    scanner = Bm25(licenseList)
