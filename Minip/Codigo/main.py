import wfdb
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display
import savefig



record = wfdb.rdsamp('training2017/A00001')
wfdb.plotrec(record, title='Record A00001')
display(record.__dict__)
