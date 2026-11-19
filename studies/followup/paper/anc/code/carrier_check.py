"""Geometric cross-check for larger instances: no mask/colour/exception logic is used by check()."""
from math import gcd,isqrt
from collections import Counter
from seam_caps import construction,prime

def check(P,p,n,k):
 a=((n-1)*((p+1)//2))%p;B=set(P);assert len(B)==len(P)
 assert all(0<=x<n and 0<=y<n and (x-a)*(y-a)%p==k and (n-1-x,n-1-y)in B for x,y in P)
 assert n<=4*p
 for dx in range(4):
  for dy in range(-3,4):
   if not(dx>0 or dy>0) or gcd(dx,dy)!=1:continue
   C=Counter(dy*x-dx*y for x,y in P);assert max(C.values())<=2
if __name__=='__main__':
 import sys
 cases=[(5003,17712),(5003,17711),(5009,17728),(5009,17727),(2003,8012),(2003,8011),(2017,8068),(241,964)]
 for p,n in cases:
  assert prime(p);P,A=construction(p,n);check(P,p,n,A['c']);print(A,'d>=32sqrt(p)',(4*p-n)**2>=1024*p,'PASS')
