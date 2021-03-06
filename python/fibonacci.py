#!/usr/bin/python

import sys

# "Think Python"

def fibonacci(n):
    if n==0 or n==1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)

known = {1:1,0:0}

def fast_fibonacci(n):
    if n in known:
        return known[n]
    known[n] = fast_fibonacci(n-1)+fast_fibonacci(n-2)
    return known[n]

if sys.argv[2] == 'fast':
    print fast_fibonacci(int(sys.argv[1]))
elif sys.argv[2] == 'slow':
    print fibonacci(int(sys.argv[1]))
else:
    print "exit"
