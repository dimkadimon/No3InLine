"""Fold the centrally symmetric restricted physical line model, exactly."""
from array import array
from collections import Counter
import sys
v=array('i');assert v.itemsize==4
with open(sys.argv[1],'rb')as f:v.frombytes(f.read())
n,N=v[:2];P=[tuple(v[i:i+3])for i in range(2,2+3*N,3)];U={(x,y):a for x,y,a in P};flip=lambda x,y:(n-1-x,n-1-y);V=sorted((x,y,a)for x,y,a in P if (x,y)<flip(x,y));assert len(V)*2==N;dic={q:i for i,(x,y,a) in enumerate(V)for q in [(x,y),flip(x,y)]};assert all(U[flip(x,y)]==a for x,y,a in V);ids=[dic[x,y]for x,y,a in P];L=set();i=2+3*N
while (k:=v[i]):
 A=sorted(ids[j] for j in v[i+1:i+1+k]);i+=1+k;B=tuple(sorted(set(A)))
 if len(A)==len(B):L.add((2,B))
 else:assert len(A)==2*len(B);L.add((1,B))
o=array('i',(n,len(V)));o.extend(u for z in V for u in z)
for cap,e in sorted(L):o.append(len(e)*(1 if cap==2 else -1));o.extend(e)
o.append(0)
with open(sys.argv[2],'wb')as f:o.tofile(f)
print('n',n,'orbits',len(V),'line models',dict(Counter(c for c,e in L)),flush=True)
