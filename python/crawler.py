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
while True:
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
            os.remove(targetname)
            failed.append(name)
            continue
    if len(failed)==0:
        break
    else:
        print "all these files failed"
        print failed 

