"""Mundane small-side controls from Achim Flammenkamp's published no-three-in-line database.
Source: https://wwwhomes.uni-bielefeld.de/achim/no3in/download/all_known_solutions
One full-size word per represented side, preferring board-centred half-turn symmetry.
The original initial character labels the source symmetry; later characters encode two columns per row.
None are claimed as discoveries in this project."""
from pathlib import Path
from functools import lru_cache
from math import gcd
import csv
D=Path(__file__).resolve().parents[1];ALPH='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,.'
@lru_cache(None)
def records():
 with (D/'sources'/'catalogue-examples.csv').open()as f:return [(int(r['n']),int(r['points']),bool(int(r['half_turn'])),r['original_word'])for r in csv.DictReader(f)]
def decode(word):return [(ALPH.index(t),i//2)for i,t in enumerate(word[1:])]
def audit():
 for n,k,ht,word in records():
  P=decode(word);S=set(P);assert len(S)==len(P)==k==2*n and all(0<=x<n and 0<=y<n for x,y in S);assert ht==all((n-1-x,n-1-y)in S for x,y in S)
  for x,y in P:
   ds=set()
   for a,b in P:
    u=a-x;v=b-y
    if u or v:
     h=gcd(u,v);h=h if(u>0 or not u and v>0)else -h;ds.add((u//h,v//h))
   assert len(ds)==k-1
 print(f'PASS {len(records())} public 2n-point catalogue controls, with actual centre symmetries.',flush=True)
if __name__=='__main__':audit()
