#!/usr/bin/python

import urllib as ul
import re

path='http://tracer.filesystems.org/traces/macos/2014/'
root=ul.urlopen(path)
content=root.read()
match=re.compile(r'(?<=href=["]).*?(?=["])')
names=re.findall(match, content)

for name in names:
    if name=='../':
        continue
    
    fulpath=path+name
    print fulpath
    ul.urlretrieve(fulpath,"/home/dataset/mac2014/%s"%name)
