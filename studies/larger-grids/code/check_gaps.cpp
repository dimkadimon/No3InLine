// Independent, direct integer-determinant check of gap insertions in five catalogue seeds.
// One Flammenkamp row per line. Stop counting a given gap after exceeding the best-so-far.
#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;
int main(){string w,alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,.";int index=0;while(cin>>w){int m=(w.size()-1)/2,n=m+1,k=2*m+1;if(m>80||m<1)return 2;vector<pair<int,int>>seed;for(int i=1;i<=2*m;i++){int x=alphabet.find(w[i]);if(x<0||x>=m)return 2;seed.emplace_back(x,(i-1)/2);}int best=1<<27,ties=0,zero=0;for(int a=0;a<=m;a++)for(int b=0;b<=m;b++){int X[170],Y[170];X[0]=a;Y[0]=b;for(int j=1;j<k;j++){auto[x,y]=seed[j-1];X[j]=x+(x>=a);Y[j]=y+(y>=b);}int c=0;for(int i=0;i<k&&c<=best;i++)for(int j=i+1;j<k&&c<=best;j++){int dx=X[j]-X[i],dy=Y[j]-Y[i];for(int t=j+1;t<k;t++)c+=(dx*(Y[t]-Y[i])==dy*(X[t]-X[i]));}if(c==0)zero++;if(c<best){best=c;ties=0;}if(c==best)ties++;}cout<<++index<<","<<n<<","<<n*n<<","<<best<<","<<ties<<","<<zero<<"\n"<<flush;}return 0;}
