#include <algorithm>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <vector>
using I=long long;using Wide=__int128_t;
struct Row{int h=0,a=0,b=0,s=1;I core=0,mass=0,den=1;};
bool better(const Row&a,const Row&b){return Wide(a.core)*b.den>Wide(b.core)*a.den;}
int main(int argc,char**argv){
 int minimum=argc>1?std::stoi(argv[1]):4;
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);int n;I cases=0,states=0,candidates=0,cells=0,tiles=0;
 while(std::cin>>n){int N=1;while(N<n)N*=2;int L=0;while((1<<L)<n+1)++L;int z=N+1;std::vector<I>w(2*n+1),p(N),q(N+1),pre(z);for(auto &a:w)std::cin>>a;std::copy(w.begin(),w.begin()+n,p.begin());std::copy(w.begin()+n,w.end(),q.begin());I W=std::accumulate(w.begin(),w.end(),I(0)),M=(N+1)*W+1;
  for(int j=1;j<=N;++j)pre[j]=pre[j-1]+p[j-1]+q[j];
  auto mass=[&](int a,int b){return pre[b]-pre[a]+q[a];};
  std::vector<I>old(z*z),cur(z*z),prefix(z*z);std::vector<int>roots(z*z);for(int i=0;i<=N;++i)for(int j=i;j<=N;++j)old[i*z+j]=M*(j-i);
  Row best;std::vector<Row>layers;
  for(int h=1;h<L;++h){int c=(1<<h)-1;
   for(int k=1;k<=N;++k)for(int i=0;i+k<=N;++i){int j=i+k,lo=k==1?i:roots[i*z+j-1],hi=k==1?j-1:roots[(i+1)*z+j];I val=INT64_MAX;int rbest=lo;
    for(int r=lo;r<=hi;++r){I a=old[i*z+r]+old[(r+1)*z+j];if(a<val){val=a;rbest=r;}++candidates;}
    cur[i*z+j]=mass(i,j)+val;roots[i*z+j]=rbest;++states;
   }
   std::fill(prefix.begin(),prefix.end(),0);
   for(int i=0;i<N;++i)for(int j=0;j<N;++j){I support=0;if(i<j){I D=cur[i*z+j+1]+cur[(i+1)*z+j]-cur[i*z+j]-cur[(i+1)*z+j+1];assert(D>=0);support=D>0;++cells;}
    prefix[(i+1)*z+j+1]=support+prefix[i*z+j+1]+prefix[(i+1)*z+j]-prefix[i*z+j];
   }
   Row rb;rb.h=h;
   std::function<void(int,int,int)>visit=[&](int a,int b,int s){if(b+s-1<=a)return;int lo=b-a-s+1,hi=b-a+s-1;bool hit=(lo<=0&&0<=hi)||(lo<=c&&c<=hi);
    if(!hit){I core=prefix[(a+s)*z+b+s]+prefix[a*z+b]-prefix[a*z+b+s]-prefix[(a+s)*z+b];I local=mass(a,b+s);Row r{h,a,b,s,core,local,s+local};assert(core<=s*s && core<=2*h*local);++tiles;if(s>=minimum && std::abs(b-a-c)<=3*s && c>=4*s && better(r,rb))rb=r;}
    else if(s>1){int t=s/2;visit(a,b,t);visit(a+t,b,t);visit(a,b+t,t);visit(a+t,b+t,t);}
   };visit(0,0,N);layers.push_back(rb);if(better(rb,best))best=rb;old.swap(cur);
  }
  auto print=[](Row r){std::cout<<"{\"h\":"<<r.h<<",\"a\":"<<r.a<<",\"b\":"<<r.b<<",\"side\":"<<r.s<<",\"core\":"<<r.core<<",\"mass\":"<<r.mass<<",\"denominator\":"<<r.den<<"}";};
  ++cases;std::cout<<"{\"winner\":";print(best);std::cout<<",\"layers\":[";for(size_t j=0;j<layers.size();++j){if(j)std::cout<<',';print(layers[j]);}std::cout<<"],\"counts\":{\"inputs\":"<<cases<<",\"states\":"<<states<<",\"candidates\":"<<candidates<<",\"densities\":"<<cells<<",\"tiles\":"<<tiles<<"}}\n"<<std::flush;
 }
}
