#!/usr/bin/env python3
"""Reproduce the unrestricted order-47 symmetry-core bound. The full run writes no giant intermediate file.
Use --both to confirm each core count, row-obstruction count AND surviving orbit list via the independent counter.
For a short smoke test use --max-omitted 2. Both full runs may take several minutes.
"""
import argparse,csv,os,re,subprocess,tempfile
from pathlib import Path
from core_completions import completions,expand
ROOT=Path(__file__).resolve().parent.parent

def parse(lines):
    out=[];summary=None
    for s in lines.splitlines():
        if s.startswith('solution '):out.append(tuple(sorted(tuple(int(v)//2 for v in w.split(',')) for w in s.split()[1:])))
        else:
            m=re.fullmatch(r'n=(\d+) core_size=(\d+) tested=(\d+) row_or_column_obstructions=(\d+) survivors=(\d+)',s)
            if not m or summary is not None:raise ValueError(s)
            summary=tuple(map(int,m.groups()))
    if summary is None or len(out)!=summary[-1] or len(out)!=len(set(out)):raise ValueError('incomplete/duplicate results')
    return summary,sorted(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--both',action='store_true');ap.add_argument('--max-omitted',type=int,default=5,choices=range(6));args=ap.parse_args()
    rows=list(csv.DictReader((ROOT/'data/core47-tiers.csv').open()));text=(ROOT/'data/core47-residual.txt').read_text();expected=set(tuple(sorted(tuple(int(v)//2 for v in w.split(',')) for w in l.split()[1:])) for l in text.splitlines());seen=set()
    with tempfile.TemporaryDirectory() as d:
        def build(f):
            src=ROOT/f;exe=Path(d)/src.stem;subprocess.run([os.environ.get('CXX','c++'),'-O3','-std=c++17','-march=native',str(src),'-o',str(exe)],check=True);return str(exe)
        solver=build('dihedral.cpp');obstruct=build('extras/core_obstruction.cpp');audit=build('extras/core_lines.cpp') if args.both else None
        for k in range(args.max_omitted+1):
            with subprocess.Popen([solver,'47','--tier',str(k),'--all'],stdout=subprocess.PIPE) as proc:
                try:out=subprocess.check_output([obstruct,'47'],stdin=proc.stdout,text=True)
                finally:proc.stdout.close()
                if proc.wait():raise RuntimeError('primary counter failed')
            summary,res=parse(out);rec=rows[k];want=tuple(int(rec[h]) for h in ('n','core_size','enumerated','ruled_out_by_row_or_column','survivors'))
            if want!=summary:raise RuntimeError('recorded counts disagree')
            if audit and (summary,res)!=parse(subprocess.check_output([audit,str(k)],text=True)):raise RuntimeError('the independent counters or filters disagree')
            comp=sum(completions(expand(47,s),47)[0] for s in res)
            if comp or not set(res)<=expected:raise RuntimeError('unexpected residual core or a completion found')
            seen.update(res);print(f'n=47, |S|={summary[1]}: {summary[2]:,} cores, {len(res)} survive margins, {comp} unrestricted completions'+('; independent match' if audit else ''),flush=True)
    if args.max_omitted==5 and seen!=expected:raise RuntimeError('missing residual cores')
if __name__=='__main__':main()
