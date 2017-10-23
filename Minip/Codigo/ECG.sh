##!/bin/bash

for i in $(ls $1)
do
if echo $i | grep ".mat" >> /dev/null; then
  arg="$1/$i"
  #echo $arg
  python main.py $arg
fi
done
