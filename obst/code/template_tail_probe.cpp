#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using I=long long;using Wide=__int128_t;
int main(){
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 int n,c;I inputs=0,states=0,densities=0;
 while(std::cin>>n>>c){
  std::vector<I>p(n),v(c);for(auto &a:p)std::cin>>a;for(auto &a:v)std::cin>>a;
  I P=std::accumulate(p.begin(),p.end(),I(0)),V=std::accumulate(v.begin(),v.end(),I(0)),B=*std::max_element(v.begin(),v.end());
  int z=n+1;std::vector<I>S(z*z),by(n-c+1);
  for(int i=0;i+c<=n;++i){std::vector<I>dp(c+1,INT64_MIN/4);dp[0]=0;
   for(int j=i;j<n;++j){for(int r=std::min(c,j-i+1);r>=1;--r){dp[r]=std::max(dp[r],dp[r-1]+p[j]*v[r-1]);++states;}
    if(j-i+1>=c)S[i*z+j+1]=dp[c];
   }
  }
  for(int i=0;i<n;++i)for(int j=i+c+1;j<n;++j){I D=S[i*z+j]+S[(i+1)*z+j+1]-S[i*z+j+1]-S[(i+1)*z+j];assert(D>=0);by[j-i-c]+=D;++densities;}
  for(int d=n-c-1;d>=1;--d)by[d]+=by[d+1];
  int best=1;I num=0,den=1;
  for(int d=1;d<n-c;++d){I a=by[d]*d,b=P*(B*d+V);if(b&&Wide(a)*den>Wide(num)*b){best=d;num=a;den=b;}}
  ++inputs;std::cout<<"{\"d\":"<<best<<",\"tail\":"<<by[best]<<",\"numerator\":"<<num<<",\"denominator\":"<<den<<",\"tails\":[";
  for(int d=1;d<n-c;++d){if(d>1)std::cout<<',';std::cout<<by[d];}
  std::cout<<"],\"counts\":{\"inputs\":"<<inputs<<",\"score_states\":"<<states<<",\"densities\":"<<densities<<"}}\n"<<std::flush;
 }
}
