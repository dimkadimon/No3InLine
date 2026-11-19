#!/usr/bin/env python3
"""Offline verification of every project count W in the manuscript, independent of upstream downloads.
Python >=3.9; C++17, a few hundred MB of RAM. No solver or third-party Python packages.
--hashes-only verifies the release manifest without compiling. --expand-large also writes the two omitted legacy CSVs.
"""
import argparse, csv, filecmp, hashlib, os, shlex, shutil, subprocess, sys
from math import gcd
from pathlib import Path
from tempfile import TemporaryDirectory
R=Path(__file__).resolve().parents[1];E=R/'studies/improvements';L=R/'studies/larger-grids';U=R/'unbounded-gain';S=R/'small-prime-examples';P=sys.executable
if not __debug__:sys.exit('Do not use python -O; the verification scripts use assertions.')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
def h(f):
    a=hashlib.sha256()
    with f.open('rb') as q:
        for z in iter(lambda:q.read(1048576),b''):a.update(z)
    return a.hexdigest()
def lines(f):
    return dict((path,sha) for sha,path in (line.split('  ',1) for line in f.read_text().splitlines()))
def hashes():
    m=lines(R/'MANIFEST.sha256')
    for name,sha in m.items():assert h(R/name)==sha,name
    print('PASS release manifest:',len(m),'files',flush=True)
def run(args,**kw):return subprocess.run([str(x) for x in args],check=True,**kw)
def pts(f):
    with f.open() as q:return [(int(r['x']),int(r['y'])) for r in csv.DictReader(q)]
def medium(n,k):
    p=pts(L/'coordinates'/f'n{n}.csv');s=set(p);assert len(s)==len(p)==k and all(0<=x<n and 0<=y<n for x,y in p)
    if n==202:assert all((n-1-y,x) in s for x,y in p)
    for i,(x,y) in enumerate(p):
        seen=set()
        for X,Y in p[i+1:]:
            a,b=X-x,Y-y;d=gcd(a,b);d=d if (a>0 or (a==0 and b>0)) else -d;v=a//d,b//d;assert v not in seen,(n,i,v);seen.add(v)
    print('PASS unrestricted integer directions for medium witness',n,k,flush=True)
def build(src,dest):run(shlex.split(os.environ.get('CXX','c++'))+['-std=c++17','-O3',src,'-o',dest]);return dest
def check_all(expand):
    run([P,R/'scripts/comparison.py']); counts={int(z['n']):int(z['certified_count']) for z in csv.DictReader((R/'results/lower-bounds.csv').open())}
    for n in (201,202):medium(n,counts[n])
    run([P,S/'verify.py']);run([P,U/'code/sample_root.py']);run([P,U/'code/check_identities.py'])
    with TemporaryDirectory() as td:
        t=Path(td);matcher=build(U/'code/match_example.cpp',t/'match');verify=build(U/'code/verify_example.cpp',t/'ring')
        with (t/'cert').open('wb') as a,(t/'match.txt').open('wb') as b:run([matcher],stdout=a,stderr=b)
        assert filecmp.cmp(t/'cert',U/'data/certificate.txt',shallow=False) and filecmp.cmp(t/'match.txt',U/'data/matching.txt',shallow=False)
        print((t/'match.txt').read_text(),end='',flush=True)
        with (t/'cert').open('rb') as f:res=run([verify],stdin=f,capture_output=True).stdout
        assert res==(U/'data/verification.txt').read_bytes() and f"total={counts[3188645]}\n".encode() in res;print(res.decode(),end='',flush=True)
        dirs=build(E/'code/check_stream.cpp',t/'dirs')
        with (t/'sets').open('w') as out:
            for n in (293,389,4037,10085):
                a=pts(E/'coordinates'/f'n{n}.csv');assert len(a)==counts[n];print(n,len(a),file=out)
                if n in (293,389):
                    s=set(a);q=pts(E/'data'/f'orbits{n}.csv');assert {(A,B) for x,y in q for A,B in [(x,y),(n-1-y,x),(n-1-x,n-1-y),(y,n-1-x)]}==s
                for x,y in a:print(x,y,file=out)
        with (t/'sets').open() as f:run([dirs],stdin=f)
        frame=build(E/'code/verify_frame.cpp',t/'frame');legacy=lines(L/'SHA256SUMS')
        for n in (16018,32002,64006,131074,1000018):
            source=E/'data'/f'final-{n//2}.txt' if n in (16018,32002,64006) else L/'data'/f'edits_{n//2}.txt';dest=t/'expanded.csv';text=run([frame,source,dest],capture_output=True,text=True).stdout;assert f' total={counts[n]} ' in text;print(text,end='',flush=True)
            if n in (16018,32002,64006):assert pts(dest)==sorted(pts(E/'coordinates'/f'n{n}.csv'))
            else:
                rel=f'coordinates/n{n}.csv';assert h(dest)==legacy[rel],rel
                if expand:shutil.copyfile(dest,L/rel)
        print('PASS matching rebuilt byte-for-byte; all 15 table witnesses verified. Counts are lower bounds, not optimality certificates.',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--hashes-only',action='store_true');p.add_argument('--expand-large',action='store_true');p.add_argument('--skip-manifest',action='store_true',help='for development before a release manifest exists');a=p.parse_args()
    if a.hashes_only and a.skip_manifest:p.error('hashes requested but disabled')
    if not a.skip_manifest:hashes()
    if not a.hashes_only:check_all(a.expand_large)
