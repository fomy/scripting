#!/usr/bin/python

import os
import urllib as ul
import re

path='http://tracer.filesystems.org/traces/macos/2014/'
target='/home/dataset/mac2014/'
root=ul.urlopen(path)
content=root.read()
match=re.compile(r'(?<=href=["]).*?(?=["])')
names=re.findall(match, content)

failed=[]
for name in names:
    if name=='../':
        continue
    targetname=target+name
    if os.path.exists(targetname):
        print "skip %s"%name
        continue

    fulpath=path+name
    print "downloading %s"%fulpath
    try:
        ul.urlretrieve(fulpath,targetname)
    except ul.ContentTooShortError:
        print "failed %s"%name
        failed.append(name)
        continue


print "all these files failed"
print failed 
