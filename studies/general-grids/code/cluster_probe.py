"""Heuristic lower-bound search on neighbouring reciprocal fibres near the upper edge. Not part of the theorem."""
from rect_probe import DIR,short
from ortools.sat.python import cp_model
from collections import defaultdict,Counter
from itertools import product
import sys

def setup(p,k,d):
 n=4*p-d;chi={a*a%p for a in range(1,p)};S={};H={};tall=Counter();dims={}
 for u in range(1,p):
  x=u;y=k*pow(u,-1,p)%p;w=len(range(x,1+n,p));h=len(range(y,1+n,p));dims[u]=w,h;t=(int(u not in chi)-x-y)%2;H[u]=[(x+i*p,y+j*p)for i,j in product(range(w),range(h))];S[u]=[(x+i*p,y+j*p)for i,j in short[w,h][t]]
  tall.update((a,b,b*X-a*Y)for X,Y in S[u]for a,b in DIR)
 return dims,H,S,tall

def solve(U,H,S,tall,sec):
 P=[];T=set();lines=defaultdict(list);outside=tall.copy();
 for u in U:
  T.update(S[u]);P.extend(H[u]);outside.subtract((a,b,b*x-a*y)for x,y in S[u]for a,b in DIR)
 M=cp_model.CpModel();B=[M.new_bool_var('') for _ in P]
 for i,(x,y)in enumerate(P):
  for a,b in DIR:lines[a,b,b*x-a*y].append(B[i]);
  M.add_hint(B[i],int((x,y)in T))
 for line,bs in lines.items():
  c=2-outside[line];
  if len(bs)>c:M.add(sum(bs)<=c)
 M.maximize(sum(B));s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=sec;st=s.solve(M);v=round(s.objective_value) if st in (cp_model.FEASIBLE,cp_model.OPTIMAL)else len(T);return max(0,v-len(T)),round(s.best_objective_bound)-len(T),s.status_name(st)
if __name__=='__main__':
 p,k,d=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]);dims,H,S,t=setup(p,k,d);roots=[u for u in S if dims[u]!=(4,4)];done=set()
 for u in roots:
  if u in done:continue
  v=k*pow(u,-1,p)%p;R={z%p for z in [u,v,-u,-v]};done.update(R);out=[]
  for f in ([1],[1,2],[1,3],[1,2,3]):
   U={a*b%p for a in R for b in (f+[pow(w,-1,p)for w in f])};out.append((len(U),solve(U,H,S,t,1)))
  print('u',u,'deficient fibres',len(R&set(roots)),'results',out,flush=True)
