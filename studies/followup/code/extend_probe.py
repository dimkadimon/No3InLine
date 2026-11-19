"""Exact local tests for adding outer wrong-parity lifts to the 4-period ring."""
from math import gcd
from itertools import product,combinations
from functools import lru_cache
@lru_cache(None)
def sq(p):return {x*x%p for x in range(1,p//2+1)}
D=[(a,b)for a in range(5)for b in range(-4,5)if (a or b>0)and gcd(a,b)==1]
def level(p,k,d,flip=0,check_pair=True):
 R=sq(p);N=4*p+d  # board 0..4p+d, d extra rows/columns beyond the anchored board
 def old(x,y):return 0<x<4*p and 0<y<4*p and not(p<x<3*p and p<y<3*p) and (x+y)%2==(int(x%p not in R)^flip)
 def pieces(x,y,a,b):
  if a*b:
   rp=(-(x*b+y*a)*pow(a*b,-1,p))%p
  else:rp=0
  P=[]
  for r in ({0,rp}):
   for s in range(-5,6):
    t=r+s*p;X=x+a*t;Y=y+b*t
    if 0<=X<=N and 0<=Y<=N:P.append((X,Y))
  return P
 C=set()
 for u in range(1,d+1):
  v=k*pow(u,-1,p)%p
  for x,y,vert in ((u,v,True),(v,u,False)):
   t=(int(x not in R)^flip^((x+y)&1));j=1+t;C.add((4*p+x,y+j*p)if vert else (x+j*p,4*p+y))
   if x<=d and y<=d and t==1:C.add((x+4*p,y+4*p))
 F=[];bl={}
 for q in sorted(C):
  for a,b in D:
   P=pieces(*q,a,b)
   if sum(old(x,y)for x,y in P)>=2:bl[q]=(a,b);break
  else:F.append(q)
 S=set(F)
 if check_pair:
  for q in F:
   if q not in S:continue
   for a,b in D:
    P=pieces(*q,a,b)
    if sum(old(x,y)or (x,y)in S for x,y in P)>2:S.remove(q);break
 return F,sorted(S),bl
if __name__=='__main__':
 import sys
 p=int(sys.argv[1]) if len(sys.argv)>1 else 2521;R=sq(p)
 for d in (1,2,3,4,5,8,12,20,30):
  best=(-999,());maxfree=0
  for k in range(2,p):
   if k in R:continue
   f,s,b=level(p,k,d)
   if len(s)>best[0]:best=len(s),(k,s)
   maxfree=max(maxfree,len(f))
  print(p,d,best[0],maxfree,'first-level',best[1][0],flush=True)
