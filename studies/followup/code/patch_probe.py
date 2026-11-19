"""Symmetry optional exact finite neighbourhood reconstruction. Axes and all primitive repeated-fibre directions up to height 4; off-carrier anchors protected by reflection for p=1 mod840."""
from extend_probe import D,sq
from itertools import product
from ortools.sat.python import cp_model
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
import sys
A=((0,1),(0,3),(4,1),(4,3),(1,0),(3,0),(1,4),(3,4))

def patch(p,k,d,U,ax=0,ay=0,sym=False,sec=.5,anchors=True,relax=False):
 R=sq(p);n=4*p+1+d;lx=-ax;ly=-ay;hx=lx+n-1;hy=ly+n-1
 def old(x,y):return 0<x<4*p and 0<y<4*p and not(p<x<3*p and p<y<3*p) and (x+y)%2==int(x%p not in R)
 P=[]
 for u in U:
  X=lx+(u-lx)%p;Y=ly+(k*pow(u,-1,p)-ly)%p
  P.extend(product(range(X,hx+1,p),range(Y,hy+1,p)))
 M=cp_model.CpModel();B={q:M.new_bool_var('')for q in P};line=defaultdict(list)
 if relax:dirs=[(0,1),(1,0),(1,1),(1,-1)]
 else:dirs=D
 for x,y in P:
  for a,b in dirs:line[a,b,b*x-a*y].append((x,y))
 for (a,b,m),T in line.items():
  x,y=T[0];out=0
  if a*b and not relax:
   rr=(-(a*y+b*x)*pow(a*b,-1,p))%p
   if (x+a*rr)%p not in U:
    for j in range(-5,6):
     t=rr+j*p;X=x+a*t;Y=y+b*t
     if old(X,Y):out+=1
  if len(T)>2-out:M.add(sum(B[q]for q in T)<=2-out)
 if anchors and not relax:
  assert p%840==1 and d<p//2
  for i,j in A:
   for x,y in P:
    Q=(2*i*p-x,2*j*p-y)
    if Q in B:
     if Q>(x,y):M.add(B[x,y]+B[Q]<=1)
    elif old(*Q):M.add(B[x,y]==0)
 if sym:
  for x,y in P:M.add(B[x,y]==B[lx+hx-x,ly+hy-y]);
 for q in P:M.add_hint(B[q],int(old(*q)))
 orig=sum(old(*q)for q in P);M.maximize(sum(B.values()));s=cp_model.CpSolver();s.parameters.max_time_in_seconds=sec;s.parameters.num_workers=1;s.parameters.random_seed=41;status=s.solve(M)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):S={q for q in P if s.value(B[q])};O={q for q in P if old(*q)};delta=len(S)-orig;return delta,round(s.best_objective_bound)-orig,sorted(S-O),sorted(O-S)
 return 0,round(s.best_objective_bound)-orig,[],[]

def groups(p,k,starts,ratios):return {s*z%p for r in starts for t in ratios for a in (t,1/t)for b in (a,-a)for s in (b.numerator*pow(b.denominator,-1,p)%p,) for z in (r,k*pow(r,-1,p)%p)}
if __name__=='__main__':
 p,k,d=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]);rat=[[F(1)],[F(1),F(2)],[F(1),F(3)],[F(1),F(2),F(3)]]
 for ax in range(d+1):
  for ay in range(d+1):
   roots={abs(i)for a in (ax,ay)for i in range(-a,d+1-a)if i};res=[]
   for j,r in enumerate(rat):
    U=groups(p,k,roots,r);dl,ub,ins,rm=patch(p,k,d,U,ax,ay,False,1,True);res.append((len(U),dl,ub))
   print(p,k,d,ax,ay,res,flush=True)
