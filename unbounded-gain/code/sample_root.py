#!/usr/bin/env python3
"""Reproduce the parameter search for the example, not the theorem's full height-eight test."""
from math import gcd
from itertools import combinations

p,k = 797161,11
state = 91371
mask = (1 << 64)-1

def random64():
    global state
    state ^= (state << 13) & mask
    state ^= state >> 7
    state ^= (state << 17) & mask
    return state

squares=bytearray(p)
for a in range(1,p): squares[a*a%p]=1
betas={((r-s)*pow(r+s,-1,p))**2 % p for r in range(1,4) for s in range(-3,4) if s and abs(s)!=r and gcd(r,s)==1}
slopes=[(a,b) for a in (1,2) for b in (-2,-1,1,2) if gcd(a,b)==1]
anchors=[(i*p,j*p) for i,j in ((0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4))]

def collinear(P,Q,R):
    return (Q[0]-P[0])*(R[1]-P[1])==(Q[1]-P[1])*(R[0]-P[0])

for trial in range(1,50001):
    x=p+1+random64()%(p-1);y=p+1+random64()%(p-1)
    d=x*y%p
    if not squares[d] or d==k or squares[(k-d)%p]:continue
    if any(not squares[(k-b*d)%p] for b in betas):continue
    Ds=[((a*y-b*x)**2+4*a*b*k)%p for a,b in slopes]
    if any(t==0 or squares[t] for t in Ds):continue
    if any(collinear((x,y),(4*p-x,4*p-y),B) for B in anchors):continue
    if any(collinear(A,B,(x,y)) for A,B in combinations(anchors,2)):continue
    assert (trial,x,y)==(46175,1591070,845785)
    print(f'trial={trial} representative=({x},{y}); second representative is its transpose')
    break
else:
    raise RuntimeError('no candidate')
