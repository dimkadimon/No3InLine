#!/usr/bin/env python3
"""Finite diagnostic tests of the R2 counting lemmas. Not a proof of any asymptotic inequality.
All examples are enumerated with integer/rational arithmetic; no external inputs or packages.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import gcd
import sys
if not __debug__:sys.exit('Do not run with -O.')

def signs():
    small={F(u,v) for v in range(2,9) for u in range(1,v) if gcd(u,v)==1};assert len(small)==21
    low={((1-t)/(1+t))**2 for t in small};ratios=low|{1/t for t in low}
    direct={F(r-s,r+s)**2 for r,s in product(range(-8,9),repeat=2) if r*s and r not in (s,-s)};assert direct==ratios and len(direct)==42
    slopes={(a,b) for a in range(1,9) for b in range(-8,9) if b and gcd(a,b)==1}
    polys={(-F(b,4*a),F(1,2),-F(a,4*b)) for a,b in slopes}|{(0,t,0) for t in ({0,1}|ratios)};assert len(polys)==130
    print('PASS: 21 proper reduced fractions, 86 signed slopes, 42 ratio shifts; 130 distinct rational coefficient triples (88 negative, 42 positive signs of the level).')

def gcd_rows():
    p=13;H=4*p;pool=defaultdict(list);seen=[0]*4
    for a,b,t,u in product(range(1,4),range(-3,4),range(-4,5),range(-4,5)):
        if gcd(a,b)==1 and b*t*u and t!=u:pool[a*b*t*u%p].append((a,b,t,u))
    for v in pool.values():
        for (a,b,t,u),(c,d,s,w) in product(v,repeat=2):
            gs=[gcd(a,c),gcd(b,d),gcd(u,s),gcd(t,w)];prod1=a*b*t*u;prod2=c*d*s*w
            for row,g in enumerate(gs):
                for l in range(2,g+1):
                    if g%l:continue
                    if row==0:i,j,ip,jp=(a//l)*t,b*u,(c//l)*s,d*w
                    elif row==1:i,j,ip,jp=(b//l)*t,a*u,(d//l)*s,c*w
                    elif row==2:i,j,ip,jp=a*(u//l),b*t,c*(s//l),d*w
                    else:i,j,ip,jp=a*(t//l),b*u,c*(w//l),d*s
                    assert l*i*j==prod1 and l*ip*jp==prod2 and (i*j-ip*jp)%p==0 and (i*j*ip*jp)%p!=0
                    assert 0<max(abs(i),abs(ip))*l<=H and 0<max(abs(j),abs(jp))<=H;seen[row]+=1
    assert all(seen);print('PASS: signed product-cancellation incidences for the four gcd rows:',*seen)

def rectangles():
    cases=0
    for p in (5,7,11,13,17,19):
        for S,T in product(range(1,10),repeat=2):
            counts=defaultdict(list)
            for a,b in product(range(-S,S+1),range(-T,T+1)):
                if a*b%p:counts[b*pow(a,-1,p)%p].append((a,b))
            for c in range(1,p):
                for G in (1,2,3,4):
                    n=sum(gcd(a,b)<=G for a,b in counts[c]);assert p*n<=2*p*G+26*S*T;cases+=1
                dirs={(a,b) for a,b in counts[c] if a>0 and gcd(a,b)==1}
                if 2*S*T<p:assert len(dirs)<=1
    assert (1* -1-2*3)==-7 and 2*3<7 and (-1-2*3)%7==0
    print('PASS:',cases,'rectangle/ratio/gcd cases. At p=7, S=2, T=3 the different directions (1,3),(2,-1) share one residue slope although ST<p.')

def cross(p):
    # Directly enumerate roots, recording the actual level at each designated abscissa U.
    gs=[]
    for a,b,t,u in product((1,2),range(1,p),range(1,p),range(1,p)):
        if t==u:continue
        levels={}
        for x,y in product(range(p),repeat=2):
            U=(x+a*t)%p;k=U*(y+b*t)%p
            if k and k==(x+a*u)*(y+b*u)%p:
                assert U not in levels;levels[U]=k
        gs.append((a,b,u-t,levels))
    exc=ordinary=impossible=0
    for (a,b,D,v),(A,B,d,w) in product(gs,repeat=2):
        es=[]
        for e in range(1,p):
            l=(b*pow(a,-1,p)-e*e*B*pow(A,-1,p))%p;r=(e*B*d-b*D)%p
            actual={U for U,k in v.items() if w.get(e*U%p)==k}
            if not l and not r:
                es.append(e);assert len(actual)==p-2;exc+=1
            elif l:
                assert actual<={r*pow(l,-1,p)%p};ordinary+=1
            else:assert not actual;impossible+=1
        inv=(a*b*D*D-A*B*d*d)%p
        assert es==([b*D*pow(B*d,-1,p)%p] if inv==0 else [])
    print(f'PASS: p={p}, {len(gs)} marked templates, {ordinary} nonsingular, {impossible} inconsistent and {exc} exceptional pair/ratio systems; direct root enumeration agrees.')
if __name__=='__main__':
    signs();gcd_rows();rectangles();cross(5);cross(7)
