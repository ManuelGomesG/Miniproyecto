import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import sys 

fullpath=sys.argv[1][:-4]
record = wfdb.rdsamp( fullpath)
rname=fullpath.split("/")[-1]

# Detecting R peaks for QRS segments 
d_signal = record.adc()[:,0]
peak_indices = wfdb.processing.gqrs_detect(x=d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
print(rname, ' gqrs detected peak indices:', peak_indices)

# RR segments 
#ecgrecord = wfdb.rdsamp(fullpath, sampfrom=153, sampto = 306)
