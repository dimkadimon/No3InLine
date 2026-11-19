// Identify extra depth-two candidates whose original blocking line is hit by a current deletion.
// Usage: enrich p previous-edits original-depth-scan > new candidates (x y).
#include <fstream>
#include <iostream>
#include <vector>
#include <array>
using namespace std;using I=long long;struct P{int x,y;bool operator==(P b)const{return x==b.x&&y==b.y;}};int main(int ac,char**av){if(ac!=4)return 2;int p=stoi(av[1]),h=p/2;ifstream f(av[2]),s(av[3]);int q,nr,na;f>>q>>nr>>na;if(q!=p)return 2;vector<P>R(nr);for(auto&v:R)f>>v.x>>v.y;vector<int>iv(p);iv[1]=1;for(int a=2;a<p;a++)iv[a]=p-I(p/a)*iv[p%a]%p;vector<vector<P>>root(p);for(int a=1;a<p;a++){int b=(h+iv[a])%p;for(int x:{a,a+p})for(int y:{b,b+p})if(!(h<x&&x<=h+p&&h<y&&y<=h+p))root[a].push_back({x,y});}int x,y,d,k=0;while(s>>x>>y>>d)if(d>=2){bool good=false;for(P r:R){int dx=x-r.x,dy=y-r.y;if(!dx&&!dy)continue;if(dx%p==0&&dy%p==0){dx/=p;dy/=p;}auto scan=[&](int a){for(P v:root[a])if(!(v==r)&&I(v.x-r.x)*dy==I(v.y-r.y)*dx)return true;return false;};if((abs(dx)<=abs(p)&&abs(dy)<=abs(p))&&(dx==0||dy==0||abs(dx)==abs(dy)))good=scan(r.x%p);if(!good&&dy%p!=0){int a=int(((-I(dx)*iv[(p+dy%p)%p])%p)*iv[r.x%p]%p);a=(a+p)%p;if(a!=r.x%p)good=scan(a);}if(good)break;}if(good){cout<<x<<" "<<y<<"\n";k++;}}cerr<<"p="<<p<<" targeted candidates="<<k<<"\n";}
