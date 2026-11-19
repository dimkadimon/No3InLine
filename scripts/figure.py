#!/usr/bin/env python3
"""Draw the opening example from its certificate and check the two stages.

The board, the six-for-six switch and the line show the same side-293 example.
Matplotlib is needed only to redraw; the TeX distribution includes the vector PDF.
"""
import csv
from datetime import datetime, timezone
from math import gcd
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'small-prime-examples'
values = list(map(int, (S/'certificates/p73.txt').read_text().split()))
p, k, m, nflip = values[:4]
reps = set(zip(values[4:4+2*m:2], values[5:4+2*m:2]))
flips = set(values[4+2*m:])
assert (p, k, m, nflip, flips) == (73, 28, 5, 1, {1})
span = 4*p
mate = lambda q: (span-q[0], span-q[1])
proposals = reps | {mate(q) for q in reps}
anchors = {(p*i, p*j) for i, j in ((0,1),(0,3),(1,0),(3,0),(4,1),(4,3),(1,4),(3,4))}

H = {1}
u = 3
while u not in H:
    H.add(u)
    u = 3*u % p
H |= {(-v) % p for v in H}
assert len(H) == 12


def make_ring(switched):
    ring = set()
    for u in range(1, p):
        v = k*pow(u, -1, p) % p
        # Least element of the union of the two partner cosets is the switch label.
        switch = min({u*a % p for a in H} | {v*a % p for a in H})
        parity = int(pow(u, (p-1)//2, p) != 1) ^ (switch in switched)
        copies = {(u+i*p, v+j*p) for i in range(4) for j in range(4)
                  if i in (0,3) or j in (0,3)}
        keep = {(x,y) for x,y in copies if (x+y) % 2 == parity}
        assert (len(copies), len(keep)) == (12, 6)
        ring |= keep
    return ring


def directions(points, q):
    """Group physical sites on each whole line through q (not directed rays)."""
    groups = {}
    for x, y in points - {q}:
        a, b = x-q[0], y-q[1]
        d = gcd(a, b) if (a > 0 or (a == 0 and b > 0)) else -gcd(a, b)
        groups.setdefault((a//d, b//d), set()).add((x, y))
    return groups


def check_cap(points):
    assert {mate(q) for q in points} == points
    assert all(len(directions(points, q)) == len(points)-1 for q in points)


before, after = make_ring(set()), make_ring(flips)
q, stays, leaves = (131,122), (96,52), (193,246)
assert len(before) == len(after) == 432 and len(before - after) == len(after - before) == 144
assert q in reps and mate(q) == (161,170) and leaves == (47+2*p, 27+3*p)
assert [v for v in directions(before | anchors, q).values() if len(v) > 1] == [{stays, leaves}]
assert stays in before & after and leaves in before - after
assert all(y == 2*x-140 for x, y in (q, stays, leaves))
one_pair = after | anchors | {q, mate(q)}
final = after | anchors | proposals
assert [len(x) for x in (before | anchors, after | anchors, one_pair, final)] == [440, 440, 442, 450]
with (S/'coordinates/p73.csv').open() as f:
    assert final == {(int(r['x']), int(r['y'])) for r in csv.DictReader(f)}
for pts in (before | anchors, one_pair, final):
    check_cap(pts)

ink, ring_col, anchor_col, new_col = '#172f45', '#516374', '#005c70', '#a33e22'
grid, stroke = '#c2cbd0', '#79868d'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':8.2,
                     'text.color':ink, 'pdf.fonttype':42, 'axes.unicode_minus':False})
f = plt.figure(figsize=(7.0, 2.94))
board = f.add_axes([.050, .172, .313, .715])
board.set_aspect('equal'); board.set(xlim=(-7, span+7), ylim=(-7, span+7),
                                    xticks=(0,146,292), yticks=(0,146,292))
board.tick_params(length=0, pad=1, labelsize=7)
for spine in board.spines.values():
    spine.set_visible(False)
# For every seed the outer twelve tiles alternate between two colours; the
# colours are schematic, but every dot is at its certified physical location.
for i in range(4):
    for j in range(4):
        middle = i in (1,2) and j in (1,2)
        colour = '#e2eeec' if middle else ('#eff2f3' if (i+j) % 2 else 'white')
        board.add_patch(Rectangle((i*p, j*p), p, p, fc=colour, ec=grid, lw=.45, zorder=-3))
board.add_patch(Rectangle((0,0), span, span, fc='none', ec=stroke, lw=.7, zorder=-2))
board.plot([70,216], [0,span], color=stroke, lw=.8, linestyle=(0,(3,2)), zorder=-1)
for points, mark, col, size in ((after,'o',ring_col,3.1),(anchors,'s',anchor_col,22),(proposals,'D',new_col,15.5)):
    xs, ys = zip(*sorted(points))
    board.scatter(xs, ys, s=size, marker=mark, c=col, linewidths=0, zorder=3)
for x, title in ((.056, 'The final board'), (.391, 'One seed'), (.561, 'One line through the new site')):
    f.text(x, .975, title, va='top', fontsize=9.35, fontweight='bold')
f.text(.391, .842, '(47, 27)', fontsize=7.9, color=ring_col)
f.text(.561, .842, 'The dashed line, drawn horizontally.', fontsize=7.9, color=ring_col)

# The middle panels show the actual membership, not a single moving dot. The
# mark within each tile has the same fractional offset as on the big board.
seed = (47,27)
for cy, old in ((.646, before), (.282, after)):
    patch = f.add_axes([.391, cy-.139, .118, .278], aspect='equal')
    patch.set(xlim=(-.07,4.07), ylim=(-.07,4.07)); patch.axis('off')
    selected = []
    for i in range(4):
        for j in range(4):
            centre = i in (1,2) and j in (1,2)
            fc = '#e2eeec' if centre else ('#f1f3f4' if (i+j)%2 else 'white')
            patch.add_patch(Rectangle((i,j),1,1,fc=fc,ec=grid,lw=.56))
            if (seed[0]+p*i,seed[1]+p*j) in old:
                selected.append((i+seed[0]/p, j+seed[1]/p))
    assert len(selected) == 6
    patch.add_patch(Rectangle((0,0),4,4,fc='none',ec=stroke,lw=.70))
    patch.add_patch(Rectangle((2,3),1,1,fc='none',ec=new_col,lw=1.03))
    patch.scatter(*zip(*selected), s=11, marker='o', c=ring_col, linewidths=0, zorder=3)

line = f.add_axes([.557,.08,.427,.72]); line.axis('off')
line.set(xlim=(-.12,1.13), ylim=(0,1))
# Keep the actual positions along the line in their correct ratio (35:62).
t = (q[0]-stays[0])/(leaves[0]-stays[0]); top, bottom = (.646-.08)/.72, (.282-.08)/.72
for y, label in ((top, 'Before: site blocked'), (bottom, 'After: site added')):
    line.text(-.105,y+.12,label,va='bottom',fontsize=8.05, fontweight='bold')
    line.plot([-.09,1.08],[y,y],color='#91a1a9',lw=.95,zorder=0)
    line.scatter([0],[y],s=30,c=ring_col,linewidths=0,zorder=2)
line.scatter([1],[top],s=30,c=ring_col,linewidths=0,zorder=2)
line.scatter([t],[top],marker='D',s=28,facecolors='white',edgecolors=new_col,linewidths=1.2,zorder=2)
line.scatter([t],[bottom],marker='D',s=30,facecolors=new_col,edgecolors=new_col,linewidths=.8,zorder=2)
line.scatter([1],[bottom],marker='x',s=31,c=stroke,linewidths=1.3,zorder=2)
for x, lab in ((0,'(96, 52)'), (t,'(131, 122)'), (1,'(193, 246)')):
    line.text(x, bottom-.123, lab, ha='center', va='center', fontsize=7.5, color=ring_col)
handles = [Line2D([],[],ls='',marker=mark,ms=4.9,color=col,label=label)
           for mark,col,label in [('o',ring_col,'Ring'),('s',anchor_col,'Anchor'),('D',new_col,'Added')]]
f.legend(handles=handles,loc='lower left',bbox_to_anchor=(.04,.015),frameon=False,ncol=3,
         handlelength=.8, columnspacing=1.1, handletextpad=.35,fontsize=7.9)
w = ROOT/'paper/figures'; w.mkdir(exist_ok=True)
dt = datetime(2026,11,19,tzinfo=timezone.utc)
f.savefig(w/'one-flip.pdf',facecolor='white',metadata={'Creator':'No3InLine figure script',
          'Title':'The ring, a blocked site and a six-for-six flip','CreationDate':dt,'ModDate':dt})
previews = w/'previews'; previews.mkdir(exist_ok=True)
f.savefig(previews/'one-flip.png', dpi=165, facecolor='white')
plt.close(f)
print('PASS side 293: 432 ring points and 8 anchors; flip exchanges 144 for 144. Exact geometry at 440, 442 and 450 points; final coordinates equal p73.csv.')
