import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import savefig as sf
import sys
import wfdbi




fullpath=sys.argv[1][:-4]
f=open(fullpath+".hea", "r")
samp=int(f.readline().split(" ")[3])

record = wfdb.rdsamp( fullpath , sampto=samp)
rname=fullpath.split("/")[-1]
print(rname)
fig=wfdbi.plotrec(record, title=rname, timeunits='seconds',figsize = (200,5), ecggrids='all', returnfig = True)
#fig.savefig("/home/manuel/Documents/Minip/"+rname+".png")
#sf.save(rname,ext="png", close=True, verbose=True)

#display(record.__dict__)
