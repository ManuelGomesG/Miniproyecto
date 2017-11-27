#Autor Manuel Gomes    Noviembre 2017
#Extrae 5 latidos al azar de una senal y la guarda en imagen


#IMPORTANTE: MODIFICAR LA CARPETA DE DONDE SE VA A GUARDAR LAS IMAGENES

#Uso: python randomsegs.py <directorio con el REFERENCE-v3.csv y la data>



import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import sys
import wfdbi
import csv
import random



#MODIFICAR LA CARPETA DE SALIDA AQUI
OUTDIR="/home/manuel/muestrag/"








tc=0
normalc=0
noisyc=0
ac=0
oc=0

fullpath=sys.argv[1]
rpath=fullpath+"REFERENCE-v3.csv"
with open(rpath, 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in spamreader:
         rname  = ', '.join(row).split(",")[0]
         rclass = ', '.join(row).split(",")[1]

         print" tc: " , tc, "oc: ", oc, "noisy: ", noisyc, "ac: ", ac

         if tc<430:

             if rclass=="N":
                if normalc<257:
                    f=open(fullpath+rname+".hea", "r")
                    samp=int(f.readline().split(" ")[3])
                    if samp > 9000:
                        continue
                    elif samp < 9000:
                        print rname,"menor de 9000"


                    record = wfdb.rdsamp(  fullpath+rname, sampto=samp)
                    d_signal = record.adc()[:,0]
                    peak_indices = wfdb.processing.gqrs_detect(d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
                    min_bpm = 20
                    max_bpm = 230
                    min_gap = record.fs*60/min_bpm
                    max_gap = record.fs*60/max_bpm
                    peak_indices = wfdb.processing.correct_peaks(d_signal, peak_indices=peak_indices, min_gap=min_gap, max_gap=max_gap, smooth_window=150)
                    peak_indices = sorted(peak_indices)

                    #genera los 5 beats al azar
                    r=random.randint(2,len(peak_indices)-6)

                    sf = (peak_indices[r] + peak_indices[r-1])//2
                    st = (peak_indices[r+4] + peak_indices[r+5])//2
                    record  = wfdb.rdsamp(  fullpath+rname, sampto=st, sampfrom=sf)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (20,10),picpath=OUTDIR, returnfig = False, ext='N')

                    normalc+= 1
                    tc+= 1
                    print(rname)
                else:
                    continue
             elif rclass=="O":
                if oc<128:
                    f=open(fullpath+rname+".hea", "r")
                    samp=int(f.readline().split(" ")[3])
                    if samp > 9000:
                        continue
                    elif samp < 9000:
                        print rname,"menor de 9000"
                    oc+= 1
                    tc+= 1
                    record = wfdb.rdsamp(  fullpath+rname, sampto=samp)
                    d_signal = record.adc()[:,0]
                    peak_indices = wfdb.processing.gqrs_detect(d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
                    min_bpm = 20
                    max_bpm = 230
                    min_gap = record.fs*60/min_bpm
                    max_gap = record.fs*60/max_bpm
                    peak_indices = wfdb.processing.correct_peaks(d_signal, peak_indices=peak_indices, min_gap=min_gap, max_gap=max_gap, smooth_window=150)
                    peak_indices = sorted(peak_indices)

                    #genera los 5 beats al azar
                    r=random.randint(2,len(peak_indices)-6)

                    sf = (peak_indices[r] + peak_indices[r-1])//2
                    st = (peak_indices[r+4] + peak_indices[r+5])//2
                    record  = wfdb.rdsamp(  fullpath+rname, sampto=st, sampfrom=sf)
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (20,10),picpath=OUTDIR, returnfig = False, ext='O')
                else:
                    continue
             elif rclass=="~":
                if noisyc<5:
                    f=open(fullpath+rname+".hea", "r")
                    samp=int(f.readline().split(" ")[3])
                    if samp > 9000:
                        continue
                    elif samp < 9000:
                        print rname,"menor de 9000"
                    noisyc+= 1
                    tc+= 1
                    record = wfdb.rdsamp(  fullpath+rname, sampto=samp)
                    d_signal = record.adc()[:,0]
                    peak_indices = wfdb.processing.gqrs_detect(d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
                    min_bpm = 20
                    max_bpm = 230
                    min_gap = record.fs*60/min_bpm
                    max_gap = record.fs*60/max_bpm
                    peak_indices = wfdb.processing.correct_peaks(d_signal, peak_indices=peak_indices, min_gap=min_gap, max_gap=max_gap, smooth_window=150)
                    peak_indices = sorted(peak_indices)

                    #genera los 5 beats al azar
                    r=random.randint(2,len(peak_indices)-6)

                    sf = (peak_indices[r] + peak_indices[r-1])//2
                    st = (peak_indices[r+4] + peak_indices[r+5])//2
                    record  = wfdb.rdsamp(  fullpath+rname, sampto=st, sampfrom=sf)
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (20,10),picpath=OUTDIR, returnfig = False, ext='Y')
                else:
                    continue
             elif rclass=="A":
                if ac<40:
                    f=open(fullpath+rname+".hea", "r")
                    samp=int(f.readline().split(" ")[3])
                    if samp > 9000:
                        continue
                    elif samp < 9000:
                        print rname,"menor de 9000"
                    ac+= 1
                    tc+= 1
                    record = wfdb.rdsamp(  fullpath+rname, sampto=samp)
                    d_signal = record.adc()[:,0]
                    peak_indices = wfdb.processing.gqrs_detect(d_signal, fs=record.fs, adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
                    min_bpm = 20
                    max_bpm = 230
                    min_gap = record.fs*60/min_bpm
                    max_gap = record.fs*60/max_bpm
                    peak_indices = wfdb.processing.correct_peaks(d_signal, peak_indices=peak_indices, min_gap=min_gap, max_gap=max_gap, smooth_window=150)
                    peak_indices = sorted(peak_indices)

                    #genera los 5 beats al azar
                    r=random.randint(2,len(peak_indices)-6)

                    sf = (peak_indices[r] + peak_indices[r-1])//2
                    st = (peak_indices[r+4] + peak_indices[r+5])//2
                    record  = wfdb.rdsamp(  fullpath+rname, sampto=st, sampfrom=sf)
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (20,10),picpath=OUTDIR, returnfig = False, ext='A')
                else:
                    continue





         else:
             quit()
