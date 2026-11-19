// Dynamic local search on ordinary grid points modulo 1, 2 or 4 rotations.
// Input: N order iterations seed output.csv [zero-based input.csv]. Feasibility is checked separately.
// A pair of occupied orbits sends a counter and two algebraic moments to all orbits
// met by a cross-orbit secant. Two moments identify both blockers when count<=2.
#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;using U=uint64_t;int n,g,m,side;U rs;U rnd(){rs^=rs<<13;rs^=rs>>7;return rs^=rs<<17;}
struct P{short x,y;};P rotate(P a){return {(short)(n-1-a.y),a.x};}vector<array<P,4>>orb;vector<int>idx,active,ap,cl,slot,cnt,tabu;vector<U>s1,s2;vector<vector<int>>binary,B(3);vector<P>delta;
int at(P p){return p.y*n+p.x;}void bucket(int i){int c=(ap[i]<0&&cnt[i]<3)?cnt[i]:-1;if(c==cl[i])return;if(cl[i]>=0){auto&b=B[cl[i]];int u=b.back();b[slot[i]]=u;slot[u]=slot[i];b.pop_back();}cl[i]=c;if(c>=0){slot[i]=B[c].size();B[c].push_back(i);}}
inline void change(int i,int d,U key,U square){cnt[i]+=d;if(d>0){s1[i]+=key;s2[i]+=square;}else{s1[i]-=key;s2[i]-=square;}if(cnt[i]<4)bucket(i);}
template<class Fn>inline void line(P p,P q,Fn action){auto v=delta[(q.x-p.x+n-1)*side+q.y-p.y+n-1];int dx=v.x,dy=v.y;for(int a=p.x,b=p.y;a>=0&&a<n&&b>=0&&b<n;a+=dx,b+=dy)action(idx[b*n+a]);for(int a=p.x-dx,b=p.y-dy;a>=0&&a<n&&b>=0&&b<n;a-=dx,b-=dy)action(idx[b*n+a]);}
void edit(int i,int d){if(d<0){int j=active.back();active[ap[i]]=j;ap[j]=ap[i];active.pop_back();ap[i]=-1;}else assert(ap[i]<0&&cnt[i]==0);U key=U(i)*m+i;for(int j:binary[i])change(j,d,key,key*key);
 for(int j:active){int a=min(i,j),b=max(i,j);U k=U(a)*m+b,ks=k*k;P z=orb[i][0];for(int t=0;t<g;t++)line(z,orb[j][t],[&](int v){if(v>=0&&v!=i&&v!=j)change(v,d,k,ks);});}
 if(d>0){ap[i]=active.size();active.push_back(i);}bucket(i);}
void save(const char*path,const vector<int>&S){ofstream f(path);f<<"x,y\n";for(int u:S)for(int j=0;j<g;j++)f<<orb[u][j].x<<","<<orb[u][j].y<<"\n";}
int main(int ac,char**av){if(ac<6)return 2;n=stoi(av[1]);g=stoi(av[2]);if(n>490 || !(g==1||g==2||g==4))return 2;long iters=stol(av[3]);rs=stoull(av[4]);idx.assign(n*n,-1);side=2*n-1;delta.resize(side*side);
 for(int a=1-n;a<n;a++)for(int b=1-n;b<n;b++)if(a||b){int h=gcd(abs(a),abs(b));delta[(a+n-1)*side+(b+n-1)]={(short)(a/h),(short)(b/h)};}
 for(short y=0;y<n;y++)for(short x=0;x<n;x++){P q{x,y};if(idx[at(q)]>=0||(g>1&&2*x==n-1&&2*y==n-1))continue;array<P,4>W;for(int t=0;t<g;t++){W[t]=q;idx[at(q)]=orb.size();for(int z=0;z<4/g;z++)q=rotate(q);}orb.push_back(W);}m=orb.size();if(m>65535)return 2;binary.resize(m);
 for(int i=0;i<m;i++)for(int t=1;t<g;t++)line(orb[i][0],orb[i][t],[&](int j){if(j>=0&&j!=i){binary[i].push_back(j);binary[j].push_back(i);}});
 for(auto&v:binary){sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());}cnt.resize(m);s1.resize(m);s2.resize(m);ap.assign(m,-1);cl.assign(m,-1);slot.resize(m);tabu.assign(m,-100);for(int i=0;i<m;i++)bucket(i);
 if(ac>6){ifstream f(av[6]);string s;getline(f,s);vector<int>z;int x,y;char c;while(f>>x>>c>>y){if(c!=','||min(x,y)<0||max(x,y)>=n)return 2;int j=idx[y*n+x];if(j<0)return 2;z.push_back(j);}sort(z.begin(),z.end());for(size_t t=0;t<z.size();t+=g){if(t+g>z.size()||z[t+g-1]!=z[t])return 2;edit(z[t],1);}}
 vector<int>win=active;save(av[5],win);int freq=30000,offset=win.size(),best=win.size(),resets=0;
 for(long t=1;t<=iters;t++){
  if(t%freq==0&&active.size()+4<win.size()){vector<char>in(m);for(int i:win)in[i]=1;auto V=active;for(int i:V)if(!in[i])edit(i,-1);for(int i:win)if(ap[i]<0)edit(i,1);resets++;}
  int c=0;if(B[c].empty()){int temp=(t%freq<3000)?80:18;if(!B[1].empty()&&int(rnd()%1000)>=temp)c=1;else if(!B[2].empty())c=2;else if(!B[1].empty())c=1;else {if(active.empty())break;edit(active[rnd()%active.size()],-1);continue;}}
  int i=B[c][rnd()%B[c].size()];if(c&&t-tabu[i]<12)continue;U h=s1[i],k=h;int a=-1,b=-1;
  if(c==2){U sq=2*s2[i]-h*h,root=(U)(sqrt((long double)sq)+0.5L);assert(root*root==sq);k=(h-root)/2;h-=k;}
  if(c){int u=k/m,v=k%m;if(c==2&&(u==int(h/m)||u==int(h%m)))a=u;else if(c==2&&(v==int(h/m)||v==int(h%m)))a=v;else a=(rnd()&1)?u:v;
   if(c==2&&a!=int(h/m)&&a!=int(h%m)){b=(rnd()&1)?int(h/m):int(h%m);}assert(ap[a]>=0);edit(a,-1);tabu[a]=t;if(b>=0){assert(ap[b]>=0);edit(b,-1);tabu[b]=t;}}
  assert(cnt[i]==0);edit(i,1);if(int(active.size())>best){win=active;best=win.size();save(av[5],win);if(best>offset&&best*g>=int(n*1.65))cerr<<"n="<<n<<" g="<<g<<" step="<<t<<" best="<<best*g<<"\n";}}
 cout<<"final n="<<n<<" order="<<g<<" points="<<best*g<<" resets="<<resets<<"\n";}
