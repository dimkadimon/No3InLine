import itertools,json,math,collections,sys
from pathlib import Path
from ortools.sat.python import cp_model
import networkx as nx
p=int(sys.argv[1]);n=2*p;h=p//2
S={(x,y)for a in range(1,p)for b in [(pow(a,-1,p)+h)%p]for x in(a,a+p)for y in (b,b+p)if not(h<x<=h+p and h<y<=h+p)}
Q=[tuple(map(int,z.split())) for z in Path(f'free{p}.txt').read_text().splitlines()[1:]];id={q:i for i,q in enumerate(Q)};G=nx.Graph();G.add_nodes_from(range(len(Q)));lines=set();pairroot={}
for i,(x,y) in enumerate(Q):
 for j in range(i):
  a,b=Q[j];dx=x-a;dy=y-b;g=math.gcd(dx,dy);dx//=g;dy//=g;root=[];ix={i}
  for sign in (-1,1):
   u=x+sign*dx;v=y+sign*dy
   while 0<=u<n and 0<=v<n:
    if (u,v) in S:root.append((u,v))
    if (u,v) in id:ix.add(id[u,v]);
    u+=sign*dx;v+=sign*dy
  assert len(root)<=1
  if root:G.add_edge(i,j);pairroot[i,j]=root[0]
  elif len(ix)>2:lines.add(tuple(sorted(ix)))
clq=[tuple(sorted(C)) for C in nx.find_cliques(G) if len(C)>1]
groups=sorted({(q,1)for q in clq}|{(q,2)for q in lines});M=cp_model.CpModel();V=collections.defaultdict(list);choices=[];terms=[]
for g,c in groups:
 enable=M.new_bool_var('');members=[enable]*len(g) if len(g)==c+1 else [M.new_bool_var('')for j in g]
 if len(g)>c+1:
  for a in members:M.add(a<=enable)
  M.add(sum(members)>=(c+1)*enable)
 for i,b in zip(g,members):V[i].append(b)
 choices.append((enable,members));terms.append(sum(members)-c*enable)
for a in V.values():M.add_at_most_one(a)
M.maximize(sum(terms));sol=cp_model.CpSolver();sol.parameters.num_workers=1;sol.parameters.max_time_in_seconds=30;status=sol.solve(M);print('free, edges, lines, maximal cliques, savings, upper',len(Q),G.number_of_edges(),len(lines),len(clq),sol.objective_value,len(Q)-sol.objective_value,sol.status_name(status));out=[]
for (enable,members),(g,c) in zip(choices,groups):
 if not sol.value(enable):continue
 t=[i for i,v in zip(g,members) if sol.value(v)];group={'sites':[Q[i]for i in t],'capacity':c}
 if c==1:group['pair_blockers']=[pairroot[max(i,j),min(i,j)]for i,j in itertools.combinations(t,2)]
 out.append(group)
print('groups',collections.Counter((len(v['sites']),v['capacity'])for v in out));Path(f'cover{p}.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
