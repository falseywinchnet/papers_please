#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <vector>
using I=long long;
I transitions=0,inputs=0;
int score(const std::vector<int>& p,const std::vector<int>&v){
 int c=int(v.size());std::vector<int> dp(c+1,-1000000);dp[0]=0;int j=0;
 for(int x:p){++j;for(int r=std::min(c,j);r>=1;--r){dp[r]=std::max(dp[r],dp[r-1]+x*v[r-1]);++transitions;}}
 return dp[c];
}
bool test(const std::vector<int>&p,int h){
 int c=(1<<h)-1;std::vector<int>v(c),levels;
 for(int r=1;r<=c;++r)v[r-1]=__builtin_ctz(unsigned(r));
 int full=score(p,v),sum=0;
 for(int a=1;a<h;++a){std::vector<int>w(c);for(int r=0;r<c;++r)w[r]=v[r]>=a;int x=score(p,w);levels.push_back(x);sum+=x;}
 ++inputs;assert(full<=sum);
 if(full<sum){std::cout<<"{\"h\":"<<h<<",\"p\":[";for(size_t j=0;j<p.size();++j){if(j)std::cout<<',';std::cout<<p[j];}std::cout<<"],\"full\":"<<full<<",\"levels\":[";for(size_t j=0;j<levels.size();++j){if(j)std::cout<<',';std::cout<<levels[j];}std::cout<<"],\"inputs\":"<<inputs<<",\"transitions\":"<<transitions<<"}\n";return false;}
 return true;
}
int main(){
 for(int n=7;n<=15;++n)for(unsigned mask=0;mask<(1u<<n);++mask){std::vector<int>p(n);for(int i=0;i<n;++i)p[i]=(mask>>i)&1u;if(!test(p,3))return 0;}
 std::mt19937 rng(42113);
 for(int h=4;h<=7;++h){int c=(1<<h)-1;for(int k=0;k<10000;++k){int n=c+1+int(rng()%unsigned(c+1));std::vector<int>p(n);unsigned threshold=rng()%100;for(int&i:p)i=rng()%100<threshold;if(!test(p,h))return 0;}}
 std::cout<<"{\"counterexample\":false,\"inputs\":"<<inputs<<",\"transitions\":"<<transitions<<"}\n";
}
