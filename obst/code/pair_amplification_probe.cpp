// Fixed-tile support probe; exact integer layers and operation counts.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using I=long long;
int main(){
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);int n;I cases=0,states=0,candidates=0,cells=0;
 while(std::cin>>n){int target_h,ta,tb,ts;std::cin>>target_h>>ta>>tb>>ts;int N=1;while(N<n)N*=2;int z=N+1;std::vector<I>w(2*n+1),p(N),q(N+1),pre(z);for(auto &a:w)std::cin>>a;std::copy(w.begin(),w.begin()+n,p.begin());std::copy(w.begin()+n,w.end(),q.begin());I W=std::accumulate(w.begin(),w.end(),I(0)),M=(N+1)*W+1;
  for(int j=1;j<=N;++j)pre[j]=pre[j-1]+p[j-1]+q[j];
  auto mass=[&](int a,int b){return pre[b]-pre[a]+q[a];};
  std::vector<I>old(z*z),cur(z*z);std::vector<int>roots(z*z);for(int i=0;i<=N;++i)for(int j=i;j<=N;++j)old[i*z+j]=M*(j-i);
  for(int h=1;h<=target_h;++h){int c=(1<<h)-1;
   for(int k=1;k<=N;++k)for(int i=0;i+k<=N;++i){int j=i+k,lo=k==1?i:roots[i*z+j-1],hi=k==1?j-1:roots[(i+1)*z+j];I val=INT64_MAX;int rbest=lo;
    for(int r=lo;r<=hi;++r){I a=old[i*z+r]+old[(r+1)*z+j];if(a<val){val=a;rbest=r;}++candidates;}
    cur[i*z+j]=mass(i,j)+val;roots[i*z+j]=rbest;++states;
   }
   if(h!=target_h){old.swap(cur);continue;}
   I total_core=0,off_core=0,density_mass=0;
   for(int i=ta;i<ta+ts;++i)for(int j=tb;j<tb+ts;++j){
    assert(i<j && j<N && j-i!=c);I D=cur[i*z+j+1]+cur[(i+1)*z+j]-cur[i*z+j]-cur[(i+1)*z+j+1];assert(D>=0);
    int g=std::abs(j-i-c);bool dyadic=((g+1)&g)==0 || (j-i<c && ((g+2)&(g+1))==0);
    total_core+=D>0;off_core+=D>0 && !dyadic;density_mass+=D;++cells;
   }
   I local=mass(ta,tb+ts);++cases;
   std::cout<<"{\"core\":"<<total_core<<",\"off_core\":"<<off_core<<",\"mass\":"<<local<<",\"density_mass\":"<<density_mass<<",\"counts\":{\"inputs\":"<<cases<<",\"states\":"<<states<<",\"candidates\":"<<candidates<<",\"densities\":"<<cells<<"}}\n"<<std::flush;
  }
 }
}
