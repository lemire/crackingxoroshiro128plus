#!/usr/bin/python
# usage : python xoroshiftall.py 0 0xdeadbeef
import sys, z3
bit64 = 0xffffffffffffffff

def LShL(x, n): return (x << n) & bit64

def xo128(x, y, LShR = lambda x,i: x>>i):
    y ^= x
    return y ^ LShL(y, 14) ^ (LShL(x,55)|LShR(x,9)), (LShL(y,36)|LShR(y,28))

if sys.argv[1] == 'seed':       # usage xo128.py seed x y
    x = int(sys.argv[2], 0)
    y = int(sys.argv[3], 0)
    for i in range(10):         # generate random numbers
        print hex((x+y)&bit64)
        x, y = xo128(x, y)
    sys.exit()

x0, y0 = z3.BitVecs('x0 y0', 64)
x, y = x0, y0
s = z3.SimpleSolver()

for v in sys.argv[1:]:
    n = int(v, 0)
    s.add((x + y) & bit64 == n)
    x, y = xo128(x, y, z3.LShR)

for i in xrange(1, sys.maxint):
    print '\n#%d = %s' % (i, s.check())
    if s.check().r != 1: break  # quit if failed
    soln = s.model()
    x, y = (soln[i].as_long() for i in (x0,y0))
    print 'state =', hex(x), hex(y)
    for j in range(10):         # show predictions
        print hex((x+y) & bit64)
        x, y = xo128(x, y)
    s.add(x0 != soln[x0], y0 != soln[y0])
