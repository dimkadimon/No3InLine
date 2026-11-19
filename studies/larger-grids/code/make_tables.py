"""Regenerate the note's tables and data/results.csv from the compact certificates."""
import csv,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];rows=[];table=[r'\small\begin{tabular}{r r r r r}',r'\toprule Side $n$ & Published witness & This construction & Gain & Points/$n$\\\midrule'];fixed=[r'\small\begin{tabular}{r r r r r}',r'\toprule Side & Individually legal & Simultaneously legal$^{*}$ & Frozen total$^{*}$ & With deletions\\\midrule'];ds=[]
for p in (8009,16001,32003,65537,500009):
 a,r,k=map(int,(R/f'data/edits_{p}.txt').read_text().splitlines()[0].split());assert a==p;n=2*p;t=3*(p-1)-r+k;assert f' total={t} 'in(R/f'logs/verification_{p}.txt').read_text();f=R/f'inputs/insertions_{p}.txt';b=3*(p-1)+int(f.read_text().splitlines()[0].split()[1])if f.exists() else None;delta=t-b if b else None;rows.append((p,n,3*(p-1),r,k,t,b,delta,t-3*p,f'{t/n:.9f}'));table.append(f'{n:,} & '+(f'{b:,}'if b else '---')+f' & \\textbf{{{t:,}}} & '+(f'+{delta}'if b else '---')+f' & {t/n:.6f}'+r'\\');ds.append(delta)
 f=R/f'data/fixed_{p}.txt'
 if f.exists():
  _,r2,k2=map(int,f.read_text().splitlines()[0].split());assert r2==0;ns=int((R/f'data/free{p}.txt').read_text().splitlines()[0].split()[1]);fixed.append(f'{n:,} & {ns:,} & {k2:,} & {3*(p-1)+k2:,} & {t:,}'+r'\\')
for f,l in [('large-table',table),('fixed-table',fixed)]:
 (R/(f+'.tex')).write_text('\n'.join(l+[r'\bottomrule\end{tabular}'])+'\n')
(R/'numbers.tex').write_text(''.join('\\newcommand{\\'+s+'}{'+str(t)+'}\n'for s,t in [('diffOne',ds[0]),('diffTwo',ds[1]),('diffThree',ds[2]),('firstAdded',rows[0][4])]))
with (R/'data/results.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['p','side','frame','removed_from_frame','added','points','paper47_witness','gain_over_paper47','excess_over_1.5n','points_per_side']);w.writerows(rows)
