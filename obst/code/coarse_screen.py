#!/usr/bin/env python3
"""Exact full mixed-OBST refinement by height-bounded coarse regret.

Every arbitrary nonnegative fine input is supported. A coarse-near-optimal
root superset replaces the small-error acceptance test. A counted expansion
budget protects dense cases with ordinary Knuth fallback.
"""
from collections import Counter
from fractions import Fraction
from compact_obst import solve as compact
from root_ranges import RootRanges
from trimmed_height import height_bound,knuth_fallback,balanced
from coarse_face import evaluate


class ScreenBudget(Exception):
    pass


class Prepared:
    def __init__(self,p,q,stats=None):
        stats=Counter() if stats is None else stats
        n=len(p);assert n and len(q)==n+1
        assert all(isinstance(x,int) and x>=0 for x in (*p,*q))
        self.n=n;self.p=tuple(p);self.q=tuple(q);self.mass=sum(p)+sum(q)
        final=[]
        def observe(h,matrix,witness):final[:]=[matrix]
        value,tree,counts,layers=compact(p,q,observer=observe)
        matrix=final[0];self.coarse_height=len(layers);self.value=value;self.core=matrix.k
        self.ranges=RootRanges(matrix)
        stats.update(matrix.stats)
        self.prefix=[0]
        for a,b in zip(p,q[1:]):self.prefix.append(self.prefix[-1]+a+b)
        stats['screen_coarse_prefix_items']+=n
        stats['screen_stored_base_items']+=2*n+1
    def refine(self,p,q,delta,stats=None,budget='default',observer=None):
        stats=Counter() if stats is None else stats;n=self.n;delta=Fraction(delta)
        assert delta>0 and len(p)==n and len(q)==n+1
        assert all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
        budget=4*n*n.bit_length() if budget=='default' else budget
        assert budget is None or isinstance(budget,int) and budget>=0
        hf=height_bound(p,q,stats)['height'];hc=self.coarse_height
        errors=[x-delta*a for x,a in zip((*p,*q),(*self.p,*self.q))]
        pos=[max(0,e) for e in errors];neg=[max(0,-e) for e in errors]
        plus=[0];minus=[0];fine=[0]
        for k in range(n):
            plus.append(plus[-1]+pos[k]+pos[n+k+1])
            minus.append(minus[-1]+neg[k]+neg[n+k+1])
            fine.append(fine[-1]+p[k]+q[k+1])
        stats['screen_error_items']+=2*n+1;stats['screen_prefix_items']+=3*n
        work=0
        def charge(kind):
            nonlocal work
            if budget is not None and work>=budget:raise ScreenBudget
            work+=1;stats[kind]+=1
        pending=[(0,n)];scheduled={(0,n)};rules={}
        try:
            while pending:
                i,j=pending.pop();charge('screen_reached_states');m=j-i
                positive=plus[j]-plus[i]+pos[n+i]
                negative=minus[j]-minus[i]+neg[n+i]
                allowance=(min(m,hc)-1)*positive+(min(m,hf)-1)*negative
                mass=self.prefix[j]-self.prefix[i]+self.q[i]
                threshold=self.ranges.base.query(i,j,stats)-mass+allowance/delta
                roots=[]
                for r in self.ranges.below(i,j,threshold,stats):
                    charge('screen_retained_roots');roots.append(r)
                    for child in ((i,r),(r+1,j)):
                        stats['screen_child_checks']+=1
                        if child[0]!=child[1] and child not in scheduled:
                            scheduled.add(child);pending.append(child)
                            stats['screen_scheduled_states']+=1
                assert roots
                rules[i,j]=roots
                if observer is not None:observer(i,j,roots,threshold)
        except ScreenBudget:
            stats['screen_budget_exhaustions']+=1
            value,tree=knuth_fallback(p,q,stats)
            return dict(cost=value,tree=tree,method='knuth',coarse_mass=self.mass,coarse_core=self.core,
                        coarse_height=hc,fine_height=hf,
                        processed_states=len(rules),expansion_charges=work)
        buckets=[[] for _ in range(n+1)];stats['screen_order_buckets']+=n+1
        for i,j in rules:buckets[j-i].append((i,j));stats['screen_order_items']+=1
        values={};chosen={}
        for bucket in buckets:
            for i,j in bucket:
                best=None;root=None
                for r in rules[i,j]:
                    candidate=values.get((i,r),0)+values.get((r+1,j),0)
                    stats['screen_fine_candidates']+=1
                    if best is None or candidate<best:best=candidate;root=r
                values[i,j]=best+fine[j]-fine[i]+q[i];chosen[i,j]=root
                stats['screen_fine_states']+=1
        stack=[(0,n,False)];built={}
        while stack:
            i,j,ready=stack.pop()
            if i==j:continue
            r=chosen[i,j]
            if ready:
                built[i,j]=(r,built.pop((i,r),None),built.pop((r+1,j),None))
                stats['screen_output_keys']+=1
            else:stack.extend(((i,j,True),(r+1,j,False),(i,r,False)))
        value=values[0,n];tree=built[0,n]
        assert evaluate(tree,p,q,stats)==value
        stats['screen_completed_queries']+=1
        return dict(cost=value,tree=tree,method='screen',states=len(rules),
                    arcs=sum(map(len,rules.values())),coarse_mass=self.mass,coarse_core=self.core,
                    fine_height=hf,coarse_height=hc,expansion_charges=work)


def solve(p,q,stats=None,precision=None,budget='default'):
    stats=Counter() if stats is None else stats;n=len(p)
    assert len(q)==n+1 and all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
    if not n:return dict(cost=0,tree=None,method='empty')
    if all(x==p[0] for x in p) and all(x==q[0] for x in q):
        stats['screen_uniform_items']+=2*n+1
        tree=balanced(0,n);value=evaluate(tree,p,q,stats)
        stats['screen_uniform_output_keys']+=n
        return dict(cost=value,tree=tree,method='uniform')
    b=n.bit_length()**3 if precision is None else precision
    assert isinstance(b,int) and b>=1
    delta=Fraction(max((*p,*q)),b);coarse=[]
    for x in (*p,*q):
        ratio=Fraction(x)/delta
        coarse.append((2*ratio.numerator+ratio.denominator)//(2*ratio.denominator))
        stats['screen_rounding_items']+=1
    pre=Counter();query=Counter();prepared=Prepared(coarse[:n],coarse[n:],pre)
    result=prepared.refine(p,q,delta,query,budget)
    stats.update(pre);stats.update(query)
    result['preparation_counts']=dict(pre);result['query_counts']=dict(query)
    result['precision']=b;result['delta']=delta
    return result
