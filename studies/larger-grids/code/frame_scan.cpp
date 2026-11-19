// For EVERY pair of seed sites, rasterize its ordinary lattice line, clipped to a box.
// Output every cell in the requested box on at most D seed secants. All coordinates zero based.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <numeric>
#include <vector>
#include <array>
#include <cstdlib>
#include <cmath>
using namespace std;
struct Pt{int x,y;};
int ceildiv(int a,int b){return a>=0?(a+b-1)/b:a/b;}int floordiv(int a,int b){return a>=0?a/b:-((-a+b-1)/b);}
int main(int argc,char**argv){if(argc!=8){cerr<<"p x0 x1 y0 y1 D output\n";return 2;}int p=atoi(argv[1]),h=p/2,x0=atoi(argv[2]),x1=atoi(argv[3]),y0=atoi(argv[4]),y1=atoi(argv[5]),D=atoi(argv[6]);if(x0<0||x1>=2*p||y0<0||y1>=2*p||x0>x1||y0>y1||D>240||D<0)return 2;int W=x1-x0+1,H=y1-y0+1;vector<unsigned char>grid(size_t(W)*H,0);vector<Pt>P;vector<int>iv(p,0);iv[1]=1;for(int i=2;i<p;i++)iv[i]=p-int((int64_t(p/i)*iv[p%i])%p);for(int a=1;a<p;a++){int b=(iv[a]+h)%p;for(int x:{a,a+p})for(int y:{b,b+p})if(!(h<x&&x<=h+p&&h<y&&y<=h+p))P.push_back({x,y});}sort(P.begin(),P.end(),[](Pt a,Pt b){return a.x<b.x || (a.x==b.x&&a.y<b.y);});
 // For a fixed first point, first reject all second points outside the cone of lines reaching the box.
 const int bins=2048;vector<vector<int>> bucket(bins);vector<int>which(P.size());
 double R=.5*hypot(W-1,H-1),rm=1e100,pi=acos(-1.0);for(size_t i=0;i<P.size();i++){double x=P[i].x-.5*(x0+x1),y=P[i].y-.5*(y0+y1);rm=min(rm,hypot(x,y));double a=atan2(y,x);if(a<0)a+=pi;if(a>=pi)a-=pi;int b=max(0,min(bins-1,int(bins*a/pi)));which[i]=b;bucket[b].push_back(i);}
 // Optional angular sieve for small tiles. Every line through the tile passes within R of its centre;
 // each radial direction is then within asin(R/rm) of the line, modulo pi. Pad two entire bins.
 int spread=rm>R?int(ceil(2*asin(R/rm)*bins/pi))+2:bins;bool narrow=spread<bins/4;
 for(size_t i=0;i<P.size();i++){int x=P[i].x,y=P[i].y;int cx=x0+x1-2*x,cy=y0+y1-2*y;auto pairvisit=[&](int j){
 int dx=P[j].x-x,dy=P[j].y-y;if(llabs(int64_t(dx)*cy-int64_t(dy)*cx)>int64_t(W-1)*abs(dy)+int64_t(H-1)*dx)return;
 int g=gcd(dx,abs(dy));dx/=g;dy/=g;int lo=-100000000,hi=100000000;
 if(dx){lo=ceildiv(x0-x,dx);hi=floordiv(x1-x,dx);}else if(x<x0||x>x1)return;
 if(dy>0){lo=max(lo,ceildiv(y0-y,dy));hi=min(hi,floordiv(y1-y,dy));}else if(dy<0){lo=max(lo,ceildiv(y-y1,-dy));hi=min(hi,floordiv(y-y0,-dy));}else if(y<y0||y>y1)return;
 if(lo>hi)return;int64_t z=int64_t(y+lo*dy-y0)*W+x+lo*dx-x0,step=int64_t(dy)*W+dx;
 for(int t=lo;t<=hi;++t,z+=step){auto&c=grid[z];if(c<=D)++c;}
 };if(narrow){for(int t=-spread;t<=spread;t++){auto& b=bucket[(which[i]+t+bins)%bins];for(auto it=upper_bound(b.begin(),b.end(),(int)i);it!=b.end();++it)pairvisit(*it);}}else{for(size_t j=i+1;j<P.size();j++)pairvisit(j);}}

 for(auto a:P)if(a.x>=x0&&a.x<=x1&&a.y>=y0&&a.y<=y1)grid[size_t(a.y-y0)*W+a.x-x0]=255;
 ofstream f(argv[7]);vector<int64_t>hist(D+1);for(int y=y0;y<=y1;y++)for(int x=x0;x<=x1;x++){auto b=grid[size_t(y-y0)*W+x-x0];if(b<=D){hist[b]++;f<<x<<" "<<y<<" "<<int(b)<<"\n";}}
 cout<<"p="<<p<<" box="<<x0<<":"<<x1<<","<<y0<<":"<<y1<<" seed="<<P.size()<<" hist:";for(auto c:hist)cout<<" "<<c;cout<<"\n";
}
