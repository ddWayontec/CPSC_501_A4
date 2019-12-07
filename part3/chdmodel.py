# -*- coding: utf-8 -*-
"""CHDModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WrvmH36rxoCAW-1cOi5On9hn7iHfpiTa
"""

# Commented out IPython magic to ensure Python compatibility.
try:
  # %tensorflow_version only exists in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass

"""Necessary imports"""

import sys
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import io
from __future__ import absolute_import, division, print_function, unicode_literals
import functools
import pandas as pd
from tensorflow_core.python.keras import regularizers

"""Upload heart_train.csv and heart_test.csv"""

from google.colab import files
uploaded = files.upload()

"""Parse training data and fit model"""

print("--Process data--")
train_data = pd.read_csv('heart_train.csv')
test_data = pd.read_csv('heart_test.csv')

train_data['famhist'] = pd.Categorical(train_data['famhist'])
train_data['famhist'] = train_data.famhist.cat.codes

target = train_data.pop('chd')
dataset = tf.data.Dataset.from_tensor_slices((train_data.values, target.values))
train_dataset = dataset.shuffle(len(train_data)).batch(1)

print("--Make model--")
model = tf.keras.Sequential([
  tf.keras.layers.Dense(64, activation='relu'),
  tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.4),
  tf.keras.layers.Dense(32, activation='relu'),
  tf.keras.layers.Dense(16, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(1, activation='sigmoid')
])



model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("--Fit model--")
model.fit(train_dataset, epochs=20, verbose=2)

"""Parse test data and evaluate model"""

test_data['famhist'] = pd.Categorical(test_data['famhist'])
test_data['famhist'] = test_data.famhist.cat.codes

target2 = test_data.pop('chd')

dataset2 = tf.data.Dataset.from_tensor_slices((test_data.values, target2.values))

test_dataset = dataset.shuffle(len(test_data)).batch(1)

print("--Evaluate model--")
model_loss, model_acc = model.evaluate(test_dataset, verbose=2)
print(f"Model Loss:    {model_loss:.2f}")
print(f"Model Accuracy: {model_acc*100:.1f}%")