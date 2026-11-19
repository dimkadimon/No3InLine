// Unrestricted positive exchanges from a modular frame with published or other insertions.
// Usage: exchanges original_additions scan_file max_initial_frame_secants runs output [seed].
// Input/output use zero-based ordinary integer coordinates. No numerical tolerances.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <unordered_map>
#include <vector>
using namespace std;using I=int64_t;using U=uint64_t;
struct Pt{int x,y;bool operator<(const Pt&b)const{return x<b.x||(x==b.x&&y<b.y);}bool operator==(const Pt&b)const{return x==b.x&&y==b.y;}};
int p,h,N,nb,nold;vector<Pt> old,F,Q;vector<vector<pair<int,int>>> blocks;vector<int> iv,sq;vector<vector<int>> fiber;vector<unsigned char>removed,taken;vector<int>added;mt19937 rng;
U direction(Pt a,Pt b){int x=b.x-a.x,y=b.y-a.y,g=gcd(abs(x),abs(y));x/=g;y/=g;if(x<0||(!x&&y<0))x=-x,y=-y;return (U(x)<<32)|uint32_t(y);}
struct cachehash{size_t operator()(U x)const{x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;return x^(x>>31);}};
int mod(I x){return int((x%p+p)%p);}bool col(Pt a,Pt b,Pt q){return I(b.x-a.x)*(q.y-a.y)==I(b.y-a.y)*(q.x-a.x);}
struct Ed{int a=-1,b=-1;void add(int u){if(u==a||u==b)return;if(a<0)a=u;else if(b<0)b=u;else{cerr<<"old set not clean\n";exit(2);}}};
unordered_map<U,Ed,cachehash> memo;
Ed pair_old(int i,int j){if(i<j)swap(i,j);U key=(U(i)<<32)|j;auto it=memo.find(key);if(it!=memo.end())return it->second;Pt u=Q[i],v=Q[j];int dx=v.x-u.x,dy=v.y-u.y;if(dx%p==0&&dy%p==0){dx/=p;dy/=p;}int a=mod(dy),b=mod(I(dx)*(u.y-h)-I(dy)*u.x),c=mod(-dx);Ed out;
 auto hit=[&](int z){for(int k:fiber[z])if(col(u,v,old[k]))out.add(k);};
 if(a){int d=sq[mod(I(b)*b-4LL*a*c)];if(d>=0){int inv=iv[(2*a)%p];hit(mod(I(-b+d)*inv));if(d)hit(mod(I(-b-d)*inv));}}
 else if(b)hit(mod(-I(c)*iv[b]));
 for(int t=nb;t<nold;t++)if(col(u,v,old[t]))out.add(t);
 if(memo.size()<2500000)memo.emplace(key,out);return out;
}
bool dead(int t,int victim){return t<0||t==victim||removed[t];}
bool compatible(int q,int victim){vector<U>dirs;dirs.reserve(added.size());for(int i:added){auto z=pair_old(q,i);if(!dead(z.a,victim)||!dead(z.b,victim))return false;dirs.push_back(direction(Q[q],Q[i]));}sort(dirs.begin(),dirs.end());return adjacent_find(dirs.begin(),dirs.end())==dirs.end();}
struct Tags{vector<U> keys;vector<int>stamp,val;int token=0,mask;Tags(int k){int s=1;while(s<3*k)s*=2;mask=s-1;keys.resize(s);stamp.resize(s);val.resize(s);}void reset(){token++;}int put(U q,int v){int i=cachehash{}(q)&mask;while(stamp[i]==token){if(keys[i]==q)return val[i];i=(i+1)&mask;}stamp[i]=token;keys[i]=q;val[i]=v;return -1;}};
int main(int argc,char**argv){if(argc<6)return 2;ifstream f(argv[1]),scan(argv[2]);int mx=atoi(argv[3]),runs=atoi(argv[4]),k;f>>p>>k;h=p/2;N=2*p;iv.resize(p);sq.assign(p,-1);fiber.resize(p);iv[1]=1;for(int a=2;a<p;a++)iv[a]=p-I(p/a)*iv[p%a]%p;for(int a=0;a<p;a++)sq[I(a)*a%p]=a;
 for(int a=1;a<p;a++){int b=(iv[a]+h)%p;for(int x:{a,a+p})for(int y:{b,b+p})if(!(x>h&&x<=h+p&&y>h&&y<=h+p)){fiber[a].push_back(old.size());old.push_back({x,y});}}
 nb=old.size();Pt u;for(int i=0;i<k;i++){if(!(f>>u.x>>u.y))return 2;old.push_back(u);F.push_back(u);}nold=old.size();set<Pt>occupied(old.begin(),old.end());if(occupied.size()!=old.size())return 2;set<Pt>seen;Tags tag(nold);int d;while(scan>>u.x>>u.y>>d){if(d>mx||occupied.count(u)||!seen.insert(u).second)continue;vector<pair<int,int>>b;tag.reset();for(int j=0;j<nold;j++){int t=tag.put(direction(u,old[j]),j);if(t>=0){b.push_back({t,j});if(int(b.size())>mx)break;}}if(int(b.size())<=mx){Q.push_back(u);blocks.push_back(b);}}
 int nq=Q.size();rng.seed(argc>6?stoul(argv[6]):42791);cout<<"p="<<p<<" initial="<<nold<<" pool="<<nq<<" (including mixed-pair filters)\n"<<flush;int record=-1;
 for(int run=0;run<runs;run++){removed.assign(nold,0);taken.assign(nq,0);added.clear();int lost=0;vector<int>perm(nq),order(nold);iota(perm.begin(),perm.end(),0);iota(order.begin(),order.end(),0);bool gain=true;while(gain){gain=false;shuffle(perm.begin(),perm.end(),rng);shuffle(order.begin(),order.end(),rng);vector<vector<int>>bucket(nold);
 for(int q:perm)if(!taken[q]){int ct=0,a=-1,b=-1;for(auto e:blocks[q])if(!removed[e.first]&&!removed[e.second]){ct++;a=e.first;b=e.second;}if(!ct){if(compatible(q,-1)){taken[q]=1;added.push_back(q);gain=true;}}else if(ct==1){bucket[a].push_back(q);bucket[b].push_back(q);}}
 for(int r:order)if(!removed[r]&&bucket[r].size()>=2){vector<int>local;for(int q:bucket[r])if(!taken[q]&&compatible(q,r)){local.push_back(q);added.push_back(q);}if(local.size()>=2){lost++;removed[r]=1;for(int q:local)taken[q]=1;gain=true;}else added.resize(added.size()-local.size());}
 }
 int total=nold-lost+added.size();if(total>record){record=total;ofstream o(argv[5]);int nr=accumulate(removed.begin(),removed.begin()+nb,0);o<<p<<" "<<nr<<" "<<total-(nb-nr)<<"\n";for(int i=0;i<nb;i++)if(removed[i])o<<old[i].x<<" "<<old[i].y<<"\n";for(int i=nb;i<nold;i++)if(!removed[i])o<<old[i].x<<" "<<old[i].y<<"\n";for(int i:added)o<<Q[i].x<<" "<<Q[i].y<<"\n";cout<<"run="<<run<<" total="<<total<<" added="<<added.size()<<" removed="<<lost<<" seed_deletions="<<nr<<"\n"<<flush;}}
}
