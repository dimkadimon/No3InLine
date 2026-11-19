"""Run the new construction, including partial-short as well as chart modes.
Small cases go to the independent ordinary integer line checker. Larger on-carrier cases use the
conic property and test all directions of height <=3 (a triple has a congruent pair).
"""
from chart_caps import best,prime
from math import gcd
from collections import Counter
from itertools import product
import sys
for p in range(5,72):
 if prime(p):
  for n in range(3*p,4*p+1):
   P,I=best(p,n,False);print(n,len(P));print('\n'.join(f'{x} {y}'for x,y in P))
for p in (73,97,101,107,127,163,193,251,1009,1601,2003,2027,2053,2521,3001,5003,5009):
 assert prime(p)
 for d in (0,1,2,5,15,18,19,20,p//2,p-2,p):
  n=4*p-d;P,I=best(p,n,False);U=2*n-2*p-(4 if n%2 else 6);assert len(P)>=U-({1:0,5:4}.get(p%12,4 if d>=19 else 6));S=set(P);assert len(P)==len(S);a=(n-1)*pow(2,-1,p)%p;cv={(x-a)*(y-a)%p for x,y in P};assert len(cv)==1 and 0 not in cv;assert all(0<=x<n and 0<=y<n and(n-1-x,n-1-y)in S for x,y in P)
  for x,y in product(range(4),range(-3,4)):
   if gcd(x,y)==1 and(x>0 or y>0):assert max(Counter(y*a-x*b for a,b in P).values())<=2
 print(f'PASS 11 parameter cases at p={p}, including short, long and near-full windows.',file=sys.stderr,flush=True)
