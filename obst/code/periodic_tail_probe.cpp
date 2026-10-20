#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using I=long long;
int main(){
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 int n,c;I evaluations=0,states=0,candidates=0,densities=0;
 while(std::cin>>n>>c){
  std::vector<I> p(n),v(c);for(auto &x:p)std::cin>>x;for(auto &x:v)std::cin>>x;
  assert(c>=1&&c<=n);const I bad=-(1LL<<60);int stride=n+1;
  std::vector<I>S(stride*stride,bad),tail(n+1,0),support(n+1,0);
  for(int i=0;i+c<=n;++i){std::vector<I>dp(c+1,bad);dp[0]=0;
   for(int j=i+1;j<=n;++j){for(int r=std::min(c,j-i);r>=1;--r){++candidates;if(dp[r-1]!=bad)dp[r]=std::max(dp[r],dp[r-1]+p[j-1]*v[r-1]);}
    if(j-i>=c){S[i*stride+j]=dp[c];++states;}
   }
  }
  for(int i=0;i<n;++i)for(int j=i+c+1;j<n;++j){I z=S[i*stride+j]+S[(i+1)*stride+j+1]-S[i*stride+j+1]-S[(i+1)*stride+j];assert(z>=0);tail[j-i-c]+=z;support[j-i-c]+=(z>0);++densities;}
  for(int d=n-1;d>=1;--d){tail[d]+=tail[d+1];support[d]+=support[d+1];}
  ++evaluations;std::cout<<"{\"tail\":[";for(int d=0;d<=n;++d){if(d)std::cout<<',';std::cout<<tail[d];}
  std::cout<<"],\"support\":[";for(int d=0;d<=n;++d){if(d)std::cout<<',';std::cout<<support[d];}
  std::cout<<"],\"counts\":{\"evaluations\":"<<evaluations<<",\"scores\":"<<states<<",\"candidates\":"<<candidates<<",\"densities\":"<<densities<<"}}\n"<<std::flush;
 }
}
