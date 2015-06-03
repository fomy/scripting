#!/bin/bash


for file in $(find /home/dataset/synthetic  -name "*.trace");do
    #echo $file
    #./convert $file
    python convert.py $file
done
