#!/usr/bin/env python3
"""
Copyright 2019 Ayush Bhardwaj (classicayush@gmail.com)

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
import gensim
import os
import glob
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
LabeledSentence = gensim.models.doc2vec.LabeledSentence

__author__ = "Ayush Bhardwaj"
__email__ = "classicayush@gmail.com"

lic_text = []
path = 'text/*.txt'
files = glob.glob(path)

# Open and add documents in list
for name in files:
  with open(name):
    doc = open(name, 'r+').read().splitlines()
    doc = [x.lower() for x in doc]
    lic_text.append(doc)

# Get Name of the files(Actual license Name)
temp = os.listdir('text')
filename = [x.split('.')[0] for x in temp]

# Prepare data for the training
tagged_data = [TaggedDocument(words=(''.join(_d)).split(), tags=[str(i)]) for i, _d in zip(filename, lic_text)]

# Training the Model
''' 
values for epochs vec_size and learning rate alpha can be changed as per requirements.
Better results might be found by changing the learning rates or iterating randomly
Explained at: https://rare-technologies.com/doc2vec-tutorial/ 
'''
max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=1,
                dm=1)

model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("spdxDoc2Vec.model")
print("Model Saved")
