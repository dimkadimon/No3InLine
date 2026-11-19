// Standalone exact verifier; shares neither the search code nor its modular intersection routine.
// c++ -std=c++17 -O3 verify_frame.cpp -o verify_frame; ./verify_frame edits.txt [expanded.csv]
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <vector>
using Point=std::pair<int,int>;
void require(bool ok,const char*s){if(!ok)throw std::runtime_error(s);}
int power(int a,int e,int p){int64_t x=a,r=1;while(e){if(e%2)r=r*x%p;x=x*x%p;e/=2;}return int(r);}
int main(int argc,char**argv){try{
 require(argc==2||argc==3,"usage: verify_frame edit_file [csv_file]");std::ifstream f(argv[1]);int p,nr,na;require(bool(f>>p>>nr>>na),"bad header");require(p>2&&p<10000000&&nr>=0&&na>=0,"unsupported parameters");for(int d=2;int64_t(d)*d<=p;d++)require(p%d!=0,"modulus is not prime");int n=2*p,h=(p-1)/2;
 std::set<Point>S,extras;
 for(int x=0;x<n;x++)if(x%p){int r=(power(x%p,p-2,p)+h)%p;for(int y=r;y<n;y+=p){require(int64_t(x)*(y-h)%p==1 || int64_t(x)*(y-h)%p==1-p,"invalid base congruence");if(!(h<x&&x<=h+p&&h<y&&y<=h+p))S.insert({x,y});}}
 require(int(S.size())==3*(p-1),"base size mismatch");
 for(int i=0;i<nr;i++){int x,y;require(bool(f>>x>>y)&&S.erase({x,y})==1,"impossible or repeated deletion");}
 // A primitive Euclidean line reduces to a genuine line mod p. The conic x*(y-h)=1 meets
 // it in at most two residues. A collinear base triple would thus contain a congruent pair,
 // whose displacement in this box is (ap,bp), a,b in {-1,0,1}: only four directions.
 std::vector<int>X(n),Y(n),plus(2*n),minus(2*n);
 for(auto [x,y]:S)require(++X[x]<=2 && ++Y[y]<=2 && ++plus[x+y]<=2 && ++minus[x-y+n-1]<=2,"retained frame has a forbidden line");
 int retained=S.size();for(int i=0;i<na;i++){int x,y;require(bool(f>>x>>y)&&x>=0&&y>=0&&x<n&&y<n,"bad addition");Point u{x,y};require(!S.count(u)&&extras.insert(u).second,"duplicate point");}std::string tail;require(!(f>>tail),"trailing data");S.insert(extras.begin(),extras.end());require(int(S.size())<=2*n,"row-cap excess");
 std::vector<Point>P(S.begin(),S.end());std::vector<std::pair<int,int>>dirs;dirs.reserve(P.size());
 for(auto [u,v]:extras){dirs.clear();for(auto [x,y]:P){int a=x-u,b=y-v;if(!a&&!b)continue;int d=std::gcd(std::abs(a),std::abs(b));if(b<0||(!b&&a<0))d=-d;dirs.emplace_back(b/d,a/d);}std::sort(dirs.begin(),dirs.end());require(std::adjacent_find(dirs.begin(),dirs.end())==dirs.end(),"collinear triple through an added site");}
 if(argc==3){std::ofstream out(argv[2]);require(bool(out),"CSV open failed");out<<"x,y\n";for(auto [x,y]:P)out<<x<<','<<y<<'\n';}
 std::cout<<"VERIFIED n="<<n<<" p="<<p<<" retained="<<retained<<" removed="<<nr<<" additions="<<na<<" total="<<S.size()<<" exact_anchor_directions="<<uint64_t(na)*(P.size()-1)<<"\n";return 0;
 }catch(const std::exception&e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
