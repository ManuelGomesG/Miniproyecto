import sys 
import csv

with open('training.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Signal_name', 'Segment','Sample','Channel','Num','Symbol'])