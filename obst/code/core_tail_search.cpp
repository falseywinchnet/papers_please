// Exact dense diagnostic for the proposed off-capacity mass bound.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using I=int64_t; using Wide=__int128_t;
struct Counts { I evaluations=0,states=0,candidates=0,densities=0,bands=0; } counts;
struct Row { int h=0,c=0,d=1;I mass=0,support=0,num=0,den=1; };
bool better(const Row&a,const Row&b){return Wide(a.num)*b.den>Wide(b.num)*a.den;}
struct Result {Row best;std::vector<Row> layers;};
Result evaluate(const std::vector<int>&w){
 int n=(int(w.size())-1)/2,N=n+1,L=0;while((I(1)<<L)<n+1)++L;
 I W=std::accumulate(w.begin(),w.end(),I(0));assert(W<=(I(1)<<32));I M=(L+2)*W+1;
 std::vector<I>old(N*N),cur(N*N),pre(N);std::vector<int>root(N*N);
 for(int j=1;j<=n;++j)pre[j]=pre[j-1]+w[j-1]+w[n+j];
 for(int i=0;i<=n;++i)for(int j=i;j<=n;++j)old[i*N+j]=M*(j-i);
 Result out;++counts.evaluations;
 for(int h=1;h<L;++h){int c=(1<<h)-1;
  for(int k=1;k<=n;++k)for(int i=0;i+k<=n;++i){int j=i+k;
   int lo=k==1?i:root[i*N+j-1],hi=k==1?j-1:root[(i+1)*N+j];I best=INT64_MAX;int rbest=-1;
   for(int r=lo;r<=hi;++r){I v=old[i*N+r]+old[(r+1)*N+j];if(v<best){best=v;rbest=r;}++counts.candidates;}
   cur[i*N+j]=best+pre[j]-pre[i]+w[n+i];root[i*N+j]=rbest;++counts.states;
  }
  std::vector<I>mass(n+1),support(n+1);
  for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){
   I d=cur[i*N+j+1]+cur[(i+1)*N+j]-cur[i*N+j]-cur[(i+1)*N+j+1];assert(d>=0);++counts.densities;
   int distance=std::abs(j-i-c);if(distance){mass[distance]+=d;support[distance]+=(d>0);}
  }
  for(int d=n-1;d>=1;--d){mass[d]+=mass[d+1];support[d]+=support[d+1];}
  Row rb;rb.h=h;rb.c=c;
  for(int d=1;d<=n;++d){Row r{h,c,d,mass[d],support[d],mass[d]*d,W?W*(I(L)*d+c):1};++counts.bands;
   if(better(r,rb))rb=r;}
  out.layers.push_back(rb);if(better(rb,out.best))out.best=rb;old.swap(cur);
 }
 return out;
}
void row(const Row&r){std::cout<<"{\"h\":"<<r.h<<",\"c\":"<<r.c<<",\"d\":"<<r.d<<",\"mass\":"<<r.mass<<",\"support\":"<<r.support<<",\"numerator\":"<<r.num<<",\"denominator\":"<<r.den<<"}";}
void print(const std::vector<int>&w,const Result&r){int n=(int(w.size())-1)/2;std::cout<<"{\"n\":"<<n<<",\"W\":"<<std::accumulate(w.begin(),w.end(),I(0))<<",\"winner\":";row(r.best);
 std::cout<<",\"layers\":[";for(size_t j=0;j<r.layers.size();++j){if(j)std::cout<<",";row(r.layers[j]);}
 std::cout<<"],\"weights\":[";for(size_t j=0;j<w.size();++j)std::cout<<(j?",":"")<<w[j];
 std::cout<<"],\"counts\":{\"evaluations\":"<<counts.evaluations<<",\"states\":"<<counts.states<<",\"candidates\":"<<counts.candidates<<",\"densities\":"<<counts.densities<<",\"bands\":"<<counts.bands<<"}}\n"<<std::flush;
}
int main(int argc,char**argv){
 if(argc==1){int n;while(std::cin>>n){assert(n>=2 && n<=2048);std::vector<int>w(2*n+1);for(int&x:w){std::cin>>x;assert(x>=0 && x<=(1<<20));}print(w,evaluate(w));}return 0;}
 assert(argc==4);int n=std::stoi(argv[1]),steps=std::stoi(argv[2]);assert(n>=2&&n<=2048&&steps>=0);std::mt19937 rng(std::stoul(argv[3]));std::vector<int>w(2*n+1);
 for(int i=0;i<n;++i)++w[rng()%w.size()];auto current=evaluate(w),best=current;auto winner=w;
 for(int t=0;t<steps;++t){auto next=w;int a,b;do{a=rng()%w.size();}while(!next[a]);b=rng()%w.size();--next[a];++next[b];
  if(t%17==0){a=rng()%w.size();b=rng()%w.size();if(a>b)std::swap(a,b);std::reverse(next.begin()+a,next.begin()+b+1);}
  auto result=evaluate(next);double v=double(result.best.num)/result.best.den,u=double(current.best.num)/current.best.den;
  double temp=0.015*(1.-double(t%std::max(1,steps/3))/std::max(1,steps/3));
  if(v>=u || std::generate_canonical<double,32>(rng)<std::exp((v-u)/std::max(0.001,temp))){w=next;current=result;}
  if(better(result.best,best.best)){best=result;winner=next;}
  if(t && t%std::max(1,steps/3)==0){w=winner;current=best;}
 }
 assert(std::accumulate(winner.begin(),winner.end(),0)==n);print(winner,best);return 0;
}
