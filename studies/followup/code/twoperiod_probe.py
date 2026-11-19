"""Window enlargements of the HJSW frame. Mixed-slope repeated-fibre pairs forbidden here."""
from itertools import combinations
from functools import lru_cache
from math import gcd
from collections import Counter
@lru_cache(None)
def masks(w,h,strict=True):
 S=[(x,y) for x in range(w)for y in range(h)];R=[]
 for r in range(len(S),-1,-1):
  for Z in combinations(S,r):
   if strict and any(a!=x and b!=y and abs(x-a)!=abs(y-b) for (a,b),(x,y)in combinations(Z,2)):continue
   if any((a-x)*(v-y)==(b-y)*(u-x) for (x,y),(a,b),(u,v)in combinations(Z,3)):continue
   R.append(Z)
 return R

def solve_orbit(p,k,n,lx,ly,u,strict=True):
 v=k*pow(u,-1,p)%p;O=sorted({u,v,-u%p,-v%p});P=[];base=[];D=Counter();dirs=lambda x,y:((1,x+y),(-1,x-y))
 for z in O:
  w=k*pow(z,-1,p)%p;x0=lx+(z-lx)%p;y0=ly+(w-ly)%p;xw=1+(lx+n-1-x0)//p;yh=1+(ly+n-1-y0)//p
  pts=[(x0+a*p,y0+b*p) for a in range(xw)for b in range(yh)];D.update(d for x,y in pts for d in dirs(x,y));base.append((x0,y0,xw,yh))
 ids={d:1<<i for i,d in enumerate(d for d,count in sorted(D.items())if count>2)}
 for x,y,w,h in base:
  z=[]
  for M in masks(w,h,strict):
   a=b=0
   for i,j in M:
    X=x+i*p;Y=y+j*p;bits=ids.get((1,X+Y),0)|ids.get((-1,X-Y),0);b|=a&bits;a|=bits
   z.append((len(M),a,b))
  P.append(tuple(sorted(set(z),reverse=True)))
 return opt(tuple(P))
@lru_cache(10000)
def opt(P):
 best=0;rem=[0]*(len(P)+1)
 for i in range(len(P)-1,-1,-1):rem[i]=rem[i+1]+P[i][0][0]
 def rec(i,t,a,b):
  nonlocal best
  if i==len(P):best=max(t,best);return
  if t+rem[i]<=best:return
  for sz,x,y in P[i]:
   if t+sz+rem[i+1]<=best:break
   if x&b or y&a:continue
   rec(i+1,t+sz,a|x,b|y|(a&x))
 rec(0,0,0,0);return best

def solve(p,k,d,ax=0,ay=0,strict=True,verbose=False):
 h=p//2;n=2*p+d;lx=-ax;ly=-h-ay;assert 0<=ax<=d and 0<=ay<=d
 E={i%p for i in list(range(lx,lx+d))+list(range(ly,ly+d))}-{0};O={min(u,-u%p,k*pow(u,-1,p)%p,-k*pow(u,-1,p)%p)for u in E};Z=[]
 for u in sorted(O):
  v=k*pow(u,-1,p)%p;g=len({u,-u%p,v,-v%p});b=solve_orbit(p,k,n,lx,ly,u,strict);Z.append((u,v,b-3*g))
 if verbose:print('mods',Z)
 return 3*(p-1)+sum(t for u,v,t in Z)
if __name__=='__main__':
 import sys,random
 from math import lcm
 p=int(sys.argv[1])if len(sys.argv)>1 else 1009
 for d in (1,2,3,4,5,8,12,20,32):
  ks={1,-1,2,-2,lcm(*range(1,2*d+3))%p,-lcm(*range(1,2*d+3))%p,*random.Random(13).sample(range(1,p),24)};z=[]
  for k in ks:
   if not k%p:continue
   for ax,ay in {(0,0),(d//2,d//2),(0,d//2),(d//2,0),(d,0)}:z.append((2*solve(p,k%p,d,ax,ay)-3*(2*p+d),k%p,ax,ay))
  a=max(z);print(p,d,a,flush=True)
