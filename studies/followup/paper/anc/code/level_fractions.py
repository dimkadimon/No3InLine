"""Count levels passing the sufficient small-root test, not all legal levels."""
from fractions import Fraction as F
from seam_caps import prime
from itertools import product

def count(p):
 assert prime(p)and p%24==1;root={j*j%p:j for j in range(1,(p+1)//2)};s5=5 in root;s7=7 in root;nu=5 if not s5 else 7 if not s7 else next(k for k in range(2,p)if k not in root)
 ds=[(sg*d,h)for sg in(-1,1)for d,h in[(5,5),(15,5),(7,7),(21,7),(35,7)]if sg*d%p not in root];R=[(root[nu*pow(d,-1,p)%p],h)for d,h in ds];hist=sum(all(min(z*r%p,-z*r%p)*h<(h-4)*p for r,h in R)for z in range(1,(p+1)//2));rho=F(1)
 for d,h in ds:rho*=F(2*(h-4),h)
 return s5,s7,hist,(p-1)//2,rho
if __name__=='__main__':
 seen=set()
 for p in range(200017,400000,24):
  if not prime(p):continue
  tag=(pow(5,p//2,p),pow(7,p//2,p));tag=tuple(x==1 for x in tag)
  if tag in seen:continue
  seen.add(tag);a,b,s,k,rho=count(p);print(p,int(a),int(b),s,k,round(s/k,6),str(rho));
  if len(seen)==4:break
