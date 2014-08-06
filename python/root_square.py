import sys

a = float(sys.argv[1])
x = float(sys.argv[1])
while True:
    print x
    y = (x+a/x)/2
    if abs(y-x)<0.00000001:
        break
    x=y

print x
