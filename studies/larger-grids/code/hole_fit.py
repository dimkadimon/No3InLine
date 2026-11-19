"""Choose compatible hole insertions above a fixed modular frame. Python 3.10+, OR-Tools."""
from pathlib import Path
from math import gcd
from collections import defaultdict
from ortools.sat.python import cp_model
import sys

def read(f):
    rows=[tuple(map(int,l.split())) for l in Path(f).read_text().splitlines() if l.strip()];(p,k),*L=rows;assert len(set(L))==len(L)==k;return p,set(L)
def base(p):
    h=(p-1)//2;roots=[[] for _ in range(p)]
    for a in range(1,p):
        b=(pow(a,-1,p)+h)%p
        roots[a]=[(x,y) for x in (a,a+p) for y in (b,b+p) if not(h<x<=h+p and h<y<=h+p)]
    return roots

def fit(p,F,Cs,seconds=30,seed=3):
    M=cp_model.CpModel();roots=base(p);h=p//2;inv=[0]+[pow(a,-1,p) for a in range(1,p)];sq=[-1]*p
    for a in range(p):sq[a*a%p]=a
    P=sorted(Cs);B=[M.new_bool_var(str(i)) for i in range(len(P))];edges=defaultdict(list);hard=0;trip=0
    # Work per anchor. A seed hit is solved by reducing the line modulo p and then checking its actual lifts.
    for i,(x,y) in enumerate(P):
        L=defaultdict(list)
        for j in range(i+1,len(P)):
            u,v=P[j];dx=u-x;dy=v-y;g=gcd(dx,dy);dx//=g;dy//=g
            if dx<0 or (dx==0 and dy<0):dx=-dx;dy=-dy
            L[dx,dy].append(j)
        for (dx,dy),js in L.items():
            # dy X^2 + (dx*(y-h)-dy*x) X - dx = 0 mod p.
            a=dy%p;b=(dx*(y-h)-dy*x)%p;c=(-dx)%p
            if a:
                d=sq[(b*b-4*a*c)%p]
                rr=() if d<0 else (((-b+d)*inv[(2*a)%p])%p,((-b-d)*inv[(2*a)%p])%p)
            else:rr=((-c*inv[b])%p,) if b else ()
            hit=any((u-x)*dy==(v-y)*dx for z in rr for u,v in roots[z]);
            if hit:M.add_at_most_one([B[i]]+[B[j] for j in js]);hard+=1
            elif len(js)>=2:M.add(B[i]+sum(B[j] for j in js)<=2);trip+=1
    M.maximize(sum(B));
    for i,q in enumerate(P):M.add_hint(B[i],int(q in F))
    solver=cp_model.CpSolver();solver.parameters.num_workers=1;solver.parameters.max_time_in_seconds=seconds;solver.parameters.random_seed=seed
    status=solver.solve(M);assert status in (cp_model.FEASIBLE,cp_model.OPTIMAL),solver.status_name(status);res=[q for i,q in enumerate(P) if solver.value(B[i])];print('p',p,'starting',len(F),'pool',len(P),'line_constraints',hard,trip,'new',len(res),'pool upper',solver.best_objective_bound,solver.status_name(status),flush=True);return res
if __name__=='__main__':
    p,F=read(sys.argv[1]);G={(2*p-x,2*p-1-y) for x,y in F};C=F|G
    for f in sys.argv[3:]:
        pp,li=read(f);assert pp==p;C|=li
    res=fit(p,F,C);Path(sys.argv[2]).write_text(f'{p} {len(res)}\n'+''.join(f'{x} {y}\n' for x,y in sorted(res)))
