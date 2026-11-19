// Construct the finite example in the note. This is NOT needed for the theorem.
// c++ -O3 -std=c++17 match_example.cpp -o match; ./match > certificate.txt
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using namespace std;
using I = int64_t; using U = uint64_t;
constexpr int p=797161, k=11, top=4*p, stride=2*top+1;
struct Point {int x,y;};
struct DirectionSite {U direction; unsigned site;};
struct Endpoint {int bit, on, coset;};
using Clause = array<Endpoint,2>;
void check(bool x) {if(!x){cerr << "construction check failed\n"; exit(1);}}
U direction(int a, int b) {int g=gcd(a,b); check(g>0); if(a<0||(a==0&&b<0))g=-g; return U(a/g)*stride+(b/g+top);}
int main(){
  vector<int> inv(p), rep(p), mate(p); vector<char> sq(p); inv[1]=1;
  for(int a=1;a<p;++a){sq[I(a)*a%p]=1; if(a>1)inv[a]=p-I(p/a)*inv[p%a]%p;}
  vector<int> H, reps;
  for(int v=1;;){H.push_back(v);H.push_back(p-v);v=I(3)*v%p;if(v==1)break;}
  sort(H.begin(),H.end());H.erase(unique(H.begin(),H.end()),H.end());
  for(int a=1;a<p;++a)if(!rep[a]){reps.push_back(a);for(int h:H)rep[I(a)*h%p]=a;}
  for(int a:reps)mate[a]=rep[I(k)*inv[a]%p];
  check(!sq[k]);check((int)H.size()*(int)reps.size()==p-1);
  vector<Point> sites;sites.reserve(12*(p-1));
  for(int u=1;u<p;++u)for(int i=0;i<=3;++i)for(int j=0;j<=3;++j)
    if(i==0||i==3||j==0||j==3)sites.push_back({u+i*p,int(I(k)*inv[u]%p)+j*p});
  vector<Point> roots={{1591070,845785},{845785,1591070}};
  vector<Clause> cls;set<int> cosets;int reference_hits=0;
  auto ident=[&](Point z){int u=z.x%p, r=rep[u];return Endpoint{min(r,mate[r]),((z.x+z.y)&1)^(!sq[u]),r};};
  for(Point q:roots){vector<DirectionSite> lines;lines.reserve(sites.size());
    for(unsigned i=0;i<sites.size();++i){int a=sites[i].x-q.x, b=sites[i].y-q.y;if(a&&b)lines.push_back({direction(a,b),i});}
    sort(lines.begin(),lines.end(),[](const DirectionSite&a,const DirectionSite&b){return a.direction!=b.direction?a.direction<b.direction:a.site<b.site;});
    int old_count=cls.size(),ref=0;
    for(size_t i=0,j;i<lines.size();i=j){for(j=i+1;j<lines.size()&&lines[j].direction==lines[i].direction;++j){}
      for(size_t a=i;a<j;++a)for(size_t b=a+1;b<j;++b){auto A=ident(sites[lines[a].site]),B=ident(sites[lines[b].site]);
        cosets.insert(A.coset);cosets.insert(B.coset);cls.push_back({A,B});ref+=!A.on&&!B.on;}}
    cerr<<"representative "<<q.x<<","<<q.y<<": potential secants="<<cls.size()-old_count<<", initially blocking="<<ref<<"\n";reference_hits+=ref;
  }
  // Find an injection from physical clauses to bits. Prefer disabling an endpoint already off.
  vector<int> owner(p,-1),seen(p,-1),chosen(cls.size(),-1);
  auto augment=[&](auto self,int row,int epoch)->bool {auto c=cls[row];if(c[1].on>c[0].on)swap(c[0],c[1]);
    for(auto ep:c){int b=ep.bit;if(seen[b]==epoch)continue;seen[b]=epoch;
      if(owner[b]<0||self(self,owner[b],epoch)){owner[b]=row;chosen[row]=b;return true;}}
    return false;};
  int matched=0; for(int i=0;i<(int)cls.size();++i)matched+=augment(augment,i,i);
  cerr<<"p="<<p<<" level="<<k<<" subgroup order="<<H.size()<<" index="<<reps.size()<<"\n"
      <<"nonaxial physical clauses="<<cls.size()<<" coset occurrences="<<2*cls.size()<<" distinct cosets="<<cosets.size()<<" initial blocking secants="<<reference_hits<<"\n"
      <<"matched="<<matched<<"\n";check(matched==(int)cls.size());
  set<int> flips;
  for(int i=0;i<matched;++i){auto c=cls[i];if(c[1].on>c[0].on)swap(c[0],c[1]);for(auto ep:c)if(ep.bit==chosen[i]){if(!ep.on)flips.insert(ep.bit);break;}}
  for(auto c:cls)check(c[0].on!=int(flips.count(c[0].bit))||c[1].on!=int(flips.count(c[1].bit)));
  cerr<<"flipped components="<<flips.size()<<"\n";
  cout<<p<<' '<<k<<' '<<roots.size()<<' '<<flips.size()<<'\n';for(auto q:roots)cout<<q.x<<' '<<q.y<<'\n';for(int x:flips)cout<<x<<'\n';
}
