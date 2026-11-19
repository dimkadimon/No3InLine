#!/usr/bin/env python3
"""The chart repair on 3p<=n<=4p. Exact zero-based coordinates, half-turn about board centre.
Imports the reviewed-in-draft sheet masks (no third-party packages). Finite exceptional
boards use the bundled explicit caps, not an assumption about a search algorithm.
"""
from pathlib import Path
import sys,argparse,csv
from collections import Counter
from functools import lru_cache
from seam_caps import prime,signrep,mask,FAMILY,construction as previous
from anchor_ring import M
BASE=Path(__file__).resolve().parents[1]
@lru_cache(None)
def params(p):
 sg=lambda u:signrep(u,p);H=[1];x=sg(3)
 while x!=1:H.append(x);x=sg(3*x)
 if p%4==1:r=next(j for j in range(2,p)if j*j%p==p-1)
 else:r=pow(3,(len(H)+1)//2,p)
 return H,r

def chart(p,n):
 H,r=params(p);d=4*p-n;b=(n-1)%2;even=p%4==1
 if len(H)<(4 if even else 5):return None
 a=lambda x:d<x<2*p-d
 for z in range(b or 2,2*p,2):
  if not a(z) or not a(3*z)or(not even and not a(9*z-2*p)):continue
  for w0 in (r*z,-r*z):
   w=w0%p;w=w if w%2==b else w+p
   if a(w)and a(3*w):return z,w
 return None

def best(p,n,use_older=True):
 if not prime(p) or p<=3 or not 3*p<=n<=4*p:raise ValueError('need prime p>3 and 3p<=n<=4p')
 U=2*n-2*p-(4 if n%2 else 6);d=4*p-n;E=p%4==1;target=U-({1:0,5:4}.get(p%12,4 if d>=19 else 6));half=lambda x,y:(n-1-x,n-1-y)
 if use_older or p%12==1:
  P,I=previous(p,n)
  if len(P)>=target:return P,dict(p=p,n=n,points=len(P),ideal=U,loss=U-len(P),method='earlier exact masks')
 sg=lambda u:signrep(u,p);H,r=params(p);L=len(H);h=L//2;short=d>=19
 if short:z=1 if n%2==0 else 2
 else:
  v=chart(p,n)
  if v is None:
   f=BASE/'data'/'small'/f'n{n}.csv'
   with f.open()as stream:P=[tuple(map(int,row))for row in list(csv.reader(stream))[1:]]
   assert len(P)>=target;return P,dict(p=p,n=n,points=len(P),ideal=U,loss=U-len(P),method='finite board witness')
  z,w=v
 t=(3*z*pow(2,-1,p))%p;c=t*t*(pow(3,-1,p)if E else 1)%p;A=(n-1)*pow(2,-1,p)%p
 if E:C=[int(i>=h)for i in range(L)]
 else:C=[1 if 0<=i<=h else 0 for i in range(L)]
 T={sg(t*u):C[i]for i,u in enumerate(H)}
 for u in range(1,(p+1)//2):
  if u in T:continue
  v=c*pow(u,-1,p)%p
  for e in H:T[sg(u*e)]=0;T[sg(v*e)]=1
 P=[]
 for rep in range(1,(p+1)//2):
  u=t if not E and rep==sg(t) else 3*t%p if not E and rep==sg(3*t) else rep
  v=c*pow(u,-1,p)%p;x=(A+u)%p;y=(A+v)%p;w=1+(n-1-x)//p;k=1+(n-1-y)//p;phase=(T[rep]-x-y)%2
  bad={(a,b)for a,b in FAMILY if (other:=-a*v*pow(b,-1,p)%p)!=u and T[sg(other)]==T[rep]}
  if not E and rep==sg(t):
   if short:assert w==k==3;S=((0,1),(0,2),(1,1),(1,2))
   else:assert w==k==4 and phase==1;S=((0,1),(0,3),(1,0),(3,0))
  elif not short and not E and rep==sg(3*t):assert w==k==4 and phase==0;S=M[0]
  elif not short and len(bad)==1 and w==k==4 and all(sg(-a*v*pow(b,-1,p))==rep for a,b in bad):
   a,b=next(iter(bad));m=M[phase];off=[b*(2*(x+p*i)-n+1)-a*(2*(y+p*j)-n+1)for i,j in m];C=Counter(off+[-t0 for t0 in off]);S=m if max(C.values())<=2 else mask(w,k,phase,frozenset(bad))
  else:S=mask(w,k,phase,frozenset(bad))
  for i,j in S:q=(x+p*i,y+p*j);P.extend([q,half(*q)])
 assert len(P)>=target,(p,n,c,t,len(P),target);return P,dict(p=p,n=n,c=c,t=t,points=len(P),ideal=U,loss=U-len(P),method='partial short'if short else 'radial charts')
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('p',type=int);ap.add_argument('n',type=int);ap.add_argument('--csv');ap.add_argument('--use-new',action='store_true',help='use new repair even if the old masks already meet the new guarantee');o=ap.parse_args();P,I=best(o.p,o.n,not o.use_new);print(I)
 if o.csv:
  with open(o.csv,'w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(sorted(P))
