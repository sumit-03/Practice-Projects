# -*- coding: utf-8 -*-
"""Bunny or Dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VeW7T2cGS7ca6drZkwjyZzv9sYXIz0YM
"""

#Mount my drive- run the code, go to the link, accept.
from google.colab import drive
drive.mount('/content/gdrive')

#Change working directory to make it easier to access the files- (Folder inside of Colab- CNN folder- Images- Train/Test folder- Inside of each there are bunny/dog folders) 
import os
os.chdir("/content/gdrive/My Drive/Colab Notebooks/Simple CNN Image Tutorial")
os.getcwd()

#Check if the images were uploaded
img_folder = 'images'
#1. Get sample file
#2. Read image and display
from IPython.display import Image
Image("Cute-puppy-photos-82.jpg")

# Import libraries
from __future__ import print_function, division

import numpy as np
import random
import os
import glob
import cv2
import datetime
import pandas as pd
import time
import h5py
import csv

from scipy.misc import imresize, imsave

from sklearn.metrics import log_loss, confusion_matrix
from sklearn.utils import shuffle
from sklearn import model_selection
from sklearn.model_selection import train_test_split, KFold
from PIL import Image, ImageChops, ImageOps

import matplotlib.pyplot as plt

from keras import backend as K
from keras.callbacks import EarlyStopping, Callback
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras import optimizers
from keras.models import Sequential, model_from_json
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, Activation, Dropout, Flatten, Dense

#Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

#Step 1- Convolution
#Make 32 feature detectors (filters/kernels) with a size of 3x3
#Choose the input-image's format to be 64x64 with 3 channels
classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation="relu"))

# Step 2 - Pooling - the window is 2x2 pixels
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
#Make 32 feature detectors (filters/kernels) with a size of 3x3
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2))) #the window is 2x2 pixels

# Step 3 - Flattening- transforming the NxN matrix to Nx1 (A.K.A 1 column)
classifier.add(Flatten())

# Step 4 - Full connection - "units" is the dimensionality of the output space - so here we send it to 128 neurons and then all of those go to 1 neuron
classifier.add(Dense(activation="relu", units=128))
classifier.add(Dense(activation="sigmoid", units=1))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# use ImageDataGenerator to preprocess the data
from keras.preprocessing.image import ImageDataGenerator

#Augment the data so we can "create" a larger dataset 
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

#Prepare the training data:
#1st input is the directory where the different folders of images are (folder of bunnies, folder of dogs here)
#2nd input is target_size=  tuple of integers (height, width) - default: `(256, 256)`. The dimensions to which all images found will be resized.
#3rd input is batch= size of the batches of data (default: 32).One of "categorical", "binary", "sparse", "input", or None. Default: "categorical". Determines the type of label arrays that are returned:
#"categorical" will be 2D one-hot encoded labels, "binary" will be 1D binary labels, "sparse" will be 1D integer labels, "input" will be images identical to input images (mainly used to work with autoencoders).
#If None, no labels are returned (the generator will only yield batches of image data, which is useful to use with model.predict_generator(),  model.evaluate_generator(), etc.). Please note that in case of class_mode None, the data still needs to reside in a subdirectory of directory for it to work correctly.
#Note that you can also subset it here with "subset"- to create validation / training 
#batch_size determines the number of samples in each mini batch. Its maximum is the number of all samples, which makes gradient descent accurate, the loss will decrease towards the minimum if the learning rate is small enough, but iterations are slower. Its minimum is 1, resulting in stochastic gradient descent: Fast but the direction of the gradient step is based only on one example, the loss may jump around.
training_data = train_datagen.flow_from_directory('./images/train',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

#Prepare the test data
test_data = test_datagen.flow_from_directory('./images/test',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

#Start the computation
#Generator- a python training data batch generator; endlessly looping over its training data
#steps_per_epoch the number of batch iterations before a training epoch is considered finished. If you have a training set of fixed size you can ignore it but it may be useful if you have a huge data set or if you are generating random data augmentations on the fly, i.e. if your training set has a (generated) infinite size.
#validation_steps similar to steps_per_epoch but on the validation data set instead on the training data. If you have the time to go through your whole validation data set I recommend to skip this parameter.
#To improve the model accuracy you can increase the number of steps_per_epoch to e.g. 8000
#The number of samples processed for each epoch is batch_size * steps_per_epochs (here the batch size is 32, so the samples processed will be 8000 per epoch)

classifier.fit_generator(training_data,
                         steps_per_epoch = (8000 / 32),
                         epochs = 25,
                         validation_data = test_data,
                         validation_steps = 8000/32)

import numpy as np
from keras.preprocessing import image

#Show a new image - an image that you want to test out on the model
from IPython.display import Image
Image("./newimages/bunny3.jpg")

#To make predictions on a the new image
#target_size ‘squishes’ the photos down to appropriate size.
#image.img_to_array converts a PIL (Python Imaging Library) image instance to a Numpy array.
#np.expand_dims(a,axis) expands the shape of an array. Insert a new axis that will appear at the axis position in the expanded array shape. 
#classifier.predict(test_image) returns an array of integers
#predict_classes (docs) outputs A numpy array of class predictions. Which in your model case, the index of neuron of highest activation from your last(softmax) layer. [[0]] means that your model predicted that your test data is class 0. (usually you will be passing multiple image, and the result will look like [[0], [1], [1], [0]])
#e.g You must convert your actual label (e.g. 'cancer', 'not cancer') into binary encoding (0 for 'cancer', 1 for 'not cancer') for binary classification. Then you will interpret your sequence output of [[0]] as having class label 'cancer'

test_image = image.load_img('./newimages/puppy1.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)

#Training_set.class_indices
if result[0][0] == 1:
    prediction = 'puppy'
else:
    prediction = 'bunny'
    
print(result)
print(prediction)

#Saving / uploading the weights for the model

#Model weights are saved to HDF5 format. This is a grid format that is ideal for storing multi-dimensional arrays of numbers.
#The model structure can be described and saved using two different formats: JSON and YAML

#JSON
#Save model to JSON
model_json = classifier.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
#Serialize weights to HDF5
classifier.save_weights("model.h5")
print("Saved model to disk")

# later...

#Load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
#Load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

#Evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


#ORRRRRR

# serialize model to YAML
model_yaml = classifier.to_yaml()
with open("model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
# serialize weights to HDF5
classifier.save_weights("model.h5")
print("Saved model to disk")

# later...

# load YAML and create model
yaml_file = open('model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))