// Build a local exact-integer model about a valid seed for the ordinary no-three-in-line problem.
// Input: n k then k zero-based x y pairs. Usage: near_model D [model_file [pool_cap [rng_seed]]].
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using namespace std;
int n;template<class F>void line(int a,int b,F f){int x=a%n,y=a/n,dx=b%n-x,dy=b/n-y,g=gcd(abs(dx),abs(dy));dx/=g;dy/=g;for(int s:{1,-1})for(int u=x+s*dx,v=y+s*dy;u>=0&&u<n&&v>=0&&v<n;u+=s*dx,v+=s*dy)f(u+n*v);}
int main(int argc,char**argv){if(argc<2)return 2;int D=stoi(argv[1]),k;cin>>n>>k;if(n<2||n>5000||D<0||D>30||k<=0||k>2*n)return 2;vector<int>P(k),id(n*n,-1),count(n*n);for(int i=0;i<k;i++){int x,y;if(!(cin>>x>>y)||x<0||y<0||x>=n||y>=n||id[x+y*n]>=0)return 2;P[i]=x+y*n;id[P[i]]=i;}
 for(int i=1;i<k;i++)for(int j=0;j<i;j++)line(P[i],P[j],[&](int z){if(z!=P[j]){if(id[z]>=0){cerr<<"invalid seed\n";exit(2);}++count[z];}});
 vector<int>Q,h(D+1);for(int z=0;z<n*n;z++)if(id[z]<0&&count[z]<=D){Q.push_back(z);h[count[z]]++;}
 cout<<n<<" "<<k;for(int v:h)cout<<" "<<v;cout<<"\n";if(argc<3)return 0;
 if(argc>3){int cap=stoi(argv[3]);mt19937 gen(argc>4?stoul(argv[4]):1);shuffle(Q.begin(),Q.end(),gen);stable_sort(Q.begin(),Q.end(),[&](int a,int b){return count[a]<count[b];});if(cap>0 && int(Q.size())>cap)Q.resize(cap);}
 sort(Q.begin(),Q.end());int q=Q.size();vector<vector<pair<int,int>>> blockers(q);for(int i=0;i<q;i++)id[Q[i]]=k+i;
 for(int i=1;i<k;i++)for(int j=0;j<i;j++)line(P[i],P[j],[&](int z){if(id[z]>=k)blockers[id[z]-k].push_back({j,i});});
 ofstream f(argv[2]);if(!f)return 2;f<<n<<" "<<k<<" "<<q<<"\n";for(int z:P)f<<z<<" ";f<<"\n";for(int i=0;i<q;i++){f<<Q[i]<<" "<<blockers[i].size();for(auto [a,b]:blockers[i])f<<" "<<a<<" "<<b;f<<"\n";}
 // Unique physical lines with >=2 Q and >=3 total sites. Point ids <k are seed points.
 vector<int>l;for(int i=1;i<q;i++)for(int j=0;j<i;j++){l.clear();l.push_back(k+i);int mn=k+i,mn2=k+q;line(Q[i],Q[j],[&](int z){int u=id[z];if(u<0)return;l.push_back(u);if(u>=k){if(u<mn)mn2=mn,mn=u;else if(u<mn2)mn2=u;}});if(mn!=k+j||mn2!=k+i||l.size()<3)continue;f<<l.size();for(int v:l)f<<" "<<v;f<<"\n";}
}
