#!/usr/bin/env python3
"""Half-turn caps in a 3-to-4 period square; pure Python, all arithmetic exact.
Run --help. Coordinates are zero based. By default the scale search tries to place the
exceptional classes in 3 by 3 rectangles; --unscaled skips that search. No external packages are needed.
"""
from collections import Counter
from functools import lru_cache
from itertools import product,combinations
from math import gcd,isqrt
import argparse,csv

def prime(p):return p>=2 and all(p%i for i in range(2,isqrt(p)+1))
def signrep(a,p):a%=p;return min(a,p-a)
FAMILY=((1,1),(1,-1),(3,1),(3,-1),(1,3),(1,-3))
@lru_cache(None)
def bank(w,h,t):
 A=[(i,j)for i in range(w)for j in range(h) if (i+j)%2==t];rows=[]
 for k in range(len(A),-1,-1):
  for P in combinations(A,k):
   slopes=set();lines=set();good=True
   for (i,j),(k,l)in combinations(P,2):
    a=k-i;b=l-j;g=gcd(a,b);a//=g;b//=g
    if a*b and (a,b)not in FAMILY:good=False;break
    z=(a,b,a*j-b*i)
    if z in lines:good=False;break
    lines.add(z);slopes.add((a,b))
   if good:rows.append((P,frozenset(slopes)))
 return rows
@lru_cache(None)
def mask(w,h,t,bad=frozenset()):return next(P for P,D in bank(w,h,t)if not D&bad)

def choose_scale(p,n,H):
 """Return t with all defect fibres in short rectangles if found, zero otherwise."""
 d=4*p-n
 if d<=0:return 0
 if p%4==1: # r= sqrt(-1)
  r=next(a for a in range(2,p)if a*a%p==p-1);factors=(1,3,r,3*r)
 else:
  r=pow(3,(len(H)+1)//2,p);assert r*r%p in (3,p-3);factors=(1,3,9,r,3*r)
 alpha=(n-1)*pow(2,-1,p)%p
 def w(u):return 1+(n-1-(alpha+u)%p)//p
 for s in range(1,p//2+1):
  if all(w(s*a)==w(-s*a)==3 for a in factors):return 3*s%p
 return 0

def construction(p,n,scale=True):
 if not prime(p)or p<=3 or not 3*p<=n<=4*p:raise ValueError('need a prime p>3 and 3p<=n<=4p')
 sg=lambda u:signrep(u,p);R={i*i%p for i in range(1,p//2+1)};alpha=(n-1)*pow(2,-1,p)%p;H=[];T={};t=1;short=False
 if p%12==1:
  c=next(k for k in range(2,p)if k not in R);T={i:int(i not in R) for i in range(1,(p+1)//2)}
 else:
  v=1
  while not H or v!=1:H.append(v);v=sg(3*v)
  L=len(H);h=L//2
  if scale:
   z=choose_scale(p,n,H)
   if z:t=z;short=True
  c=(t*t*(pow(3,-1,p) if p%4==1 else 1))%p
  # The exceptional signed coset is [t]H. Other cosets are paired.
  if p%4==1:assert not L%2;colors=[int(j>=h)for j in range(L)]
  else:
   assert L%2;colors=[int(j>h)for j in range(L)];x=(alpha+t)%p;w=1+(n-1-x)//p
   colors[0]=int(w==4) # diagonal root; best checkerboard phase for 3x3 or 4x4
  T={sg(a*t):colors[i]for i,a in enumerate(H)}
  for a in range(1,(p+1)//2):
   if a in T:continue
   b=c*pow(a,-1,p)%p
   for z in H:
    i=sg(a*z);j=sg(b*z);assert i!=j;T[i]=0;T[j]=1
 points=[];debits=Counter();badclasses=[]
 for u in range(1,(p+1)//2):
  v=c*pow(u,-1,p)%p;x=(alpha+u)%p;y=(alpha+v)%p;w=1+(n-1-x)//p;h=1+(n-1-y)//p
  bad=set()
  for a,b in FAMILY:
   z=-a*v*pow(b,-1,p)%p
   if z!=u and T[sg(z)]==T[u]:bad.add((a,b))
  if short and p%4==3 and u==sg(t):
   assert w==h==3 and x==y
   S=((0,1),(0,2),(1,1),(1,2))
  else:S=mask(w,h,(T[u]-x-y)%2,frozenset(bad))
  if bad:badclasses.append(u)
  for i,j in S:
   X=x+i*p;Y=y+j*p;points.extend(((X,Y),(n-1-X,n-1-Y)))
  debits[w+h-2-len(S)]+=2
 mu=3 if n%2 else 4;bench=2*n-2*p+2-2*mu;loss=bench-len(points)
 assert loss<=({1:0,5:8}.get(p%12,10)) and (not short or loss==0)
 return points,dict(p=p,n=n,c=c,t=t,short_patch=short,ideal=bench,loss=loss,points=len(points),bad_signed=len(badclasses))

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('p',type=int);ap.add_argument('n',type=int);ap.add_argument('--unscaled',action='store_true');ap.add_argument('--csv');a=ap.parse_args();P,info=construction(a.p,a.n,not a.unscaled);print(' '.join(str(k)+'='+str(v)for k,v in info.items()))
 if a.csv:
  with open(a.csv,'w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(sorted(P))
