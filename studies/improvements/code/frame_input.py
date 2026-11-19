"""Frame and search pool from the earlier archive. Not used to certify feasibility."""
import sys
from pathlib import Path
p=int(sys.argv[1]);depth=int(sys.argv[2]);L=Path(__file__).resolve().parents[1]/'sources';h=p//2;n=2*p
O={(x,y)for a in range(1,p)for b in [(h+pow(a,-1,p))%p]for x in(a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)}
raw=(L/f'edits_{p}.txt').read_text().splitlines();_,r,ad=map(int,raw[0].split());
if len(sys.argv)>3:raw=Path(sys.argv[3]).read_text().splitlines();_,r,ad=map(int,raw[0].split())
P=[tuple(map(int,l.split()))for l in raw[1:]];R=set(P[:r]);A=set(P[r:]);F=O-R|A
Q={(x,y)for x,y,d in(map(int,l.split())for l in (L/f'scan{p}.dat').read_text().splitlines())if d<=depth}|A;Q-=O
if len(sys.argv)>4:Q|={tuple(map(int,l.split()))for l in Path(sys.argv[4]).read_text().splitlines()}-O
print(n,len(O),len(Q));print('\n'.join(f'{x} {y} {int((x,y)in F)}'for S in (sorted(O),sorted(Q))for x,y in S))
