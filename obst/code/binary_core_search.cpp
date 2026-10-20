// Binary-weight adversarial diagnostic; reuse the independently audited evaluator.
#define main core_size_reference_main
#include "core_size_search.cpp"
#undef main
int main(int argc,char**argv) {
  if(argc==1)return core_size_reference_main(argc,argv);
  assert(argc==6);
  int n=std::stoi(argv[1]),steps=std::stoi(argv[2]);
  unsigned seed=std::stoul(argv[3]);std::string mode=argv[4],start=argv[5];
  assert(n>=2 && n<=4096 && steps>=0);
  std::mt19937 rng(seed);std::vector<int> slots;
  if(mode=="mixed")for(int i=0;i<2*n+1;++i)slots.push_back(i);
  else if(mode=="keys")for(int i=0;i<n;++i)slots.push_back(i);
  else {assert(mode=="gaps");for(int i=n;i<2*n+1;++i)slots.push_back(i);}
  int mass=int(slots.size())/2;std::vector<int>w(2*n+1),order=slots;
  if(start=="random")std::shuffle(order.begin(),order.end(),rng);
  else if(start=="alternating")std::stable_sort(order.begin(),order.end(),[&](int a,int b){return (a-slots[0])%2<(b-slots[0])%2;});
  else if(start=="center")std::stable_sort(order.begin(),order.end(),[&](int a,int b){return std::abs(2*(a-slots[0])-int(slots.size()))<std::abs(2*(b-slots[0])-int(slots.size()));});
  else assert(start=="prefix");
  for(int i=0;i<mass;++i)w[order[i]]=1;
  auto current=evaluate(w),best=current;auto winner=w;
  for(int step=0;step<steps;++step){
    auto next=w;int a,b;
    do{a=slots[rng()%slots.size()];}while(!next[a]);
    do{b=slots[rng()%slots.size()];}while(next[b]);
    next[a]=0;next[b]=1;
    if(step%11==0){int l=rng()%slots.size(),r=rng()%slots.size();if(l>r)std::swap(l,r);
      while(l<r){std::swap(next[slots[l]],next[slots[r]]);++l;--r;}}
    auto candidate=evaluate(next);int gain=candidate.maximum()-current.maximum();
    double temp=std::max(0.1,0.006*n*(1.-double(step%std::max(1,steps/3))/std::max(1,steps/3)));
    if(gain>=0 || std::generate_canonical<double,32>(rng)<std::exp(gain/temp)){w=next;current=candidate;}
    if(candidate.maximum()>best.maximum()){best=candidate;winner=next;}
    if(step && step%std::max(1,steps/3)==0){w=winner;current=best;}
  }
  assert(std::accumulate(winner.begin(),winner.end(),0)==mass);
  assert(std::all_of(winner.begin(),winner.end(),[](int v){return v==0 || v==1;}));
  print(winner,best);
}
