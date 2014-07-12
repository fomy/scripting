#!/usr/bin/python

import sys

# "Think Python"

# In my macbook pro with a 2.4GHz i5 processor,
# fast_fibonacci is not faster than fibonacci when n < 40.

def fibonacci(n):
    if n==0 or n==1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)

known = {1:1,0:0}

def fast_fibonacci(n):
    if n in known:
        return known[n]
    return fast_fibonacci(n-1)+fast_fibonacci(n-2)

if sys.argv[2] == 'fast':
    print fast_fibonacci(int(sys.argv[1]))
elif sys.argv[2] == 'slow':
    print fibonacci(int(sys.argv[1]))
else:
    print "exit"
