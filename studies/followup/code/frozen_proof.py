"""Exact geometric packing number for frozen, half-turn append-only packing (no solver).
Input: the complete list of individually free points and the original cap. Each
edge has a geometrically forbidden triple in the union of its endpoint orbits and
at most one old point. Ordinary lines on three distinct new orbits supply the
remaining ternary conflicts. Branch on each ternary; solve the graph problems by
branching and splitting disconnected components. No external packages required.
"""
import csv,sys
from functools import lru_cache
from itertools import combinations
from collections import defaultdict
from math import gcd
from pathlib import Path

def read(fname):
 with open(fname)as f:return [tuple(map(int,r))for r in list(csv.reader(f))[1:]]
def axis(a,b):
 d=gcd(a,b);assert d
 if a<0 or a==0 and b<0:d=-d
 return a//d,b//d

def conflict(n,O,F):
 S=set(F);m=n//2;assert len(S)==len(F)and n%2==1 and(m,m)not in S
 rev=lambda p:(2*m-p[0],2*m-p[1]);V=sorted(x for x in S if x<rev(x));assert set(V)|{rev(x)for x in V}==S
 assert len(set(O))==len(O)and set(map(rev,O))==set(O)
 N=[0]*len(V)
 for i,(x,y)in enumerate(V):
  dirs={axis(a-x,b-y)for a,b in O};assert len(dirs)==len(O) # free as reported
  rad=axis(m-x,m-y);assert rad not in dirs
  for j in range(i):
   a,b=V[j]
   if axis(m-a,m-b)==rad or axis(x-a,y-b)in dirs or axis(x-2*m+a,y-2*m+b)in dirs:
    N[i]|=1<<j;N[j]|=1<<i
 return V,N

def ternaries(n,F,V,N):
 idx={q:i for i,v in enumerate(V)for q in(v,(n-1-v[0],n-1-v[1]))};E=set()
 for i,(x,y)in enumerate(F):
  D=defaultdict(list)
  for a,b in F[i+1:]:D[axis(a-x,b-y)].append(idx[a,b])
  for T in D.values():
   for j,k in combinations(T,2):
    w=sorted(set((idx[x,y],j,k)))
    if len(w)==3 and all(not ((N[a]>>b)&1) for a,b in combinations(w,2)):E.add(sum(1<<b for b in w))
 return sorted(E)

def independence(N,E):
 def bits(M):
  while M:
   z=M&-M;yield z.bit_length()-1;M^=z
 @lru_cache(None)
 def rec(M):
  if not M:return 0
  comp=todo=M&-M
  while todo:
   z=todo&-todo;todo^=z;ns=N[z.bit_length()-1]&M&~comp;todo|=ns;comp|=ns
  if comp!=M:return rec(comp)+rec(M^comp)
  i=min(bits(M),key=lambda i:(N[i]&M).bit_count());d=(N[i]&M).bit_count()
  if d<=1:return 1+rec(M&~(N[i]|(1<<i))) # choose a leaf instead of its neighbour
  i=max(bits(M),key=lambda i:(N[i]&M).bit_count())
  return max(rec(M^(1<<i)),1+rec(M&~(N[i]|(1<<i))))
 @lru_cache(None)
 def hyper(M):
  t=next((e for e in E if M&e==e),0)
  if not t:return rec(M)
  return max(hyper(M^(1<<v)) for v in bits(t))
 M=(1<<len(N))-1;v=hyper(M);return rec(M),v,rec.cache_info().currsize,hyper.cache_info().currsize
if __name__=='__main__':
 D=Path(__file__).resolve().parents[1];E=D/'data'
 for n in map(int,sys.argv[1:]or[293,389,4037,10085]):
  O=read(E/f'seed{n}.csv');F=read(E/f'free{n}.csv');V,N=conflict(n,O,F);E3=ternaries(n,F,V,N);ub,v,c,h=independence(N,E3);A=read(E/f'augmented{n}.csv');added=len(A)-len(O)
  assert set(O)<=set(A)and set(A)-set(O)<=set(F);assert added==2*v
  print(f'n={n} orbits={len(V)} edges={sum(M.bit_count()for M in N)//2} irreducible_triples={len(E3)} graph_bound={ub} hypergraph_optimum={v} upper={2*v} achieved={added} graph_states={c} hypergraph_states={h}',flush=True)
