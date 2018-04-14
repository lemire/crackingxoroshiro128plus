#!/usr/bin/python
# usage : python xoroshift.py " Daniel Lemire  "
from z3 import *
import sys
bit64 = 0xffffffffffffffff

if(len(sys.argv) <2):
    print("please provide a string argument (ASCII)")
    sys.exit(-1)
mystr = sys.argv[1]
if(len(mystr) != 16):
    print("provided string should have 16 characters, found "+str(len(mystr)))
    sys.exit(-1)

# assume little endian!
def convertstringtovalues(mystring):
    assert len(mystring) == 16
    array = [ord(c) for c in mystring]
    x, y = 0, 0
    for i in range(8):
        x = x + (array[i] << (64 - 8 * (7 - i)))
        y = y + (array[i + 8] << (64 - 8 * (7 - i)))
    return x,y


out1, out2 = convertstringtovalues(mystr);
# in case the provided string is bad
backout1, backout2 = convertstringtovalues("Sorry,  I can't.");


def rotl64(x, shift):
    return ((x << shift) | LShR(x, 64 - shift))  & bit64

a, b = BitVec('a', 64), BitVec('b', 64)
axorb = a ^ b
newa, newb = (rotl64(a,55) ^ axorb ^ (axorb << 14)) & bit64, rotl64(axorb,36)
s = Solver()
s.add((a + b)  & bit64 == out1, (newa + newb) & bit64 == out2)
try:
  s.check()
  m = s.model()
  print("%s %s"%(hex(m[a].as_long()).upper(), hex(m[b].as_long()).upper()))
except:
  backs = Solver()
  backs.add((a + b)  & bit64 == backout1, (newa + newb) & bit64 == backout2)
  backs.check()
  m = backs.model()
  print("      %s    %s   " %(hex(m[a].as_long()).upper(), hex(m[b].as_long()).upper()))
