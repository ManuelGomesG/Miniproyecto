import sys 
import csv
import os

os.remove('training.csv')

with open('training.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Record', 'Segment', 'Signal', 'Symbol', 'Length'])