from twoperiod_probe import *

def crop(p,k,d,ax,ay,verbose=False):
 h=p//2;n=2*p-d;lx=ax;ly=-h+ay
 E={i%p for i in list(range(ax-d,ax))+list(range(ly-d,ly))}-{0};Os={min(z,-z%p,k*pow(z,-1,p)%p,-k*pow(z,-1,p)%p) for z in E};Z=[]
 for u in sorted(Os):
  v=k*pow(u,-1,p)%p;g=len({u,-u%p,v,-v%p});b=solve_orbit(p,k,n,lx,ly,u);Z.append((u,v,b-3*g))
 if verbose:print(Z)
 return 3*(p-1)+sum(z[2] for z in Z)
if __name__=='__main__':
 from math import lcm
 import random,sys
 p=int(sys.argv[1]) if len(sys.argv)>1 else 1009
 for d in (1,2,3,4,5,8,12,16,24,32):
  ks=set(random.Random(13).sample(range(1,p),24))|{x%p for v in (1,2,3,5,lcm(*range(1,2*d+3)))for x in (v,-v)};arr=[]
  for k in ks:
   if not k:continue
   for ax,ay in {(0,0),(d,0),(0,d),(d,d),(d//2,d//2),(0,d//2),(d//2,0)}:arr.append((2*crop(p,k,d,ax,ay)-3*(2*p-d),k,ax,ay))
  print(p,d,max(arr),flush=True)
