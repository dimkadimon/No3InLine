import sys,itertools,math
from anchor_ring import chi,prime,nonsquare
I=[(0,i)for i in (1,2,3)]+[(4,i)for i in (1,2,3)]+[(i,0)for i in (1,2,3)]+[(i,4)for i in (1,2,3)];Ps=list(itertools.combinations([1,2,3],2));A=[set([(0,y)for y in a]+[(4,y)for y in b]+[(x,0)for x in c]+[(x,4)for x in d])for a,b,c,d in itertools.product(Ps,repeat=4)];S=[s for s in A if {(4-x,4-y)for x,y in s}==s];
def make(p):
 R={t*t%p:t for t in range(1,p//2+1)};D={}
 for i,j in I:
  L=[]
  for a,b in itertools.product(range(-7,8), repeat=2):
   if not a*b or math.gcd(a,b)!=1:continue
   stop=min(((4-i if a>0 else i)*p)//abs(a),((4-j if b>0 else j)*p)//abs(b));
   if stop<1 or a*b%p in R:continue
   hits=[(m,l)for m,l in I if (m,l)!=(i,j) and a*(l-j)==b*(m-i)];L.append((a,b,stop,pow(a*b,-1,p),hits))
  D[i,j]=L
 return R,D

def check(p,k,R,D):
 bad=set();pairs=set()
 for (i,j),ds in D.items():
  for a,b,stop,inv,hits in ds:
   r=R[k*inv%p];P=[]
   for s in (r,p-r):
    for t in range(s,stop+1,p):
     x=i*p+a*t;y=j*p+b*t
     if not (1<=x//p<=2 and 1<=y//p<=2) and (x+y)%2==int(x%p not in R):P.append(t)
   if len(P)>1:bad.add((i,j));break
   if P:
    for q in hits:pairs.add(frozenset(((i,j),q)))
 for idx,B in enumerate(S+A):
  if not B&bad and not any(s<=B for s in pairs):return idx
 return -1
for p in range(13,1300,24):
 if not prime(p):continue
 R,D=make(p);ok=None;ord=None
 for k in range(1,p):
  if k in R:continue
  v=check(p,k,R,D)
  if v!=-1:
   if ord is None:ord=(v,k)
   if v<len(S):ok=v,k;break
 print('p',p,'any',ord,'half',ok,flush=True)
