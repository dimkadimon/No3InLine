// Verify the actual finite set from a compact certificate, independently of the matching search.
// c++ -O3 -std=c++17 verify_example.cpp -o check; ./check < certificate.txt
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <utility>
#include <vector>
using namespace std;
using I = int64_t; using U = uint64_t;
using P = pair<int,int>;
void insist(bool ok,const char* msg) {if(!ok){cerr<<"FAIL: "<<msg<<'\n';exit(1);}}
int power(int a,int e,int p) {I s=1,b=a;for(;e;e/=2,b=b*b%p)if(e&1)s=s*b%p;return int(s);}
struct DSU {vector<int> par;explicit DSU(int n):par(n){iota(par.begin(),par.end(),0);}int find(int a){while(a!=par[a]){par[a]=par[par[a]];a=par[a];}return a;}
 void join(int a,int b){a=find(a);b=find(b);if(a!=b)par[max(a,b)]=min(a,b);}};
P dir(int a,int b) {int g=gcd(a,b);insist(g>0,"repeated physical site");a/=g;b/=g;if(a<0||(a==0&&b<0)){a=-a;b=-b;}return {a,b};}
int main(){
 int p,k,m,f;insist(bool(cin>>p>>k>>m>>f),"certificate header");insist(840<p&&p<10000000&&p%840==1&&m>0&&f>=0,"parameters");
 for(int d=2;I(d)*d<=p;++d)insist(p%d,"p is composite");insist(0<k&&k<p&&power(k,(p-1)/2,p)==p-1,"level not a nonsquare");
 int top=4*p;vector<P> special={{0,p},{0,3*p},{p,0},{3*p,0},{top,p},{top,3*p},{p,top},{3*p,top}};
 for(int i=0;i<m;++i){int x,y;insist(bool(cin>>x>>y),"missing representative");special.emplace_back(x,y);special.emplace_back(top-x,top-y);}
 set<int> flip;for(int i=0;i<f;++i){int u;insist(bool(cin>>u),"missing component");flip.insert(u);}insist((int)flip.size()==f,"non-distinct flips");int trailing;insist(!(cin>>trailing),"extra integers");
 set<P> specials(special.begin(),special.end());insist(specials.size()==special.size(),"duplicate anchor or target");
 for(auto [x,y]:special){insist(0<=x&&x<=top&&0<=y&&y<=top,"off board");insist(specials.count({top-x,top-y}),"specials not half-turn invariant");insist(I(x)*y%p!=k,"special on conic");}
 // Independent description of the bit: connected components under multiplication by 3, negation and reciprocal k/u.
 vector<int> v(p);DSU d(p);for(int u=1;u<p;++u){v[u]=I(k)*power(u,p-2,p)%p;d.join(u,p-u);d.join(u,3LL*u%p);d.join(u,v[u]);}
 for(int u:flip)insist(u>0&&u<p&&d.find(u)==u,"flip label not the minimum of its component");
 vector<int> colour(p); vector<P> old;old.reserve(6*(p-1));for(int u=1;u<p;++u){colour[u]=(power(u,(p-1)/2,p)!=1)^flip.count(d.find(u));}
 for(int u=1;u<p;++u){insist(colour[u]==colour[p-u]&&v[p-u]==p-v[u],"half-turn of fibre not respected");int ct=0;
   for(int i=0;i<4;++i)for(int j=0;j<4;++j){if(0<i&&i<3&&0<j&&j<3)continue;int x=u+i*p,y=v[u]+j*p;
    if((x+y)%2==colour[u]){insist(I(x)*y%p==k,"old point outside conic");old.emplace_back(x,y);++ct;}}
   insist(ct==6,"incorrect fibre size");}
 // Prove completeness of this finite old-triple direction screen by enumerating the two masks. Every physical line meets at most two different conic residues, so a triple has a same-fibre pair.
 set<P> dirs;for(int c:{0,1}){vector<P> mask;for(int i=0;i<4;++i)for(int j=0;j<4;++j)if((i==0||j==0||i==3||j==3)&&(i+j)%2==c)mask.emplace_back(i,j);
   for(auto a:mask)for(auto b:mask)if(a!=b)dirs.insert(dir(a.first-b.first,a.second-b.second));}
 for(auto [a,b]:dirs){int lo=top*(min(b,0)-max(a,0)),hi=top*(max(b,0)-min(a,0));vector<unsigned char> hit(hi-lo+1);
   for(auto [x,y]:old)insist(++hit[b*x-a*y-lo]<=2,"three old points on a physical line");}
 cout<<"prime="<<p<<" side="<<top+1<<" old="<<old.size()<<" anchors=8 central="<<2*m<<" total="<<old.size()+special.size()<<"\n";
 cout<<"complete same-fibre direction set="<<dirs.size()<<"; integer line intercepts checked against every old point: PASS\n";
 // No structure assumptions for any triple touching an anchor or target. Equal canonical directions at that point are exactly a collinear triple, regardless of slope or distance.
 I tested=0;vector<U> keys;keys.reserve(old.size()+special.size());for(auto [x,y]:special){keys.clear();auto emit=[&](int X,int Y){auto[a,b]=dir(X-x,Y-y);keys.push_back((U(a)<<32) | uint32_t(b+top));};
   for(auto [X,Y]:old)emit(X,Y);for(auto [X,Y]:special)if(X!=x||Y!=y)emit(X,Y);sort(keys.begin(),keys.end());insist(adjacent_find(keys.begin(),keys.end())==keys.end(),"triple through anchor or target");tested+=keys.size();}
 cout<<special.size()<<" full ordinary direction screens; directions checked="<<tested<<": PASS\n";
 cout<<"half-turn, cardinality, old/old/old and all triples involving additions: PASS\n";
}
