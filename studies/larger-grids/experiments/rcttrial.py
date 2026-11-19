import sys,subprocess,random,tempfile,collections,os
from pathlib import Path
from pysat.formula import CNF
from pysat.solvers import Solver
A='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,.'
S=[s for s in Path('high.dat').read_text().splitlines() if s[0] in ('o','c')];rng=random.Random(753701);out=Path('rctout');out.mkdir(exist_ok=True)
def es(w,n,rand):
 m=len(w)//2;rr=range(1,m//2+1);tt=range(1,n//2+1);e=list(rr);a=list(tt);d=len(e)-len(a)
 if d>0:
  drop=rng.sample(e,d) if rand else e[-d:];e=[i for i in e if i not in drop]
 elif d<0:
  drop=rng.sample(a,-d) if rand else a[d:];a=[i for i in a if i not in drop]
 rank=dict(zip(e,a));res=set()
 for j,t in enumerate(w[1:]):
  x,y=A.index(t),j//2;x=(abs(2*x-m+1)+1)//2;y=(abs(2*y-m+1)+1)//2
  if x in rank and y in rank and x!=y:res.add(tuple(sorted((rank[x],rank[y]))))
 return res
stats=collections.Counter()
for it in range(65):
 n=73 if it==0 else [75,77,79][(it-1)%3];near=[s for s in S if abs(len(s)//2-n)<=5];
 if not it:near=[s for s in S if len(s)//2==n and s[0]=='c'];words=near[:1]
 else:words=rng.sample(near,rng.choice([2,2,3,4,5]));
 E=set();
 for w in words:E|=es(w,n,it and rng.randrange(3)>0)
 if it:
  for _ in range(rng.randrange(0,12)): E.add(tuple(sorted(rng.sample(range(1,n//2+1),2))))
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);tab=d/'v';c=d/'i';
  with c.open('wb') as f:subprocess.run(['./orbit_cnf',str(tab)],input=(str(n)+'\n'+''.join(f'{a} {b}\n'for a,b in sorted(E))).encode(),stdout=f,check=True)
  cn=CNF(from_file=str(c));
  with Solver(name='g4',bootstrap_with=cn) as s:
   s.conf_budget(25000);val=s.solve_limited();stats[n,str(val)]+=1;print('it',it,'n',n,'edges',len(E),'clauses',len(cn.clauses),'SAT',val,flush=True)
   if val:
    yes=set(z for z in s.get_model() if z>0);pts=sorted((a%n,a//n) for l in tab.read_text().splitlines() for j,*v in [list(map(int,l.split()))] if j in yes for a in v);assert len(pts)==2*n
    (out/f'{n}-{it}.txt').write_text(f'{n} {len(pts)}\n'+''.join(f'{x} {y}\n' for x,y in pts));
   elif not it:raise ValueError('failed planted order 73')
print(stats)
