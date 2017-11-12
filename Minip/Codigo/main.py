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

         if tc<430:

             if rclass=="N":
                if normalc<257:
                    normalc+= 1
                    tc+= 1
                else:
                    continue
             elif rclass=="O":
                if oc<128:
                    oc+= 1
                    tc+= 1
                else:
                    continue
             elif rclass=="~":
                if noisyc<5:
                    noisyc+= 1
                    tc+= 1
                else:
                    continue
             elif rclass=="A":
                if ac<40:
                    ac+= 1
                    tc+= 1
                else:
                    continue

             f=open(fullpath+rname+".hea", "r")
             samp=int(f.readline().split(" ")[3])
             record = wfdb.rdsamp(  fullpath+rname, sampto=samp)


             print(rname)
             wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5), returnfig = False)
         else:
             quit()



#fig.savefig("/home/manuel/Documents/Minip/"+rname+".png")
#sf.save(rname,ext="png", close=True, verbose=True)

#display(record.__dict__)
