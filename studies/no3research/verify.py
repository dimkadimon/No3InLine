#!/usr/bin/env python3
"""Verify coordinates with ordinary integer determinants; optionally compare the full-size supplement.
No third-party Python modules. Run from anywhere with python3 verify.py [--catalogue /path/to/file].
Witness verification is not an upper bound: reproduce.py runs the exhaustive counters separately.
"""
import argparse
import csv
import hashlib
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
ALPH = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,.'
DB_HASH = '2aa1d0565e6792177c4dbb7a145257739d2008f7b9c126be7ea6be076f16eed5'

def require(b, msg):
    if not b:
        raise ValueError(msg)

def expand(n, reps):
    m = n // 2
    return {(m + i*u, m + j*v) for a,b in reps for u,v in ((a,b),(b,a))
            for i in (-1,1) for j in (-1,1)}

def check(P, n, size):
    require(len(P)==size and all(type(x) is int and type(y) is int and
            0<=x<n and 0<=y<n for x,y in P), f'bad size or coordinates at n={n}')
    for (x,y),(u,v),(w,z) in combinations(P,3):
        if (u-x)*(z-y)==(v-y)*(w-x):
            raise ValueError(f'collinear at n={n}: {(x,y),(u,v),(w,z)}')

def images(P,n):
    Q=set(P)
    for _ in range(4):
        yield frozenset(Q)
        yield frozenset((y,x) for x,y in Q)
        Q={(n-1-y,x) for x,y in Q}

def enc(P):
    return ''.join(ALPH[x] for x,y in sorted(P,key=lambda p:(p[1],p[0])))

def dec(w):
    return {(ALPH.index(t), i//2) for i,t in enumerate(w)}

def augmentable(P,n):
    candidates={(x,y) for x in range(n) for y in range(n)}-P
    # First apply the horizontal/vertical lines, then test all remaining secants.
    candidates={(x,y) for x,y in candidates if sum(a==x for a,b in P)<2
                and sum(b==y for a,b in P)<2}
    for (a,b),(u,v) in combinations(P,2):
        candidates={ (x,y) for x,y in candidates if (u-a)*(y-b)!=(v-b)*(x-a) }
        if not candidates: break
    return candidates

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--catalogue', type=Path, help='Flammenkamp all_known_solutions file (compare under D4)')
    args=ap.parse_args()
    summaries={int(row['n']):row for row in csv.DictReader((DATA/'census.csv').open())}
    witnesses=json.loads((DATA/'witnesses.json').read_text()); triples=0
    from math import comb
    for w in witnesses:
        n=w['n']; size=int(summaries[n]['maximum']); P=expand(n,w['centered_representatives'])
        check(P,n,size); require(len(set(images(P,n)))==1,'not D4-invariant'); triples+=comb(size,3)
    require(sorted(w['n'] for w in witnesses)==sorted(summaries),'witness/table mismatch')
    Q={}
    for row in csv.DictReader((DATA/'coordinates.csv').open()):
        n,x,y=(int(row[k]) for k in ('n','x','y'));Q.setdefault(n,[]).append((x,y))
    require(set(Q)==set(summaries),'expanded coordinate file missing a board')
    for w in witnesses:
        n=w['n'];p=expand(n,w['centered_representatives']);require(len(Q[n])==len(p) and set(Q[n])==p,'expanded CSV mismatch')
    print(f'{len(witnesses)} census witnesses verified; {triples:,} exact triple determinants.')
    ceiling=json.loads((DATA/'ceiling_configurations.json').read_text()); open_counts=[]; per={}; allsets=set()
    for w in ceiling:
        n=w['n']; P=expand(n,w['centered_representatives']);check(P,n,2*n-2)
        h=(n,frozenset(P)); require(h not in allsets,'repeated ceiling configuration');allsets.add(h)
        per[n]=per.get(n,0)+1; add=augmentable(P,n)
        if add:open_counts.append((n,len(add)))
    for n,row in summaries.items():
        require(per.get(n,0)==(int(row['count']) if int(row['maximum'])==2*n-2 else 0),'ceiling count mismatch')
    require(open_counts==[(3,4)],'ceiling augmentation census mismatch')
    print(f'{len(ceiling)} ceiling configurations checked; just the order-3 axial cross admits an added point.')
    entries=json.loads((DATA/'catalogue_additions.json').read_text())
    seen=set(); seeds=set(); allwords=set()
    for e in entries:
        n=e['n'];seed=e['seed'];P=dec(seed[1:]);seeds.add(seed)
        if e['method']=='cyclic cut':
            P={((x-e['xcut'])%n,(y-e['ycut'])%n) for x,y in P}
        else:
            if e['method']=='boundary exchange':
                P={(x+e['dx'],y+e['dy']) for x,y in P if 0<=x+e['dx']<n and 0<=y+e['dy']<n}
            R={tuple(q) for q in e['removed']}; A={tuple(q) for q in e['added']}
            require(R<=P and not A&(P-R),'invalid exchange');P=(P-R)|A
        check(P,n,2*n); require(all(sum(y==j for x,y in P)==2 and sum(x==j for x,y in P)==2 for j in range(n)),'bad margins')
        im=set(images(P,n));words={enc(x) for x in im}; k=min(words)
        require(k==e['canonical'] and k not in seen,'canonical word mismatch or duplicate');seen.add(k);allwords.update(words)
        if e['symmetry']=='.':require(len(im)==8,'nontrivial stabilizer')
        elif e['symmetry']==':': require(len(im)==4 and {(n-1-x,n-1-y) for x,y in P}==P,'not exactly half-turn symmetric')
        else:raise ValueError('unknown symmetry class')
    require((DATA/'catalogue-additions.txt').read_text().splitlines()==[e['symmetry']+e['canonical'] for e in entries],'text inventory mismatch')
    Q={}
    for row in csv.DictReader((DATA/'catalogue-coordinates.csv').open()):
        i=int(row['record']);e=entries[i-1];require(int(row['n'])==e['n'] and row['symmetry']==e['symmetry'],'record label mismatch');Q.setdefault(i,[]).append((int(row['x']),int(row['y'])))
    for i,e in enumerate(entries,1):
        require(len(Q[i])==2*e['n'] and set(Q[i])==dec(e['canonical']),'catalogue coordinate CSV mismatch')
    print(f'{len(entries)} mutually inequivalent ordinary 2n-point configurations verified.')
    frontier=(ROOT/'extras/frontier-seeds.txt').read_text().splitlines()
    for word in frontier:
        P=dec(word[1:]); n=(len(word)-1)//2; check(P,n,2*n)
        require({(n-1-y,x) for x,y in P}==P,'frontier seed is not quarter-turn invariant')
        seeds.add(word)
    print(f'{len(frontier)} credited frontier seeds verified geometrically.')
    if args.catalogue:
        b=args.catalogue.read_bytes(); digest=hashlib.sha256(b).hexdigest();db=set(b.decode('ascii').splitlines());print('Catalogue SHA-256:',digest)
        if digest!=DB_HASH:print('NOTE: not the historical 28 October 2026 byte snapshot; testing the supplied file.')
        # Normalise the order of the two entries of each row, independent of display convention.
        # For the pinned file every pair is already in ascending column order.
        rank={v:i for i,v in enumerate(ALPH)};target_orders={e['n'] for e in entries};oriented=set()
        for s in db:
            if (len(s)-1)//2 not in target_orders:continue
            u=s[1:];oriented.add(''.join(a+b if rank[a]<rank[b] else b+a for a,b in zip(u[::2],u[1::2])))
        missing=seeds-db; overlaps=allwords & oriented;print(f'{len(missing)} source words absent; {len(overlaps)} matching oriented result words in supplied catalogue.')
        if digest==DB_HASH:
            require(not missing and not overlaps,'historical comparison failed')
            require({w for w in db if (len(w)-1)//2 in (74,76,78)}==set(frontier),'frontier seed coverage differs')

if __name__=='__main__': main()
