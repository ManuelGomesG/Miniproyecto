#Manuel Gomes 11-10375 10/11/17
#Hace resize, recolor a las imagenes, y luego hace un modelelo y lo entrena para clasificarlas segun la patologia
#IMPORTANTE: MODIFICAR LAS CARPETAS DE ENTRADA: DE LAS IMAGENES ANTES DE PROCESAR Y LUEGO DE PROCESAR

#Para usarlo : python neuroecg,py

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, RMSprop, adam
from keras.utils import np_utils
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras.layers.normalization import BatchNormalization

import numpy as np
import matplotlib.pyplot  as plt
import matplotlib
import os
import theano
from PIL import Image
from numpy import *

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import h5py

#import neuroecg as n

from keras import backend as K
K.set_image_dim_ordering('th')




def train(x,y):
   model = create_model()
   #sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
   model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])

   checkpointer = ModelCheckpoint(filepath="/home/manuel/Documents/Minip/Codigo/Manuel/ecg1S.h5", verbose=1, save_best_only=True)
   model.fit(x,y,batch_size=batch_size,epochs=nb_epoch,
                verbose=1)

def load_trained_model(weights_path):
   model = create_model()
   model.load_weights(weights_path)


def create_model():
    model = Sequential()

    model.add(Convolution2D(nb_filters,(nb_conv,nb_conv),padding='valid',input_shape=(1,imag_rows,imag_cols)))
    convout1 =Activation('relu')
    model.add(convout1)
    model.add(Convolution2D(nb_filters,(nb_conv,nb_conv)))
    convout2=Activation('relu')
    model.add(convout2)
    model.add(MaxPooling2D(pool_size=(nb_pool,nb_pool)))
    model.add(Dropout(0.25))

    #model.add(BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))


    model.add(Flatten())
    #model.add(Dense(128))
    model.add(Activation('relu'))
    #model.add(Dropout(0.25))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    #model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
    return model


imag_rows=1500
imag_cols=750
batch_size = 10
nb_classes = 4
nb_epoch   = 20
img_channels=1
nb_filters = 4
nb_pool    = 4
nb_conv    = 4


path1='/home/manuel/nmuestra'
path2='/home/manuel/nmuestra2'
listing=os.listdir(path1)
numsamples=size(listing)
"""
guh=0
for img in listing:
    guh+=1
    print img,"  " ,guh

    im = Image.open(path1+'/'+img)
    imag = im.resize((imag_rows,imag_cols))
    grey=imag.convert('L')
    imag.save(path2+'/'+img,"png")
    grey.save(path2+'/'+img,"png")
"""


list2=os.listdir(path2)
#print '[%s]' % ', '.join(map(str, list2))

nlist=[]
ylist=[]
olist=[]
alist=[]

for i in list2:
    if "N-" in i:
        nlist.append(i)
    elif "O-" in i:
        olist.append(i)
    elif "A-" in i:
        alist.append(i)
    else:
        ylist.append(i)

#print "ns: ", len(nlist), " os: " ,len(olist), " as: " ,len(alist), " ys: " ,len(ylist)
fullglist=[]
fullglist.extend(nlist)
fullglist.extend(olist)
fullglist.extend(alist)
fullglist.extend(ylist)
#print '[%s]' % ', '.join(map(str, nlist))
print len(fullglist)


im1=array(Image.open(path2+'/'+fullglist[0]))
m,n=im1.shape[0:2]


immatrix = array([array(Image.open(path2+'/'+im2)).flatten() for im2 in fullglist],'f')


label=np.ones((numsamples,),dtype = int)
label[0:len(nlist)]=0                                               #label de las n
label[len(nlist):len(nlist)+len(olist)]=1                           #label de las o
label[len(nlist)+len(olist):len(nlist)+len(olist)+len(alist)]=2     #label de las a
label[len(nlist)+len(olist)+len(alist):]=3                          #label de las noisy (y)


data,Label = shuffle(immatrix,label, random_state=2)
train_data = [data,Label]


(X,Y) = (train_data[0],train_data[1])
X = X.reshape(X.shape[0],1,imag_rows,imag_cols)
print "reshape"
X = X.astype('float32')
X /= 255


model = Sequential()

model.add(Convolution2D(nb_filters,(nb_conv,nb_conv),padding='valid',input_shape=(1,imag_rows,imag_cols)))
convout1 =Activation('relu')
model.add(convout1)
model.add(Convolution2D(nb_filters,(nb_conv,nb_conv)))
convout2=Activation('relu')
model.add(convout2)
model.add(MaxPooling2D(pool_size=(nb_pool,nb_pool)))
model.add(Dropout(0.25))

#model.add(BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))


model.add(Flatten())
#model.add(Dense(128))
model.add(Activation('relu'))
#model.add(Dropout(0.25))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath="/home/manuel/Documents/Minip/Codigo/Manuel/ecg1S.h5", verbose=1, save_best_only=True)
res=model.predict_classes(X)
print("******************************")
print(len(Y))

valx=0
for i in range(0,len(Y)):
    if Y[i]==res[i]:
        valx+=1

print "clasification: ", valx, "/", len(Y), (valx*100)/len(Y), "%"
