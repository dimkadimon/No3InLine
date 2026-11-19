#!/usr/bin/env python3
"""Reconstruct the precisely defined comparison B_ref(n); generate or compare paper tables.
No record or optimality hypothesis. Python >=3.9, standard library only. --write rebuilds outputs.
"""
from pathlib import Path
from math import isqrt
from functools import lru_cache
import argparse, bisect, csv, io, json, sys
if not __debug__:raise SystemExit("run without Python -O")
R=Path(__file__).resolve().parents[1]; L=R/'studies/larger-grids'; E=R/'studies/improvements'; S=R/'small-prime-examples'; M=R/'unbounded-gain'
# Selected actual witnesses, not an optimization over every possible crop of project data.
sides=[201,202,293,389,773,4037,10085,13445,16018,16805,32002,64006,131074,1000018,3188645]

def csv_count(path):
    with path.open() as f:
        h=next(f).strip();assert h=='x,y',path
        return sum(1 for line in f if line.strip())

def sieve(B):
    s=bytearray(b'\1')*(B+1);s[:2]=b'\0\0'
    for a in range(2,isqrt(B)+1):
        if s[a]:s[a*a::a]=b'\0'*((B-a*a)//a+1)
    return [i for i in range(2,B+1) if s[i]]
P=sieve(max(sides)//2+5000);P4=[p for p in P if p%12==1]
refs=json.loads((L/'experiments/seedindex.json').read_text());assert len(refs)==146 and {r['source'] for r in refs}=={'22v4'}
@lru_cache(None)
def samples(i):
    r=refs[i]; h,*z=(L/'experiments/seeds'/(r['id']+'.txt')).read_text().splitlines();s,k=map(int,h.split());assert (s,k)==(r['n'],r['points']);pts=[tuple(map(int,q.split())) for q in z];assert len(set(pts))==k
    return pts

def best_square(pts,m,n):
    # Enumerate all integer n-square windows inside [0,m)^2, including all possible axis-aligned crops.
    # For fixed left edge, scan the sorted y coordinates of points inside its horizontal span.
    best=(-1,0,0)
    for a in range(m-n+1):
        ys=sorted(y for x,y in pts if a<=x<a+n); i=j=0
        for b in range(m-n+1):
            while i<len(ys) and ys[i]<b:i+=1
            while j<len(ys) and ys[j]<b+n:j+=1
            if j-i>best[0]:best=(j-i,a,b)
    return best

CROPS={(int(r['side']),r['source_member']):tuple(int(r[k]) for k in ('points_in_crop','x0','y0')) for r in csv.DictReader((R/'results/p22-crops.csv').open())}
REPORTS=list(csv.DictReader((R/'results/forum-counts.csv').open()))

def audit_sources():
    # Validate all pinned source coordinates for the P22 bank, not just the winning crop.
    from math import gcd
    for i,r in enumerate(refs):
        points=samples(i);m=r['n'];assert all(0<=x<m and 0<=y<m for x,y in points)
        for j,(x,y) in enumerate(points):
            seen=set()
            for X,Y in points[j+1:]:
                a,b=X-x,Y-y;g=gcd(a,b);g=g if (a>0 or (a==0 and b>0)) else -g
                v=(a//g,b//g);assert v not in seen,(r['member'],j);seen.add(v)
        for n in sides:
            if n<m:assert best_square(points,m,n)==CROPS[n,r['member']]
    for p,m in ((8009,282),(16001,421),(32003,810)):
        header,*pairs=(E/'sources'/f'insertions_{p}.txt').read_text().splitlines();assert tuple(map(int,header.split()))==(p,m) and len(set(pairs))==m
    print('PASS all 146 P22 seed geometries and all window maxima; P47 versioned header counts.')

def benchmarks(n):
    # For the crop inequality |S|-4d the prime score increases to n/s, then decreases.
    cand=[]
    for pp,s,a,tag in [(P,2,3,'C'),(P4,4,6,'R')]:
        i=bisect.bisect_right(pp,n//s);assert 0<i<len(pp)
        for q in pp[i-1:i+1]:cand.append((a*(q-1)-4*max(s*q-n,0),tag,f'prime {q}, side {s*q}'))
    for i,r in enumerate(refs):
        m=r['n'];k=r['points'];a=b=0
        if n<m:k,a,b=CROPS[n,r['member']]
        cand.append((k,'K',f"22v4 {r['member']}; source side {m}; lower left ({a},{b})"))
    for z in REPORTS:
        m=int(z['side']); k=int(z['points']);cand.append((k-4*max(m-n,0),'F',f"{z['report']}; source side {m}, {k} points; ordinary square transfer"))
    for p,m in [(8009,282),(16001,421),(32003,810)]:
        cand.append((3*(p-1)+m-4*max(2*p-n,0),'S',f'47v1 section 8; prime {p}; source side {2*p}'))
    mx=max(c[0] for c in cand);bs=sorted(set(c for c in cand if c[0]==mx));return mx,[c for c in bs if c[1]!='F' or all(y[1]=='F' for y in bs)]

def project(n):
    small=json.loads((S/'examples.json').read_text());small={4*d['p']+1:d for d in small};A=[]
    f=E/'coordinates'/f'n{n}.csv'
    if f.exists(): A.append((csv_count(f),'Q' if n in (293,389) else 'H' if n in (4037,10085) else 'U',f.relative_to(R).as_posix()))
    if n in small:
        d=small[n];f=S/'coordinates'/f"p{d['p']}.csv";v=csv_count(f);assert v==d['points'];A.append((v,'H',f.relative_to(R).as_posix()))
    if n==4037:
        f=R/'studies/followup/data/augmented4037.csv';A.append((csv_count(f),'H',f.relative_to(R).as_posix()))
    if n in (201,202):
        f=L/'coordinates'/f'n{n}.csv';A.append((csv_count(f),'Q' if n==202 else 'U',f.relative_to(R).as_posix()))
    if n in (131074,1000018):
        f=L/'data'/f'edits_{n//2}.txt';h,*xy=f.read_text().splitlines();p,r,a=map(int,h.split());assert n==2*p and len(xy)==r+a;A.append((3*(p-1)-r+a,'U',f.relative_to(R).as_posix()))
    if n==3188645:
        f=M/'data/certificate.txt';p,k,m,nflip=map(int,f.read_text().splitlines()[0].split());assert n==4*p+1;A.append((6*(p-1)+8+2*m,'H',f.relative_to(R).as_posix()))
    return max(A,key=lambda q:q[0])

def fmt(i): return f'{i:,}'.replace(',',r'\,')
def go(write):
    of=io.StringIO(newline='');w=csv.writer(of,lineterminator='\n');w.writerow(['n','B_ref','source_codes','benchmark_details','certified_count','symmetry','delta_vs_ref','excess_vs_1.5n','certificate_or_coordinates']);panels={'ring':[],'other':[]}
    for n in sides:
        v,tag,path=project(n);mx,bs=benchmarks(n);c=','.join(sorted(set(b[1] for b in bs)));delta=v-mx;sur=2*v-3*n;ex=(str(sur//2) if not sur%2 else f'{sur//2}.5');w.writerow((n,mx,c,' | '.join(b[2] for b in bs),v,tag,delta,ex,path));fmt_ex=fmt(sur//2)+('.5' if sur%2 else '')
        row=f"{fmt(n)} & {fmt(mx)} & {c} & {fmt(v)} & {tag} & ${' +' if delta>0 else ''}{fmt(delta)}$ & $+{fmt_ex}$ "+r'\\';panels['ring' if n in (293,389,773,4037,10085,13445,16805,3188645) else 'other'].append(row)
    out={R/'results/lower-bounds.csv':of.getvalue()}
    # The compact replay ZIP stores these table fragments as plain text (no TeX inputs in the ancillary kit).
    tabdir=R/'paper'; ext='tex' if (tabdir/'main.tex').is_file() else 'txt'
    out.update({tabdir/f'table-{key}.{ext}':'% Generated by scripts/comparison.py; do not edit by hand.\n'+'\n'.join(rows)+'\n' for key,rows in panels.items()})
    for f,s in out.items():
        if write:f.write_text(s)
        elif s!=f.read_text():raise ValueError(f'comparison changed: {f}')
    print('PASS counts and benchmark provenance for all',len(sides),'sides.' )
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');ap.add_argument('--audit-sources',action='store_true',help='recheck all P22 points and crop counts; requires restore_inputs.py first');opts=ap.parse_args()
    if opts.audit_sources:audit_sources()
    go(opts.write)
