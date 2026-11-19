#!/usr/bin/env python3
"""Independent arithmetic pass over Table 1's K/S source data (optional NumPy).

Usage: python3 scripts/recheck_benchmarks.py CACHE
CACHE holds the two version-pinned rStation supplements 22.zip and 47.zip.
Reads the original archive members directly, never executes upstream code,
never imports the project's geometry/crop routines, and never writes source data.
"""
import argparse
import csv
import hashlib
import io
import json
import tarfile
import zipfile
from math import isqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PINS = {'22.zip': '704cba3c87fc5882aa323c51ead7bb6ce9157a92932814b5b9dcf19ff88e1f68',
        '47.zip': 'cb218228a2e7a1e5d801cbf85bb360ee7007ad7f5352d8ecf9e95e6fc1b214cd'}
SCALE = 1 << 32


def read_points(data):
    rows = [tuple(map(int, row.split())) for row in data.splitlines() if row.strip()]
    assert rows and all(len(r) == 2 for r in rows)
    n, count = rows[0]
    points = np.array(rows[1:], dtype=np.int64)
    assert points.shape == (count, 2)
    return n, points


def screen(points, side, centres):
    # Two distinct nonvertical slopes on this board differ by at least
    # 1/(side-1)^2 > 2^-32. Thus floor(2^32 dy/dx) is an exact *line* key,
    # even for negative differences (integer floor, no floating point or gcd).
    assert 1 < side <= 64006 and (side-1)**2 < SCALE and SCALE*(side-1) < 1 << 63
    assert np.all((0 <= points) & (points < side))
    assert len(np.unique(points[:, 0]*side + points[:, 1])) == len(points)
    xx, yy = points.T
    for x,y in centres:
        dx = xx-x
        nonvert = dx != 0
        assert len(dx)-int(nonvert.sum()) <= 2, (x,y,'vertical')  # includes the centre
        keys = ((yy[nonvert]-y)*SCALE)//dx[nonvert]
        assert len(np.unique(keys)) == len(keys), (x,y,'collinear')


def read_ks(cache):
    for name,expected in PINS.items():
        assert hashlib.sha256((cache/name).read_bytes()).hexdigest() == expected, name
    with (ROOT/'results/checked-comparisons.csv').open() as f:
        table = {int(r['n']): (int(r['B_checked']), set(r['source_codes'].split(',')))
                 for r in csv.DictReader(f)}
    with (ROOT/'results/p22-crops.csv').open() as f:
        crops = {(int(r['side']), r['source_member']): tuple(int(r[k]) for k in ('points_in_crop','x0','y0'))
                 for r in csv.DictReader(f)}
    ref = json.loads((ROOT/'studies/larger-grids/experiments/seedindex.json').read_text())
    assert len(ref) == len({r['member'] for r in ref}) == 146
    kval = dict.fromkeys(table, 0); sval = dict.fromkeys(table, 0); windows = set()
    with zipfile.ZipFile(cache/'22.zip') as archive, tarfile.open(fileobj=io.BytesIO(archive.read('runs.tar.gz'))) as runs:
        outer = set(archive.namelist())
        for r in ref:
            name = r['member']
            side,P = read_points(archive.read(name) if name in outer else runs.extractfile(name).read())
            P -= 1  # K coordinates in the original supplement start at 1.
            assert (side,len(P)) == (r['n'],r['points'])
            screen(P,side,P)
            # Summed-area table evaluates every integer crop in one array slice.
            A = np.zeros((side+1,side+1), dtype=np.int64)
            A[P[:,0]+1,P[:,1]+1] = 1
            A = A.cumsum(axis=0).cumsum(axis=1)
            for n in table:
                hits = len(P)
                if n < side:
                    counts = A[n:,n:] - A[:-n,n:] - A[n:,:-n] + A[:-n,:-n]
                    x,y = map(int,np.unravel_index(counts.argmax(), counts.shape))
                    hits = int(counts[x,y]); key = n,name
                    assert (hits,x,y) == crops[key], key
                    windows.add(key)
                kval[n] = max(kval[n],hits)
    assert windows == set(crops)
    print(f'K: all {len(ref)} original coordinate sets pass; all {len(windows)} recorded crop count/corner pairs equal prefix-sum maxima.', flush=True)
    with zipfile.ZipFile(cache/'47.zip') as archive:
        for p,m in ((8009,282),(16001,421),(32003,810)):
            header,adds = read_points(archive.read(f'insertions_{p}.txt'))
            assert header==p and len(adds)==m and all(p%a for a in range(2,isqrt(p)+1))
            h=(p-1)//2; side=2*p; frame=[]
            # Enumerate by *ordinate*: x(y-h)=1 mod p. The middle square
            # removes one of the four lifts of each residue point.
            for b in range(p):
                if b==h: continue
                a=pow((b-h)%p,-1,p)
                copies=[(x,y) for y in (b,b+p) for x in (a,a+p) if not (h<x<=h+p and h<y<=h+p)]
                assert len(copies)==3
                frame.extend(copies)
            base=np.array(frame,dtype=np.int64); xx,yy=base.T
            assert len(base)==3*(p-1) and np.all(xx*(yy-h)%p==1)
            # A primitive physical line reduces to a line meeting the nonsingular
            # conic in at most two residues. A frame-only triple therefore uses
            # a congruent pair. Its direction in these two sheets is axial or diagonal.
            for label in (xx, yy, xx+yy, xx-yy):
                assert np.unique(label,return_counts=True)[1].max()<=2
            pts=np.vstack((base,adds)); screen(pts,side,adds)
            for n in table: sval[n]=max(sval[n], len(pts)-4*max(side-n,0))
            print(f'S: side {side}, {len(base)} frame + {m} additions = {len(pts)}; {m*(len(pts)-1)} exact directions through additions.',flush=True)
    for n,(B,tags) in table.items():
        for code,score in (('K',kval[n]),('S',sval[n])):
            assert score<=B and ((score==B)==(code in tags)), (n,code,score,B,tags)
    assert len(table)==15
    print('PASS K/S contributions and ties for all 15 Table 1 sides. No reported-only counts used.')


if __name__ == '__main__':
    if not __debug__: raise SystemExit('Run without -O; checks use assertions.')
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('cache',type=Path)
    read_ks(ap.parse_args().cache)
