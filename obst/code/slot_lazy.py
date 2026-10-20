"""Exact queried-prefix search with a rearrangement bound and counted fallback.

No universal subquadratic search-size bound is asserted. Dictionary/address
operations and exact arithmetic are counted separately from operand bit cost.
"""
from collections import Counter
from slot_vector import normalize
from slot_punctured import sparse_repair
from trimmed_height import height_bound,knuth_fallback


class Exhausted(Exception):pass


class Meter:
    def __init__(self,stats=None,limit=None):
        self.stats=Counter() if stats is None else stats;self.limit=limit
    def tick(self,name):
        self.stats[name]+=1;self.stats['lazy_work']+=1
        if self.limit is not None and self.stats['lazy_work']>self.limit:raise Exhausted


def merge_sort(values,meter):
    out=list(values);width=1
    while width<len(out):
        target=[]
        for start in range(0,len(out),2*width):
            mid=min(start+width,len(out));end=min(start+2*width,len(out));i=start;j=mid
            while i<mid or j<end:
                if i==mid:take=False
                elif j==end:take=True
                else:meter.tick('lazy_sort_comparisons');take=out[i]<=out[j]
                meter.tick('lazy_sort_moves')
                if take:target.append(out[i]);i+=1
                else:target.append(out[j]);j+=1
        out=target;width*=2
    return out


class PrefixTop:
    def __init__(self,values,meter):
        self.meter=meter;ordered=merge_sort(values,meter);self.values=[];ranks={}
        for x in ordered:
            meter.tick('lazy_coordinate_items')
            if x not in ranks:ranks[x]=len(self.values);self.values.append(x)
        self.nodes=[(0,0,0,0)];self.roots=[0]
        def insert(node,lo,hi,pos,value):
            meter.tick('lazy_index_nodes');count,total,left,right=self.nodes[node]
            if hi-lo>1:
                mid=(lo+hi)//2
                if pos<mid:left=insert(left,lo,mid,pos,value)
                else:right=insert(right,mid,hi,pos,value)
            self.nodes.append((count+1,total+value,left,right));return len(self.nodes)-1
        for x in values:
            meter.tick('lazy_index_insertions');self.roots.append(insert(self.roots[-1],0,len(self.values),ranks[x],x))
    def top(self,prefix,count):
        self.meter.tick('lazy_top_queries')
        assert 0<=count<=prefix
        if not count:return 0
        node=self.roots[prefix];lo=0;hi=len(self.values);answer=0
        while True:
            self.meter.tick('lazy_top_visits');size,total,left,right=self.nodes[node]
            if count==size:return answer+total
            if hi-lo==1:return answer+count*self.values[lo]
            mid=(lo+hi)//2;right_size,right_total,_,_=self.nodes[right]
            if count<=right_size:node=right;lo=mid
            else:answer+=right_total;count-=right_size;node=left;hi=mid


class Search:
    def __init__(self,w,g,h,meter):
        self.w=w;self.g=g;self.h=h;self.n=len(w);self.meter=meter
        assert self.n and self.n<(1<<h)
        self.coefficients=[]
        for i,x in enumerate(w):
            meter.tick('lazy_coefficient_items');self.coefficients.append(2*x+g[i]+g[i+1])
        self.index=PrefixTop(self.coefficients,meter);self.bounds={};self.exact={}
    def lower2(self,k,b):
        self.meter.tick('lazy_bound_calls');key=k,b
        if key not in self.bounds:
            self.meter.tick('lazy_bound_states');v=(b&-b).bit_length()-1
            upper=(2*self.w[k-1]+self.g[k-1])*v
            count=(b-1)//2
            while count and k>1:
                self.meter.tick('lazy_bound_levels');upper+=self.index.top(k-1,min(k-1,count));count//=2
            self.bounds[key]=-upper
        return self.bounds[key]
    def frame(self,k,b):
        self.meter.tick('lazy_expanded_states')
        root=k==self.n+1;gap=0 if root else self.g[k-1]
        e=(b&-b).bit_length()-1;extra=0 if root else -self.w[k-1]*e
        bits=b-1;pos=0;candidates=[]
        for d in range(bits.bit_length()-1,-1,-1):
            self.meter.tick('lazy_skyline_bits')
            if bits>>d&1:
                pos+=1<<d
                if pos>=k-1:
                    self.meter.tick('lazy_candidates');shift=extra-gap*min(d,e)
                    candidates.append((self.lower2(k-1,pos)+2*shift,pos,shift))
        assert candidates
        return [k,b,merge_sort(candidates,self.meter),0,None,None]
    def run(self):
        stack=[self.frame(self.n+1,1<<self.h)]
        while stack:
            k,b,candidates,index,best,pred=stack[-1]
            self.meter.tick('lazy_stack_visits')
            if index==len(candidates):
                assert best is not None;self.exact[k,b]=best,pred;stack.pop();continue
            bound,a,shift=candidates[index]
            if best is not None and bound>=2*best:
                # The candidates are sorted by valid optimistic bounds.
                self.meter.stats['lazy_pruned_candidates']+=len(candidates)-index
                stack[-1][3]=len(candidates);continue
            child=k-1,a
            if child not in self.exact:
                if k-1==1:
                    self.meter.tick('lazy_base_states');self.exact[child]=-self.w[0]*((a&-a).bit_length()-1),0
                else:stack.append(self.frame(*child));continue
            self.meter.tick('lazy_evaluated_candidates');value=self.exact[child][0]+shift
            if best is None or value<best:stack[-1][4:6]=[value,a]
            stack[-1][3]+=1
        value,b=self.exact[self.n+1,1<<self.h];slots=[]
        for k in range(self.n,0,-1):
            self.meter.tick('lazy_trace_steps');slots.append(b);_,b=self.exact[k,b]
        slots.reverse();self.meter.stats['lazy_cached_exact_states']=len(self.exact)
        self.meter.stats['lazy_cached_bounds']=len(self.bounds)
        return value,slots


def solve(p,q,stats=None,limit=None,force_height=None):
    stats=Counter() if stats is None else stats;n=len(p)
    if not n:return dict(cost=0,tree=None,method='empty',limit=0)
    plan=height_bound(p,q,stats);h=plan['height']
    if force_height is not None:assert force_height>=n;h=force_height
    budget=8*n*n if limit is None else limit
    w,g,constant=normalize(p,q)
    try:
        search=Search(w,g,h,Meter(stats,budget));value,slots=search.run()
    except Exhausted:
        stats['lazy_fallbacks']+=1;value,tree=knuth_fallback(p,q,stats)
        return dict(cost=value,tree=tree,method='knuth',limit=budget,plan=plan,height=h)
    tree=sparse_repair(slots,h,stats)
    return dict(cost=h*(sum(w)+sum(g))+value+constant,tree=tree,slots=slots,
                method='lazy',limit=budget,plan=plan,height=h)
