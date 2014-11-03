#!/usr/bin/python

import os
import urllib as ul
import re
import ftplib import FTP

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
    ul.urlretrieve(fulpath,"C:\\trace\\%s"%name)

    ftp=FTP()
    ftp.connect('192.168.0.1','21')
    ftp.login('ftp','ftp')
    ftp.cwd('/srv/ftp/')

    fh=open("C:\\trace\\%s"%name, 'rb')
    ftp.storbinary("STOR %s"%name,fh)
    fh.close()
    os.remove("C:\\trace\\%s"%name)
