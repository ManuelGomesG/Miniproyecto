##!/bin/bash

python createcsv.py 

for i in $(ls $1)
do
if echo $i | grep ".mat" >> /dev/null; then
  arg="$1/$i" 
  python divide.py $arg 
  python main.py $arg
fi
done

# Flag for dividing 

