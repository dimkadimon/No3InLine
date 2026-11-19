"""Expand a selected restricted model to CSV or to modular-frame edits. Used only in discovery."""
from array import array
from pathlib import Path
import csv,sys

def parse(path):
 with open(path,'rb')as f:
  a=array('i');a.fromfile(f,2);n,k=a;a=array('i');a.fromfile(f,k*3);return n,[tuple(a[i:i+3])for i in range(0,3*k,3)]
if __name__=='__main__':
 model,ids,out=sys.argv[1:4];n,V=parse(model);I={int(l)for l in Path(ids).read_text().splitlines()};S={(V[j][0],V[j][1])for j in I};out=Path(out)
 if n%2:
  S|={(n-1-x,n-1-y)for x,y in list(S)}
 if out.suffix=='.csv':
  with out.open('w',newline='')as f:w=csv.writer(f);w.writerow(('x','y'));w.writerows(sorted(S))
 else:
  p=n//2;h=p//2;O={(x,y)for a in range(1,p)for b in[(h+pow(a,-1,p))%p]for x in(a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)};R=O-S;A=S-O
  out.write_text(f'{p} {len(R)} {len(A)}\n'+''.join(f'{x} {y}\n'for x,y in sorted(R))+''.join(f'{x} {y}\n'for x,y in sorted(A)))
 print('n',n,'points',len(S),out)
