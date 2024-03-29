# -*- coding: utf-8 -*-
"""Aditi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OPRdYGTt4iv293jsYIabv-qibaynEZ9K
"""

from google.colab import drive
drive.mount('/gdrive')

"""# **Object Bounding Box Detection**"""

import cv2
import pandas as pd
import numpy as np
import keras 
import os
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense , Conv2D, MaxPooling2D,Flatten,Dropout
from keras.layers import LeakyReLU
from keras.layers.normalization import BatchNormalization

def extract_features(data):
  data['X'] = (data['x1'] + data['x2'])*255/(2*640)
  data['Y'] = (data['y1'] + data['y2'])*255/(2*480)
  data['bw']= (data['x2']-data['x1'])*255/640
  data['bh']= (data['y2']-data['y1'])*255/480
  return data.loc[:,"X":"bh"]

def retrieve_dimensions(data):
    data['bw']= data['bw']*640/255
    data['bh']= data['bh']*480/255
    data['X'] = data['X']*2*640/255
    data['Y'] = data['Y']*2*480/255
    data['x1']= (data['X']-data['bw'])/2
    data['x2']= (data['X']+data['bw'])/2
    data['y1']= (data['Y']-data['bh'])/2
    data['y2']= (data['Y']+data['bh'])/2
    return data

def read_image(data):
  PATH   = os.getcwd()
  image_train = list(data.iloc[:,0])
  image_dir = '/images'
  x =[]
  for image in image_train:
    i = cv2.imread(PATH +'/images/' + image)
    
    x.append(cv2.resize(i, (255,255), interpolation=cv2.INTER_CUBIC))
             
  x = np.array(x)
  return x

def createModel():
  model = Sequential()
  model.add(Conv2D(32, (3, 3), padding='same', activation=None, kernel_initializer='glorot_uniform', bias_initializer='zeros',))
  model.add(BatchNormalization())
  model.add(LeakyReLU(alpha=0.1))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  
  model.add(Conv2D(64, (3, 3), padding='same', activation=None, kernel_initializer='glorot_uniform', bias_initializer='zeros'))
  model.add(BatchNormalization())
  model.add(LeakyReLU(alpha=0.1))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  
  model.add(Conv2D(32, (3, 3), padding='same', activation=None, kernel_initializer='glorot_uniform', bias_initializer='zeros'))
  model.add(BatchNormalization())
  model.add(LeakyReLU(alpha=0.1))
  model.add(MaxPooling2D(pool_size=(2, 2)))   
  model.add(Conv2D(16, (3, 3), padding='same', activation=None, kernel_initializer='glorot_uniform', bias_initializer='zeros'))
  model.add(BatchNormalization())
  model.add(LeakyReLU(alpha=0.1))
  model.add(MaxPooling2D(pool_size=(2, 2)))
 
  model.add(Conv2D(16, (3, 3), padding='same', activation='relu', kernel_initializer='glorot_uniform', bias_initializer='zeros'))
  model.add(Flatten())
  model.add(Dense(512, activation='relu'))
  model.add(Dropout(0.25))
  model.add(Dense(4, activation='linear'))
   
  return model

data = pd.read_csv("./gdrive/My Drive/training.csv")
datat =pd.read_csv("./gdrive/My Drive/test.csv")

x_train = read_image(data)
y_train = extract_features(data)
y_train.head()
x_valid = x_train[5501:6000,:,:,:]
y_valid = y_train.iloc[5501:6000,:]
X_train = x_train[0:5000,:,:,:]
Y_train = y_train.iloc[0:5000,:]
x_test = read_image(datat)
y_valid = y_valid.values
Y_train = Y_train.values



model = createModel()
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
history = model.fit(X_train, Y_train,
          batch_size=30,
          epochs=20,
          verbose=1,
          validation_data=(x_valid, y_valid),shuffle=True)

y_predict = model.predict(x_test)

predictions = pd.DataFrame(y_predict, columns=['X','Y','bw','bh'])

pred = retrieve_dimensions(predictions)

pred2 = pred.iloc[:,4:8]

predictions.head()

image_name = datat.iloc[:,0]
image_name.head()

test = pd.concat([image_name, pred2], axis=1)
test.to_csv('test.csv')