#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)

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

import joblib
import os
import argparse
from atarashi.agents.atarashiAgent import AtarashiAgent
from atarashi.libs.initialmatch import spdx_identifer


class Model(AtarashiAgent):
  
  '''
  Class Model Inherits the Atarashi Agent class inorder to follow a linear and similar interface.
  Few Methods of parent class are required in Model class.

  :Inherits: Atarashi Agent
  :Inherited_Method_1(__init__): Parent class constructor to verify the provided licenseList
  :Inherited_Method_2(loadFile): Extracting the license text from the source code and returning a pre-processed comment text.

  :Derived Class: Model
  :Method_1(__init__): Initialising absolute path of the models directory
  :Method_2(similarity_calc): Classifying the license name from the input processed comment.
  :Method_3(model_predict): Returning a list containing respective metadata.
  :Method_4(getSimalgo): Getter method
  :Method_5(setSimAlgo): Setter method for assigning the algorithm to use.
  :Method_6(scan): Acts as a control method which allows to move forward when everything asked for is there.
  
  '''

  lr_classifier = "lr_classifier"
  nb_classifier = "nb_classifier"
  svc_classifier = "svc_classifier"

  def __init__(self, licenseList, modelsLoc):
    super().__init__(licenseList)
    self.models_folder = os.path.abspath(modelsLoc)

  def similarity_calc(self, processed_comment):

    '''
    The function is designed to give the prediction results of the specific model
    asked by the user. Implementation of all three models and their binary files 
    is done here.
    
    :param processed_comment: Pre-processed string derived from the input extracted license.
    :return: A list containing the predicted license name by the specific model.
    :rtype: list() 
    
    '''

    with open(os.path.join(self.models_folder, 'vectorizer.pkl'), 'rb') as f:
      loaded_vect = joblib.load(f)

    if self.getSimAlgo() == self.lr_classifier:
      classifier = joblib.load(os.path.join(self.models_folder, 'lr_model.pkl'))
    elif self.getSimAlgo() == self.nb_classifier:
      classifier = joblib.load(os.path.join(self.models_folder, 'nb_model.pkl'))
    elif self.getSimAlgo() == self.svc_classifier:
      classifier = joblib.load(os.path.join(self.models_folder, 'svc_model.pkl'))

    return classifier.predict((loaded_vect.transform([processed_comment])))


  def model_predict(self, filePath):

    '''
    The function is designed to give output as the most similar predicted files
    provided by the user. Three different model approaches are designed
    which can result into different similarities. The comments from files are
    extracted and then the prediction is done on the basis of pre-trained
    models in data folder.

    :param filePath: Input file path to scan
    :return: Result with license shortname, sim_score, sim_type and description
    :rtype: list(JSON Format)
    '''

    match = []

    with open(filePath) as file:
      raw_data = file.read()

    # Match SPDX identifiers
    spdx_identifiers = spdx_identifer(raw_data, self.licenseList['shortname'])
    match.extend(spdx_identifiers)

    processed_comment = super().loadFile(filePath)
    license_name = self.similarity_calc(processed_comment)

    match.append({
      'shortname': str(license_name[0]),
      'sim_score': 1,
      'sim_type': self.getSimAlgo(),
      'description': "Shortname: is the predicted license by the model"
    })
    return match

  def getSimAlgo(self):
    return self.algo

  def setSimAlgo(self, newAlgo):
    if newAlgo in (Model.lr_classifier, Model.nb_classifier, Model.svc_classifier):
      self.algo = newAlgo

  def scan(self, filePath):
    if self.algo in (Model.lr_classifier, Model.nb_classifier, Model.svc_classifier):
      return self.model_predict(filePath)
    else:
      return -1


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("processedLicenseList", help="Specify the processed license list file")
  parser.add_argument("modelFolder", help="Specify the location of folder with models")
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("-m","--modelname",default="lr_classifier",choices=["lr_classifier","nb_classifier","svc_classifier"], help = "Specify the model name")
  args = parser.parse_args()

  licenseList = args.processedLicenseList
  filename = args.inputFile
  model = args.modelname
  modelFolder = args.modelFolder

  scanner = Model(licenseList, modelFolder)
  scanner.setSimAlgo(model)
  scanner.scan(filename)
