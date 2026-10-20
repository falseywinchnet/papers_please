#!/usr/bin/env python3
"""Adaptive coarse-optimal grammar and exact original-weight refinement.

This is an output-sensitive construction. A counted expansion budget protects
against dense grammars; exhausted plans use the full ordinary Knuth solver.
No interval cost table is materialized during successful preparation.
"""
from collections import Counter
from fractions import Fraction
from compact_obst import solve as compact
from core_monge import multiply
from coarse_face import certificate,evaluate
from trimmed_height import balanced,knuth_fallback


class EntryIndex:
    """Persistent column-sum tree, one version per core row prefix."""
    def __init__(self,matrix):
        self.top=matrix.top;self.left=matrix.left;self.width=matrix.q
        self.stats=matrix.stats;self.nodes=[(0,0,0)];self.versions=[0]
        for row in matrix.rows:
            root=self.versions[-1]
            for j,value in row:root=self._add(root,0,self.width,j,value)
            self.versions.append(root);self.stats['grammar_index_versions']+=1
    def _add(self,node,lo,hi,j,value):
        left,right,total=self.nodes[node]
        if hi-lo>1:
            mid=(lo+hi)//2
            if j<mid:left=self._add(left,lo,mid,j,value)
            else:right=self._add(right,mid,hi,j,value)
        self.nodes.append((left,right,total+value))
        self.stats['grammar_index_nodes']+=1
        return len(self.nodes)-1
    def query(self,i,j):
        node=self.versions[i];lo=0;hi=self.width;total=0
        while node and lo<j:
            self.stats['grammar_index_query_nodes']+=1
            left,right,value=self.nodes[node]
            if hi<=j:total+=value;break
            mid=(lo+hi)//2
            if j<=mid:node=left;hi=mid
            else:
                total+=self.nodes[left][2];node=right;lo=mid
        self.stats['grammar_entry_queries']+=1
        return self.left[i]+self.top[j]-self.top[0]-total


class CostRoots:
    def __init__(self,p,q):
        self.n=len(p);self.counters=[];self.witnesses=[]
        for pp,qq in ((p,q),(p[::-1],q[::-1])):
            final=[]
            def observe(h,matrix,witness):final[:]=[matrix]
            value,tree,counts,layers=compact(pp,qq,observer=observe)
            matrix=final[0];stats=matrix.stats
            aa=matrix.select(list(range(self.n+1)),list(range(self.n)))
            bb=matrix.select(list(range(1,self.n+1)),list(range(self.n+1)))
            product,witness=multiply(aa,bb)
            stats['grammar_closure_products']+=1
            self.counters.append(stats);self.witnesses.append(witness)
            if len(self.witnesses)==1:
                self.value=value;self.index=EntryIndex(matrix)
            else:assert value==self.value
    def extremes(self,i,j):
        return (self.witnesses[0].query(i,j),
                self.n-1-self.witnesses[1].query(self.n-j,self.n-i))
    def counts(self):
        out=Counter()
        for stats in self.counters:
            for key,value in stats.items():
                if key.startswith('maximum_'):out[key]=max(out[key],value)
                else:out[key]+=value
        return out


class ExpansionBudget(Exception):
    pass


class Prepared:
    def __init__(self,p,q,stats=None,budget='default'):
        stats=Counter() if stats is None else stats;n=len(p)
        assert n and len(q)==n+1 and all(isinstance(x,int) and x>=0 for x in (*p,*q))
        assert budget in ('default',None) or isinstance(budget,int) and budget>=0
        self.p=tuple(p);self.q=tuple(q);self.n=n;self.mass=sum(p)+sum(q)
        self.budget=4*n*n.bit_length() if budget=='default' else budget
        self.rules={};self.order=[];self.plan=[];self.states=0;self.arcs=0
        self.available=False;self.expansion_work=0
        oracle=CostRoots(p,q);self.value=oracle.value
        prefix=[0]
        for a,b in zip(p,q[1:]):prefix.append(prefix[-1]+a+b)
        stats['grammar_coarse_prefix_items']+=n
        stats['grammar_base_items']+=2*n+1
        def charge(kind):
            if self.budget is not None and self.expansion_work>=self.budget:
                raise ExpansionBudget
            self.expansion_work+=1;stats[kind]+=1
        pending=[(0,n)];scheduled={(0,n)}
        try:
            while pending:
                i,j=pending.pop();charge('grammar_reached_states')
                lo,hi=oracle.extremes(i,j);assert i<=lo<=hi<j
                roots=[]
                target=oracle.index.query(i,j) if lo<hi else None
                weight=prefix[j]-prefix[i]+q[i]
                for r in range(lo,hi+1):
                    charge('grammar_candidate_roots')
                    if lo<hi:
                        candidate=oracle.index.query(i,r)+oracle.index.query(r+1,j)+weight
                        if candidate!=target:continue
                    charge('grammar_retained_arcs');roots.append(r)
                    for child in ((i,r),(r+1,j)):
                        stats['grammar_child_checks']+=1
                        if child[0]!=child[1] and child not in scheduled:
                            scheduled.add(child);pending.append(child)
                            stats['grammar_scheduled_states']+=1
                assert roots;self.rules[i,j]=roots
            # Integer interval lengths give a linear bucket topological order.
            buckets=[[] for _ in range(n+1)];stats['grammar_order_buckets']+=n+1
            for i,j in self.rules:
                buckets[j-i].append((i,j));stats['grammar_order_items']+=1
            self.order=[ij for bucket in buckets for ij in bucket]
            self.states=len(self.rules);self.arcs=sum(map(len,self.rules.values()))
            ids={ij:k for k,ij in enumerate(self.order)}
            for i,j in self.order:
                arcs=[]
                for r in self.rules[i,j]:
                    arcs.append((r,-1 if i==r else ids[i,r],
                                 -1 if r+1==j else ids[r+1,j]))
                    stats['grammar_compiled_arcs']+=1
                self.plan.append((i,j,arcs))
            self.root_id=ids[0,n]
            self.available=True;stats['grammar_completed_plans']+=1
        except ExpansionBudget:
            self.rules={};self.order=[];stats['grammar_budget_exhaustions']+=1
        stats.update(oracle.counts())
        # The cost index, Monge layers and closure witnesses are now released.
    def refine(self,p,q,delta,stats=None):
        stats=Counter() if stats is None else stats;n=self.n;delta=Fraction(delta)
        assert delta>0 and len(p)==n and len(q)==n+1
        assert all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
        error=sum(abs(x-delta*y) for x,y in zip((*p,*q),(*self.p,*self.q)))
        stats['grammar_fixed_error_items']+=2*n+1
        if (n-1)*error>=delta or not self.available:
            if (n-1)*error>=delta:stats['grammar_certificate_rejections']+=1
            else:stats['grammar_unavailable_fallbacks']+=1
            value,tree=knuth_fallback(p,q,stats)
            return dict(cost=value,tree=tree,method='knuth')
        prefix=[0]
        for a,b in zip(p,q[1:]):prefix.append(prefix[-1]+a+b)
        stats['grammar_fine_prefix_items']+=n
        values=[];chosen=[]
        for i,j,arcs in self.plan:
            best=None;choice=None
            for r,left,right in arcs:
                z=(0 if left<0 else values[left])+(0 if right<0 else values[right])
                stats['grammar_fine_candidates']+=1
                if best is None or z<best:best=z;choice=(r,left,right)
            values.append(best+prefix[j]-prefix[i]+q[i]);chosen.append(choice)
            stats['grammar_fine_states']+=1
        stack=[(self.root_id,False)];built=[None]*self.states
        while stack:
            k,ready=stack.pop()
            if k<0:continue
            r,left,right=chosen[k]
            if ready:
                built[k]=(r,None if left<0 else built[left],None if right<0 else built[right])
                stats['grammar_output_keys']+=1
            else:stack.extend(((k,True),(right,False),(left,False)))
        tree=built[self.root_id];value=values[self.root_id]
        assert evaluate(tree,p,q,stats)==value
        return dict(cost=value,tree=tree,method='grammar',error=error,delta=delta,
                    coarse_mass=self.mass,states=self.states,arcs=self.arcs)


def solve(p,q,stats=None,delta=None,budget='default'):
    stats=Counter() if stats is None else stats;n=len(p)
    assert len(q)==n+1 and all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
    if not n:return dict(cost=0,tree=None,method='empty')
    top=max((*p,*q));cert=None
    scales=[Fraction(delta)] if delta is not None else ([Fraction(top,m) for m in range(1,17)] if top else [Fraction(1)])
    for scale in scales:
        cert=certificate(p,q,scale,stats)
        if cert is not None:break
    if cert is None:
        stats['grammar_certificate_rejections']+=1
        value,tree=knuth_fallback(p,q,stats)
        return dict(cost=value,tree=tree,method='knuth')
    prepared=Prepared(cert['p'],cert['q'],stats,budget)
    return prepared.refine(p,q,cert['delta'],stats)


def two_tree_refine(p,q,delta,stats=None):
    """Direct linear constructor for the proved two-marked-key coarse base."""
    stats=Counter() if stats is None else stats;n=len(p);m=(n+1)//3
    assert n==3*m-1 and m>=2 and m&(m-1)==0 and len(q)==n+1
    assert all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
    delta=Fraction(delta);assert delta>0;a=m-1;c=2*m-1
    error=sum(abs(x-delta*(2 if i in (a,c) else 1)) for i,x in enumerate(p))
    error+=sum(abs(x-delta) for x in q)
    stats['two_tree_certificate_items']+=2*n+1
    if (n-1)*error>=delta:
        value,tree=knuth_fallback(p,q,stats);stats['two_tree_rejections']+=1
        return dict(cost=value,tree=tree,method='knuth')
    difference=p[c]+sum(p[c+1:n])+sum(q[c+1:n+1])-p[a]-sum(p[:a])-sum(q[:a+1])
    stats['two_tree_choice_items']+=4*m
    left=balanced(0,a);middle=balanced(a+1,c);right=balanced(c+1,n)
    tree=(a,left,(c,middle,right)) if difference<=0 else (c,(a,left,middle),right)
    stats['two_tree_output_keys']+=n
    value=evaluate(tree,p,q,stats)
    return dict(cost=value,tree=tree,method='two_tree',difference=difference)
