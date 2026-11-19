#!/usr/bin/env python3
"""Construct a half-turn invariant no-three-in-line set on any positive integer side.
--ordinary also compares against embedding or cropping the classical frame.
Compares stated guaranteed counts; not an optimizer. Coordinates are zero based.
"""
from pathlib import Path
import argparse,csv
from anchor_ring import prime,best_spec,realize
from seam_caps import construction

def run(n,ordinary=False):
 if n<1:raise ValueError('side must be positive')
 if ordinary:
  sym,info=run(n,False);opts=[(len(sym),'already built',None)]
 else:
  spec=best_spec(n);opts=[(spec[0],'earlier',spec)]
 if ordinary and n%2==0 and n>1:
  z=best_spec(n-1);opts.append((z[0],'earlier',z))
 for cls in (None,1):
  for ran in (range((n+(n%2))//4,4,-1), range((n+3)//4,n//3+1)):
   p=next((u for u in ran if (cls is None or u%12==cls)and prime(u)),None)
   if p is None:continue
   m=min(n,4*p-(n%2))
   if not 3*p<=m<=4*p:continue
   delta={1:0,5:8}.get(p%12,10);delta=0 if (4*p-m)**2>=1024*p else delta
   lower=2*m-2*p-(4 if m%2 else 6)-delta;opts.append((lower,'rectangular repair',(p,m)))
 if ordinary and n>=6:
  q=next(i for i in range(n//2,2,-1)if prime(i));opts.append((3*(q-1),'ordinary frame',q));q=(n+1)//2
  while not prime(q):q+=1
  opts.append((3*(q-1)-4*(2*q-n),'ordinary crop',q))
 E=Path(__file__).resolve().parents[1]/'data'
 for side,k in ((293,446),(389,594),(4037,6176),(10085,15364)):
  if side<=n and(ordinary or(side-n)%2==0):opts.append((k,'embedded verified example',side))
 lower,mode,arg=max(opts,key=lambda v:v[0]);p=None
 if mode=='already built':return sym,info
 if ordinary:del sym
 if mode=='earlier':label,p,k,P=realize(n,arg);mode=label
 elif mode=='rectangular repair':
  p,m=arg;P,_=construction(p,m);d=(n-m)//2
  if d:P=[(x+d,y+d)for x,y in P]
 elif mode.startswith('ordinary '):
  p=arg;m=2*p;_,_,_,P=realize(m,(3*(p-1),'classical embedded frame',p,m,None))
  if m>n:
   dx,dy=max(((a,b)for a in (0,m-n)for b in(0,m-n)),key=lambda s:sum(s[0]<=x<s[0]+n and s[1]<=y<s[1]+n for x,y in P))
   P=[(x-dx,y-dy)for x,y in P if dx<=x<dx+n and dy<=y<dy+n]
  else:
   d=(n-m)//2;P=[(x+d,y+d)for x,y in P]
 else:
  d=(n-arg)//2
  with (E/f'augmented{arg}.csv').open()as f:P=[(int(r['x'])+d,int(r['y'])+d)for r in csv.DictReader(f)]
 S=set(P);half=all((n-1-x,n-1-y)in S for x,y in P);assert len(S)==len(P)>=lower and all(0<=x<n and 0<=y<n for x,y in P) and(ordinary or half)
 return P,dict(side=n,points=len(P),guarantee=lower,construction=mode,prime=p,half_turn=half)
if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('n',type=int);a.add_argument('--ordinary',action='store_true');a.add_argument('--csv');o=a.parse_args();P,I=run(o.n,o.ordinary);print(I)
 if o.csv:
  with open(o.csv,'w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(sorted(P))
