#!/usr/bin/env python3
"""Recheck the seven exhibited sets, every comparison, all finite exceptions used by the theorem,
and the constructive examples. Requires Python 3.9+ and a C++17 compiler, no packages or network.
Optional --rescan also regenerates the two whole-board free-site lists and the four-axis scan.
Run without Python's -O flag. Never imports the discovery heuristics."""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,csv,json,subprocess,sys,os,hashlib,shlex
D=Path(__file__).resolve().parent;C=D/'code';E=D/'data';S=D/'sources';P=D/'coordinates';sys.path.insert(0,str(C))
from direct_append import test as literal_test
from construct import make
from catalogue_small import audit as audit_catalogue

def check(ok,msg):
 if not ok:raise ValueError(msg)
def readings(f):
 a=f.read_text().splitlines();return tuple(map(int,a[0].split())),list(tuple(map(int,l.split()))for l in a[1:])
def coords(f):
 with f.open()as z:r=list(csv.DictReader(z));T={(int(q['x']),int(q['y']))for q in r};check(len(r)==len(T),'duplicate coordinate: '+str(f));return T
def frame_edit(f,O):
 h,Q=readings(f);p,r,a=h;check(len(Q)==r+a and len(set(Q))==len(Q),'bad edits '+str(f));R=set(Q[:r]);A=set(Q[r:]);check(R<=O and not A&O,'nonstandard frame edits');return (O-R)|A

def rundata(exe,cmd):
 with subprocess.Popen(cmd,stdout=subprocess.PIPE)as p:
  subprocess.run([exe],stdin=p.stdout,check=True);p.stdout.close();check(p.wait()==0,'input test failed')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--rescan',action='store_true');ap.add_argument('--skip-digests',action='store_true');o=ap.parse_args();check(__debug__,'do not run with python -O');info=list(csv.DictReader((E/'comparison.csv').open()))
 if not o.skip_digests:
  for line in(D/'SHA256SUMS').read_text().splitlines():
   h,path=line.split('  ',1);check(hashlib.sha256((D/path).read_bytes()).hexdigest()==h,path+' digest mismatch')
  print('PASS bundled SHA256SUMS',flush=True)
 with TemporaryDirectory()as tmp:
  T=Path(tmp)
  def build(src):
   exe=T/src;subprocess.run(shlex.split(os.environ.get('CXX','c++'))+['-O3','-std=c++17',str(C/(src+'.cpp')),'-o',str(exe)],check=True);return exe
  vf=build('verify_frame');vs=build('check_stream');free=build('enumerate_free')if o.rescan else None;axis=build('axis_scan')if o.rescan else None
  for row in info[:3]:
   n=int(row['n']);p=n//2;h=p//2;O={(x,y)for a in range(1,p)for b in[(h+pow(a,-1,p))%p]for x in(a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)}
   pubh,A=readings(S/f'insertions_{p}.txt');check(pubh==(p,len(A)),'public header');pub=O|set(A);prior=frame_edit(S/f'edits_{p}.txt',O);fresh=frame_edit(E/f'final-{p}.txt',O);litfile=E/f'literal-{p}.txt';lit=frame_edit(litfile,O)
   check([len(pub),len(prior),len(fresh),len(fresh)-len(pub),len(fresh)-len(prior),len(pub-fresh),len(fresh-pub),len(lit)-len(pub)]==[int(row[k]) for k in ('public_points','previous_points','new_points','net_over_public','net_over_previous','removed_from_public','inserted_vs_public','literal_public_append')],'comparison '+str(n));v=json.loads((E/f'append{n}.json').read_text());check(pub|set(map(tuple,v['compatible_additions']))==lit,'literal is not exactly an extension of the public set');cp=T/'expanded.csv';subprocess.run([vf,litfile],check=True);subprocess.run([vf,E/f'final-{p}.txt',cp],check=True);check(coords(cp)==fresh==coords(P/f'n{n}.csv'),'certificate vs CSV mismatch')
   if free and p!=32003:
    outfile=T/f'free{p}.txt'
    with outfile.open('w')as f:subprocess.run([free,str(p)],stdout=f,check=True)
    check(readings(outfile)==readings(S/outfile.name),'regenerated full-board free list')
   if axis and p==32003:
    z=subprocess.check_output([axis,S/f'insertions_{p}.txt'],text=True);check(z.split()==(E/'axis32003.txt').read_text().split(),'regenerated four-axis list')
   literal_test(p);print(f'PASS n={n}: vs public -{len(pub-fresh)} +{len(fresh-pub)}; vs previous -{len(prior-fresh)} +{len(fresh-prior)}.',flush=True)
  with (T/'rotations.txt').open('w')as stream:
   for row in info[3:]:
    n=int(row['n']);A=coords(P/f'n{n}.csv');B=coords(S/f'previous{n}.csv');check(len(A)==int(row['new_points']) and len(B)==int(row['previous_points'])and len(A)-len(B)==int(row['net_over_previous']),'rotational comparison')
    if n in(293,389):
     R=coords(E/f'orbits{n}.csv');V=set();check(len(R)*4==len(A),'orbit count')
     for x,y in R:V.update(((x,y),(n-1-y,x),(n-1-x,n-1-y),(y,n-1-x)))
     check(V==A,'quarter turns failed')
    print(n,len(A),file=stream);stream.writelines(f'{x} {y}\n'for x,y in sorted(A));print(f'PASS n={n}: vs previous -{len(B-A)} +{len(A-B)}.',flush=True)
  with (T/'rotations.txt').open()as f:subprocess.run([vs],stdin=f,check=True)
  _,Q=readings(S/'public300-crop-seed.txt');check(sum(4<=x<297 and 4<=y<297 for x,y in Q)==504,'public crop')
  rundata(vs,[sys.executable,C/'check_charts.py']);rundata(vs,[sys.executable,C/'test_chart_examples.py'])
  audit_catalogue()
  for n in(1,2,3,12,19,74,139,201,202,293,389,405,4000,4037,8012,10085,15901,16018,31669,32002,32558,64006):
   u,i=make(n);v,j=make(n,True);check(len(v)>=len(u) and i['half_turn'],'any-side mode');
   if 31669<=n<=32558:check(2*len(v)>3*n,'crop/pad interval')
   if n in(202,293,389,4037,10085,16018,32002,64006):print(f'Construction smoke n={n}: half-turn {len(u)}, ordinary {len(v)}.',flush=True)
 print('PASS finite witnesses, comparisons, theorem finite branch, construction checks and transfer interval.',flush=True)
if __name__=='__main__':main()
