// Dense exact diagnostic: maximize off-capacity interaction over unit profiles.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using I = int64_t;
using Wide = __int128_t;
struct Counts { I evaluations=0, states=0, candidates=0, densities=0, bands=0; } counts;
struct Profile { std::vector<std::vector<I>> tails; std::vector<I> full; };
Profile profile(const std::vector<int>& w) {
 int n=(int(w.size())-1)/2, N=n+1, L=0;
 while ((I(1)<<L)<n+1) ++L;
 I W=std::accumulate(w.begin(),w.end(),I(0)), M=(L+2)*W+1;
 assert(W<=(I(1)<<32));
 std::vector<I> old(N*N), cur(N*N), pre(N);
 std::vector<int> roots(N*N);
 for (int j=1;j<=n;++j) pre[j]=pre[j-1]+w[j-1]+w[n+j];
 for (int i=0;i<=n;++i) for (int j=i;j<=n;++j) old[i*N+j]=M*(j-i);
 Profile out; ++counts.evaluations;
 for (int h=1;h<L;++h) {
  int c=(1<<h)-1;
  for (int k=1;k<=n;++k) for (int i=0;i+k<=n;++i) {
   int j=i+k, lo=k==1?i:roots[i*N+j-1], hi=k==1?j-1:roots[(i+1)*N+j];
   I best=INT64_MAX; int arg=-1;
   for (int r=lo;r<=hi;++r) {
    I v=old[i*N+r]+old[(r+1)*N+j]; ++counts.candidates;
    if (v<best) { best=v;arg=r; }
   }
   cur[i*N+j]=best+pre[j]-pre[i]+w[n+i]; roots[i*N+j]=arg; ++counts.states;
  }
  std::vector<I> tail(n+1);
  for (int i=0;i<n;++i) for (int j=i+1;j<n;++j) {
   I delta=cur[i*N+j+1]+cur[(i+1)*N+j]-cur[i*N+j]-cur[(i+1)*N+j+1];
   assert(delta>=0); ++counts.densities;
   int distance=std::abs(j-i-c); if (distance) tail[distance]+=delta;
  }
  for (int d=n-1;d>=1;--d) tail[d]+=tail[d+1];
  out.tails.push_back(tail); out.full.push_back(cur[n]-M*std::max(0,n-c));
  old.swap(cur);
 }
 return out;
}
struct Row { int h=1,d=1; I mass=0,unit=0,excess=0,den=1,full_excess=0; };
bool better(const Row& a,const Row& b) { return Wide(a.excess)*b.den>Wide(b.excess)*a.den; }
struct Basis {
 int n; std::vector<Profile> units;
 explicit Basis(int size):n(size) {
  for (int x=0;x<2*n+1;++x) { std::vector<int> w(2*n+1);w[x]=1;units.push_back(profile(w)); }
 }
 Row evaluate(const std::vector<int>& w) const {
  Profile p=profile(w); I W=std::accumulate(w.begin(),w.end(),I(0)); Row best;
  for (int h=1;h<=int(p.tails.size());++h) {
   I full=p.full[h-1];
   for (int x=0;x<2*n+1;++x) full-=w[x]*units[x].full[h-1];
   assert(full>=0);
   for (int d=1;d<=n;++d) {
    I unit=0;for (int x=0;x<2*n+1;++x) unit+=w[x]*units[x].tails[h-1][d];
    Row r{h,d,p.tails[h-1][d],unit,p.tails[h-1][d]-unit,W?h*W:1,full};
    ++counts.bands;if (better(r,best)) best=r;
   }
  }
  return best;
 }
};
void print(const std::vector<int>& w,const Row& r) {
 std::cout<<"{\"n\":"<<(w.size()-1)/2<<",\"h\":"<<r.h<<",\"d\":"<<r.d
 <<",\"mass\":"<<r.mass<<",\"unit_mass\":"<<r.unit<<",\"excess\":"<<r.excess
 <<",\"denominator\":"<<r.den<<",\"full_excess\":"<<r.full_excess<<",\"weights\":[";
 for (size_t i=0;i<w.size();++i) std::cout<<(i?",":"")<<w[i];
 std::cout<<"],\"counts\":{\"evaluations\":"<<counts.evaluations<<",\"states\":"<<counts.states
 <<",\"candidates\":"<<counts.candidates<<",\"densities\":"<<counts.densities<<",\"bands\":"<<counts.bands<<"}}\n"<<std::flush;
}
int main(int argc,char**argv) {
 if(argc==1) {
  int n,oldn=0;Basis* basis=nullptr;
  while(std::cin>>n) {
   assert(n>=2&&n<=512);if(n!=oldn){delete basis;basis=new Basis(n);oldn=n;}
   std::vector<int>w(2*n+1);for(int& x:w){std::cin>>x;assert(x>=0&&x<=(1<<20));}
   print(w,basis->evaluate(w));
  }
  delete basis;return 0;
 }
 assert(argc==5);int n=std::stoi(argv[1]),steps=std::stoi(argv[2]),mode=std::stoi(argv[4]);
 assert(n>=2&&n<=512&&steps>=0&&mode>=0&&mode<=2);Basis basis(n);
 std::mt19937 rng(std::stoul(argv[3]));std::vector<int>w(2*n+1);
 if(mode==0)for(int i=0;i<n;++i)++w[rng()%w.size()];
 if(mode==1)for(int i=0;i<n;++i)w[i]=1;
 if(mode==2)for(int i=0;i<n;++i)w[n+i]=1;
 Row current=basis.evaluate(w),best=current;auto winner=w;
 for(int t=0;t<steps;++t){
  auto next=w;int a,b;do{a=rng()%w.size();}while(!next[a]);b=rng()%w.size();--next[a];++next[b];
  if(t%17==0){a=rng()%w.size();b=rng()%w.size();if(a>b)std::swap(a,b);std::reverse(next.begin()+a,next.begin()+b+1);}
  Row r=basis.evaluate(next);double v=double(r.excess)/r.den,u=double(current.excess)/current.den;
  double temp=0.02*(1.-double(t%std::max(1,steps/3))/std::max(1,steps/3));
  if(v>=u||std::generate_canonical<double,32>(rng)<std::exp((v-u)/std::max(0.001,temp))){w=next;current=r;}
  if(better(r,best)){best=r;winner=next;}
  if(t&&t%std::max(1,steps/3)==0){w=winner;current=best;}
 }
 assert(std::accumulate(winner.begin(),winner.end(),0)==n);print(winner,best);
}
