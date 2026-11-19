// Input: a stream of n, count then count coordinate pairs. Independent of all modular rules.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using namespace std;int main(){ios::sync_with_stdio(false);uint64_t cases=0,dirs=0;int n,k;while(cin>>n>>k){vector<pair<int,int>>P(k);for(auto&[x,y]:P){if(!(cin>>x>>y)||min(x,y)<0||max(x,y)>=n)return 2;}set<pair<int,int>>S(P.begin(),P.end());if(int(S.size())!=k)return 3;vector<pair<int,int>>D;D.reserve(k);for(auto [x,y]:P){if(!S.count({n-1-x,n-1-y}))return 4;D.clear();for(auto [a,b]:P){int u=a-x,v=b-y;if(!u&&!v)continue;int g=gcd(u,v);if(u<0||(!u&&v<0))g=-g;D.emplace_back(u/g,v/g);}sort(D.begin(),D.end());auto it=adjacent_find(D.begin(),D.end());if(it!=D.end()){cerr<<"FAIL n="<<n<<" k="<<k<<" through "<<x<<","<<y<<" direction "<<it->first<<","<<it->second<<"\n";return 5;}}dirs+=uint64_t(k)*(k-1);cases++;}cout<<"PASS "<<cases<<" whole-board tests; "<<dirs<<" ordered exact integer directions, plus half-turn, uniqueness and coordinate bounds.\n";}
