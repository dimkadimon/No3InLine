from ortools.sat.python import cp_model
import sys,subprocess,random,tempfile
from pathlib import Path

def solve(src,n,ox,oy,D,cap,tm,seed,addlim=15):
 a=src.read_text().splitlines();m,k=map(int,a[0].split());P=[(x+ox,y+oy) for x,y in (map(int,l.split()) for l in a[1:]) if 0<=x+ox<n and 0<=y+oy<n];k=len(P);inp=f'{n} {k}\n'+''.join(f'{x} {y}\n' for x,y in P)
 with tempfile.TemporaryDirectory() as d:
  v=Path(d)/'model';subprocess.run(['./near',str(D),str(v),str(cap),str(seed)],input=inp,text=True,stdout=subprocess.DEVNULL,check=True)
  with v.open()as f:
   n,k,q=map(int,f.readline().split());old=list(map(int,f.readline().split()));M=cp_model.CpModel();pres=[M.new_bool_var(f'p{i}') for i in range(k+q)];A=[]
   if addlim:M.add(sum(pres[:k])>=k-addlim)
   for i in range(q):
    z,num,*e=map(int,f.readline().split());A.append(z)
    for a,b in zip(e[::2],e[1::2]):M.add_bool_or([~pres[k+i],~pres[a],~pres[b]])
   for l in f:
    sz,*ix=map(int,l.split());M.add(sum(pres[i] for i in ix)<=2)
   for i,vv in enumerate(pres):M.add_hint(vv,i<k)
   M.maximize(sum(pres));sol=cp_model.CpSolver();sol.parameters.num_workers=1;sol.parameters.max_time_in_seconds=tm;sol.parameters.random_seed=seed;status=sol.solve(M)
   if status not in [cp_model.OPTIMAL,cp_model.FEASIBLE]:return k,None
   R=[z for v,z in zip(pres,old+A) if sol.value(v)];return len(R),[(z%n,z//n)for z in R]
if __name__=='__main__':
 import json
 srcs=json.loads(Path('seedindex.json').read_text());random.Random(37).shuffle(srcs);best={};rng=random.Random(37);out=Path('hits');out.mkdir(exist_ok=True)
 for e in srcs:best[e['n']]=max(best.get(e['n'],0),e['points'])
 for e in sorted(srcs,key=lambda e: not e['id'].startswith('sets_')):
  m=e['n'];src=Path('seeds')/(e['id']+'.txt');
  if e['points']<best.get(m,0)-5:continue
  for diff in (0,1,2, -1):
   n=m+diff;k,P=solve(src,n,min(0,diff)//2,min(0,diff)//2,3,135,1.45,rng.randrange(99999999))
   if P and k>best.get(n,0):
    best[n]=k; print('best',n,k,'from',e['id'],flush=True);f=out/f'n{n}_{k}.json';f.write_text(json.dumps({'n':n,'points':P,'source':e['id'],'m':m,'dx':min(0,diff)//2,'dy':min(0,diff)//2}))
