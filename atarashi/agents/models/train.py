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

import pandas as pd
import os
import joblib
from atarashi.libs.commentPreprocessor import CommentPreprocessor
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB



def model_train():

  '''
  This function is a very versatile function which starts from loading the Pandas Dataframe
  and applying the pre-defined preprocessing technique. It also generates a vocabulary of words
  for each license text. Initialisation of all three models followed by the training of each 
  model on the provided training dataset. Finally, it stores the binary file into models 
  folder for quick classification in future.
  
  '''

  current_dir = os.path.dirname(os.path.abspath(__file__))
  data_dir = os.path.abspath(os.path.join(current_dir,os.path.join(os.pardir,os.pardir)))

  licensepath = os.path.join(data_dir, "data/licenses/licenseList.csv")
  binary1 = os.path.join(data_dir, 'data/models/lr_model.pkl')
  binary2 = os.path.join(data_dir, 'data/models/nb_model.pkl')
  binary3 = os.path.join(data_dir, 'data/models/svc_model.pkl')
  binary4 = os.path.join(data_dir, 'data/models/vectorizer.pkl')

  data = pd.read_csv(licensepath)
  data.drop(['parent_shortname', 'report_shortname', 'url', 'notes', 'source', 'risk','fullname'], axis = 1, inplace = True)
  data.dropna(inplace=True)
  data['text'] = data['text'].astype(str)
  data['cleaned'] = data['text'].apply(CommentPreprocessor.preprocess)

  X_train, y_train = data['cleaned'],data['shortname']
  count_vect = CountVectorizer()
  X_train_counts = count_vect.fit_transform(X_train)
  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

  ##Initialisation of Models and creating
  naive_bayes = MultinomialNB()
  l_regress =  LogisticRegression()
  svc_classifier = LinearSVC()

  print("Model training is going on")
  naive_bayes.fit(X_train_tfidf,y_train)
  print("First training completed")
  l_regress.fit(X_train_tfidf,y_train)
  print("Second training completed")
  svc_classifier.fit(X_train_tfidf,y_train)
  print("Third training completed")

  print("All the models have been trained perfectly!!")
  print("Saving the models into data folder....")
  joblib.dump(naive_bayes,binary2)
  joblib.dump(l_regress,binary1)
  joblib.dump(svc_classifier,binary3)
  joblib.dump(count_vect,binary4)
  print("Done")



if __name__ == "__main__":
  model_train()
