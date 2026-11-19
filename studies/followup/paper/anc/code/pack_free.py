"""Maximise a half-turn append-only extension of an explicit frozen cap on its legal sites.
All new/old mixed pairs and lines containing new sites are imposed. Solver for discovery only.
"""
from collections import defaultdict
from pathlib import Path
from itertools import combinations
from math import gcd
from ortools.sat.python import cp_model
import csv,sys

def read(path):
 with path.open()as f:return [tuple(map(int,r))for r in list(csv.reader(f))[1:]]
def run(n,seed,free,out):
 O=read(seed);F=read(free);idx={q:i for i,q in enumerate(F)}
 M=cp_model.CpModel();B=[M.new_bool_var('')for q in F];
 for i,(x,y) in enumerate(F):M.add(B[i]==B[idx[n-1-x,n-1-y]])
 for i,(x,y)in enumerate(F):
  old=set();lines=defaultdict(list)
  def direction(a,b):
   g=gcd(a,b);g=-g if a<0 or a==0 and b<0 else g;return a//g,b//g
  for a,b in O:old.add(direction(a-x,b-y))
  for j in range(i+1,len(F)):
   a,b=F[j];d=direction(a-x,b-y)
   if d in old:M.add_bool_or([~B[i],~B[j]])
   else:lines[d].append(j)
  for T in lines.values():
   if len(T)>=2:M.add(B[i]+sum(B[j]for j in T)<=2)
 M.maximize(sum(B));s=cp_model.CpSolver();s.parameters.max_time_in_seconds=120;s.parameters.num_workers=1;st=s.solve(M);assert st in (cp_model.OPTIMAL,cp_model.FEASIBLE);A=[q for q,b in zip(F,B)if s.value(b)];P=sorted(O+A)
 with out.open('w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(P)
 print(f'n={n} base={len(O)} free={len(F)} added={len(A)} total={len(P)} upper_on_additions={s.best_objective_bound:.0f} solver={s.status_name(st)}',flush=True)
if __name__=='__main__':
 D=Path(__file__).resolve().parents[1];n=int(sys.argv[1]);run(n,D/f'data/seed{n}.csv',D/f'data/free{n}.csv',D/f'data/augmented{n}.csv')
