#!/usr/bin/env python3
"""Independent determinant/direction tests of small rectangular constructions and the coarse-edit count."""
from math import gcd
from itertools import combinations,product
from anchor_ring import rect,ring,prime,base_level,M,MESH,any_n

def check(n,L):
 S=set(L);assert len(S)==len(L);assert S=={(n-1-x,n-1-y)for x,y in L};assert all(0<=x<n and 0<=y<n for x,y in S)
 for x,y in L:
  D=set()
  for a,b in L:
   dx=a-x;dy=b-y
   if not (dx or dy):continue
   h=gcd(dx,dy)
   if dx<0 or dx==0 and dy<0:h=-h
   d=dx//h,dy//h;assert d not in D;D.add(d)
def col(A):return any((b-x)*(v-y)==(c-y)*(u-x)for(x,y),(b,c),(u,v)in combinations(A,3))
for (w,h),Ms in MESH.items():
 for t,A in enumerate(Ms):
  assert len(A)==w+h-2 and not col(A);assert all(0<=x<w and 0<=y<h and (x+y)%2==t for x,y in A)
  for (a,b),(x,y) in combinations(A,2):
   dx=a-x;dy=b-y;g=gcd(dx,dy)
   if dx*dy:assert abs(dx//g)in (1,3)and abs(dy//g)in (1,3)
cases=0
for p in range(5,44):
 if prime(p):
  for n in range(3*p,4*p+1):
   k,P=rect(n,p);check(n,P);assert len(P)>=2*n-2*p-42;cases+=1
for n in range(1,122):
 l,p,k,P=any_n(n);check(n,P)
print(f'PASS: all rectangular masks; {cases} full rectangular constructions at primes 5..43; 121 consecutive inputs of the all-n generator.')
for p in (73,97,193,241,1009):
 O=set(ring(p,base_level(p)));size=6*(p-1);assert len(O)==size
 for i,j in product(range(5),repeat=2):
  pairs=sum((2*i*p-x,2*j*p-y)in O for x,y in O)//2
  expected=0 if (i in (0,4)or j in(0,4))else 3*(p-1)if i==j==2 else p-1 if 2 in(i,j)else (p-1)//2
  assert pairs==expected
pairs=list(combinations((1,2,3),2));ct=rot=0
for a,b,c,d in product(pairs,repeat=4):
 A={(0,y)for y in a}|{(4,y)for y in b}|{(x,0)for x in c}|{(x,4)for x in d};assert len(A)==8 and not col(A);ct+=1;rot+=A=={(4-x,4-y)for x,y in A}
print(f'PASS: 5 complete midpoint-count tables; {ct} labelled maximal boundary lists, {rot} invariant under the half-turn.')
