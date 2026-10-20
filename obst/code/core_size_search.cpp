// Dense adversarial diagnostic, NOT the sparse construction algorithm.
// Fixed integer mass; objective is the maximum completed core over all layers.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>
using I = int64_t;
struct Counts { I evaluations=0, states=0, candidates=0, densities=0; } counts;
struct Result { std::vector<int> cores; I value; int H; int maximum() const {
  return *std::max_element(cores.begin(), cores.end()); } };
Result evaluate(const std::vector<int>& w) {
  const int n=(int(w.size())-1)/2, d=n+1;
  I W=std::accumulate(w.begin(),w.end(),I(0)), fa=0,fb=1;
  int f=0,L=0; while ((I(1)<<L)<n+1) ++L;
  while(fa<=W) {I fc=fa+fb;fa=fb;fb=fc;++f;}
  bool positive=std::all_of(w.begin(),w.begin()+n,[](int x){return x>0;});
  int H=std::min(n,f+(positive?0:L)); I M=(H+1)*W+1;
  std::vector<I> old(d*d), cur(d*d), pre(d);
  std::vector<int> roots(d*d);
  for(int j=1;j<=n;++j) pre[j]=pre[j-1]+w[j-1]+w[n+j];
  for(int i=0;i<=n;++i) for(int j=i;j<=n;++j) old[i*d+j]=M*(j-i);
  Result result{{n},0,H}; ++counts.evaluations;
  for(int h=1;h<=H;++h) {
    for(int len=1;len<=n;++len) for(int i=0;i+len<=n;++i) {
      int j=i+len, lo=len==1?i:roots[i*d+j-1], hi=len==1?j-1:roots[(i+1)*d+j];
      I best=INT64_MAX; int root=-1;
      for(int r=lo;r<=hi;++r) {I z=old[i*d+r]+old[(r+1)*d+j];
        if(z<best) {best=z;root=r;} ++counts.candidates;}
      cur[i*d+j]=best+pre[j]-pre[i]+w[n+i]; roots[i*d+j]=root; ++counts.states;
      assert(cur[i*d+j]<=old[i*d+j]);
    }
    int core=n;
    for(int i=0;i<n;++i) for(int j=i+1;j<n;++j) {
      I delta=cur[i*d+j+1]+cur[(i+1)*d+j]-cur[i*d+j]-cur[(i+1)*d+j+1];
      assert(delta>=0); core+=(delta>0); ++counts.densities;
    }
    result.cores.push_back(core);
    bool fixed=(old==cur); old.swap(cur);
    // Whole-table equality is a fixed point, so every omitted layer is identical.
    if(fixed) {result.cores.resize(H+1,core);break;}
  }
  result.value=old[n]; return result;
}
void print(const std::vector<int>& w,const Result& r) {
  int n=(int(w.size())-1)/2,L=0; while((I(1)<<L)<n+1)++L;
  I W=std::accumulate(w.begin(),w.end(),I(0));
  std::cout<<"{\"n\":"<<n<<",\"mass\":"<<W<<",\"H\":"<<r.H<<",\"cost\":"<<r.value
    <<",\"maximum_completed_core\":"<<r.maximum()<<",\"ratio\":";
  if(W)std::cout<<r.maximum()/(n*std::sqrt(double(W)*L));else std::cout<<"null";
  std::cout<<",\"weights\":[";
  for(size_t i=0;i<w.size();++i) std::cout<<(i?",":"")<<w[i];
  std::cout<<"],\"cores\":[";for(size_t i=0;i<r.cores.size();++i)std::cout<<(i?",":"")<<r.cores[i];
  std::cout<<"],\"counts\":{\"evaluations\":"<<counts.evaluations<<",\"states\":"<<counts.states
    <<",\"candidates\":"<<counts.candidates<<",\"densities\":"<<counts.densities<<"}}\n"<<std::flush;
}
int main(int argc,char**argv) {
  if(argc==1) {int n;while(std::cin>>n){assert(n>=1 && n<=4096);std::vector<int>w(2*n+1);
    for(auto&x:w){std::cin>>x;assert(x>=0);}auto r=evaluate(w);print(w,r);}return 0;}
  assert(argc==5);int n=std::stoi(argv[1]),steps=std::stoi(argv[2]);
  unsigned seed=std::stoul(argv[3]);std::string mode=argv[4];
  assert(n>=1 && n<=4096 && steps>=0);
  std::mt19937 rng(seed);int slots=mode=="keys"?n:2*n+1;
  std::vector<int>w(2*n+1);for(int t=0;t<n;++t)++w[rng()%slots];
  if(mode=="uniform") {std::fill(w.begin(),w.end(),0);std::fill(w.begin(),w.begin()+n,1);}
  if(mode=="spaced" || mode=="ramp" || mode=="cluster" || mode=="sparse") {
    std::fill(w.begin(),w.end(),0);int k=std::max(1,int(std::sqrt(n))),used=0;
    for(int t=0;t<k;++t){int pos=mode=="cluster"?n/2-k/2+t:(t*n/k+n/(2*k));
      if(mode=="sparse")pos=rng()%n;
      int value=mode=="ramp"?std::min(n-used,2*(t+1)):n/k;
      w[std::min(n-1,pos)]+=value;used+=value;}
    w[n/2]+=n-used;
  }
  auto current=evaluate(w),best=current;auto winner=w;std::vector<int> history{best.maximum()};
  for(int step=0;step<steps;++step) {
    auto next=w;int a=rng()%slots,b=rng()%slots;
    unsigned kind=rng()%10;
    if(kind<7){while(!next[a])a=rng()%slots;int amount=kind==0?1+rng()%next[a]:1;next[a]-=amount;next[b]+=amount;}
    else if(kind<9)std::swap(next[a],next[b]);
    else {if(a>b)std::swap(a,b);std::reverse(next.begin()+a,next.begin()+b+1);}
    if(next==w)continue;
    auto candidate=evaluate(next); int gain=candidate.maximum()-current.maximum();
    // Annealing explores plateaus; objective and all layer arithmetic are exact.
    double temp=std::max(0.15,0.012*n*(1.-double(step%std::max(1,steps/3))/std::max(1,steps/3)));
    if(gain>=0 || std::generate_canonical<double,32>(rng)<std::exp(gain/temp)) {w=next;current=candidate;}
    if(candidate.maximum()>best.maximum()){winner=next;best=candidate;history.push_back(best.maximum());}
    if(step && step%std::max(1,steps/3)==0){w=winner;current=best;}
  }
  print(winner,best);
}
