import sys,subprocess,tempfile,json,itertools,random
from pathlib import Path
from ortools.sat.python import cp_model
from math import gcd

def run(src,dmax=8):
 ls=src.read_text().splitlines();m,k=map(int,ls[0].split());P=[tuple(map(int,l.split())) for l in ls[1:]];S=set(P);z=m+2*dmax
 inp=f'{z} {k}\n'+''.join(f'{x+dmax} {y+dmax}\n' for x,y in P)
 with tempfile.TemporaryDirectory() as t:
  f=Path(t)/'q';subprocess.run(['./near','0',f.as_posix()],input=inp,text=True,stdout=subprocess.DEVNULL,check=True)
  with f.open() as h:
   _,_,c=map(int,h.readline().split());h.readline();Q=[(u%z-dmax,u//z-dmax)for u in (int(h.readline().split()[0])for _ in range(c))];cs=[]
   for l in h:
    ids=list(map(int,l.split()))[1:];t=sum(v<k for v in ids);cs.append(([i-k for i in ids if i>=k],2-t))
 out={};xmin=min(x for x,y in P);xmax=max(x for x,y in P);ymin=min(y for x,y in P);ymax=max(y for x,y in P)
 for d in range(1,dmax+1):
  n=m+d;eligible=[i for i,(x,y)in enumerate(Q) if max(xmax-x,x-xmin,y-ymin,y-ymin,ymax-y)<n];M=cp_model.CpModel();B={i:M.new_bool_var('') for i in eligible};
  for ix,c in cs:
   vv=[B[i] for i in ix if i in B];
   if len(vv)>c:M.add(sum(vv)<=c)
  for i,j in itertools.combinations(eligible,2):
   if max(abs(Q[i][0]-Q[j][0]),abs(Q[i][1]-Q[j][1]))>=n:M.add_bool_or([~B[i],~B[j]])
  M.maximize(sum(B.values()));opt=cp_model.CpSolver();opt.parameters.num_workers=1;opt.parameters.max_time_in_seconds=.4;status=opt.solve(M)
  if status in [cp_model.OPTIMAL,cp_model.FEASIBLE]:
   a=[Q[i] for i in eligible if opt.value(B[i])];R=S|set(a);dx=-min(x for x,y in R);dy=-min(y for x,y in R);out[n]=(len(R),{'n':n,'m':m,'source':src.stem,'dx':dx,'dy':dy,'points':sorted((x+dx,y+dy) for x,y in R),'added_in_source_frame':a,'halo_exact_for_seed':status==cp_model.OPTIMAL})
 return out
if __name__=='__main__':
 ids=json.loads(Path('seedindex.json').read_text());best0={};out=Path('halo');out.mkdir(exist_ok=True)
 for e in ids:best0[e['n']]=max(best0.get(e['n'],0),e['points'])
 best=best0.copy()
 for e in sorted(ids,key=lambda e:(e['n']!=200,not e['id'].startswith('sets_'),-e['points'])):
  m=e['n'];
  if e['points']<best0[m]-4:continue
  for n,(k,r) in run(Path('seeds')/(e['id']+'.txt'),6).items():
   if k>best.get(n,0):
    best[n]=k;(out/f'n{n}_{k}.json').write_text(json.dumps(r));
    if k>1.8*n or n in best0:print('halo',n,k,'from',e['id'],r['added_in_source_frame'],flush=True)
