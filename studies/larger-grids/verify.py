#!/usr/bin/env python3
"""Check the supplied results. Requires Python 3.9+ and a C++17 compiler, offline.
--enumerate-free also regenerates both whole-board inputs to the fixed-frame upper certificates.
--symmetry reruns all four complete D4 tiers by both methods; this is the longest option.
"""
import argparse,csv,filecmp,hashlib,os,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'code'));from verify_cover import check as check_cover
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--enumerate-free',action='store_true');ap.add_argument('--symmetry',action='store_true');ap.add_argument('--skip-digests',action='store_true');args=ap.parse_args()
def demand(x,msg):
 if not x:raise RuntimeError(msg)
def run(cmd,**kw):return subprocess.run(list(map(str,cmd)),check=True,**kw)
def digest(f):
 h=hashlib.sha256()
 with f.open('rb')as d:
  for c in iter(lambda:d.read(1048576),b''):h.update(c)
 return h.hexdigest()
if not args.skip_digests and (R/'SHA256SUMS').exists():
 for line in (R/'SHA256SUMS').read_text().splitlines():
  sha,name=line.split('  ',1);demand(digest(R/name)==sha,'SHA256 mismatch: '+name)
 print('File checksums match.',flush=True)
for py in ('verify_small.py','search_boundary.py','check_example.py'):run([sys.executable,R/'code'/py])
with tempfile.TemporaryDirectory() as t:
 t=Path(t)
 def build(name):
  out=t/name;run([os.environ.get('CXX','c++'),'-O3','-std=c++17',R/'code'/(name+'.cpp'),'-o',out]);return out
 ex=build('verify_frame');enum=build('enumerate_free')if args.enumerate_free else None
 for row in csv.DictReader((R/'data/results.csv').read_text().splitlines()):
  p=int(row['p']);n=int(row['side']);dest=t/'expanded.csv';edits=R/f'data/edits_{p}.txt';s=run([ex,edits,dest],capture_output=True,text=True).stdout;print(s,end='',flush=True)
  demand(f" total={row['points']} " in s and f'n={n} ' in s,'wrong size');demand(filecmp.cmp(dest,R/f'coordinates/n{n}.csv',shallow=False),'CSV mismatch')
 for F in sorted((R/'data').glob('fixed_*.txt')):
  p=int(F.stem.split('_')[1]);_,deln,add=map(int,F.read_text().splitlines()[0].split());demand(deln==0,'frame was not retained');run([ex,F]);ub=check_cover(p);demand(ub==add,f'upper/lower mismatch p={p}: {ub}/{add}')
  if enum:
   dest=t/'free.txt'
   with dest.open('wb')as o:run([enum,p],stdout=o)
   demand(filecmp.cmp(dest,R/f'data/free{p}.txt',shallow=False),'whole-board free set mismatch')
 ctrl=t/'control.txt';ctrl.write_text('101 0 0\n');run([ex,ctrl])
 # Column 1 contains (1,51) and (1,152); (1,0) would be a third point.
 for source in ('101 0 1\n1 0\n','101 2 0\n1 51\n1 51\n'):
  ctrl.write_text(source);s=subprocess.run([ex,ctrl],capture_output=True);demand(s.returncode!=0,'bad control passed')
 gap=build('check_gaps');res=run([gap],input=(R/'inputs/frontier-seeds.txt').read_text(),capture_output=True,text=True).stdout.splitlines();demand(res==(R/'data/frontier-gaps.csv').read_text().splitlines()[1:],'gap audit mismatch');print('Frontier gap cases independently agree.',flush=True)
 if args.symmetry:
  d=build('dihedral');a=build('line_audit')
  for n,k,c in ((67,0,0),(67,1,1),(69,0,0),(69,1,0)):
   for cmd in ([d,n,'--tier',k],[a,n,k]):
    text=run(cmd,capture_output=True,text=True).stdout;print(text,end='',flush=True);demand(f'size={4*(n//2-k)} count={c} ' in text,'symmetry count mismatch')
print('PASS',flush=True)
