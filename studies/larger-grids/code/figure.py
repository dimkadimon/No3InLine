"""Optional: rebuild the vector/raster figure used in note.tex (Matplotlib)."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1];L=(R/'data/edits_8009.txt').read_text().splitlines();p,nr,na=map(int,L[0].split());h=p//2;removed={tuple(map(int,l.split())) for l in L[1:nr+1]};extra=[tuple(map(int,l.split())) for l in L[1+nr:]]
old=[(x,y)for a in range(1,p)for b in [(pow(a,-1,p)+h)%p] for x in(a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)and (x,y)not in removed];E=json.loads((R/'data/example-exchange.json').read_text());
fig,(a,b)=plt.subplots(1,2,figsize=(7.45,3.5),layout='constrained');gray='#435961';teal='#007974';orange='#b24a24';ink='#1c3542'
for ax in a,b:
 ax.set_aspect('equal');ax.tick_params(labelsize=7,color=gray,labelcolor=ink,length=2.8);ax.spines[['top','right']].set_visible(False);ax.spines[['bottom','left']].set_color('#a7b4b9')
 ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:,.0f}'));ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:,.0f}'))
a.scatter(*zip(*old),s=0.36,c=gray,linewidths=0,alpha=.68,rasterized=True);a.scatter(*zip(*extra),s=2.2,c=teal,linewidths=0,rasterized=True);a.add_patch(Rectangle((h+.5,h+.5),p,p,fill=False,lw=.5,ec=teal));a.set(xlim=(-160,2*p+160),ylim=(-160,2*p+160),xticks=[0,8000,16000],yticks=[0,8000,16000]);a.set_title(f'A  The {len(old)+len(extra):,}-point packing',loc='left',color=ink,fontsize=9,weight='bold',pad=6)
r=E['remove'];qs=E['insert'];ss=E['other_blocking_endpoints'];
for i,(q,s) in enumerate(zip(qs,ss),1):
 pts=sorted([q,s,r],key=lambda u:u[0]);b.plot(*zip(*pts),c='#8b9fa3',lw=1.1,ls='--',zorder=1);b.scatter(*s,c=gray,s=26,linewidths=0,zorder=4);b.scatter(*q,c=teal,s=38,marker='o',linewidths=0,zorder=5);b.annotate(f'$q_{i}$',q,xytext=(5,4),textcoords='offset points',color=teal,fontsize=9);b.annotate(f'$s_{i}$',s,xytext=(5,4),textcoords='offset points',color=gray,fontsize=9)
b.scatter(*r,c=orange,marker='x',s=50,lw=1.4,zorder=6);b.annotate('$r$',r,xytext=(6,1),textcoords='offset points',color=orange,fontsize=10);b.set(xlim=(1200,10700),ylim=(1600,11700),xticks=[2000,6000,10000],yticks=[2000,6000,10000]);b.set_title('B  One deletion frees two sites',loc='left',color=ink,fontsize=9,weight='bold',pad=6)
fig.savefig(R/'exchange-figure.pdf',dpi=230,metadata={'Title':'A large modular packing and an actual profitable exchange'});plt.close(fig)
