#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2022 Sushant Kumar (sushantmishra02102002@gmail.com)
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

__author__ = 'Sushant Kumar'
__email__ = 'sushantmishra02102002@gmail.com'

import argparse

from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.initialmatch import spdx_identifer
from linearsvc import linearsvc


class Linearsvc(AtarashiAgent):

    def __init__(self, licenseList):
        super().__init__(licenseList)

    def predict_shortname(self, processed_comment):
        '''
        :param filePath: extracted and preprocessed comment
        :return: Returns the predicted license's short name
        '''

        processed_comment = [processed_comment]
        classifier = linearsvc(processed_comment)
        predictor = classifier.classify()
        return predictor.predict(processed_comment)

    def scan(self, filePath):
        '''
        Read the content of filename, extract the comments and preprocess them.
        Find the predicted short name for the preprocessed file.
        :param filePath: Path of the file to scan
        :return: Returns the license's short name
        '''

        match = []

        with open(filePath) as file:
            raw_data = file.read()

        spdx_identifers = spdx_identifer(raw_data,
                                         self.licenseList['shortname'])
        if spdx_identifers:
            match.extend(spdx_identifers)
        else:
            processed_comment = super().loadFile(filePath)
            license_name = self.predict_shortname(processed_comment)

            match.append({
                'shortname': str(license_name[0]),
                'sim_score': 1.0,
                'sim_type': 'linearsvc',
                'description': '',
            })
        return match


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('processedLicenseList',
                        help='Specify the processed license list file')
    parser.add_argument('inputFile',
                        help='Specify the input file which needs to be scanned'
                        )

    args = parser.parse_args()

    licenseList = args.processedLicenseList
    filename = args.inputFile

    scanner = Linearsvc(licenseList)
    scanner.scan(filename)
