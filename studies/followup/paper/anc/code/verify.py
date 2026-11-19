#!/usr/bin/env python3
"""Verification entry point. Run with Python 3.10+ (no packages); a C++17 compiler is needed.
Use --rescan to regenerate every individually free site before the fixed-seed optimality proof.
Use --seams for the 712 all-direction rectangular tests; together these operations can take minutes.
"""
import argparse,csv,os,subprocess,sys,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent;E=D.parent/'data';ns=(293,389,4037,10085)

def coords(path):
 with path.open()as f:return [tuple(map(int,r))for r in list(csv.reader(f))[1:]]
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--rescan',action='store_true');a.add_argument('--seams',action='store_true');o=a.parse_args();assert __debug__,'do not use python -O'
 from anchor_ring import anchored
 from test_seams import finite_table
 finite_table();subprocess.run([sys.executable,D/'check_certificates.py'],check=True)
 for p,k in ((73,28),(97,17),(1009,11),(2521,11)):
  n,_,P=anchored(p,k);assert sorted(P)==sorted(coords(E/f'seed{n}.csv'))
 with tempfile.TemporaryDirectory()as tmp:
  T=Path(tmp);exe=T/'check';cc=os.environ.get('CXX','c++');subprocess.run([cc,'-O3','-std=c++17',D/'check_stream.cpp','-o',exe],check=True)
  stream=[]
  for n in ns:
   P=coords(E/f'augmented{n}.csv');stream.append(f'{n} {len(P)}');stream.extend(f'{x} {y}'for x,y in P)
  subprocess.run([exe],input='\n'.join(stream)+'\n',text=True,check=True)
  if o.rescan:
   scan=T/'free';subprocess.run([cc,'-O3','-std=c++17',D/'free_sites.cpp','-o',scan],check=True)
   for n in ns:
    out=T/'free.csv';subprocess.run([scan,str(n),E/f'seed{n}.csv',out],check=True);assert sorted(coords(out))==sorted(coords(E/f'free{n}.csv'))
  subprocess.run([sys.executable,D/'frozen_proof.py'],check=True)
  if o.seams:
   with subprocess.Popen([sys.executable,D/'test_seams.py'],stdout=subprocess.PIPE)as g:
    subprocess.run([exe],stdin=g.stdout,check=True);assert g.wait()==0
   subprocess.run([sys.executable,D/'carrier_check.py'],check=True)
 print('PASS. Free-site lists '+('regenerated.'if o.rescan else 'read from tables (use --rescan for completeness).'))
if __name__=='__main__':main()
