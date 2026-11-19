"""Search for sixth points in damaged fibres near side 4p. Exact per-fibre replacement with exterior frozen."""
from math import gcd
from collections import Counter,defaultdict
from itertools import combinations,product
from functools import lru_cache
import sys,random,json
@lru_cache(None)
def candidates(w,h,r):
 # use row/col caps; exhaustive for six points on a 3 by 4 rectangle
 out=[]
 for S in combinations(product(range(w),range(h)),r):
  if max(Counter(x for x,y in S).values())>2 or max(Counter(y for x,y in S).values())>2:continue
  if all((x-u)*(b-v)!=(y-v)*(a-u) for (u,v),(x,y),(a,b) in combinations(S,3)):out.append(S)
 return out
M0=((0,0),(0,2),(1,3),(2,0),(3,1),(3,3));M1=tuple((x,3-y)for x,y in M0)
short={(3,3):(((0,0),(0,2),(2,0),(2,2)),((0,1),(1,0),(1,2),(2,1))), (3,4):(((0,0),(0,2),(1,3),(2,0),(2,2)),((0,1),(0,3),(1,0),(2,1),(2,3))), (4,4):(M0,M1)}
short[4,3]=tuple(tuple((y,x)for x,y in S)for S in short[3,4]);DIR=set((a,b)for a in range(4)for b in range(-3,4)if (a or b>0) and gcd(a,b)==1)
def experiment(p,k,d,ox=1,oy=1,alternate=False):
 n=4*p-d; chi={a*a%p for a in range(1,p)};old={};spots={};dims={};
 for u in range(1,p):
  v=k*pow(u,-1,p)%p;x=ox+(u-ox)%p;y=oy+(v-oy)%p;w=len(range(x,ox+n,p));h=len(range(y,oy+n,p));t=(int(u not in chi)-x-y+int(alternate))%2;M=short[w,h][t];old[u]=[(x+a*p,y+b*p)for a,b in M];spots[u]=x,y;dims[u]=w,h
 lines=Counter((a,b,b*x-a*y)for P in old.values() for x,y in P for a,b in DIR)
 assert max(lines.values())<=2
 base=sum(map(len,old.values()));g=Counter();gains=[]
 for u,(w,h)in dims.items():
  if (w,h)==(4,4):continue
  x,y=spots[u];P=old[u];local=Counter((a,b,b*s-a*t)for s,t in P for a,b in DIR)
  free={};bad=set();pairs=set()
  for i,j in product(range(w),range(h)):
   s=x+p*i;t=y+p*j;cap=tuple(lines[a,b,b*s-a*t]-local[a,b,b*s-a*t] for a,b in DIR);free[i,j]=cap
   if 2 in cap:bad.add((i,j))
  for z,Z in combinations(free,2):
   dx=Z[0]-z[0];dy=Z[1]-z[1];D=gcd(dx,dy);a=dx//D;b=dy//D
   if (not a and b<0) or a<0:a,b=-a,-b
   s=x+p*z[0];t=y+p*z[1]
   if lines[a,b,b*s-a*t]-local[a,b,b*s-a*t]:pairs.add(frozenset([z,Z]))
  best=len(P);MS=None
  for sz in range(2*min(w,h),best,-1):
   for S in candidates(w,h,sz):
    T=set(S)
    if bad&T or any(ed<=T for ed in pairs):continue
    best=sz;MS=S;break
   if MS:break
  g[w,h,best-len(P)]+=1
  if MS:gains.append([u,len(MS)-len(P)])
 return base,dict(g),gains
if __name__=='__main__':
 from math import isqrt
 for p in (241,673,1009,1201,3361,7561):
  if not all(p%t for t in range(2,isqrt(p)+1)):continue
  ks=[k for k in range(2,100)if pow(k,p//2,p)==p-1][:3];d=max(5,p//75)
  for k in ks:
   base,g,gs=experiment(p,k,d);print(p,k,d,base,g,'solo excess',sum(t for u,t in gs),'needed',1.5*(4*p-d)-base,flush=True)
