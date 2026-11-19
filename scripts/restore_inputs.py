#!/usr/bin/env python3
"""Restore separately credited, unmodified historical inputs; these files are deliberately not shipped under MIT.
Use --fetch to enable HTTPS or supply the pinned files via --cache DIR. Every archive and every generated output is hash checked.
Refuses to replace a differing existing file. Never executes upstream code or extracts filenames from an untrusted archive to disk.
"""
from pathlib import Path
import argparse, csv, hashlib, io, json, os, tarfile, urllib.request, zipfile
R=Path(__file__).resolve().parents[1];E=R/'studies/improvements';L=R/'studies/larger-grids';N=R/'studies/no3research'
URL='https://rstation.ai/api/v1/papers/no_three_in_line_';B='https://wwwhomes.uni-bielefeld.de/achim/no3in/'
PINS={'22.zip':(URL+'22/versions/4/supplement','704cba3c87fc5882aa323c51ead7bb6ce9157a92932814b5b9dcf19ff88e1f68'),
      '47.zip':(URL+'47/versions/1/supplement','cb218228a2e7a1e5d801cbf85bb360ee7007ad7f5352d8ecf9e95e6fc1b214cd'),
      'all.dat':(B+'download/all_known_solutions','2aa1d0565e6792177c4dbb7a145257739d2008f7b9c126be7ea6be076f16eed5'),
      'defect.txt':(B+'table_min_defect','057a2ae75457e01fcb8464bbc0d3f317078742463baaf88191edb70b7719b55c')}
def digest(b):return hashlib.sha256(b).hexdigest()
def load(name,cache,fetch):
    url,sha=PINS[name];f=cache/name
    if f.is_file():b=f.read_bytes()
    elif fetch:
        with urllib.request.urlopen(url,timeout=90) as h:b=h.read(64*1024*1024+1)
    else:raise SystemExit(f'Missing {name}. Place this pinned input in {cache}, or use --fetch. Source: {url}')
    if digest(b)!=sha:raise SystemExit(f'{name} is not the pinned snapshot; expected {sha}. Obtain the dated original; nothing is installed from changed bytes.')
    if not f.is_file():cache.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    print(f'PIN {name} {sha}',flush=True);return b
expected={base/path:sha for base in (E,L,N) for sha,path in (s.split('  ',1) for s in (base/'SHA256SUMS').read_text().splitlines())}
written=[]
def install(path,b):
    if digest(b)!=expected[path]:raise ValueError(f'generated data differ from the historical manifest: {path}')
    if path.exists() and path.read_bytes()!=b:raise SystemExit(f'refusing to overwrite differing existing input: {path}')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b);written.append(path)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--cache',type=Path,default=R/'.cache/upstream');ap.add_argument('--fetch',action='store_true');ap.add_argument('--group',choices=('station','catalogue','all'),default='all');args=ap.parse_args()
    if args.group in ('station','all'):
        with zipfile.ZipFile(io.BytesIO(load('22.zip',args.cache,args.fetch))) as z, tarfile.open(fileobj=io.BytesIO(z.read('runs.tar.gz')),mode='r:gz') as t:
            for rec in json.loads((L/'experiments/seedindex.json').read_text()):
                name=rec['member'];raw=z.read(name) if name in z.namelist() else t.extractfile(name).read();h,*q=raw.decode().splitlines();nums=sorted(tuple(int(k)-1 for k in row.split()) for row in q if row.strip());n,count=map(int,h.split())
                if n!=rec['n'] or count!=rec['points'] or len(nums)!=count:raise ValueError(name)
                b=(f'{n} {count}\n'+''.join(f'{x} {y}\n' for x,y in nums)).encode();install(L/'experiments/seeds'/(rec['id']+'.txt'),b)
                if name=='sets/n200_c.txt':install(L/'inputs/n200_c_zero_based.txt',b)
                if name=='runs/greedy/out_300_3.txt':install(E/'sources/public300-crop-seed.txt',b)
        with zipfile.ZipFile(io.BytesIO(load('47.zip',args.cache,args.fetch))) as z:
            for p in (8009,16001,32003):
                fn=f'insertions_{p}.txt';b=z.read(fn);install(L/'inputs'/fn,b);install(E/'sources'/fn,b)
    if args.group in ('catalogue','all'):
        a=load('all.dat',args.cache,args.fetch).splitlines(keepends=True);high=b''.join(x for x in a if (len(x.strip())-1)//2>=58);fr=b''.join(x for x in a if (len(x.strip())-1)//2>=74);install(L/'experiments/high.dat',high);install(L/'inputs/frontier-seeds.txt',fr);install(N/'extras/frontier-seeds.txt',fr)
        s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\r\n');w.writerow(('n','points','half_turn','original_word'))
        for r in csv.DictReader((R/'results/catalogue-index.csv').open()):
            w.writerow((r['n'],r['points'],r['half_turn'],a[int(r['source_row_1_based'])-1].decode('ascii').strip()))
        install(E/'sources/catalogue-examples.csv',s.getvalue().encode());install(N/'comparison/flammenkamp-2026-05-03.txt',load('defect.txt',args.cache,args.fetch))
    print(f'PASS restored or checked {len(written)} source files against historical output digests.')
if __name__=='__main__':main()
