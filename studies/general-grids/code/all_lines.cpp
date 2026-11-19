// Independent exhaustive geometry check, no modular, colouring, construction or slope-height logic.
// c++ -O3 -std=c++17 all_lines.cpp -o check; ./check n points.csv [number_expected] [--ordinary]
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <utility>
#include <vector>
using namespace std;
int main(int argc,char**argv){bool ord=argc>1 && string(argv[argc-1])=="--ordinary";if(ord)--argc;if(argc<3||argc>4)return 2;int n=stoi(argv[1]);if(n<1||n>10000000)return 2;ifstream f(argv[2]);string line;getline(f,line);if(line.size()&&line.back()=='\r')line.pop_back();if(line!="x,y")return 2;vector<pair<int,int>>P;while(getline(f,line)){if(line.empty())continue;auto i=line.find(',');if(i==string::npos)return 2;int x=stoi(line.substr(0,i)),y=stoi(line.substr(i+1));if(x<0||y<0||x>=n||y>=n)return 3;P.emplace_back(x,y);}set<pair<int,int>>S(P.begin(),P.end());if(S.size()!=P.size()||(argc==4&&int(S.size())!=stoi(argv[3])))return 3;bool half=true;for(auto [x,y]:P)if(!S.count({n-1-x,n-1-y})){half=false;break;}if(!half&&!ord)return 4;vector<pair<int,int>>dirs;dirs.reserve(P.size());for(auto [x,y]:P){dirs.clear();for(auto [u,v]:P){int a=u-x,b=v-y;if(!a&&!b)continue;int d=gcd(a,b);if(b<0||(!b&&a<0))d=-d;dirs.emplace_back(a/d,b/d);}sort(dirs.begin(),dirs.end());if(adjacent_find(dirs.begin(),dirs.end())!=dirs.end()){cerr<<"collinear through "<<x<<","<<y<<"\n";return 5;}}cout<<"PASS n="<<n<<" points="<<P.size()<<" half_turn="<<(half?"yes":"no")<<" full_integer_directions="<<uint64_t(P.size())*(P.size()-1)<<"\n";}
