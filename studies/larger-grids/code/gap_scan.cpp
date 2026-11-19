// Test all m+1 row gaps and m+1 column gaps of a given ordinary 2m-set. After inserting empty lines,
// insert their intersection; count all collinear triples in these 2m+1-point candidate sets.
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;struct Pt {int x,y;};
int main(){int m,k;cin>>m>>k;if(m>120||k!=2*m)return 2;vector<Pt>P(k);for(auto&v:P)cin>>v.x>>v.y;int n=m+1;vector<vector<int>>diff(n+1,vector<int>(n+1)),extra(n,vector<int>(n));
 for(int a=0;a<k;a++)for(int b=0;b<a;b++)for(int c=0;c<b;c++){array<int,5>X={0,P[a].x+1,P[b].x+1,P[c].x+1,n},Y={0,P[a].y+1,P[b].y+1,P[c].y+1,n};sort(X.begin(),X.end());sort(Y.begin(),Y.end());int dx=P[b].x-P[a].x,dy=P[b].y-P[a].y,ex=P[c].x-P[a].x,ey=P[c].y-P[a].y;if(abs(dx*ey-dy*ex)>abs(dx)+abs(dy)+abs(ex)+abs(ey)+2)continue;
 for(int u=0;u<4;u++){int x=X[u];if(x==X[u+1])continue;int d1=dx+(P[b].x>=x)-(P[a].x>=x),e1=ex+(P[c].x>=x)-(P[a].x>=x);for(int v=0;v<4;v++){int y=Y[v];if(y==Y[v+1])continue;int d2=dy+(P[b].y>=y)-(P[a].y>=y),e2=ey+(P[c].y>=y)-(P[a].y>=y);if(d1*e2==e1*d2){diff[x][y]++;diff[X[u+1]][y]--;diff[x][Y[v+1]]--;diff[X[u+1]][Y[v+1]]++;}}}}
 for(int a=0;a<k;a++)for(int b=0;b<a;b++){array<int,4>X={0,P[a].x+1,P[b].x+1,n},Y={0,P[a].y+1,P[b].y+1,n};sort(X.begin(),X.end());sort(Y.begin(),Y.end());for(int u=0;u<3;u++)for(int v=0;v<3;v++){int x0=X[u],y0=Y[v],x1=X[u+1],y1=Y[v+1];if(x0==x1||y0==y1)continue;int x=P[a].x+(P[a].x>=x0),y=P[a].y+(P[a].y>=y0),dx=P[b].x+(P[b].x>=x0)-x,dy=P[b].y+(P[b].y>=y0)-y,g=gcd(abs(dx),abs(dy));dx/=g;dy/=g;for(int s:{-1,1})for(int i=x+s*dx,j=y+s*dy;i>=0&&j>=0&&i<n&&j<n;i+=s*dx,j+=s*dy)if(x0<=i&&i<x1&&y0<=j&&j<y1)extra[i][j]++;}}
 for(int i=0;i<n;i++)for(int j=0;j<n;j++){int &z=diff[i][j];if(i)z+=diff[i-1][j];if(j)z+=diff[i][j-1];if(i&&j)z-=diff[i-1][j-1];cout<<i<<" "<<j<<" "<<z<<" "<<extra[i][j]<<"\n";}}
