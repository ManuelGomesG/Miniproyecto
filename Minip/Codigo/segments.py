import wfdb
import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import savefig as sf
import sys
import wfdbi



wfdbi.gqrs_plot("/home/manuel/Documents/Minip/Dataset/training2017/A00002", tf=9000)
fullpath="/home/manuel/Documents/Minip/Dataset/training2017/A00002"
rname=fullpath.split("/")[-1]
f=open(fullpath+".hea", "r")
samp=int(f.readline().split(" ")[3])
record = wfdb.rdsamp(  fullpath, sampto=samp)

d_signal = record.adc()[:,0]
peak_indices = wfdb.processing.gqrs_detect(d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
min_bpm = 20
max_bpm = 230
min_gap = record.fs*60/min_bpm
max_gap = record.fs*60/max_bpm
peak_indices = wfdb.processing.correct_peaks(d_signal, peak_indices=peak_indices, min_gap=min_gap, max_gap=max_gap, smooth_window=150)
peak_indices = sorted(peak_indices)
for i in range(1,len(peak_indices)-3):
    print("Graficando: " + str(i) + "/"+ str(len(peak_indices)-4))
    j = i - 1
    if i == 1:
        sf = 0
        st = (peak_indices[j+4] + peak_indices[j+5])//2
        print("["+str(sf)+","+str(st)+"]")
        record  = wfdb.rdsamp(  fullpath, sampto=st, sampfrom=sf)
        wfdbi.plotrec(record, title=rname+"-"+str(i), timeunits='seconds',figsize = (20,10), ecggrids='all', returnfig = False)
    elif i == len(peak_indices)-4:
        sf = (peak_indices[j] + peak_indices[j-1])//2
        st = samp
        print("["+str(sf)+","+str(st)+"]")
        record  = wfdb.rdsamp(  fullpath, sampto=st, sampfrom=sf)
        wfdbi.plotrec(record, title=rname+"-"+str(i), timeunits='seconds',figsize = (20,10), ecggrids='all', returnfig = False)

    else:
        sf = (peak_indices[j] + peak_indices[j-1])//2
        st = (peak_indices[j+4] + peak_indices[j+5])//2
        record  = wfdb.rdsamp(  fullpath, sampto=st, sampfrom=sf)
        wfdbi.plotrec(record, title=rname+"-"+str(i), timeunits='seconds',figsize = (20,10), ecggrids='all', returnfig = False)

        print("["+str(sf)+","+str(st)+"]")
