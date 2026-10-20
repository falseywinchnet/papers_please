// Exact fixed-tile local support diagnostic. No timings or inferred upper bound.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using I=long long;
int main(){
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 I cases=0,states=0,candidates=0,densities=0;int h,s,above;
 while(std::cin>>h>>s>>above){
  int C=1<<h,b=above?C+s:C-2*s,n=b+s,z=n+1;
  assert(s>=2&&!(s&(s-1))&&C>=4*s);
  std::vector<I>p(n),q(z),pre(z);for(auto&x:p)std::cin>>x;for(auto&x:q)std::cin>>x;
  I W=std::accumulate(p.begin(),p.end(),I(0))+std::accumulate(q.begin(),q.end(),I(0)),M=(h+2)*W+1;
  for(int j=1;j<=n;++j)pre[j]=pre[j-1]+p[j-1]+q[j];
  std::vector<I>old(z*z),cur(z*z);std::vector<int>root(z*z);
  for(int i=0;i<=n;++i)for(int j=i;j<=n;++j)old[i*z+j]=M*(j-i);
  for(int ell=1;ell<=h;++ell){
   for(int k=1;k<=n;++k)for(int i=0;i+k<=n;++i){int j=i+k,lo=k==1?i:root[i*z+j-1],hi=k==1?i:root[(i+1)*z+j],best=lo;I val=INT64_MAX;
    for(int r=lo;r<=hi;++r){I v=old[i*z+r]+old[(r+1)*z+j];++candidates;if(v<val){val=v;best=r;}}
    cur[i*z+j]=pre[j]-pre[i]+q[i]+val;root[i*z+j]=best;++states;
   }
   old.swap(cur);
  }
  I K=0,mass=0;
  for(int i=0;i<s;++i)for(int j=b;j<b+s;++j){I d=old[i*z+j+1]+old[(i+1)*z+j]-old[i*z+j]-old[(i+1)*z+j+1];assert(d>=0);K+=d>0;mass+=d;++densities;}
  ++cases;std::cout<<"{\"core\":"<<K<<",\"mass\":"<<W<<",\"density_mass\":"<<mass<<",\"counts\":{\"inputs\":"<<cases<<",\"states\":"<<states<<",\"root_candidates\":"<<candidates<<",\"density_cells\":"<<densities<<"}}\n"<<std::flush;
 }
}
