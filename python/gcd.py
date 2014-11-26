import sys

# calculate the greatest common divisor
def gcd(x,y): 
    if x==0:
        return y
    if y==0:
        return x
    if x < y:
        return gcd(x, y%x)
    return gcd(x%y,y)

def gcd2(x,y):
    if x==0:
        return y
    if y==0:
        return x
    if x < y:
        return gcd(x, y-x)
    return gcd(x-y,y)

# calculate the least common multiply
def lcm(x,y):
    return x*y/gcd(x,y)

print gcd(int(sys.argv[1]), int(sys.argv[2]))
print gcd2(int(sys.argv[1]), int(sys.argv[2]))
print lcm(int(sys.argv[1]), int(sys.argv[2]))
