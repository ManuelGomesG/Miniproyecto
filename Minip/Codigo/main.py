import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import savefig



record = wfdb.rdsamp('/home/manuel/Documents/Minip/Dataset/training2017/A00001', sampto=700)
wfdb.plotrec(record, title='Record A00001', timeunits='seconds',figsize = (10,4), ecggrids='all')
display(record.__dict__)
