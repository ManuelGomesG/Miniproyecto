#Autor Manuel Gomes    Octubre 2017
#Genera y guarda imagenes con la proporcion dada

#IMPORTANTE: MODIFICAR LA CARPETA DE DONDE SE VA A GUARDAR LAS IMAGENES



#Uso: python main.py <directorio con el REFERENCE-v3.csv y la data>



import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import savefig as sf
import sys
import wfdbi
import csv



tc=0
normalc=0
noisyc=0
ac=0
oc=0

#MODIFICAR LA CARPETA DE SALIDA AQUI
outdir="/home/manuel/muestrag/"

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
                    normalc+= 1
                    tc+= 1
                    record = wfdb.rdsamp(  fullpath+rname, sampto=samp)
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5),picpath=outdir, returnfig = False, ext='N')
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
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5),picpath=outdir, returnfig = False, ext='O')
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
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5),picpath=outdir, returnfig = False, ext='Y')
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
                    print(rname)
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5),picpath=outdir, returnfig = False, ext='A')
                else:
                    continue





         else:
             quit()



#fig.savefig("/home/manuel/Documents/Minip/"+rname+".png")
#sf.save(rname,ext="png", close=True, verbose=True)

#display(record.__dict__)
