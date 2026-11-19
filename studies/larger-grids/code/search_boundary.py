#!/usr/bin/env python3
"""Find the exact largest translated extension of the supplied 360-set at sides 201 and 202.
The retained 200x200 seed has full bounding box. Positions here are in its original coordinates.
Independent of the exploratory local optimizer; no solver required.
"""
from itertools import combinations
from pathlib import Path
from math import gcd
R=Path(__file__).resolve().parents[1]
S={tuple(map(int,l.split())) for l in (R/'inputs/n200_c_zero_based.txt').read_text().splitlines()[1:]}
assert (min(x for x,y in S),max(x for x,y in S),min(y for x,y in S),max(y for x,y in S))==(0,199,0,199)
Q={(x,y)for x in range(-2,202)for y in range(-2,202)}-S
for (x,y),(a,b) in combinations(S,2):
 dx=a-x;dy=b-y;g=gcd(dx,dy);dx//=g;dy//=g
 for s in (-1,1):
  u=x+s*dx;v=y+s*dy
  while -2<=u<202 and -2<=v<202:Q.discard((u,v));u+=s*dx;v+=s*dy

def col(a,b,c):return (b[0]-a[0])*(c[1]-a[1])==(c[0]-a[0])*(b[1]-a[1])
bad2={frozenset((a,b))for a,b in combinations(Q,2) if any(col(a,b,s) for s in S)}
bad3={frozenset((a,b,c))for a,b,c in combinations(Q,3) if col(a,b,c)}
for n in (201,202):
 best=-1;all_best=set()
 for ox in range(n-199):
  for oy in range(n-199):
   C=sorted((x,y)for x,y in Q if 0<=x+ox<n and 0<=y+oy<n)
   for k in range(len(C),max(0,best)-1,-1):
    ok=False
    for t in combinations(C,k):
     t=frozenset(t)
     if any(e<=t for e in bad2|bad3):continue
     if k>best:all_best.clear();best=k
     all_best.add(tuple(sorted(t)));ok=True
    if ok:break
 print(f'n={n} entire_204_window_free={len(Q)} max_added={best} distinct_optimal_extension_lists_without_translation={len(all_best)} total={len(S)+best}');print('example',min(all_best))
 assert best=={201:2,202:4}[n]
