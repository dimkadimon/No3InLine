#!/usr/bin/env python3
"""Independent audit of the finite exception table; does not import the search/generator."""
from pathlib import Path
import csv,math,itertools
R=Path(__file__).resolve().parents[1]
N=50625;isprime=bytearray(b'\1')*(N+1);isprime[0:2]=b'\0\0'
for a in range(2,math.isqrt(N)+1):
 if isprime[a]:isprime[a*a::a]=b'\0'*((N-a*a)//a+1)
records={}
for row in csv.DictReader((R/'data/prime-certificates.csv').read_text().splitlines()):
 p=int(row['p']);assert p not in records;records[p]=int(row['level'])
used=set();small=direct=0
def direction(dx,dy):
 g=math.gcd(dx,dy);assert g
 if dx<0 or dx==0 and dy<0:g=-g
 return dx//g,dy//g
for p in range(2,N+1):
 if not isprime[p]or p%24!=1:continue
 neg=lambda d:pow(d%p,(p-1)//2,p)==p-1
 # Box factors for +/-5,+/-15; +/-7,+/-21; +/-35.
 H=[(d,h)for s in (-1,1)for v,h in [(5,5),(15,5),(7,7),(21,7),(35,7)]for d in [s*v]if neg(d)]
 B=math.prod(5 if h==5 else 3 for _,h in H);assert B<=50625
 if p>B:continue
 used.add(p);k=records[p];assert neg(k);root={v*v%p:v for v in range(1,p//2+1)}
 if all(h*root[k*pow(d,-1,p)%p]<(h-4)*p for d,h in H):small+=1;continue
 # Direct check for rare small primes: enumerate all physically selected old points independently.
 old=[]
 for x in range(1,4*p):
  if not x%p:continue
  b=k*pow(x,-1,p)%p
  for y in range(b,4*p,p):
   if p<x<3*p and p<y<3*p:continue
   if (x+y)%2==int(neg(x)):old.append((x,y))
 assert len(old)==6*(p-1)
 border=[(p*x,p*y)for x,y in itertools.product(range(5),repeat=2)if (x in (0,4)) != (y in (0,4))]
 for x,y in border:
  dirs={direction(a-x,b-y) for a,b in old};assert len(dirs)==len(old)
  for u,v in border:
   if (u,v)!=(x,y):assert direction(u-x,v-y)not in dirs
 direct+=1
assert used==set(records)
print(f'PASS: independently enumerated {len(used)} moduli requiring finite witnesses; {small} certified by least roots, {direct} by complete old-point scans over all 12 open-side anchors.')
