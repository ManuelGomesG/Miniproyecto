#Autor Manuel Gomes    Octubre 2017


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

fullpath=sys.argv[1]
rpath=fullpath+"REFERENCE-v3.csv"
with open(rpath, 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in spamreader:
         rname  = ', '.join(row).split(",")[0]
         rclass = ', '.join(row).split(",")[1]

         print" tc: " , tc, "oc: ", oc, "noisy: ", noisyc, "ac: ", ac

         if tc<1000:

             if rclass=="N":
                if normalc<598:
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
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5), returnfig = False, ext='N')
                else:
                    continue
             elif rclass=="O":
                if oc<298:
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
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5), returnfig = False, ext='O')
                else:
                    continue
             elif rclass=="~":
                if noisyc<11:
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
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5), returnfig = False, ext='Y')
                else:
                    continue
             elif rclass=="A":
                if ac<93:
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
                    wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5), returnfig = False, ext='A')
                else:
                    continue





         else:
             quit()



#fig.savefig("/home/manuel/Documents/Minip/"+rname+".png")
#sf.save(rname,ext="png", close=True, verbose=True)

#display(record.__dict__)
