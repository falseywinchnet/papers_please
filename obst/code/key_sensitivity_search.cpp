#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using I=long long;
struct V{I score,slope;};
bool less(V a,V b){return a.score<b.score || (a.score==b.score && a.slope<b.slope);}
int main(){
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 int n,h,x;I cases=0,states=0,candidates=0,cells=0;
 while(std::cin>>n>>h>>x){int c=(1<<h)-1,N=n+1;assert(c<n&&x>=0&&x<n);std::vector<I>p(n);for(auto &a:p)std::cin>>a;
  const V bad{-(1LL<<60),0};std::vector<V>S(N*N,bad);std::vector<I>tail(N),deriv(N);
  for(int i=0;i+c<=n;++i){std::vector<V>dp(c+1,bad);dp[0]={0,0};
   for(int j=i+1;j<=n;++j){for(int r=std::min(c,j-i);r>=1;--r){++candidates;if(dp[r-1].score==bad.score)continue;int v=__builtin_ctz(unsigned(r));V a{dp[r-1].score+p[j-1]*v,dp[r-1].slope+(j-1==x?v:0)};if(less(dp[r],a))dp[r]=a;}
    if(j-i>=c){S[i*N+j]=dp[c];++states;}
   }
  }
  for(int i=0;i<n;++i)for(int j=i+c+1;j<n;++j){V a=S[i*N+j],b=S[(i+1)*N+j+1],z=S[i*N+j+1],w=S[(i+1)*N+j];I mass=a.score+b.score-z.score-w.score,ds=a.slope+b.slope-z.slope-w.slope;assert(mass>=0 && (mass||ds>=0));tail[j-i-c]+=mass;deriv[j-i-c]+=ds;++cells;}
  for(int d=n-1;d>=1;--d){tail[d]+=tail[d+1];deriv[d]+=deriv[d+1];}
  ++cases;std::cout<<"{\"tail\":[";for(int d=0;d<N;++d){if(d)std::cout<<',';std::cout<<tail[d];}std::cout<<"],\"derivative\":[";for(int d=0;d<N;++d){if(d)std::cout<<',';std::cout<<deriv[d];}std::cout<<"],\"counts\":{\"inputs\":"<<cases<<",\"scores\":"<<states<<",\"candidates\":"<<candidates<<",\"density_derivatives\":"<<cells<<"}}\n"<<std::flush;
 }
}
