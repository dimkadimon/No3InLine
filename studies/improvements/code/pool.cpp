// Build an exact finite induced ordinary-line model: all frame points O and the supplied Q.
// Input stdin: n |O| |Q| then O and Q in that order, x y initial(0/1).
// The supplied O must be a cap. All possibly overfull lines then pass through a Q.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
#include <unordered_set>
using namespace std;using U=uint64_t; struct P{int x,y,start;};
unsigned mix(unsigned k){k^=k>>16;k*=0x7feb352d;k^=k>>15;k*=0x846ca68b;return k^(k>>16);}
int main(int argc,char**argv){ios::sync_with_stdio(false);if(argc!=2)return 2;int n,o,k;if(!(cin>>n>>o>>k)||n>65535)return 2;int nv=o+k;vector<P>A(nv);unordered_set<U>seen;for(auto&z:A){cin>>z.x>>z.y>>z.start;if(z.x<0||z.y<0||max(z.x,z.y)>=n||!seen.insert(U(z.x)*n+z.y).second)return 2;}
 int sz=1;while(sz<3*nv)sz*=2;vector<U>keys(sz);vector<int>stamp(sz,-1),head(sz),nxt(nv),list;vector<unsigned char>state(sz);ofstream f(argv[1],ios::binary);auto put=[&](int v){f.write((char*)&v,4);};put(n);put(nv);for(auto q:A){put(q.x);put(q.y);put(q.start);}U nlines=0,ninc=0;
 for(int i=o;i<nv;i++){auto v=A[i];list.clear();for(int j=0;j<nv;j++)if(j!=i){int x=A[j].x-v.x,y=A[j].y-v.y,g=gcd(abs(x),abs(y));if(x<0||(!x&&y<0))g=-g;x/=g;y/=g;U key=U(x)*(2*n+1)+unsigned(y+n);unsigned h=mix(unsigned(key)^unsigned(key>>32)*2654435761u)&(sz-1);while(stamp[h]==i&&keys[h]!=key)h=(h+1)&(sz-1);if(stamp[h]!=i){stamp[h]=i;keys[h]=key;head[h]=-1;state[h]=0;}else if(state[h]==0){list.push_back(h);state[h]=1;}if(j>=o&&j<i)state[h]=2;nxt[j]=head[h];head[h]=j;}
  for(int h:list)if(state[h]==1){int ct=1;for(int j=head[h];j>=0;j=nxt[j])ct++;put(ct);put(i);for(int j=head[h];j>=0;j=nxt[j])put(j);nlines++;ninc+=ct;}}
 put(0);if(!f)return 2;cerr<<"n="<<n<<" old="<<o<<" candidates="<<k<<" constraints="<<nlines<<" incidences="<<ninc<<"\n";}
