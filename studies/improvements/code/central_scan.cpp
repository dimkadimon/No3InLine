// Rasterize every seed-pair line, clipped to the closed central square. Count to depth d only.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;int lo(int x,int a){return x>=0?(x+a-1)/a:x/a;}int hi(int x,int a){return x>=0?x/a:-((-x+a-1)/a);}
int main(int argc,char**av){if(argc!=4)return 2;int n=stoi(av[1]),p=(n-1)/4,D=stoi(av[2]),w=2*p+1;vector<unsigned char>ct(size_t(w)*w);vector<pair<int,int>>P;ifstream f(av[3]);string header;getline(f,header);char c;int x,y;while(f>>x>>c>>y)P.emplace_back(x-p,y-p);sort(P.begin(),P.end());for(size_t i=0;i<P.size();i++){auto[x,y]=P[i];for(size_t j=i+1;j<P.size();j++){auto[a,b]=P[j];a-=x;b-=y;int g=gcd(a,b);a/=g;b/=g;int l=-999999,r=999999;if(a){l=lo(-x,a);r=hi(w-1-x,a);}else if(x<0||x>=w)continue;if(b>0){l=max(l,lo(-y,b));r=min(r,hi(w-1-y,b));}else if(b<0){l=max(l,lo(y-w+1,-b));r=min(r,hi(y,-b));}else if(y<0||y>=w)continue;if(l>r)continue;int v=(y+l*b)*w+x+l*a,step=b*w+a;for(;l<=r;l++,v+=step){if(ct[v]<=D)ct[v]++;}}}for(auto[x,y]:P)if(x>=0&&x<w&&y>=0&&y<w)ct[y*w+x]=255;vector<int>hist(D+1);for(y=0;y<w;y++)for(x=0;x<w;x++){int s=ct[y*w+x];if(s<=D){hist[s]++;cout<<p+x<<' '<<p+y<<' '<<s<<'\n';}}cerr<<"n="<<n<<" depth counts";for(int k:hist)cerr<<' '<<k;cerr<<'\n';}
