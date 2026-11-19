"""Plots of actual coordinate files only, no illustrative or simulated points."""
import csv
from pathlib import Path
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
D=Path(__file__).resolve().parents[1]
def read(f):
 with f.open()as s:return {tuple(map(int,r))for r in list(csv.reader(s))[1:]}
fig,ax=plt.subplots(1,2,figsize=(9.2,4.0),layout='constrained');plt.rcParams['pdf.fonttype']=42
for a,n in zip(ax,(293,10085)):
 P=read(D/'coordinates'/f'n{n}.csv');O=read(D/'sources'/f'previous{n}.csv')
 def plot(Q,color,size,**kw):
  x,y=zip(*sorted(Q));a.scatter(x,y,s=size,c=color,linewidths=0,**kw)
 if n==293:
  plot(P,'#136971',5);Q={(0,114),(178,0),(292,178),(114,292)};assert Q<=P;plot(Q,'#bd431c',19);a.set_title('293 × 293  ·  508 points',loc='left',size=13,weight='bold');a.set_xticks([0,73,146,219,292]);a.set_yticks([0,73,146,219,292])
 else:
  plot(P&O,'#9eafb0',.64,rasterized=True);plot(P-O,'#b53b15',3.3);a.set_title('10,085 × 10,085  ·  15,520 points',loc='left',size=13,weight='bold');a.set_xticks([0,2521,5042,7563,10084]);a.set_yticks([0,2521,5042,7563,10084]);
 a.set_xlim(-.017*n,n*1.017);a.set_ylim(-.017*n,n*1.017);a.set_aspect('equal');a.tick_params(axis='both',labelsize=8,colors='#455b5d',length=3);a.set_axisbelow(True);a.grid(color='#dae3e3',linewidth=.55);a.spines[['top','right']].set_visible(False);a.spines[['bottom','left']].set_color('#94a7a5')
fig.savefig(D/'figures'/'two-caps.pdf',dpi=220);plt.close(fig)
