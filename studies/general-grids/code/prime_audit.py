"""Produce/check the finite part of the p=1 mod 24 extension. Offline, no third-party packages."""
import argparse,csv,math
from pathlib import Path
from anchor_ring import prime,chi,nonsquare,base_level,finite_rays,high_odd_tests
R=Path(__file__).resolve().parents[1]
def audit():
 for p in range(73,50626,24):
  if not prime(p):continue
  tests=high_odd_tests(p);bound=math.prod(5 if h==5 else 3 for _,h in tests);assert bound<=50625
  if p>bound:continue
  k=base_level(p);assert finite_rays(p,k)
  sq={r*r%p:r for r in range(1,p//2+1)};good=all(sq[k*pow(d,-1,p)%p]*h < (h-4)*p for d,h in tests)
  yield p,k,bound,'small roots' if good else 'boundary ray certificate'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();A=list(audit());path=R/'data/prime-certificates.csv';fields=['p','level','box_bound','certificate'];
 if args.write:
  with path.open('w',newline='')as f:w=csv.writer(f);w.writerow(fields);w.writerows(A)
 else:
  with path.open()as f:r=csv.reader(f);assert next(r)==fields;assert list(r)==[[str(a)for a in row]for row in A]
 print(f'PASS: exceptional branch has {len(A)} primes; small-root witnesses={sum(a[-1]=="small roots"for a in A)}; direct ray certificates={sum(a[-1]!="small roots"for a in A)}; largest prime tested in branch={A[-1][0]}')
