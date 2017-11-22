#Manuel Gomes 11-10375 10/11/17

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, RMSprop, adam
from keras.utils import np_utils
from keras.models import load_model

import numpy as np
import matplotlib.pyplot  as plt
import matplotlib
import os
import theano
from PIL import Image
from numpy import *

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

from keras import backend as K
K.set_image_dim_ordering('th')


path1='/home/manuel/muestra'
path2='/home/manuel/muestra2'

listing=os.listdir(path1)
numsamples=size(listing)
print numsamples

imag_rows=8000
imag_cols=200
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


################################################################################
#                               Parametros                                     #
################################################################################


batch_size = 10
nb_classes = 4
nb_epoch   = 10
img_channels=1
nb_filters = 4
nb_pool    = 4
nb_conv    = 4


################################################################################
#                               Entrenamiento                                  #
################################################################################

(X,y) = (train_data[0],train_data[1])

#Dividiemos en training y test

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)

X_train = X_train.reshape(X_train.shape[0],1,imag_rows,imag_cols)
X_test  = X_test.reshape(X_test.shape[0],1,imag_rows,imag_cols)
X_train = X_train.astype('float32')
X_test  = X_test.astype('float32')


################################################################################
#                                Optimizacion                                  #
X_train /= 255
X_test  /= 255
################################################################################


Y_train = np_utils.to_categorical(y_train,nb_classes)
Y_test = np_utils.to_categorical(y_test,nb_classes)


################################################################################
#                               Modelo                                         #
################################################################################


model = Sequential()

model.add(Convolution2D(nb_filters,(nb_conv,nb_conv),padding='valid',input_shape=(1,imag_rows,imag_cols)))
convout1 =Activation('relu')
model.add(convout1)
model.add(Convolution2D(nb_filters,(nb_conv,nb_conv)))
convout2=Activation('relu')
model.add(convout2)
model.add(MaxPooling2D(pool_size=(nb_pool,nb_pool)))
model.add(Dropout(0.25))

model.add(Flatten())
#model.add(Dense(128))
model.add(Activation('relu'))
#model.add(Dropout(0.25))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop',metrics=['accuracy'])
"""

model = Sequential()
model.add(Convolution2D(12, 3,3,border_mode='same',input_shape=(1,imag_rows,imag_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(12, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.5))

model.add(Convolution2D(12, 3, 3))
model.add(Activation('relu'))
#model.add(Convolution2D(64, 3, 3))
#model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.5))

model.add(Flatten())
#model.add(Dense(64))
model.add(Activation('relu'))
#model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=["accuracy"])
model.compile(loss='categorical_crossentropy', optimizer='rmsprop',metrics=["accuracy"])
"""



model.fit(X_train,Y_train,batch_size=batch_size,epochs=nb_epoch,
                verbose=1,validation_data=(X_test,Y_test))

#model.fit(X_train,Y_train,batch_size=batch_size,epochs=nb_epoch,
#                verbose=1,validation_split=0.2)


score = model.evaluate(X_test,Y_test, verbose=0)
print'Test score',score[0]
print'Test accuracy',score[1]

model.save_weights("ecg1.h5")
print("Saved model to disk")
