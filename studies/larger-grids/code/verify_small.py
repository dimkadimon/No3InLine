#!/usr/bin/env python3
"""Determinant verification of the 201-, 202-, 67- and 69-board geometry, independent of all searches."""
import csv,json,sys
from pathlib import Path
from itertools import combinations
from math import comb
R=Path(__file__).resolve().parents[1]
def data(file):
 with (R/'coordinates'/file).open()as f:return [(int(t['x']),int(t['y'])) for t in csv.DictReader(f)]
def check(P,n,k):
 if not(len(P)==len(set(P))==k and all(0<=x<n and 0<=y<n for x,y in P)):raise ValueError('coordinates/cardinality')
 for (x,y),(u,v),(a,b) in combinations(P,3):
  if (u-x)*(b-y)==(v-y)*(a-x):raise ValueError(f'collinear at order {n}')
 print(f'VERIFIED n={n} points={k} exact_determinants={comb(k,3)}')
def main():
 f=(R/'inputs/n200_c_zero_based.txt').read_text().splitlines();_,k=map(int,f[0].split());S={tuple(map(int,l.split())) for l in f[1:]};assert len(S)==k==360
 for n,k in ((201,362),(202,364)):
  e=json.loads((R/f'data/extension-n{n}.json').read_text());A=S|{tuple(q) for q in e['added_in_source_frame']};P=data(f'n{n}.csv');assert {(x+e['dx'],y+e['dy'])for x,y in A}==set(P);check(P,n,k)
  if n==202:assert {(n-1-y,x) for x,y in P}==set(P)
 reps=json.loads((R/'data/d4-n67.json').read_text())['centered_representatives'];
 for n in (67,69):
  P=data(f'd4-n{n}.csv');m=n//2;assert set(P)=={(m+i*u,m+j*v)for a,b in reps for u,v in ((a,b),(b,a))for i in (-1,1)for j in (-1,1)};check(P,n,128)
if __name__=='__main__':main()
