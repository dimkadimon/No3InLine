#!/usr/bin/env python3
"""Exhaustively fill deficient rows of the exceptional surviving cores from core_obstruction/core_lines.
Input is a text file of 'solution' rows in doubled centred coordinates (or directory instructions in README).
No group assumption on the completions. Geometry by integer determinants. Default: check the stored record.
"""
from pathlib import Path
from itertools import combinations
import argparse
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from verify import expand,check,augmentable

def completions(P,n):
    # Every remaining candidate is individually valid relative to the whole core.
    A=augmentable(P,n); original=list(P); xcnt=[0]*n;ycnt=[0]*n
    for x,y in original:xcnt[x]+=1;ycnt[y]+=1
    row={y:sorted(x for x,b in A if b==y) for y in range(n) if ycnt[y]<2}
    # The fixed order affects speed, not which row patterns are generated.
    layers=sorted(row,key=lambda y:(len(row[y])-(2-ycnt[y]),y))
    placed=[];found=nodes=0
    def valid_new(q):
        x,y=q
        # A triple newly caused by q either used two core sites (already checked),
        # one core and one earlier addition, or two earlier additions.
        for i,(a,b) in enumerate(placed):
            dx=x-a;dy=y-b
            for c,d in original:
                if dx*(d-b)==dy*(c-a):return False
            for c,d in placed[:i]:
                if dx*(d-b)==dy*(c-a):return False
        return True
    def search(i):
        nonlocal found,nodes
        nodes+=1
        if i==len(layers):
            check(P|set(placed),n,2*n);found+=1;return
        y=layers[i];xs=[x for x in row[y] if xcnt[x]<2 and valid_new((x,y))]
        for choice in combinations(xs,2-ycnt[y]):
            # A pair added together lies on this fresh row and then there is no old point there.
            for x in choice:placed.append((x,y));xcnt[x]+=1
            search(i+1)
            for x in reversed(choice):placed.pop();xcnt[x]-=1
    search(0);return found,nodes

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('files',nargs='*',type=Path);ap.add_argument('--n',type=int,default=47)
    args=ap.parse_args();n=args.n
    files=args.files or [ROOT/'data/core47-residual.txt']
    # Positive regression: the 3-board axial cross has exactly two labelled completions.
    if completions(expand(3,[(0,1)]),3)[0]!=2:raise ValueError('positive regression failed')
    counts={};seen=set()
    for f in files:
        for l in f.read_text().splitlines():
            if not l.startswith('solution '):continue
            reps=tuple(sorted(tuple(int(t)//2 for t in w.split(',')) for w in l.split()[1:]));P=expand(n,reps)
            if reps in seen:raise ValueError('repeated survivor');
            seen.add(reps);check(P,n,len(P));num,nodes=completions(P,n)
            row=counts.setdefault(len(P),[0,0,0]);row[0]+=1;row[1]+=num;row[2]+=nodes
    for sz,(ncores,comps,nodes) in sorted(counts.items(),reverse=True):
        print(f'n={n} core_size={sz} surviving_cores={ncores} completions={comps} row_search_nodes={nodes}')
    if not args.files and (not counts or any(z[1] for z in counts.values())):raise ValueError('unexpected default result')
if __name__=='__main__':main()
