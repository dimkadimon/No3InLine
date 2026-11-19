#!/usr/bin/env python3
"""Reconstruct seven sets from compact parameters, compare exact CSVs, check all lines."""
from pathlib import Path
from math import gcd
from tempfile import TemporaryDirectory
from subprocess import run
import csv,json,os,sys
D=Path(__file__).resolve().parent
A=((0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4))
ALPH='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,.'

def ring(p,k,flips):
    flips=set(flips);lab={}
    for u in range(1,p):
        if u in lab:continue
        lab[u]=u;todo=[u]
        while todo:
            a=todo.pop()
            for b in (-a%p,3*a%p,k*pow(a,-1,p)%p):
                if b not in lab:lab[b]=u;todo.append(b)
    assert flips<=set(lab.values());S=[]
    for u in range(1,p):
        v=k*pow(u,-1,p)%p;par=(pow(u,(p-1)//2,p)!=1)^(lab[u] in flips)
        for i in range(4):
            for j in range(4):
                x=u+i*p;y=v+j*p
                if (i in (0,3) or j in (0,3)) and (x+y)%2==par:S.append((x,y))
    assert len(S)==6*(p-1)
    return S

def all_lines(S):
    for x,y in S:
        seen=set()
        for X,Y in S:
            if (X,Y)==(x,y):continue
            a,b=X-x,Y-y;g=gcd(a,b)
            if a<0 or (a==0 and b<0):g=-g
            v=(a//g,b//g);assert v not in seen,(x,y,v);seen.add(v)

def read(path):return [tuple(map(int,(r['x'],r['y']))) for r in csv.DictReader(path.open())]

def main():
    records=json.loads((D/'examples.json').read_text());large=[]
    for d in records:
        p=d['p'];t=4*p;S=read(D/'coordinates'/f'p{p}.csv');P=set(S);assert len(P)==len(S)==d['points'];assert all(0<=x<=t and 0<=y<=t and (t-x,t-y) in P for x,y in S)
        if p==5:U=[(ALPH.index(a),i//2) for i,a in enumerate(d['word'][1:])]
        else:
            k=d['k'];reps=list(map(tuple,d['representatives']));U=ring(p,k,d['flips'])+[(a*p,b*p) for a,b in A]+reps+[(t-x,t-y) for x,y in reps]
            c=(D/'certificates'/f'p{p}.txt').read_text().split();assert list(map(int,c))==[p,k,len(reps),len(d['flips'])]+[a for pt in reps for a in pt]+d['flips']
        assert sorted(U)==sorted(S),(p,'certificate and CSV differ')
        if p<840:all_lines(S);print(f'p={p} side={t+1} points={len(S)} all-direction check from every point: PASS',flush=True)
        else:large.append(p)
    with TemporaryDirectory() as w:
        exe=Path(w)/'check';run([os.environ.get('CXX','c++'),'-O3','-std=c++17',str(D/'check_ring.cpp'),'-o',str(exe)],check=True)
        for p in large:
            with (D/'certificates'/f'p{p}.txt').open() as f:run([exe],stdin=f,check=True)
    print('Seven CSV coordinate lists, certificates, rotation closure and exact geometry: PASS')
if __name__=='__main__':main()
