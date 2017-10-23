import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import savefig as sf
import sys


fullpath=sys.argv[1][:-4]
record = wfdb.rdsamp( fullpath , sampto=700)
rname=fullpath.split("/")[-1]
print(rname)
plt.close(wfdb.plotrec(record, title=rname, timeunits='seconds',figsize = (200,50), ecggrids='all', returnfig = True))
sf.save(rname,ext="pdf", close=True, verbose=True)
plt.close(fig)
#display(record.__dict__)
