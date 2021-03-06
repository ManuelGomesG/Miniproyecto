#Autor Daniela Socas   Octubre 2017


import sys
import csv
import os

os.remove('training.csv')
os.remove('training-wavelet.csv')

with open('training.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Record', 'Segment', 'Signal', 'Symbol', 'Length'])

with open('training-wavelet.csv', 'wb') as csvfile_wave:
    filewriter_wave = csv.writer(csvfile_wave, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter_wave.writerow(['Record', 'Segment', 'Signal_wavelet', 'Symbol', 'Length'])
