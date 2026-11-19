"""Check all finite chart exceptions without using the construction or its scale finder.
For every remaining small-board exception stream its literal coordinates to a generic geometry checker."""
from pathlib import Path
from math import isqrt
import csv,sys
R=Path(__file__).resolve().parents[1];need={};tested=0;miss=0
for p in range(5,2025):
 if any(p%v==0 for v in range(2,isqrt(p)+1))or p%12==1:continue
 even=p%4==1;H={min(pow(3,i,p),p-pow(3,i,p))for i in range(p-1)};roots=[z for z in range(1,p) if z*z%p in((p-1,)if even else(3,p-3))];assert len(roots)==2
 for d in range(min(18,p)+1):
  n=4*p-d;tested+=1;b=(n-1)%2
  Z=[j for j in range(d+1,2*p-d,2)if d<3*j<2*p-d and(even or 2*p+d<9*j<4*p-d)]
  W={j%p for j in range(d+1,2*p-d,2)if d<3*j<2*p-d};assert all(j%2==b for j in Z)
  if len(H)>=(4 if even else 5)and any(r*z%p in W for z in Z for r in roots):continue
  miss+=1;need[n]=max(need.get(n,0),2*n-2*p-(4 if n%2 else 6)-(4 if even else 6))
for n,k in sorted(need.items()):
 with (R/'data'/'small'/f'n{n}.csv').open()as f:P=list(csv.DictReader(f));assert len(P)>=k
 print(n,len(P));print('\n'.join(q['x']+' '+q['y']for q in P))
print(f'Finite branch: {tested} prime/side pairs; {miss} exceptions on {len(need)} distinct boards, all meeting their maximum required count.',file=sys.stderr)
