// Independent exact check of the two-colour, complete-line-separation scheme on 5x5 sheets.
// Enumerate masks by rows and ordinary determinants. Tabulate by the opponent's binary support,
// then take a subset maximum over subsets of the remaining cells. No ternary zeta transform.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;int m,N,F;long leaves;vector<unsigned> own(25),reach[25],off,comp;vector<unsigned char>v,vis;vector<vector<unsigned>>rot;
int pc(unsigned s){return __builtin_popcount(s);}int pack8(unsigned s,unsigned a){int j=0,r=0;while(a){unsigned t=a&(-a);if(s&t)r|=1<<j;a-=t;j++;}return r;}int pack(unsigned s,unsigned a){return comp[(a&255)*256+(s&255)]|(comp[(a>>8)*256+(s>>8)]<<pc(a&255));}
int pos(unsigned A,unsigned B){return off[B]+pack(A,F^B);}int mod(int n){return (n%m+m)%m;}bool triple(int i,int j,int k){return (j%5-i%5)*(k/5-i/5)==(j/5-i/5)*(k%5-i%5);}
void rows(int y,vector<int>&p,unsigned U,unsigned T){if(y==5){leaves++;unsigned free=F^T;for(unsigned V=free;;V=(V-1)&free){int i=pos(U,V);if(v[i]<p.size())v[i]=p.size();if(!V)break;}return;}for(unsigned row=0;row<32;row++)if(pc(row)<=2){int z=p.size();bool good=true;unsigned u=U,t=T;for(int x=0;x<5 && good;x++)if(row>>x&1){int i=5*y+x;for(int j=0;j<(int)p.size() && good;j++){for(int k=0;k<j;k++)if(triple(i,p[j],p[k])){good=false;break;}t|=reach[i][p[j]];}p.push_back(i);u|=own[i];t|=own[i];}if(good)rows(y+1,p,u,t);p.resize(z);}}
int main(int argc,char**argv){if(argc!=2)return 2;m=atoi(argv[1]);if(m<2||m>4)return 2;N=m*m;F=(1<<N)-1;comp.resize(65536);for(int a=0;a<256;a++)for(int s=0;s<256;s++)comp[a*256+s]=pack8(s,a);off.resize(F+2);for(int b=0;b<=F;b++)off[b+1]=off[b]+(1<<pc(F^b));v.resize(off.back());vis.resize(off.back());for(int i=0;i<25;i++){own[i]=1u<<(i%5%m+m*((i/5)%m));reach[i].resize(25);for(int j=0;j<i;j++){int a=i%5-j%5,b=i/5-j/5;if(!a||!b)continue;int d=gcd(a,b);a/=d;b/=d;for(int t=0;t<m;t++)reach[i][j]|=1u<<(mod(i%5+t*a)+m*mod(i/5+t*b));}}vector<int>P;rows(0,P,0,0);
for(int V=0;V<=F;V++){int s=off[V],len=off[V+1]-s;for(int d=1;d<len;d*=2)for(int j=0;j<len;j+=2*d)for(int k=0;k<d;k++)v[s+j+d+k]=max(v[s+j+d+k],v[s+j+k]);}
rot.assign(N,vector<unsigned>(F+1));for(int h=0;h<N;h++)for(int s=1;s<=F;s++){int i=__builtin_ctz(s);rot[h][s]=rot[h][s&(s-1)]|(1u<<((i%m+h%m)%m+m*((i/m+h/m)%m)));}int best=0,orbs=0;
for(int b=0;b<=F;b++){unsigned Z=F^b;for(unsigned a=Z;;a=(a-1)&Z){int j=pos(a,b);if(!vis[j]){int sum=0;orbs++;for(int h=0;h<N;h++){int A=rot[h][a],B=rot[h][b],i=pos(A,B),k=pos(B,A);vis[i]=vis[k]=1;sum+=v[i]+v[k];}best=max(best,sum);}if(!a)break;}}
cout<<"m="<<m<<" masks="<<leaves<<" supports="<<off.back()<<" translation-and-colour orbits="<<orbs<<" maximal_mean="<<best<<"/"<<2*N<<"\n";if(leaves!=109536||best!=(m==3?5:6)*2*N)return 1;}
