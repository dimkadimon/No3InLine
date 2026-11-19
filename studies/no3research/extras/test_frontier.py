#!/usr/bin/env python3
"""Regression of repair_barrier.cpp against all near-full row patterns on 3-, 4-, and 5-boards."""
from itertools import combinations
from pathlib import Path
import subprocess,tempfile,re,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from verify import dec

def validate(W):
    S=dec(W[1:]);n=len(W)//2+1; best=len(S)+1; cols=[0]*n;points=[]
    def row(y,d):
        nonlocal best
        if y==n:
            if d==1:best=min(best,len(S-set(points)))
            return
        for k in ((2,1) if not d else (2,)):
            for choice in combinations([x for x in range(n) if cols[x]<2],k):
                old=len(points);ok=True
                for x in choice:
                    if any((u-x)*(b-y)==(v-y)*(a-x) for (u,v),(a,b) in combinations(points,2)):
                        ok=False;break
                    points.append((x,y))
                if ok:
                    for x in choice:cols[x]+=1
                    row(y+1,d+int(k==1))
                    for x in choice:cols[x]-=1
                del points[old:]
    row(0,0);return best

def main():
    # Full 2n-point seeds directly enumerated in the small catalogue.
    words=['*0101','x010212','*12030312']
    with tempfile.TemporaryDirectory() as d:
        exe=str(Path(d)/'b');subprocess.run(['c++','-O2','-std=c++17',str(ROOT/'extras/repair_barrier.cpp'),'-o',exe],check=True)
        for w in words:
            want=validate(w)
            for k in range(5):
                out=subprocess.check_output([exe,str(k)],input=w+'\n',text=True)
                hits=int(re.search(r' hits=(\d+)',out)[1]);assert bool(hits)==(k>=want),(w,k,want,hits)
            print('seed',w,': direct minimum removals =',want,'; decisions agree at budgets 0 through 4')
if __name__=='__main__':main()
