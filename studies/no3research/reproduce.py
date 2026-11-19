#!/usr/bin/env python3
"""Recompute census maxima and multiplicities. No third-party packages, catalogue, seeds or SAT software.
Examples: python3 reproduce.py --n 47 --both ; python3 reproduce.py --all --both
Large orders can take minutes or longer per counter. This runs to completion with no time limit.
"""
import argparse
import csv
from pathlib import Path
import os
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent
LINE=re.compile(r'n=(\d+) skipped=(\d+) size=(\d+) count=(\d+) nodes=(\d+)')

def run():
    ap=argparse.ArgumentParser(description=__doc__)
    group=ap.add_mutually_exclusive_group();group.add_argument('--n',type=int,default=47);group.add_argument('--all',action='store_true')
    ap.add_argument('--both',action='store_true',help='rerun every tested tier using the independent maximal-line counter')
    args=ap.parse_args()
    expected={int(r['n']):r for r in csv.DictReader((ROOT/'data/census.csv').open())}
    ns=sorted(expected) if args.all else [args.n]
    if not set(ns)<=set(expected):ap.error('order outside the supplied census')
    with tempfile.TemporaryDirectory() as d:
        def build(name):
            exe=Path(d)/name
            subprocess.run([os.environ.get('CXX','c++'),'-std=c++17','-O3','-march=native',str(ROOT/(name+'.cpp')),'-o',str(exe)],check=True)
            return str(exe)
        main=build('dihedral');audit=build('line_audit') if args.both else None
        for n in ns:
            r=expected[n];print(f'Computing n={n} ...',flush=True)
            out=subprocess.check_output([main,str(n)],text=True)
            rows=[tuple(map(int,m.groups())) for l in out.splitlines() if (m:=LINE.fullmatch(l))]
            want=int(r['unused_radii']); expected_count=int(r['count'])
            if any(nn!=n for nn,*_ in rows) or int(r['maximum'])!=4*(n//2-want) or [(k,size,c) for nn,k,size,c,_ in rows]!=[(k,4*(n//2-k),0 if k<want else expected_count) for k in range(want+1)]:
                raise RuntimeError('primary count mismatch at '+str(n))
            if audit:
                for nn,k,size,c,_ in rows:
                    s=subprocess.check_output([audit,str(n),str(k)],text=True).strip();m=LINE.fullmatch(s)
                    if not m or tuple(map(int,m.groups()[:4]))!=(nn,k,size,c):raise RuntimeError('independent count mismatch: '+s)
            print(f"n={n}: maximum={r['maximum']}, maximizers={expected_count}; {'both agree' if audit else 'main count agrees'}",flush=True)

if __name__=='__main__':run()
