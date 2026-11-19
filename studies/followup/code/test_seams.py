"""Generate cases for the independent integer-direction checker, including both parity regimes."""
from seam_caps import construction,prime,mask,FAMILY
from itertools import product
import sys

def finite_table():
 flat=frozenset([(3,1),(3,-1)]);tall=frozenset([(1,3),(1,-3)])
 for w,h in product([3,4],repeat=2):
  target=w+h-2
  for t in (0,1):
   assert len(mask(w,h,t))>=target and len(mask(w,h,t,flat))>=target-1 and len(mask(w,h,t,tall))>=target-1 and len(mask(w,h,t,flat|tall))>=target-2
  if w==h:
   for S in (flat,tall):assert len(mask(w,h,int(w==4),S|{(1,1)}))>=w
if __name__=='__main__':
 finite_table();cases=0
 for p in range(5,48):
  if not prime(p):continue
  for n in range(3*p,4*p+1):
   for s in (False,True):
    P,A=construction(p,n,s);assert len(P)>=2*n-2*p-16;print(n,len(P));print('\n'.join(f'{x} {y}'for x,y in P));cases+=1
 for p in (53,61,71,97,101,107,193,241,337,997):
  for n in (4*p-3,4*p-4,3*p+1,3*p+2):
   P,A=construction(p,n);print(n,len(P));print('\n'.join(f'{x} {y}'for x,y in P));cases+=1
 print(f'Generated {cases} cases. Four template inequalities and the square repair template checked.',file=sys.stderr)
