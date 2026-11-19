// Independent exact whole-board enumeration of single-point extensions of the p=8009 frame.
// No angular bins, floating point, candidate input, CP-SAT, or search kernel. stdout: p k and points.
// Rows/columns already holding two frame points are excluded. In the other rows/columns,
// strike the lattice points on each remaining seed secant. Coordinates here are zero-based.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>
#include <utility>
using namespace std;
struct Cell{int x,y;};
int inverse(int a,int p){int u=0,v=1,b=p;while(a){int q=b/a,t=b-q*a;b=a;a=t;t=u-q*v;u=v;v=t;}return (u%p+p)%p;}
int main(int argc,char**argv){int p=argc==2?atoi(argv[1]):8009;if(p<3||p>20000||p%2==0)return 2;for(int z=2;z*z<=p;z++)if(p%z==0)return 2;int n=p*2,h=p/2;
 vector<Cell>S;vector<int>cols(n),rows(n);for(int x=0;x<n;++x){if(x%p==0)continue;int v=inverse(x%p,p);for(int y=(v+h)%p;y<n;y+=p){if(x>=h+1&&x<=h+p&&y>=h+1&&y<=h+p)continue;S.push_back({x,y});cols[x]++;rows[y]++;}}
 if(S.size()!=size_t(3*(p-1)))return 2;vector<int>cx(n,-1),ry(n,-1);int w=0,ht=0;for(int t=0;t<n;t++){if(cols[t]<2)cx[t]=w++;if(rows[t]<2)ry[t]=ht++;}
 vector<uint64_t>bits((size_t(w)*ht+63)/64);auto strike=[&](int x,int y){if(cx[x]>=0&&ry[y]>=0){size_t k=size_t(ry[y])*w+cx[x];bits[k>>6]|=uint64_t(1)<<(k&63);}};for(auto s:S)strike(s.x,s.y);
 // Integer line walking: start at the first lattice point of the *board* on the secant.
 // The seed may be outside the admissible unsaturated region; do not stop at its boundary.
 for(size_t j=1;j<S.size();j++){int u=S[j].x,v=S[j].y;for(size_t i=0;i<j;i++){int X=u-S[i].x,Y=v-S[i].y;if(!X||!Y)continue; // horizontal/vertical pair has already killed its row/column
  int g=gcd(abs(X),abs(Y)),a=X/g,b=Y/g;int kx=a>0?u/a:(n-1-u)/(-a),ky=b>0?v/b:(n-1-v)/(-b),k=min(kx,ky);int x=u-k*a,y=v-k*b;for(;(unsigned)x<(unsigned)n&&(unsigned)y<(unsigned)n;x+=a,y+=b)strike(x,y);
 }}vector<Cell>Q;for(int x=0;x<n;x++)if(cx[x]>=0)for(int y=0;y<n;y++)if(ry[y]>=0){size_t k=size_t(ry[y])*w+cx[x];if(!(bits[k>>6]>>(k&63)&1))Q.push_back({x,y});}
 cout<<p<<' '<<Q.size()<<'\n';for(auto q:Q)cout<<q.x<<' '<<q.y<<'\n';cerr<<"whole board side="<<n<<" admissible columns="<<w<<" rows="<<ht<<" frame="<<S.size()<<" free="<<Q.size()<<"\n";
}
