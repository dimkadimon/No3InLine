#!/usr/bin/env python3
"""Check the fixed-frame upper certificate against the WHOLE-BOARD free list.
Use enumerate_free.cpp to independently regenerate the latter (see verify.py).
Geometry and group capacities use exact integers; no solver needed.
"""
from pathlib import Path
import json,sys,itertools,collections
R=Path(__file__).resolve().parents[1]
def require(ok,why):
 if not ok:raise ValueError(why)
def col(a,b,c):return (b[0]-a[0])*(c[1]-a[1])==(b[1]-a[1])*(c[0]-a[0])
def check(p):
 raw=[tuple(map(int,l.split()))for l in (R/f'data/free{p}.txt').read_text().splitlines()];head,*pts=raw;Q=set(pts);require(head==(p,len(pts)) and len(Q)==len(pts),'free list format');h=p//2;used=set();release=0;nums=collections.Counter()
 def frame(a):return all(0<=t<2*p for t in a) and a[0]*(a[1]-h)%p==1 and not all(h<t<=h+p for t in a)
 for rec in json.loads((R/f'data/cover{p}.json').read_text()):
  group=list(map(tuple,rec['sites']));cap=rec['capacity'];s=set(group);require(len(s)==len(group) and len(s)>cap and s<=Q and not s&used,'invalid, repeated, or overlapping sites');used|=s
  if cap==1:
   pairs=list(itertools.combinations(group,2));blocks=list(map(tuple,rec['pair_blockers']));require(len(pairs)==len(blocks),'wrong number of blockers');require(all(frame(b) and b not in (u,v) and col(u,v,b) for (u,v),b in zip(pairs,blocks)),'bad frame blocker')
  elif cap==2:require(all(col(group[0],group[1],q) for q in group[2:]),'group is not collinear')
  else:raise ValueError('unrecognised capacity')
  nums[len(s),cap]+=1;release+=len(s)-cap
 ub=len(Q)-release;print(f'p={p} sites={len(Q)} disjoint_groups={dict(sorted(nums.items()))} forced_omissions={release} upper={ub}');return ub
if __name__=='__main__':check(int(sys.argv[1]) if len(sys.argv)>1 else 8009)
