// All ordinary grid sites that may be individually appended to a supplied frozen cap.
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
using namespace std;int main(int argc,char**argv){if(argc!=4)return 2;int n=stoi(argv[1]);vector<pair<int,int>>P;ifstream f(argv[2]);string l;getline(f,l);while(getline(f,l)){int x,y;char c;istringstream in(l);if(!(in>>x>>c>>y)||c!=',')return 2;P.emplace_back(x,y);}vector<char>hit(n*n);for(int i=0;i<(int)P.size();i++){auto[x,y]=P[i];hit[x*n+y]=1;for(int j=0;j<i;j++){int a=P[j].first-x,b=P[j].second-y,g=gcd(a,b);if(!g)return 3;a/=g;b/=g;for(int X=x+a,Y=y+b;min(X,Y)>=0&&max(X,Y)<n;X+=a,Y+=b)hit[X*n+Y]=1;for(int X=x-a,Y=y-b;min(X,Y)>=0&&max(X,Y)<n;X-=a,Y-=b)hit[X*n+Y]=1;}}
 ofstream out(argv[3]);out<<"x,y\n";int ct=0;for(int x=0;x<n;x++)for(int y=0;y<n;y++)if(!hit[x*n+y]){ct++;out<<x<<","<<y<<"\n";}cout<<"n="<<n<<" frozen="<<P.size()<<" individually_legal="<<ct<<"\n";}
