// Condensed Monge OBST prototype. Research/exposition: OpenAI Codex Sydney.
// Product algorithm: Gawrychowski--Gorbachev--Kociumaka, ESA 2025.
// Ordinary witness arrays (not the paper's succinct rank/select storage).
// Checked signed-128 arithmetic; inputs outside the safe range are rejected.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <memory>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
using Num=__int128_t;
using Entry=std::tuple<int,int,Num>;
using List=std::vector<std::pair<int,Num>>;
struct Counts {
    uint64_t core_visits=0,core_records=0,dimension_slots=0,adjacent_visits=0;
    uint64_t product_calls=0,staircase_steps=0,border_cells=0,witness_slots=0,witness_nodes=0;
    uint64_t witness_queries=0,inner_comparisons=0,scalar_candidates=0,constructed_keys=0,tiny_cells=0;
    int max_depth=0,max_core=0,layers=0;bool fixed=false;
};
std::string str(Num x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;std::string s;while(x){s.push_back(char('0'+x%10));x/=10;}if(neg)s.push_back('-');std::reverse(s.begin(),s.end());return s;}
Num readnum(const std::string&s){Num x=0,lim=Num(1)<<120;for(char c:s){if(c<'0'||c>'9'||x>(lim-(c-'0'))/10)throw std::runtime_error("invalid or oversized integer weight");x=10*x+c-'0';}return x;}
std::vector<int> range(int a,int b){std::vector<int> x;for(int i=a;i<b;++i)x.push_back(i);return x;}
std::vector<int> edges(int n,const std::vector<int>&x){std::vector<int>m(n,-1);for(int k=0;k+1<int(x.size());++k)for(int i=x[k];i<x[k+1];++i)m[i]=k;return m;}
std::vector<int> groups(int n,const std::vector<int>&x){assert(x[0]==0);std::vector<int>m(n);for(int k=0;k<int(x.size());++k)for(int i=x[k];i<(k+1<int(x.size())?x[k+1]:n);++i)m[i]=k;return m;}
struct Mat {
    std::vector<Num>top,left;std::vector<Entry>core;std::vector<List>rows,cols;Counts* st;
    int p()const{return int(left.size());}int q()const{return int(top.size());}int k()const{return int(core.size());}
    Mat(std::vector<Num> t,std::vector<Num> l,const std::vector<Entry>&e,Counts&s):top(std::move(t)),left(std::move(l)),st(&s){
        assert(p()>0&&q()>0&&top[0]==left[0]);std::vector<List> cb(q()-1),rb(p()-1);
        s.dimension_slots+=2*(p()+q());
        for(auto[i,j,v]:e){assert(i>=0&&i<p()-1&&j>=0&&j<q()-1&&v>0);cb[j].emplace_back(i,v);++s.core_visits;}
        for(int j=0;j<q()-1;++j)for(auto[i,v]:cb[j]){rb[i].emplace_back(j,v);++s.core_visits;}
        rows.resize(p()-1);cols.resize(q()-1);
        for(int i=0;i<p()-1;++i){for(auto[j,v]:rb[i]){auto&r=rows[i];if(!r.empty()&&r.back().first==j)r.back().second+=v;else r.emplace_back(j,v);++s.core_visits;}
            for(auto[j,v]:rows[i]){cols[j].emplace_back(i,v);core.emplace_back(i,j,v);++s.core_records;}}
    }
    std::vector<Num> row(int i)const{std::vector<Num>d(q(),0),o(q());st->dimension_slots+=2*q();for(auto[a,b,v]:core){if(a<i)d[b]+=v;++st->core_visits;}Num sum=0;for(int j=0;j<q();++j){o[j]=left[i]+top[j]-top[0]-sum;sum+=d[j];}return o;}
    std::vector<Num> col(int j)const{std::vector<Num>d(p(),0),o(p());st->dimension_slots+=2*p();for(auto[a,b,v]:core){if(b<j)d[a]+=v;++st->core_visits;}Num sum=0;for(int i=0;i<p();++i){o[i]=top[j]+left[i]-left[0]-sum;sum+=d[i];}return o;}
    Num right(int i,int j,Num value)const{Num sum=0;for(auto[a,v]:cols[j]){if(a<i)sum+=v;++st->adjacent_visits;}return value+top[j+1]-top[j]-sum;}
    Num up(int i,int j,Num value)const{Num sum=0;for(auto[b,v]:rows[i]){if(b<j)sum+=v;++st->adjacent_visits;}return value-left[i+1]+left[i]+sum;}
    Mat select(const std::vector<int>&rr,const std::vector<int>&cc)const{
        auto rm=edges(p(),rr),cm=edges(q(),cc);st->dimension_slots+=p()+q();auto tr=row(rr[0]),lc=col(cc[0]);
        std::vector<Num>t,l;std::vector<Entry> e;for(int j:cc)t.push_back(tr[j]);for(int i:rr)l.push_back(lc[i]);
        for(auto[i,j,v]:core){if(rm[i]>=0&&cm[j]>=0)e.emplace_back(rm[i],cm[j],v);++st->core_visits;}
        return Mat(std::move(t),std::move(l),e,*st);
    }
};
struct Wit {
    std::vector<int>rm,cm,inner,border,leaf;int leaf_cols=0,cut=0;std::unique_ptr<Wit>left,right;Counts*st;
    int query(int i,int j)const{++st->witness_queries;i=rm[i];j=cm[j];int k=leaf.empty()?(j<=border[i]?left->query(i,j):cut+right->query(i,j)):leaf[i*leaf_cols+j];return inner[k];}
};
struct Grid{Num v[2][2]{};bool ok[2][2]{};};
Grid horizontal(const Mat&a,const Grid&g,int i,int j){Grid o;for(int r=0;r<2;++r)if(g.ok[r][1]){o.v[r][0]=g.v[r][1];o.ok[r][0]=true;if(j+2<a.q()){o.v[r][1]=a.right(i+r,j+1,g.v[r][1]);o.ok[r][1]=true;}}return o;}
Grid vertical(const Mat&a,const Grid&g,int i,int j){Grid o;for(int c=0;c<2;++c)if(g.ok[0][c]){o.v[1][c]=g.v[0][c];o.ok[1][c]=true;if(i>0){o.v[0][c]=a.up(i-1,j+c,g.v[0][c]);o.ok[0][c]=true;}}return o;}
std::pair<Mat,std::vector<int>> merge(const Mat&a,const Mat&b){
    assert(a.p()==b.p()&&a.q()==b.q());auto&s=*a.st;int p=a.p(),q=a.q(),i=p-1,j=-1;Grid ga,gb;
    ga.v[0][1]=a.left[i];gb.v[0][1]=b.left[i];ga.ok[0][1]=gb.ok[0][1]=true;
    std::vector<int>border(p,-1);std::vector<Entry>e;
    while(i>=0){++s.staircase_steps;
        if(i<p-1&&j>=0&&j<q-1){Num v=std::min(ga.v[0][1],gb.v[0][1])+std::min(ga.v[1][0],gb.v[1][0])-std::min(ga.v[0][0],gb.v[0][0])-std::min(ga.v[1][1],gb.v[1][1]);assert(v>=0);if(v)e.emplace_back(i,j,v);++s.border_cells;}
        if(j+1<q&&ga.v[0][1]<=gb.v[0][1]){ga=horizontal(a,ga,i,j);gb=horizontal(b,gb,i,j);++j;}
        else{border[i]=j;ga=vertical(a,ga,i,j);gb=vertical(b,gb,i,j);--i;}}
    for(int r=0;r<p-1;++r)assert(border[r]>=border[r+1]);
    for(auto[r,c,v]:a.core){if(c<border[r+1])e.emplace_back(r,c,v);++s.core_visits;}
    for(auto[r,c,v]:b.core){if(c>border[r])e.emplace_back(r,c,v);++s.core_visits;}
    std::vector<Num>t(q),l(p);for(int c=0;c<q;++c)t[c]=std::min(a.top[c],b.top[c]);for(int r=0;r<p;++r)l[r]=std::min(a.left[r],b.left[r]);s.dimension_slots+=p+q;
    return {Mat(std::move(t),std::move(l),e,s),std::move(border)};
}
std::pair<Mat,std::unique_ptr<Wit>> multiply(const Mat&a,const Mat&b,int depth=0){
    assert(a.q()==b.p());auto&s=*a.st;++s.product_calls;s.max_depth=std::max(s.max_depth,depth);
    std::vector<int>rr{0},cc{0},bounds{0},ss;
    for(int i=0;i<a.p()-1;++i)if(!a.rows[i].empty())rr.push_back(i+1);
    for(int j=0;j<b.q()-1;++j)if(!b.cols[j].empty())cc.push_back(j+1);
    for(int j=0;j<a.q()-1;++j)if(!a.cols[j].empty()||!b.rows[j].empty())bounds.push_back(j+1);bounds.push_back(a.q());
    for(int t=0;t+1<int(bounds.size());++t){int k=bounds[t];Num v=a.top[k]+b.left[k];for(int j=k+1;j<bounds[t+1];++j){Num z=a.top[j]+b.left[j];++s.inner_comparisons;if(z<v){v=z;k=j;}}ss.push_back(k);}
    s.dimension_slots+=a.p()+a.q()+b.q();auto aa=a.select(rr,ss),bb=b.select(ss,cc);
    assert(aa.k()==a.k()&&bb.k()==b.k());auto wit=std::make_unique<Wit>();wit->st=&s;wit->rm=groups(a.p(),rr);wit->cm=groups(b.q(),cc);wit->inner=ss;
    std::unique_ptr<Mat>c;
    if(aa.p()*bb.q()<=64){
        // A constant-size dense leaf is linear in the compressed inner dimension.
        int rows=aa.p(),cols=bb.q();std::vector<Num>vals(rows*cols),t(cols),l(rows);std::vector<Entry>ce;
        std::vector<std::vector<Num>>arows,bcols;for(int i=0;i<rows;++i)arows.push_back(aa.row(i));for(int j=0;j<cols;++j)bcols.push_back(bb.col(j));
        wit->leaf.resize(rows*cols);wit->leaf_cols=cols;s.tiny_cells+=rows*cols;
        for(int i=0;i<rows;++i)for(int j=0;j<cols;++j){Num best=arows[i][0]+bcols[j][0];int root=0;for(int k=0;k<aa.q();++k){Num v=arows[i][k]+bcols[j][k];if(v<best){best=v;root=k;}++s.scalar_candidates;}vals[i*cols+j]=best;wit->leaf[i*cols+j]=root;}
        for(int j=0;j<cols;++j)t[j]=vals[j];for(int i=0;i<rows;++i)l[i]=vals[i*cols];
        for(int i=0;i<rows-1;++i)for(int j=0;j<cols-1;++j){Num v=vals[i*cols+j+1]+vals[(i+1)*cols+j]-vals[i*cols+j]-vals[(i+1)*cols+j+1];assert(v>=0);if(v)ce.emplace_back(i,j,v);}
        c=std::make_unique<Mat>(std::move(t),std::move(l),ce,s);
    }
    else{
        std::vector<int>weights(aa.q()-1,0);for(auto[i,j,v]:aa.core){++weights[j];++s.core_visits;}for(auto[i,j,v]:bb.core){++weights[i];++s.core_visits;}
        int total=aa.k()+bb.k(),prefix=0,cut=1;for(int m=1;m<aa.q();++m){if(prefix>total/2)break;cut=m;prefix+=weights[m-1];}
        auto al=aa.select(range(0,aa.p()),range(0,cut)),bl=bb.select(range(0,cut),range(0,bb.q()));
        auto ar=aa.select(range(0,aa.p()),range(cut,aa.q())),br=bb.select(range(cut,bb.p()),range(0,bb.q()));
        assert(al.k()+bl.k()<=total/2&&ar.k()+br.k()<=total/2);
        auto left=multiply(al,bl,depth+1),right=multiply(ar,br,depth+1);auto joined=merge(left.first,right.first);
        c=std::make_unique<Mat>(std::move(joined.first));wit->border=std::move(joined.second);wit->cut=cut;wit->left=std::move(left.second);wit->right=std::move(right.second);
    }
    s.witness_slots+=wit->rm.size()+wit->cm.size()+wit->inner.size()+wit->border.size()+wit->leaf.size();++s.witness_nodes;
    std::vector<Num>t(b.q()),l(a.p());std::vector<Entry>e;
    for(int j=0;j<b.q();++j)t[j]=c->top[wit->cm[j]]+b.top[j]-b.top[cc[wit->cm[j]]];
    for(int i=0;i<a.p();++i)l[i]=c->left[wit->rm[i]]+a.left[i]-a.left[rr[wit->rm[i]]];
    for(auto[i,j,v]:c->core){e.emplace_back(rr[i+1]-1,cc[j+1]-1,v);++s.core_visits;}s.dimension_slots+=a.p()+b.q();
    Mat result(std::move(t),std::move(l),e,s);assert(result.k()<=2*(a.k()+b.k()));return {std::move(result),std::move(wit)};
}
struct Result{Num value;std::vector<int>parent;};
int fiblimit(Num w){Num a=0,b=1;int h=0;while(a<=w){Num c=a+b;a=b;b=c;++h;}return h;}
Result compact(const std::vector<Num>&p,const std::vector<Num>&q,Counts&s){
    int n=int(p.size());if(!n)return {0,{}};Num W=0;for(Num v:p)W+=v;for(Num v:q)W+=v;
    int L=0;for(int m=n;m;m>>=1)++L;bool positive=std::all_of(p.begin(),p.end(),[](Num v){return v>0;});int H=std::min(n,fiblimit(W)+(positive?0:L));
    Num denom=Num(16)*n*n*(H+2)+16;if(W>((Num(1)<<120)-1)/denom)throw std::runtime_error("input exceeds checked signed-128 arithmetic domain");
    Num M=(H+1)*W+1,P=4*n*M+4*W+1;std::vector<Num>prefix(n+1),single(n),top(n+1),left(n+1);std::vector<Entry>e;
    for(int i=0;i<n;++i){prefix[i+1]=prefix[i]+p[i]+q[i+1];single[i]=p[i]+q[i]+q[i+1];e.emplace_back(i,i,P+M);}
    for(int i=0;i<=n;++i){top[i]=M*i;left[i]=P*i;}Mat old(std::move(top),std::move(left),e,s);std::vector<std::unique_ptr<Wit>>witnesses;
    for(int h=1;h<=H;++h){
        auto aa=old.select(range(0,n+1),range(0,n)),bb=old.select(range(1,n+1),range(0,n+1));auto prod=multiply(aa,bb);e.clear();
        for(auto[i,j,v]:prod.first.core){if(j>=i+2)e.emplace_back(i,j,v);++s.core_visits;}
        for(int i=0;i<n;++i){e.emplace_back(i,i,P+single[i]);if(i+1<n){Num v=(h==1?M:std::min(single[i],single[i+1]))-q[i+1];assert(v>=0);if(v)e.emplace_back(i,i+1,v);}}
        top.assign(n+1,0);left.resize(n+1);for(int j=1;j<=n;++j)top[j]=prod.first.top[j]+prefix[j]+q[0];for(int i=0;i<=n;++i)left[i]=P*i;
        Mat next(std::move(top),std::move(left),e,s);++s.layers;s.max_core=std::max(s.max_core,next.k());
        bool equal=next.top==old.top&&next.core==old.core;witnesses.push_back(std::move(prod.second));old=std::move(next);if(equal){s.fixed=true;break;}
    }
    std::vector<int>parent(n,-2);std::vector<std::tuple<int,int,int,int>>stack{{0,n,int(witnesses.size()),-1}};
    while(!stack.empty()){auto[i,j,h,par]=stack.back();stack.pop_back();if(i==j)continue;assert(h>0);int r=witnesses[h-1]->query(i,j);assert(i<=r&&r<j);parent[r]=par;++s.constructed_keys;stack.emplace_back(i,r,h-1,r);stack.emplace_back(r+1,j,h-1,r);}
    return {old.top[n],std::move(parent)};
}
Result knuth(const std::vector<Num>&p,const std::vector<Num>&q,uint64_t&candidates){
    int n=int(p.size()),N=n+1;std::vector<Num>c(size_t(N)*N,0),prefix(N);std::vector<int>roots(size_t(N)*N,0);
    for(int i=0;i<n;++i)prefix[i+1]=prefix[i]+p[i]+q[i+1];
    for(int len=1;len<=n;++len)for(int i=0;i+len<=n;++i){int j=i+len,lo=len==1?i:roots[size_t(i)*N+j-1],hi=len==1?j-1:roots[size_t(i+1)*N+j],best=lo;Num v=c[size_t(i)*N+lo]+c[size_t(lo+1)*N+j];
        for(int r=lo;r<=hi;++r){Num z=c[size_t(i)*N+r]+c[size_t(r+1)*N+j];++candidates;if(z<v){v=z;best=r;}}roots[size_t(i)*N+j]=best;c[size_t(i)*N+j]=v+prefix[j]-prefix[i]+q[i];}
    std::vector<int>parent(n,-2);std::vector<std::tuple<int,int,int>>stack{{0,n,-1}};
    while(!stack.empty()){auto[i,j,par]=stack.back();stack.pop_back();if(i==j)continue;int r=roots[size_t(i)*N+j];parent[r]=par;stack.emplace_back(i,r,r);stack.emplace_back(r+1,j,r);}
    return {c[n],std::move(parent)};
}
int main(){try{
    std::cout<<std::setprecision(10);
    int n,index=0;while(std::cin>>n){if(n<0||n>8192)throw std::runtime_error("invalid key count");std::vector<Num>p(n),q(n+1);std::string word;Num W=0;
        for(auto&v:p){if(!(std::cin>>word))throw std::runtime_error("short input");v=readnum(word);W+=v;if(W>(Num(1)<<120))throw std::runtime_error("oversized mass");}
        for(auto&v:q){if(!(std::cin>>word))throw std::runtime_error("short input");v=readnum(word);W+=v;if(W>(Num(1)<<120))throw std::runtime_error("oversized mass");}
        if(n){int L=0;for(int m=n;m;m>>=1)++L;bool pos=std::all_of(p.begin(),p.end(),[](Num x){return x>0;});int H=std::min(n,fiblimit(W)+(pos?0:L));Num denom=Num(16)*n*n*(H+2)+16;if(W>((Num(1)<<120)-1)/denom)throw std::runtime_error("input exceeds checked signed-128 arithmetic domain");}
        Counts counts;uint64_t candidates=0;Result out,ref;double ct=0,kt=0;
        auto runC=[&](){auto t=std::chrono::steady_clock::now();out=compact(p,q,counts);ct=std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count();};
        auto runK=[&](){auto t=std::chrono::steady_clock::now();ref=knuth(p,q,candidates);kt=std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count();};
        if(index%2){runK();runC();}else{runC();runK();}if(out.value!=ref.value)throw std::runtime_error("compact/Knuth mismatch");
        std::cout<<"{\"n\":"<<n<<",\"cost\":\""<<str(out.value)<<"\",\"compact_seconds\":"<<ct<<",\"knuth_seconds\":"<<kt<<",\"compact_first\":"<<(index%2?"false":"true")<<",\"knuth_candidates\":"<<candidates<<",\"counts\":{";
#define FIELD(x) std::cout<<"\""#x"\":"<<counts.x<<",";
        FIELD(core_visits) FIELD(core_records) FIELD(dimension_slots) FIELD(adjacent_visits) FIELD(product_calls) FIELD(staircase_steps) FIELD(border_cells) FIELD(witness_slots) FIELD(witness_nodes) FIELD(witness_queries) FIELD(inner_comparisons) FIELD(scalar_candidates) FIELD(tiny_cells) FIELD(constructed_keys) FIELD(max_depth) FIELD(max_core)
#undef FIELD
        std::cout<<"\"layers\":"<<counts.layers<<",\"fixed\":"<<(counts.fixed?"true":"false")<<"},\"parent\":[";for(int i=0;i<n;++i){if(i)std::cout<<",";std::cout<<out.parent[i];}std::cout<<"]}"<<std::endl;++index;
    }
}catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 1;} }
