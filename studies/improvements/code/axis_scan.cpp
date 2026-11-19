// Exact complete search for additions on the four empty modular axes of the initial frame,
// now tested against the entire published set as well. Outside these four lines no completeness claim.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;struct P{int x,y;};using I=int64_t;int main(int ac,char**av){if(ac!=2)return 2;ifstream f(av[1]);int p,k;f>>p>>k;int n=2*p,h=p/2;vector<int>iv(p);iv[1]=1;for(int i=2;i<p;i++)iv[i]=p-I(p/i)*iv[p%i]%p;vector<array<P,3>>X(p),Y(p);vector<P>B;for(int a=1;a<p;a++){int e=iv[a],b=(h+e)%p,j=0;for(int x:{a,a+p})for(int y:{b,b+p})if(!(h<x&&x<=h+p&&h<y&&y<=h+p)){P z{x,y};X[a][j]=Y[e][j]=z;j++;B.push_back(z);}}
 for(int i=0;i<k;i++){P z;f>>z.x>>z.y;B.push_back(z);}vector<int>rows(n),cols(n),plus(2*n),minus(2*n);for(auto z:B){rows[z.y]++;cols[z.x]++;plus[z.x+z.y]++;minus[n-1+z.x-z.y]++;}
 auto test=[&](P z,auto&fib,int s){int x=z.x,y=z.y;if(max({rows[y],cols[x],plus[x+y],minus[n-1+x-y]})>=2)return false;for(int a=1;a<p;a++){int b=s-a;if(b<0)b+=p;if(b<=a)continue;for(P v:fib[a]){I dx=v.x-x,dy=v.y-y;for(P w:fib[b])if(dx*(w.y-y)==dy*(w.x-x))return false;}}
  vector<pair<int,int>>D;for(auto w:B){int a=w.x-x,b=w.y-y;if(!a&&!b)return false;int g=gcd(a,b);if(a<0||(!a&&b<0))g=-g;D.emplace_back(a/g,b/g);}sort(D.begin(),D.end());return adjacent_find(D.begin(),D.end())==D.end();};for(int x:{0,p})for(int y=0;y<n;y++)if(test({x,y},Y,((y-h)%p+p)%p))cout<<x<<' '<<y<<'\n';for(int y:{h,h+p})for(int x=0;x<n;x++)if(x%p&&test({x,y},X,x%p))cout<<x<<' '<<y<<'\n';}
