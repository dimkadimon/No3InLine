"""Vector illustration of actual coordinates, not a numerical proof."""
from pathlib import Path
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from anchor_ring import ring,B,base_level
P=Path(__file__).resolve().parents[1];p=73;k=base_level(p);fig,(ax,bx)=plt.subplots(1,2,figsize=(8,3.05),gridspec_kw={'width_ratios':[1,1]});c='#156c70';ink='#254353';gold='#bf4c27';slate='#336270'
for a in (ax,bx):
 a.set_aspect('equal');a.set_xlim(-.29,4.29);a.set_ylim(-.29,4.29);a.set_xticks(range(5),['0','$p$','$2p$','$3p$','$4p$']);a.set_yticks(range(5),['0','$p$','$2p$','$3p$','$4p$']);a.tick_params(labelsize=7,pad=0,length=0,colors=ink);a.spines[:].set_visible(False);a.add_patch(Rectangle((0,0),4,4,linewidth=1,edgecolor=slate,facecolor='none'));a.grid(color='#e2e8e7',lw=.6);a.set_axisbelow(True)
ax.add_patch(Rectangle((1,1),2,2,facecolor='#eff4f0',edgecolor='none',zorder=0));O=ring(p,k);ax.scatter([x/p for x,y in O],[y/p for x,y in O],s=3.0,c=slate,linewidths=0,alpha=.86);ax.scatter(*zip(*B),s=25,c=gold,edgecolors='white',linewidths=.25,zorder=3);ax.text(2,2,'central hole',ha='center',va='center',fontsize=8,color=slate);ax.set_title('Actual set at $n=293$',fontsize=10,color=ink,loc='left',fontweight='bold')
for x in range(5):
 for y in range(5):
  v=0 if x in [0,4]or y in [0,4]else 3*(p-1)if x==y==2 else p-1 if 2 in (x,y) else (p-1)//2
  if v:bx.text(x,y,str(v),ha='center',va='center',fontsize=9,weight='bold',color=ink,bbox={'facecolor':'#e6efec','edgecolor':'none','boxstyle':'round,pad=.22'})
  elif (x in (0,4)) !=(y in(0,4)):bx.scatter(x,y,s=22,edgecolors=gold,facecolors='white',zorder=3,linewidth=.9)
bx.set_title('Disjoint blocking pairs',fontsize=10,color=ink,loc='left',fontweight='bold');fig.subplots_adjust(left=.035,right=.99,bottom=.105,top=.89,wspace=.17);fig.savefig(P/'ring-figure.pdf',bbox_inches='tight',pad_inches=.07);plt.close(fig)
