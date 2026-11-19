#!/usr/bin/env python3
"""R3 manuscript diagrams. First two use actual certified sites; the third is a labelled schematic.
Run: python3 scripts/construction_diagrams.py [--previews DIR]. Matplotlib is only needed to redraw.
The prebuilt vector PDFs are sufficient to typeset the manuscript. Does not modify the reviewed R2 replay kit.
"""
import argparse, csv, io, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, FancyBboxPatch

R=Path(__file__).resolve().parents[1];P=R/'paper/figures';P.mkdir(parents=True,exist_ok=True)
INK='#172F45';TEAL='#086E6A';OCHRE='#A94223';SOFT='#E6F2EF';PALE='#F6F9FA';GRID='#B7C6CE';GRAY='#45606F';MUT='#788D99'
plt.rcParams.update({'font.family':'DejaVu Sans','mathtext.fontset':'dejavusans','font.size':8.4,'text.color':INK,'axes.labelcolor':GRAY,'xtick.color':GRAY,'ytick.color':GRAY,'pdf.fonttype':42,'axes.unicode_minus':False,'svg.hashsalt':'no3-diagrams-r3'})
def block(f,pos,xlim,ylim):
    ax=f.add_axes(pos);ax.set(xlim=xlim,ylim=ylim);ax.set_axis_off();return ax
def text(ax,x,y,txt,fs=8.3,**k):return ax.text(x,y,txt,fontsize=fs,**k)
def head(f,x,title):f.text(x,.965,title,fontsize=10.0,fontweight='bold',ha='left',va='top',color=INK)
def arrow(ax,a,b,color=MUT):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=11,linewidth=1.15,color=color,shrinkA=1,shrinkB=1))
def save(f,name,previews):
    # No printed dates in the manuscript/diagrams. Fixed metadata makes redraws reproducible.
    f.savefig(P/(name+'.pdf'),facecolor='white',metadata={'Creator':'No3InLine diagram generator','Title':name.replace('-',' '),'CreationDate':None,'ModDate':None})
    if previews:
        previews.mkdir(parents=True,exist_ok=True);f.savefig(previews/(name+'.png'),dpi=175,facecolor='white')
    plt.close(f)
def square(ax,hole=True,grid=True):
    ax.add_patch(Rectangle((0,0),4,4,facecolor=PALE,edgecolor=INK,lw=1.0,zorder=0))
    if hole:ax.add_patch(Rectangle((1,1),2,2,fc=SOFT,ec='none',zorder=.1))
    if grid:
        for i in (1,2,3):ax.plot([i,i],[0,4],c=GRID,lw=.55,zorder=.2);ax.plot([0,4],[i,i],c=GRID,lw=.55,zorder=.2)
    ax.set_aspect('equal');ax.set_xlim(-.18,4.18);ax.set_ylim(-.18,4.18);ax.set_axis_off()
def marker(ax,x,y,style,size,col,filled=True,z=5):
    ax.scatter([x],[y],s=size,marker=style,facecolors=col if filled else 'white',edgecolors=col,linewidths=1.15,zorder=z,clip_on=False)
def masks(previews):
    p=73;k=28;fibre=(47,27);u,v=fibre;assert u*v%p==k
    S={(int(z['x']),int(z['y'])) for z in csv.DictReader((R/'small-prime-examples/coordinates/p73.csv').open())}
    q=(131,122);mate=(4*p-q[0],4*p-q[1]);assert q in S and mate in S and len(S)==450
    outer=[(i,j) for i in range(4) for j in range(4) if i in (0,3) or j in (0,3)]
    initial={(i,j) for i,j in outer if (u+i*p+v+j*p)%2==(pow(u,(p-1)//2,p)!=1)}
    final={(i,j) for i,j in outer if (u+i*p,v+j*p) in S};assert len(initial)==len(final)==6 and not(initial&final) and (2,3) in initial and (2,3) not in final
    A=[(0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4)];assert {(a*p,b*p) for a,b in A}<=S
    f=plt.figure(figsize=(6.6,2.86));head(f,.022,'A   The physical board');head(f,.410,'B   One fibre, two masks')
    figax=f.add_axes([.015,.116,.354,.724]);square(figax)
    for i,j in outer:marker(figax,i+u/p,j+v/p,'o',20,TEAL,(i,j) in initial)
    for a,b in A:marker(figax,a,b,'s',23,INK)
    z=[(x/p,y/p) for x,y in (q,mate)];figax.plot([z[0][0],z[1][0]],[z[0][1],z[1][1]],color=OCHRE,ls=(0,(2,2)),lw=1.0)
    for x,y in z:marker(figax,x,y,'D',28,OCHRE)
    text(figax,z[0][0]-.21,z[0][1]+.04,'$q$',8.7,ha='right',va='center');text(figax,z[1][0]+.15,z[1][1]+.15,'$2C-q$',8.7,ha='left',va='bottom');text(figax,1.86,2.79,'central hole',7.7,ha='center',color=TEAL)
    text(figax,0,-.23,'0',7,ha='center',va='top');text(figax,4,-.23,'$4p$',7,ha='center',va='top');f.text(.039,.044,'Squares: eight fixed anchors',fontsize=7.9,color=INK)
    for left,d,lab in ((.410,initial,'Before the flip'),(.737,final,'After the flip')):
        ax=f.add_axes([left,.294,.249,.451]);square(ax)
        for i,j in outer:marker(ax,i+.5,j+.5,'o',24,TEAL,(i,j) in d)
        # Outline the actual sheet address of the blocker (193,246) in both masks.
        ax.add_patch(Rectangle((2.05,3.05),.9,.9,fill=False,ec=OCHRE,lw=1.25,zorder=7))
        f.text(left+.124,.793,lab,fontsize=8.6,ha='center',va='center',color=GRAY)
        f.text(left+.124,.241,'6 selected',fontsize=8.4,ha='center',va='center',fontweight='bold',color=TEAL)
    guide=block(f,[0,0,1,1],(0,1),(0,1));arrow(guide,(.663,.519),(.730,.519),TEAL)
    f.text(.413,.135,'Filled = selected     Open = alternative',fontsize=7.9,color=INK)
    f.text(.413,.044,'Outlined cell: the blocker leaves the ring.',fontsize=7.9,color=OCHRE)
    save(f,'ring-and-masks',previews)

def pt(q,t,v):return tuple(x+t*a for x,a in zip(q,v))
def matching(previews):
    raw=list(map(int,(R/'unbounded-gain/data/certificate.txt').read_text().split()));p,k,m,nf=raw[:4];reps=[tuple(raw[4+2*j:6+2*j]) for j in range(m)];flips=set(raw[4+2*m:]);assert (p,k,m,len(flips))==(797161,11,2,nf)
    q,z=reps; assert z==q[::-1];H={1};v=3
    while v not in H:H.add(v);v=3*v%p
    H|={p-u for u in H};assert len(H)==26
    def cos(u):return min(u*h%p for h in H)
    def labels(X):
        x,y=X;assert 0<=min(x,y) and max(x,y)<=4*p and x*y%p==k and (x//p in (0,3) or y//p in (0,3))
        c=cos(x%p);c2=cos(y%p);assert c2==cos(k*pow(x,-1,p)%p);bit=min(c,c2)
        before=int((x+y)%2==(pow(x,(p-1)//2,p)!=1));after=before^int(bit in flips);return c,c2,bit,before,after
    A=pt(q,155653,(3,11));B=pt(q,-14051,(3,11));AT=A[::-1];BT=B[::-1];assert AT==pt(z,155653,(11,3)) and BT==pt(z,-14051,(11,3))
    sites=[A,B,AT,BT];recs=[labels(X) for X in sites];assert recs==[(46139,55495,46139,1,1),(5045,71735,5045,1,0),(55495,46139,46139,0,0),(71735,5045,5045,0,1)]
    csvout=io.StringIO();w=csv.writer(csvout,lineterminator='\n');w.writerow(['point','qx','qy','x','y','coset_min','partner_min','bit_min','before_selected','after_selected']);
    for name,root,X,rc in zip(['P','S','P_transpose','S_transpose'],[q,q,z,z],sites,recs):w.writerow([name,*root,*X,*rc])
    (R/'results/diagram-endpoints.csv').write_text(csvout.getvalue())
    f=plt.figure(figsize=(6.6,2.78));head(f,.02,'A   Two physical secants');head(f,.410,'B   Two clauses, two bits')
    ax=f.add_axes([.005,.145,.372,.706]);square(ax,True,False)
    ax.plot([0,4],[0,4],ls=(0,(2,3)),color=GRID,lw=.7,zorder=1)
    for root,v in [(q,(3,11)),(z,(11,3))]:
        a,b=(t/p for t in root);mins=max(-a/v[0],-b/v[1]);mx=min((4-a)/v[0],(4-b)/v[1]);ax.plot([a+mins*v[0],a+mx*v[0]],[b+mins*v[1],b+mx*v[1]],lw=1.15,color=GRAY,zorder=2)
    for X,Rc,lab,dx,dy in zip(sites,recs,['$P$','$S$','$P^{T}$','$S^{T}$'],[.12,.18,.13,-.19],[.10,-.22,.22,.18]):
        x,y=(a/p for a in X);marker(ax,x,y,'o',34,TEAL,bool(Rc[-1]));text(ax,x+dx,y+dy,lab,8.4,ha='left' if dx>0 else 'right',va='center',color=TEAL)
    for r,lab,dx,dy in ((q,'$q$',.22,.14),(z,'$q^{T}$',-.35,-.35)):
        x,y=(a/p for a in r);marker(ax,x,y,'D',25,OCHRE);text(ax,x+dx,y+dy,lab,8.6,ha='left' if dx>0 else 'right',va='center',color=OCHRE)
    f.text(.023,.055,'Filled: retained    Open: absent',fontsize=7.8,color=TEAL)
    g=block(f,[.401,.128,.594,.72],(0,1),(0,1));yl,yh=.25,.76;lx,rx=.345,.62
    for a,b,solid in ((yh,yl,False),(yl,yh,False),(yl,yl,True),(yh,yh,True)):
        g.plot([lx,rx],[a,b],c=TEAL if solid else MUT,lw=2.0 if solid else .9,ls='-' if solid else (0,(3,2)),zorder=1)
    for y,main,sub in [(yh,'Secant at $q$','$P$  or  $S$'),(yl,'Secant at $q^{T}$','$P^{T}$  or  $S^{T}$')]:
        g.add_patch(FancyBboxPatch((.021,y-.136),.316,.272,boxstyle='round,pad=0.008,rounding_size=0.024',fc=PALE,ec=GRID,lw=.85));text(g,.17,y+.032,main,8.1,ha='center',va='center',fontweight='bold');text(g,.17,y-.055,sub,7.6,ha='center',va='center',color=GRAY)
    for y,mv,sub in [(yh,'Flip 5,045','omit $S$'),(yl,'Keep 46,139','omit $P^{T}$')]:
        g.add_patch(FancyBboxPatch((rx,y-.136),.36,.272,boxstyle='round,pad=0.008,rounding_size=0.024',fc=SOFT,ec=TEAL,lw=1.05));text(g,rx+.18,y+.033,mv,8.2,ha='center',va='center',fontweight='bold',color=TEAL);text(g,rx+.18,y-.057,sub,7.8,ha='center',va='center',color=INK)
    f.text(.410,.055,'Solid: assigned bit    Dashed: other choice',fontsize=7.8,color=GRAY);save(f,'matched-secants',previews)

def pruning(previews):
    # An illustrative hypergraph, not a claimed sample of lattice coordinates.
    f=plt.figure(figsize=(6.6,2.05));head(f,.017,'A   Mark conflicts at one level');head(f,.561,'B   Keep an independent family')
    pos={1:(.08,.60),2:(.28,.60),3:(.52,.70),4:(.71,.33),5:(.89,.70),6:(.16,.15)};edges=[{1,2},{3,4,5}];cut={2,4};surv=sorted(pos.keys()-cut);assert all(cut&e for e in edges)
    ax=block(f,[.013,.19,.477,.60],(0,1),(0,1));ax.plot([.08,.28],[.60,.60],lw=1.8,c=OCHRE);ax.add_patch(Polygon([pos[k] for k in (3,4,5)],closed=True,fc='#F6E8E0',ec=OCHRE,lw=1.0,ls=(0,(3,2))))
    def node(a,x,y,k):
        marker(a,x,y,'o',150,TEAL,False);text(a,x,y,str(k),8.4,ha='center',va='center',color=TEAL,fontweight='bold',zorder=6)
    for k,(x,y) in pos.items():node(ax,x,y,k)
    g=block(f,[.561,.19,.418,.60],(0,1),(0,1));
    for k,(x,y) in zip(surv,((.10,.62),(.36,.62),(.62,.62),(.88,.62))):node(g,x,y,k)
    text(g,.5,.12,'Four indices give eight sites.',8.0,ha='center',color=TEAL)
    guide=block(f,[0,0,1,1],(0,1),(0,1));arrow(guide,(.483,.50),(.546,.50),INK)
    f.text(.017,.075,'Line: a bad pair.  Shaded triangle: a bad triple.',fontsize=7.75,color=GRAY)
    f.text(.561,.075,'Discard indices 2 and 4, not ring sites.',fontsize=7.75,color=GRAY)
    save(f,'shared-level-selection',previews)
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--previews',type=Path);args=ap.parse_args();masks(args.previews);matching(args.previews);pruning(args.previews);print('PASS exact mask flip, both physical secants and their coset/bit data; three vector diagrams written.')
