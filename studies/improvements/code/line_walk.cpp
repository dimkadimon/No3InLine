// Heuristic local search on induced ordinary line capacities. Input from pool.cpp.
// No claims of optimality; certify output independently. Each line can hold 0,1,2 points.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;using U=uint64_t;U seed;U rnd(){seed^=seed<<13;seed^=seed>>7;return seed^=seed<<17;}
struct P{int x,y,init;};struct L{int a=-1,b=-1,cap=2;vector<int>v;};int nv,n,score,top;vector<P>P0;vector<L>ls;vector<vector<int>>adj,box;vector<int>pos,cls,hits,last;vector<char>active,winner;
void bucket(int u){int c=(!active[u]&&hits[u]<=4)?hits[u]:-1;if(cls[u]==c)return;if(cls[u]>=0){auto &b=box[cls[u]];int x=b.back();b[pos[u]]=x;pos[x]=pos[u];b.pop_back();}cls[u]=c;if(c>=0){pos[u]=box[c].size();box[c].push_back(u);}}
void update(int u,int val){assert(bool(val)!=bool(active[u]));active[u]=val;score+=val?1:-1;bucket(u);for(int id:adj[u]){auto&l=ls[id];bool was=(l.cap==1?l.a>=0:l.b>=0);if(val){assert(!was);if(l.a<0)l.a=u;else l.b=u;}else{if(l.a==u)l.a=l.b;else assert(l.b==u);l.b=-1;}bool now=(l.cap==1?l.a>=0:l.b>=0);if(was!=now){for(int v:l.v){hits[v]+=now?1:-1;bucket(v);}}}}
void load(vector<char> const&S){for(int i=0;i<nv;i++)if(active[i]&&!S[i])update(i,0);for(int i=0;i<nv;i++)if(!active[i]&&S[i])update(i,1);}
int main(int ac,char**av){if(ac<5)return 2;ifstream f(av[1],ios::binary);auto get=[&](){int a;if(!f.read((char*)&a,4))throw 1;return a;};n=get();nv=get();P0.resize(nv);adj.resize(nv);for(auto&z:P0){z.x=get();z.y=get();z.init=get();}for(int k;(k=get());){int id=ls.size();ls.emplace_back();if(k<0){ls.back().cap=1;k=-k;}for(int j=0;j<k;j++){int a=get();adj[a].push_back(id);ls.back().v.push_back(a);}}
 int iters=stoi(av[2]);seed=stoull(av[3]);box.resize(5);pos.resize(nv);cls.assign(nv,-1);hits.resize(nv);last.assign(nv,-100);active.assign(nv,0);for(int i=0;i<nv;i++)bucket(i);for(int i=0;i<nv;i++)if(P0[i].init)update(i,1);top=score;winner=active;
 if(ac>5){ifstream prev(av[5]);if(prev){vector<char>prevset(nv);int j;while(prev>>j)prevset[j]=1;load(prevset);if(score>=top)top=score,winner=active;}}
 cerr<<"n="<<n<<" vars="<<nv<<" lines="<<ls.size()<<" initial="<<score<<"\n";int epoch=80000,low=0;
 auto save=[&](){ofstream out(av[4]);for(int i=0;i<nv;i++)if(winner[i])out<<i<<'\n';};save();
 for(int t=1;t<=iters;t++){if(t%epoch==0){load(winner);low=0;}int c=0;int noise=(t%epoch<epoch/8)?85:15;if(box[0].empty()){if(!box[1].empty()&&int(rnd()%1000)>=noise)c=1;else if(!box[2].empty())c=2;else if(!box[1].empty())c=1;else if(!box[3].empty())c=3;else break;}int v=box[c][rnd()%box[c].size()];if(c&&t-last[v]<8)continue;vector<int>victim;for(int i:adj[v]){auto &l=ls[i];if(l.cap==1){if(l.a>=0)victim.push_back(l.a);continue;}if(l.b<0)continue;int u=l.a,w=l.b;
 // Prefer deleting a point that opens many currently saturated lines, with some noise.
 if(rnd()%6==0){if(hits[u]<hits[w])u=w;}else if(rnd()&1)u=w;victim.push_back(u);}
 for(int u:victim)if(active[u]){update(u,0);last[u]=t;}assert(hits[v]==0);update(v,1);if(score>top){top=score;winner=active;save();if(top%10==0 || top<10000)cerr<<"step="<<t<<" points="<<top<<"\n";}if(score<top-32&&++low>=200){load(winner);low=0;}}
 cerr<<"final best n="<<n<<" points="<<top<<"\n";}
