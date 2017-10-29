import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import sys 
import csv

fullpath=sys.argv[1][:-4]

#fullpath = "training2017/A00001"
record = wfdb.rdsamp(fullpath)
rname=fullpath.split("/")[-1]

# Detecting R peaks for QRS segments 
d_signal = record.adc()[:,0]
peak_indices = wfdb.processing.gqrs_detect(x=d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
print(rname, ' gqrs detected peak indices:', peak_indices)

# QRS segment  
j = 0 
filewriter = csv.writer(open('training.csv', 'ab'))

for i in range(0, len(peak_indices)-1):
    a = peak_indices[i]
    b = peak_indices[i+1]
    c = (b-a)//2
    sf = a - c
    print('qrssf', sf)
    st = a + c
    print('qrsst', st)
    ann = wfdb.rdann(fullpath, 'qrs', sampfrom = sf, sampto = st)
    filewriter.writerow([rname, 'S%d-QRS' %j, ann.sample[-1], ann.chan[-1], ann.num[-1], ann.symbol[-1]])
    j = j + 1
    # RR segment
    sf = a
    print('rrsf', sf)
    st = b 
    print('rrst', st)
    ann = wfdb.rdann(fullpath, 'qrs', sampfrom = sf, sampto = st)
    filewriter.writerow([rname, 'S%d-RR' %j, ann.sample[-1], ann.chan[-1], ann.num[-1], ann.symbol[-1]])
    j = j + 1 
# Last QRS  
ann = wfdb.rdann(fullpath, 'qrs', sampfrom = sf)
filewriter.writerow([rname, 'S%d-QRS' %j, ann.sample[-1], ann.chan[-1], ann.num[-1], ann.symbol[-1]])


#annotation = wfdb.rdann(fullpath, 'qrs', sampfrom = 549, sampto = 786)
#print('values',  annotation.sample[-1], annotation.symbol[-1], annotation.subtype[-1], annotation.num[-1])
#help(wfdb.Annotation)