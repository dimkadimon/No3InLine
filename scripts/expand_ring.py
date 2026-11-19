#!/usr/bin/env python3
"""Write the sorted x,y CSV specified by an anchored-ring certificate, without storing millions of sites.
This is a coordinate exporter, not a collinearity checker. Refuses to overwrite a file.
"""
from collections import defaultdict
from pathlib import Path
from math import isqrt
import argparse

def expand(cert,dest):
    it=iter(map(int,cert.read_text().split()));p,k,m,nf=(next(it) for _ in range(4))
    if not (p>2 and all(p%d for d in range(2,isqrt(p)+1)) and 0<k<p and pow(k,(p-1)//2,p)==p-1 and min(m,nf)>=0):raise ValueError('invalid parameters')
    reps=[(next(it),next(it)) for _ in range(m)];bits=[next(it) for _ in range(nf)]
    if next(it,None) is not None:raise ValueError('trailing data')
    allspecial=[(x*p,y*p) for x,y in [(0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4)]]+reps+[(4*p-x,4*p-y) for x,y in reps];special=defaultdict(list)
    if len(allspecial)!=len(set(allspecial)):raise ValueError('repeated site')
    for x,y in allspecial:
        if not (0<=min(x,y)<=max(x,y)<=4*p and x*y%p!=k):raise ValueError('off-board or on-carrier special site')
        special[x].append(y)
    flipped=set()
    for seed in bits:
        if not 0<seed<p or seed in flipped:raise ValueError('invalid or repeated bit')
        stack=[seed];comp={seed}
        while stack:
            t=stack.pop()
            for v in (-t%p,3*t%p,k*pow(t,-1,p)%p):
                if v not in comp:comp.add(v);stack.append(v)
        if min(comp)!=seed:raise ValueError('bit not the minimum of its component')
        flipped.update(comp)
    square=bytearray(p)
    for a in range(1,p):square[a*a%p]=1
    total=0
    with dest.open('x',newline='\n') as f:
        f.write('x,y\n')
        for x in range(4*p+1):
            i,u=divmod(x,p);ys=list(special.get(x,()))
            if u:
                v=k*pow(u,-1,p)%p;colour=(not square[u])^(u in flipped)
                for j in ((0,1,2,3) if i in (0,3) else (0,3)):
                    y=v+j*p
                    if (x+y)%2==colour:ys.append(y)
            for y in sorted(ys):f.write(f'{x},{y}\n')
            total+=len(ys)
    if total!=6*(p-1)+8+2*m:raise ValueError('cardinality')
    print(f'Expanded p={p}, side={4*p+1}, {total} points, zero-based, sorted by (x,y).')
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('certificate',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args();expand(args.certificate,args.output)
