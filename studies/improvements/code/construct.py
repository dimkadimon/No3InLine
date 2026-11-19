#!/usr/bin/env python3
"""An explicit no-three-in-line set for any positive n. Default: half-turn about the centre.
--ordinary also tries classical embeddings/crops and the large witness library. Not an optimizer.
Python 3.9+, standard library only, zero-based coordinates."""
import csv,argparse
from pathlib import Path
from chart_caps import best,prime
from catalogue_small import records,decode
from anchor_ring import best_spec,realize
D=Path(__file__).resolve().parents[1]

def read_points(path):
 with path.open()as f:return [(int(a),int(b))for a,b in list(csv.reader(f))[1:]]

def library():
 for n,k in ((293,508),(389,668),(4037,6296),(10085,15520),(16018,24588),(32002,48838),(64006,97062)):
  yield n,k,n%2==1,D/'coordinates'/f'n{n}.csv'
 for n,k in ((100,184),(200,360),(240,424),(300,528)):
  yield n,k,True,D/'data'/f'try{n}.csv'
 for n,k,h in ((201,362,False),(202,364,True)):
  yield n,k,h,D/'sources'/f'n{n}.csv'
 with (D/'data'/'small-index.csv').open()as f:
  for r in csv.DictReader(f):
   n=int(r['n']);yield n,int(r['points']),True,D/'data'/'small'/f'n{n}.csv'

def fit(P,m,n,keep_half_turn):
 if m<=n:
  d=(n-m)//2;return P if d==0 else [(x+d,y+d)for x,y in P]
 a=m-n
 if keep_half_turn:dx=dy=a//2
 else:dx,dy=max(((x,y)for x in(0,a)for y in(0,a)),key=lambda z:sum(z[0]<=x<z[0]+n and z[1]<=y<z[1]+n for x,y in P))
 return [(x-dx,y-dy)for x,y in P if dx<=x<dx+n and dy<=y<dy+n]

def make(n,ordinary=False):
 if n<1:raise ValueError('positive side required')
 if ordinary:
  sym,info=make(n,False);opts=[(len(sym),'already built',None)]
  if n%2==0 and n>1:
   spec=best_spec(n-1);opts.append((spec[0],'baseline',spec))
 else:
  spec=best_spec(n);opts=[(spec[0],'baseline',spec)]
  for cls in (0,1):
   for R in (range((n+n%2)//4,4,-1),range((n+3)//4,n//3+1)):
    p=next((v for v in R if prime(v)and(not cls or v%12==1)),None)
    if p is None:continue
    m=min(n,4*p-n%2)
    if m<3*p:continue
    d=4*p-m;loss={1:0,5:4}.get(p%12,4 if d>=19 else 6);loss=0 if d*d>=1024*p else loss
    opts.append((2*m-2*p-(4 if m%2 else 6)-loss,'chart repair',(p,m)))
 for a,k,h,word in records():
  if ordinary or (h and (n-a)%2==0):opts.append((k-4*max(a-n,0),'catalogue',(word,a)))
 for a,k,h,file in library():
  if ordinary or(h and(n-a)%2==0):opts.append((k-4*max(a-n,0),'witness',(file,a)))
 if ordinary and n>=6:
  p=next(i for i in range(n//2,2,-1)if prime(i));q=(n+1)//2
  while not prime(q):q+=1
  for r in (p,q):opts.append((3*(r-1)-4*max(2*r-n,0),'prime frame',r))
 lower,mode,arg=max(opts,key=lambda t:t[0]);p=None;m=n
 if mode=='already built':return sym,info
 if ordinary:del sym
 if mode=='baseline':label,p,_,P=realize(n,arg)
 elif mode=='chart repair':p,m=arg;P,I=best(p,m);label=I['method']
 elif mode=='prime frame':
  p=arg;m=2*p;label='classical prime frame, embedded/cropped';_,_,_,P=realize(m,(3*(p-1),'classical embedded frame',p,m,None))
 elif mode=='catalogue':
  word,m=arg;label='public Flammenkamp catalogue';P=decode(word)
 else:
  file,m=arg;label='explicit witness from '+str(file.relative_to(D));P=read_points(file)
 P=fit(P,m,n,not ordinary);S=set(P);ht=all((n-1-x,n-1-y)in S for x,y in S)
 assert len(P)==len(S)>=lower and(ordinary or ht)and all(0<=x<n and 0<=y<n for x,y in P)
 return P,dict(side=n,points=len(P),guaranteed=lower,half_turn=ht,construction=label,p=p)
if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('n',type=int);a.add_argument('--csv');a.add_argument('--ordinary',action='store_true');v=a.parse_args();P,I=make(v.n,v.ordinary);print(I)
 if v.csv:
  with open(v.csv,'w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(sorted(P))
