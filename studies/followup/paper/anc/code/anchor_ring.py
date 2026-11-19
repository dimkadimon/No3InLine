#!/usr/bin/env python3
"""Half-turn modular ring and eight protected boundary anchors. Zero-based ordinary coordinates.
With --p, use the exact prime-eligibility check, never a numerical tolerance.
With --n, produce a construction for that side. The point list on an arbitrary n is a lower bound.
Python >=3.9; no dependencies.
"""
import argparse,csv,math,sys
from itertools import product
from functools import lru_cache

def prime(p):return p>=2 and all(p%i for i in range(2,math.isqrt(p)+1))
def chi(x,p):
 a=pow(x%p,p//2,p);return -1 if a==p-1 else a
def nonsquare(p):return next(x for x in range(2,p)if chi(x,p)<0)
# Protected anchors are the D4 orbit of (0,p) about the square's centre, (2p,2p).
B=((0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4))
EDGE=tuple((a,b) for a in range(5) for b in range(5) if (a in (0,4)) != (b in (0,4)))
M=( ((0,0),(0,2),(1,3),(2,0),(3,1),(3,3)), ((0,1),(0,3),(1,0),(2,3),(3,0),(3,2)) )

def high_odd_tests(p):
 vals={};
 for a in (1,3,5,7):
  for b in (1,3,5,7):
   H=max(a,b)
   if H<5 or math.gcd(a,b)!=1:continue
   for k in (a*b,-a*b):
    if chi(k,p)==-1:vals[k]=H
 return sorted(vals.items())

def base_level(p):
 """A sufficient small-root search. If it fails at a small p, try all levels with the exact ray checker."""
 if p%24!=1 or not prime(p):raise ValueError('requires a prime equal to 1 modulo 24')
 nu=nonsquare(p);tests=high_odd_tests(p)
 if not tests:return nu
 sq={x*x%p:x for x in range(1,p//2+1)};roots=[(sq[nu*pow(d,-1,p)%p],H)for d,H in tests];Bnum=math.prod(5 if h==5 else 3 for _,h in roots)
 for z in range(1,min(p-1,Bnum)+1):
  if all(min(z*r%p,-z*r%p)*H<(H-4)*p for r,H in roots):return nu*z*z%p
 # The simultaneous-approximation proof guarantees the above search at p>Bnum.
 if p>Bnum:raise ArithmeticError('Dirichlet certificate failed')
 for k in range(1,p):
  if chi(k,p)==-1 and finite_rays(p,k,sq):return k
 raise ValueError('no working level: p='+str(p))

def finite_rays(p,k,sq=None):
 """Exact ordinary intersections with the six-cell ring. h>=8 excluded by the positive-ray lemma."""
 if p%24!=1 or chi(k,p)!=-1:return False
 if sq is None:sq={x*x%p:x for x in range(1,p//2+1)}
 for i,j in EDGE:
  X,Y=i*p,j*p
  for a,b in product(range(-7,8),repeat=2):
   if not a*b or math.gcd(a,b)!=1:continue
   tmax=min((4*p-X)//a if a>0 else X//(-a), (4*p-Y)//b if b>0 else Y//(-b))
   if tmax<2:continue
   r=sq.get(k*pow(a*b,-1,p)%p)
   if r is None:continue
   ct=0
   for r0 in (r,p-r):
    for u in range(r0,tmax+1,p):
     x=X+a*u;y=Y+b*u
     if (x//p in (1,2) and y//p in (1,2)) or (x+y)%2!=int(chi(x,p)<0):continue
     ct+=1
     if ct>1:return False
 return True

def ring(p,k,even=False):
 """Old ring in 0..4p−1; centring the residue origin differs for an odd/even final window."""
 shift=(p-1)//2 if even else 0;P=[]
 squares={a*a%p for a in range(1,p//2+1)}
 for u in range(1,p):
  x=(u+shift)%p;y=(k*pow(u,-1,p)+shift)%p;t=(int(u not in squares)-x-y)%2
  P.extend((x+p*i,y+p*j) for i,j in M[t])
 return P

def anchored(p,k=None):
 if k is None:k=base_level(p)
 if not prime(p) or not finite_rays(p,k):raise ValueError('invalid modulus or unprotected anchors')
 return 4*p+1,k,ring(p,k)+[(i*p,j*p)for i,j in B]

MESH={(4,4):M,(3,3):(((0,0),(0,2),(2,0),(2,2)),((0,1),(1,0),(1,2),(2,1))),
      (3,4):(((0,0),(0,2),(1,3),(2,0),(2,2)),((0,1),(0,3),(1,0),(2,1),(2,3)))}
MESH[4,3]=tuple(tuple((b,a)for a,b in S)for S in MESH[3,4])

@lru_cache(maxsize=16)
def exceptions(p,k):
 targets={s*r*k%p for s in (-1,1)for r in (1,3,pow(3,-1,p))}
 if p%12==1 and chi(k,p)==-1:return frozenset()
 return frozenset(x for x in range(1,p)if x*x%p in targets)

def rect_score(n,p):
 k=nonsquare(p) if p%12==1 else 1;a=(n-1)*pow(2,-1,p)%p
 def w(x):return 1+(n-1-x%p)//p
 return 2*(n-w(a))-2*(p-1)-sum(w(a+u)+w(a+k*pow(u,-1,p))-2 for u in exceptions(p,k))

def signed_colors(p,k):
 """Two-color the signed partner graph after the six quadratic exceptions of paper 38."""
 exc=exceptions(p,k);inv3=pow(3,-1,p)
 T={};sg=lambda x:min(x,p-x)
 for u in range(1,p//2+1):
  if u in T or u in exc:continue
  T[u]=0;todo=[u]
  while todo:
   a=todo.pop();v=k*pow(a,-1,p)%p
   for r in (1,3,inv3):
    b=sg(v*r%p)
    if b in exc:continue
    if b in T:
     if T[b]==T[a]:raise ArithmeticError('colouring conflict')
    else:T[b]=1-T[a];todo.append(b)
 return {a:T[sg(a)]for a in range(1,p)if a not in exc}

def rect(n,p):
 if not prime(p) or p<=3 or not 3*p<=n<=4*p:raise ValueError('require prime p>3 and 3p<=n<=4p')
 k=nonsquare(p) if p%12==1 else 1;T=signed_colors(p,k);a=(n-1)*pow(2,-1,p)%p;P=[]
 for u in range(1,p//2+1):
  if u not in T:continue
  x=(a+u)%p;y=(a+k*pow(u,-1,p))%p;w=1+(n-1-x)//p;h=1+(n-1-y)//p;M=MESH[w,h][(T[u]-x-y)%2]
  for i,j in M:
   X=x+i*p;Y=y+j*p;P.extend(((X,Y),(n-1-X,n-1-Y)))
 assert len(P)==rect_score(n,p) and len(P)>=2*n-2*p-42
 return k,P

def best_spec(n):
 """Score choices arithmetically before allocating the large coordinate lists."""
 if n<1:raise ValueError('n must be positive')
 options=[]
 if n%2:
  for p in range((n-1)//4,72,-1):
   if p%24==1 and prime(p):
    options.append((6*p+2,'odd anchored ring',p,4*p+1,None));break
 # Use a prime on each side of n/4, in all residue classes. Also try nearby 1 mod 12 primes (no exceptions).
 for special in (False,True):
  for direction in (-1,1):
   L=range((n+int(n%2))//4,4,-1)if direction<0 else range((n+3)//4,n//3+1)
   for p in L:
    if p<=3 or (special and p%12!=1) or not prime(p):continue
    m=min(n,4*p-int(n%2));
    if 3*p<=m:
     options.append((rect_score(m,p),'rectangular sheet masks',p,m,None));break
 if options and max(z[0]for z in options)>=max(n,4):return max(options,key=lambda z:z[0])
 # For small n compare the elementary circle fallback as well.
 # Small boards: a centred, no-three circle modulo a prime of the same square parity chart.
 # Its diameter is p-1 on odd boards and p-2 or p on even boards. Four corners are a fallback.
 if n==1:return 1,'singleton',None,1,(None,[(0,0)])
 best=('corners',None,None,[(0,0),(0,n-1),(n-1,0),(n-1,n-1)])
 for p in range(3,n+1,2):
  if not prime(p):continue
  # Largest centred block of side m<=p with n's parity (no residue repeats). Circle in doubled coordinates.
  m=p if n%2 else p-1;d=(n-m)//2;sets={}
  for x,y in product(range(m),repeat=2):
   k=((2*x-m+1)**2+(2*y-m+1)**2)%p
   if k:sets.setdefault(k,[]).append((x+d,y+d))
  k=max(sets,key=lambda k:len(sets[k]));P=sets[k]
  if len(P)>len(best[3]):best=('small centred circle',p,k,P)
 lab,p,k,L=best;return max(options+[(len(L),lab,p,n,(k,L))],key=lambda z:z[0])

def realize(n,spec):
 score,lab,p,m,small=spec
 if small is not None:k,P=small
 elif lab=='odd anchored ring':_,k,P=anchored(p)
 elif lab=='rectangular sheet masks':k,P=rect(m,p)
 elif lab=='classical embedded frame':
  k=1;h=(p-1)//2;P=[]
  for x in range(1,p):
   b=(h+pow(x,-1,p))%p
   for X in (x,x+p):
    for Y in (b,b+p):
     if not(h<X<=h+p and h<Y<=h+p):P.append((X,Y))
 else:raise ValueError('unknown construction')
 assert len(P)==score;d=(n-m)//2
 if d:
  for i,(x,y) in enumerate(P):P[i]=x+d,y+d
 return lab,p,k,P

def any_n(n):return realize(n,best_spec(n))

def ordinary_n(n):
 """Never worse than embedding the classical frame at the largest odd prime <= n/2."""
 best=best_spec(n)
 if not n%2 and n>1:
  z=best_spec(n-1)
  if z[0]>best[0]:best=z
 for p in range(n//2,2,-1):
  if not prime(p):continue
  if 3*(p-1)>best[0]:best=(3*(p-1),'classical embedded frame',p,2*p,None)
  break
 return realize(n,best)

def main():
 ap=argparse.ArgumentParser(description=__doc__);mode=ap.add_mutually_exclusive_group(required=True);mode.add_argument('--p',type=int);mode.add_argument('--n',type=int);ap.add_argument('--csv');ap.add_argument('--ordinary',action='store_true',help='for --n: allow breaking symmetry and compare with the classical prime embedding');z=ap.parse_args()
 if z.ordinary and z.p is not None:ap.error('--ordinary is for use with --n')
 if z.p is not None:p=z.p;n,k,P=anchored(p);lab='odd anchored ring'
 else:n=z.n;lab,p,k,P=(ordinary_n if z.ordinary else any_n)(n)
 S=set(P);half=all((n-1-x,n-1-y)in S for x,y in P);assert z.ordinary or half
 assert len(P)==len(S) and all(0<=x<n and 0<=y<n for x,y in P)
 print(f'n={n} p={p} k={k} points={len(P)} twice_surplus_over_1.5n={2*len(P)-3*n} half_turn={half} construction={lab}')
 if z.csv:
  with open(z.csv,'w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(sorted(P))
if __name__=='__main__':main()
