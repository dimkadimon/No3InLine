"""Build the self-contained illustration from the actual final and prior sets. Standard library."""
from pathlib import Path
import csv,json,base64,struct
D=Path(__file__).resolve().parents[1];S=D/'sources';data={}
def csvset(f):
 with f.open() as g:return {(int(x),int(y))for x,y in list(csv.reader(g))[1:]}
for n in (293,389,4037,10085,16018,32002,64006):
 A=csvset(D/'coordinates'/f'n{n}.csv');public=n%2==0
 if public:
  p=n//2;h=p//2;B={(x,y)for a in range(1,p)for b in[(h+pow(a,-1,p))%p]for x in (a,a+p)for y in(b,b+p)if not(h<x<=h+p and h<y<=h+p)};B|={tuple(map(int,l.split()))for l in(S/f'insertions_{p}.txt').read_text().splitlines()[1:]};X={tuple(q)for q in json.loads((D/'data'/f'append{n}.json').read_text())['compatible_additions']};ex=[min(A-B)]
  heading='Exchange on a modular frame';story=f'Remove {len(B-A):,} of the published points and insert {len(A-B):,} others. The result is a net gain of {len(A)-len(B):,} points on the same board.';context='The published reference is the coordinate set in rStation paper 47, section 8. The modular core is regenerated from its exact formula.'
 else:
  B=csvset(S/f'previous{n}.csv');X=set();x,y=min(A);ex=[(x,y),(n-1-x,n-1-y)];heading='Half-turn symmetry';story=f'Rotate the board 180 degrees about its centre: the set is unchanged. Its {len(A)//2:,} opposite pairs give {len(A):,} points.';context='The previous construction kept the original ring fixed. This search may delete ring points as well as insert new ones.'
  if n<400:
   ex=[(x,y),(n-1-y,x),(n-1-x,n-1-y),(y,n-1-x)];heading='Quarter-turn symmetry';story=f'Rotate the board 90 degrees about its centre: the set is unchanged. Its {len(A)//4:,} four-point orbits give {len(A):,} points.';context=('The preceding project set had 446 points. A crop of a published side-300 example already gives 504 here; the new set is four larger than that crop.' if n==293 else 'The 74-point gain is against our preceding 594-point half-turn example. It is not a claim about the previous global record for this side.')
 assert set(ex)<=A and not X&B
 packed=b''.join(struct.pack('<HHB',*q,(q in B)+2*(q in A)+4*(q in X))for q in sorted(A|B|X));data[n]=dict(public=public,after=len(A),before=len(B),drop=len(B-A),insert=len(A-B),example=ex,extras=sorted(X),heading=heading,story=story,context=context,packed=base64.b64encode(packed).decode('ascii'))
text=(D/'code'/'explore-template.html').read_text();assert text.count('__DATA__')==1;(D/'explore.html').write_text(text.replace('__DATA__',json.dumps(data,separators=(',',':'))));print('Built seven exact point-set layers.',flush=True)
