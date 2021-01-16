#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

import numpy as np
import pandas as pd


class LicenseLoader(object):

  @staticmethod
  def fetch_licenses(licenseList):  # common
    '''
    :param licenseList: Path to license list (CSV)
    :return: Return the CSV contents as pandas.DataFrame
    '''
    licenseDataFrame = pd.read_csv(licenseList)
    licenseDataFrame = licenseDataFrame.replace(np.nan, '', regex = True)
    return licenseDataFrame
