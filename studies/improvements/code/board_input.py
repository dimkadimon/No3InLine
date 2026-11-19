import csv,sys
from pathlib import Path
n=int(sys.argv[1]);depth=int(sys.argv[2]);D=Path(__file__).resolve().parents[1]/'sources'
def rd(path):
 with path.open()as f:return {tuple(map(int,r))for r in list(csv.reader(f))[1:]}
O=rd(D/f'seed{n}.csv');S=rd(D/f'previous{n}.csv');Q={(x,y)for x,y,d in(map(int,l.split())for l in sys.stdin)if d<=depth}|(S-O);Q-=O
print(n,len(O),len(Q));print('\n'.join(f'{x} {y} {int((x,y)in S)}'for W in (sorted(O),sorted(Q))for x,y in W))
