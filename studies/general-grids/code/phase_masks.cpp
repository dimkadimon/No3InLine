// Search for repeatable density gains, not needed for the boundary-ring theorem.
// For m=2,3 exhaust ALL ordered disjoint pairs of periodic supports mod m, including vacant colors.
// For each phase and each lawful w*h sheet mask, all its nonaxis primitive pair-lines mod m must miss
// the other color's support. Compute the average optimum by a ternary monotone maximum transform.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;int m,w,h,S,N,pp,A,phase;vector<int>pow3,idx,own;vector<vector<int>>line_mod;vector<vector<unsigned>>line;vector<unsigned char>best;vector<unsigned long long>sumH;unsigned long long cases;
void dfs(int i,unsigned selected,unsigned forbidden,unsigned need,unsigned ban,int k){if(i==w*h){cases++;int state=0;unsigned K=need|ban;while(K){int z=__builtin_ctz(K);K&=K-1;state+=pow3[z]*((need>>z&1)?2:1);}if(k>best[state])best[state]=k;return;}dfs(i+1,selected,forbidden,need,ban,k);if(forbidden>>i&1)return;unsigned M=selected,f=forbidden,g=ban;while(M){int j=__builtin_ctz(M);M&=M-1;f|=line[i][j];g|=line_mod[i][j];}dfs(i+1,selected|(1u<<i),f,need|(1u<<own[i]),g,k+1);}
int main(int argc,char**argv){if(argc!=5)return 2;m=atoi(argv[1]);w=atoi(argv[2]);h=atoi(argv[3]);if(m<2||m>4||w*h>30)return 2;N=m*m;pow3={1};for(int i=0;i<N;i++)pow3.push_back(3*pow3.back());S=pow3.back();if(m<4)sumH.resize(S);line.resize(w*h,vector<unsigned>(w*h));line_mod.resize(w*h,vector<int>(w*h));own.resize(w*h);
for(int phase=0;phase<(m==4?1:N);phase++){int X=phase%m,Y=phase/m;for(int i=0;i<w*h;i++){int x=i%w,y=i/w;own[i]=(x+X)%m+m*((y+Y)%m);for(int j=0;j<i;j++){int dx=x-j%w,dy=y-j/w,g=gcd(dx,dy);dx/=g;dy/=g;unsigned F=0,G=0;for(int t=0;t<w*h;t++)if(dy*(t%w-x)==dx*(t/w-y))F|=1u<<t;if(dx&&dy)for(int t=0;t<m;t++)G|=1u<<(((x+X+dx*t)%m+m)%m+m*(((y+Y+dy*t)%m+m)%m));line[i][j]=F;line_mod[i][j]=G;}}
 best.assign(S,0);cases=0;dfs(0,0,0,0,0,0);for(int j=0;j<N;j++){int b=pow3[j];for(int z=0;z<S;z+=3*b)for(int t=0;t<b;t++){best[z+b+t]=max(best[z+b+t],best[z+t]);best[z+2*b+t]=max(best[z+2*b+t],best[z+b+t]);}}if(m<4)for(int i=0;i<S;i++)sumH[i]+=best[i];}
 if(m==4){vector<unsigned char>vis(S);vector<vector<int>>tab(N,vector<int>(1<<N));for(int ph=0;ph<N;ph++)for(int a=1;a<(1<<N);a++){int j=__builtin_ctz((unsigned)a),k=(j%m+ph%m)%m+m*((j/m+ph/m)%m);tab[ph][a]=tab[ph][a&(a-1)]+pow3[k];}
 int best_sum=0,state=0,norb=0;for(int s=0;s<S;s++)if(!vis[s]){int own=0,opp=0,t=s,b=0;for(int j=0;j<N;j++,t/=3){if(t%3==2)own|=1<<j;if(t%3==0)opp|=1<<j;}for(int ph=0;ph<N;ph++){int i=(S-1)/2+tab[ph][own]-tab[ph][opp];b+=best[i]+best[S-1-i];vis[i]=vis[S-1-i]=1;}norb++;if(b>best_sum){best_sum=b;state=s;}}cout<<"m=4 w="<<w<<" h="<<h<<" cap_masks="<<cases<<" disjoint_support_pairs="<<S<<" translation_color_orbits="<<norb<<" best_mean="<<best_sum<<"/"<<2*N<<" state="<<state<<"\n";return 0;}
 ofstream f(argv[4]);unsigned long long M=0;int arg=0;for(int i=0;i<S;i++){auto a=sumH[i]+sumH[S-1-i];f<<a<<"\n";if(a>M){M=a;arg=i;}}cout<<"m="<<m<<" w="<<w<<" h="<<h<<" cap_masks="<<cases<<" disjoint_support_pairs="<<S<<" best_mean="<<M<<"/"<<2*N<<" state="<<arg<<"\n";}
