"""Audit the archived literal append-only construction. Does not modify certificates.
For the first two boards the source list covers the entire ordinary board. For the
third the scan and four modular axes do NOT cover the entire board. The C++ frame
verifier independently checks all the additions together. Run verify.py for the full audit.
"""
import sys,json
from pathlib import Path
from math import gcd
D=Path(__file__).resolve().parents[1];L=D/'sources'
def points(path):return [tuple(map(int,r.split()))for r in path.read_text().splitlines()[1:]]
def test(p):
 n=2*p;h=p//2;O={(x,y)for a in range(1,p)for b in[(h+pow(a,-1,p))%p]for x in(a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)};ins=points(L/f'insertions_{p}.txt');S=O|set(ins)
 if p!=32003:Q=set(points(L/f'free{p}.txt'))-S
 else:
  Q={(x,y)for x,y,s in (map(int,r.split())for r in (L/f'scan{p}.dat').read_text().splitlines())if s==0};Q|={(2*p-x,2*p-1-y)for x,y in set(ins)|Q if x};Q|={(0,y)for y in range(h+1,h+p+1,43)};Q|={tuple(map(int,l.split()))for l in(D/'data'/'axis32003.txt').read_text().splitlines()};Q-=S
 def clean(q,S):
  x,y=q;dirs=set()
  for a,b in S:
   u=x-a;v=y-b;t=gcd(u,v);t=t if(u>0 or(u==0 and v>0))else -t;w=(u//t,v//t)
   if w in dirs:return False
   dirs.add(w)
  return True
 v=json.loads((D/'data'/f'append{n}.json').read_text());Q0={q for q in Q if clean(q,S)};assert Q0==set(map(tuple,v['individual_sites']));A=list(map(tuple,v['compatible_additions']));assert set(A)<=Q0
 assert all(clean(q,S|set(A[:i]))for i,q in enumerate(A))
 if p!=32003:assert len(A)==2+sum(x!=0 for x,y in Q0)
 print(f'PASS literal n={n}: {len(Q0)} individually free in {"complete board" if p!=32003 else "tested pool only"}; {len(A)} feasible simultaneously.',flush=True)
if __name__=='__main__':
 for p in map(int,sys.argv[1:]or(8009,16001,32003)):test(p)
