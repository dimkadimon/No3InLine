"""Regenerate the vector figure in the manuscript (optional: requires matplotlib)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from verify import expand

root=Path(__file__).resolve().parent
s=next(s for s in json.loads((root/'data/witnesses.json').read_text()) if s['n']==47)
P={(x-23,y-23) for x,y in expand(47,s['centered_representatives'])}
fig,(ax,detail)=plt.subplots(1,2,figsize=(7.4,3.5),gridspec_kw={'width_ratios':(1.22,0.96)},layout='constrained')
ink='#174657';accent='#B44F29'; faint='#D8DFE0'
for a in (ax,detail):
    a.set_aspect('equal');a.tick_params(color='#7a8a90',labelcolor=ink,labelsize=8,length=3,pad=4)
    for sp in a.spines.values():sp.set_color('#9ba9ad');sp.set_linewidth(.7)
    a.set_facecolor('#fbfcfb')
ax.set(xlim=(-23.8,23.8),ylim=(-23.8,23.8),xticks=[-23,0,23],yticks=[-23,0,23]);ax.axhline(0,color=faint,lw=.8);ax.axvline(0,color=faint,lw=.8)
X,Y=zip(*P);ax.scatter(X,Y,s=11,c=ink,linewidth=0,zorder=3)
a=[(7*i,7*j) for i in (-1,1) for j in (-1,1)];X,Y=zip(*a);ax.scatter(X,Y,marker='+',s=22,c=accent,linewidths=1.2)
ax.set_title('A   The 47 × 47 board',loc='left',fontsize=10,color=ink,weight='semibold',pad=8)
detail.set(xlim=(3,11),ylim=(3,11),xticks=[3,5,7,9,11],yticks=[3,5,7,9,11]);detail.grid(color=faint,lw=.5);detail.set_axisbelow(True)
detail.plot([3,11],[11,3],ls='--',dashes=(3,3),lw=1.1,color=accent);detail.scatter([5,9],[9,5],c=ink,s=32,zorder=3);detail.scatter([7],[7],marker='+',c=accent,s=70,linewidths=1.6,zorder=4)
for (x,y),label,offset in [((5,9),'(5, 9)',(5,3)),((9,5),'(9, 5)',(-2,-14)),((7,7),'(7, 7)',(6,3))]:detail.annotate(label,(x,y),xytext=offset,textcoords='offset points',fontsize=8,color=accent if x==7 else ink)
detail.set_title('B   Why insertion fails',loc='left',fontsize=10,color=ink,weight='semibold',pad=8)
fig.savefig(root/'witness47.pdf',metadata={'Title':'The order-47 fully symmetric maximizer and its blocked midpoint','Creator':'Matplotlib'});plt.close(fig)
