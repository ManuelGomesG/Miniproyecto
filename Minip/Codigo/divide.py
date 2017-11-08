#Autor: Daniela Socas
#Fecha: Octubre 2017

import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import sys 
import csv
import pywt
import matplotlib
import wfdbi

fullpath=sys.argv[1][:-4]

#fullpath = "training2017/A00001"
record = wfdb.rdsamp(fullpath)

#fig=wfdbi.plotrec(record, title=record.recordname, timeunits='seconds', figsize = (200,5), ecggrids='all', returnfig = True)
# ca,cd = pywt.dwt(record.p_signals, 'haar')
# record_wave = wfdb.Record(recordname=record.recordname, fs=300, nsig=record.nsig, siglen=record.siglen,  p_signals = ca)
# fig=wfdbi.plotrec(record_wave, title="wave1", timeunits='seconds', figsize = (200,5), ecggrids='all', returnfig = True)

#Detecting R peaks for QRS segments
d_signal = record.adc()[:,0]
peak_indices = wfdb.processing.gqrs_detect(x=d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)

#QRS segment  
j = 0 
filewriter = csv.writer(open('training.csv', 'ab'))
filewriter_wave = csv.writer(open('training-wavelet.csv', 'ab'))
filereader = csv.reader(open('REFERENCE.csv', 'ra'))

for row in filereader:
    if row[0] == record.recordname:
        sigsym = row[1]
        break

for i in range(0, len(peak_indices)-1):
    a = peak_indices[i]
    b = peak_indices[i+1]
    c = (b-a)//2
    sf = a - c
    st = a + c
    if sf < 0: 
        sf = 0
    rec = wfdb.rdsamp(fullpath, sampfrom = sf, sampto = st)
    filewriter.writerow([rec.recordname, 'S%d-QRS' %j, rec.p_signals, sigsym, rec.siglen])
    
    ca,cd = pywt.dwt(rec.p_signals, 'haar')
    filewriter_wave.writerow([rec.recordname, 'S%d-QRS' %j, ca, sigsym, rec.siglen])
    
    j = j + 1
    # RR segment
    sf = a
    st = b 
    rec = wfdb.rdsamp(fullpath, sampfrom = sf, sampto = st)
    filewriter.writerow([rec.recordname, 'S%d-RR' %j, rec.p_signals, sigsym, rec.siglen])
    
    ca, cd = pywt.dwt(rec.p_signals, 'haar')
    filewriter_wave.writerow([rec.recordname, 'S%d-QRS' %j, ca, sigsym, rec.siglen])
    
    j = j + 1 
# Last QRS  
rec = wfdb.rdsamp(fullpath, sampfrom = sf)
filewriter.writerow([rec.recordname, 'S%d-QRS' %j, rec.p_signals, sigsym, rec.siglen ])

ca,cd = pywt.dwt(rec.p_signals, 'haar')
filewriter_wave.writerow([rec.recordname, 'S%d-QRS' %j, ca, sigsym, rec.siglen])
