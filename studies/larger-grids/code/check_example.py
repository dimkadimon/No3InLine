#!/usr/bin/env python3
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];d=json.loads((R/'data/example-exchange.json').read_text());p=d['p'];h=p//2
S={(x,y)for a in range(1,p)for b in [(pow(a,-1,p)+h)%p]for x in(a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)}
S.update(tuple(map(int,l.split())) for l in (R/f'inputs/insertions_{p}.txt').read_text().splitlines()[1:]);r=tuple(d['remove']);Add=list(map(tuple,d['insert']));assert r in S and len(S)==24306
for (x,y),s in zip(Add,map(tuple,d['other_blocking_endpoints'])):
 dirs={};block=[]
 for a,b in S:
  dx=a-x;dy=b-y;g=math.gcd(dx,dy);assert g>0
  if dx<0 or dx==0 and dy<0:g=-g
  key=dx//g,dy//g
  if key in dirs:block.append({dirs[key],(a,b)})
  dirs[key]=a,b
 assert block==[{r,s}]
(a,b),(x,y)=Add
assert not any((a-x)*(v-y)==(b-y)*(u-x)for u,v in S-{r});print('VERIFIED one-for-two example, 24306 -> 24307')
