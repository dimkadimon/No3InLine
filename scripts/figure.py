#!/usr/bin/env python3
"""Recreate the manuscript's vector figure from the released side-293 witness.
Optional: matplotlib >=3.5. A prebuilt PDF is included; no graphics package is required to compile the paper.
"""
import csv, json, os
from pathlib import Path
from datetime import datetime,timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
R=Path(__file__).resolve().parents[1];S=R/'small-prime-examples';d=next(z for z in json.loads((S/'examples.json').read_text()) if z['p']==73)
old_gray='#526374';blue='#005d72';red='#9e3822';p=73;t=4*p
A={(p*x,p*y) for x,y in [(0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4)]};Q={tuple(pt) for pt in d['representatives']};Q|={(t-x,t-y) for x,y in Q};P={(int(z['x']),int(z['y'])) for z in csv.DictReader((S/'coordinates/p73.csv').open())};O=P-A-Q
assert (96,52) in O and (131,122) in Q and (193,246) not in P
old0=set()
for u in range(1,p):
 v=d['k']*pow(u,-1,p)%p
 for i in range(4):
  for j in range(4):
   x=u+i*p;y=v+j*p
   if (i in (0,3) or j in (0,3)) and ((x+y)%2==(pow(u,(p-1)//2,p)!=1)):old0.add((x,y))
assert {(x,y) for x,y in old0 if y==2*x-140}=={(96,52),(193,246)} and {(x,y) for x,y in P if y==2*x-140}=={(96,52),(131,122)}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'pdf.fonttype':42,'axes.unicode_minus':False});f=plt.figure(figsize=(6.65,2.57));left=f.add_axes([.055,.12,.38,.78]);right=f.add_axes([.505,.09,.485,.86]);left.set_aspect('equal');left.set(xlim=(-8,300),ylim=(-8,300),xticks=[0,146,292],yticks=[0,146,292]);left.tick_params(length=2.3,pad=1.9,labelsize=7);[s.set_color('#7d8790') for s in left.spines.values()]
left.fill_between([73,219],73,219,color='#f1f5f6',zorder=-2);left.plot([70,216],[0,292],linewidth=.65,linestyle=(0,(3,2)),color='#919797',zorder=-1)
for points,marker,c,k in ((O,'o',old_gray,3),(A,'s',blue,21),(Q,'D',red,17)):
 x,y=zip(*points);left.scatter(x,y,c=c,s=k,marker=marker,linewidths=0,zorder=2)
f.text(.091,.982,'Final configuration',va='top',fontsize=9.4,fontweight='bold');right.set_xlim(-53,77);right.set_ylim(-.40,1.83);right.axis('off');f.text(.505,.982,'One line through a proposed point',va='top',fontweight='bold',fontsize=9.3);right.text(-52,1.52,r'$q+t(1,2),\qquad q=(131,122)$',fontsize=9)
for y,label in ((.96,'Before the flip'),(.33,'After the flip and insertion')):
 right.text(-52,y+.20,label,fontsize=8);right.plot([-44,71],[y,y],color='#a5afb4',lw=.85);right.scatter([-35],[y],marker='o',c=old_gray,s=28,zorder=2)
right.scatter([62],[.96],c=old_gray,s=28,zorder=2);right.scatter([0],[.96],marker='D',facecolor='white',edgecolor=red,s=25,lw=1.2,zorder=2);right.scatter([0],[.33],marker='D',c=red,s=30,zorder=2);right.scatter([62],[.33],marker='x',c='#707778',s=28,lw=1.2,zorder=2)
for t0,lab in ((-35,r'$-35$'),(0,'0'),(62,'62')):right.text(t0,.12,lab,ha='center',fontsize=7.4)
handles=[Line2D([],[],ls='',marker=m,ms=4.4,color=c,label=l) for m,c,l in [('o',old_gray,'Ring'),('s',blue,'Anchor'),('D',red,'Inserted')]];right.legend(handles=handles,loc='lower left',bbox_to_anchor=(-.015,-.015),frameon=False,ncol=3,handlelength=.8,columnspacing=1.25,handletextpad=.4,fontsize=7.5)
w=R/'paper/figures';w.mkdir(exist_ok=True);dt=datetime(2026,11,19,tzinfo=timezone.utc);f.savefig(w/'one-flip.pdf',metadata={'Creator':'No3InLine figure script','CreationDate':dt,'ModDate':dt});plt.close(f)
