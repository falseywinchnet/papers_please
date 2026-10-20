"""Certified lattice perturbations, unrestricted coarse faces and exact payloads.

The original full mixed problem is solved. The input-dependent bound includes
coarse Monge construction and all ambiguous interval refinements. Exact operand
bit costs and ordinary witness-map storage are separate from arithmetic work.
"""
from collections import Counter
from fractions import Fraction
from compact_obst import solve as compact
from core_monge import multiply
from trimmed_height import knuth_fallback


class Oracle:
    def __init__(self,p,q):
        self.n=len(p);assert self.n
        self.counters=[];self.witnesses=[];self.layers=[]
        for pp,qq in ((p,q),(p[::-1],q[::-1])):
            final=[]
            def observe(h,matrix,witness):final[:]=[matrix]
            value,tree,counts,layers=compact(pp,qq,observer=observe)
            matrix=final[0];stats=matrix.stats
            # One additional product uses unrestricted child values on both
            # sides. Its witnesses may be reused at every subtree depth.
            aa=matrix.select(list(range(self.n+1)),list(range(self.n)))
            bb=matrix.select(list(range(1,self.n+1)),list(range(self.n+1)))
            product,witness=multiply(aa,bb)
            stats['face_closure_products']+=1
            self.counters.append(stats);self.witnesses.append(witness);self.layers.append(layers)
            if len(self.witnesses)==1:self.value=value
            else:assert value==self.value
    def extremes(self,i,j):
        assert 0<=i<j<=self.n
        return self.witnesses[0].query(i,j),self.n-1-self.witnesses[1].query(self.n-j,self.n-i)
    def partition(self):
        forced={};blocks=[];pending=[(0,self.n)];queries=0
        while pending:
            i,j=pending.pop()
            if i==j:continue
            lo,hi=self.extremes(i,j);queries+=1
            assert i<=lo<=hi<j
            if lo==hi:
                forced[i,j]=lo;pending.extend(((lo+1,j),(i,lo)))
            else:blocks.append((i,j))
        return dict(forced=forced,blocks=blocks,unique=not blocks,queries=queries)
    def counts(self):
        result=Counter()
        for stats in self.counters:
            for key,value in stats.items():
                if key.startswith('maximum_'):result[key]=max(result[key],value)
                else:result[key]+=value
        return result


def certificate(p,q,delta,stats):
    delta=Fraction(delta);assert delta>0;n=len(p)
    coarse=[];error=0
    for x in (*p,*q):
        ratio=Fraction(x)/delta
        a=(2*ratio.numerator+ratio.denominator)//(2*ratio.denominator)
        coarse.append(a);error+=abs(x-delta*a);stats['face_rounding_items']+=1
    stats['face_scale_trials']+=1
    if (n-1)*error>=delta:return None
    return dict(delta=delta,error=error,p=coarse[:n],q=coarse[n:],mass=sum(coarse))


def shifted(tree,offset,stats):
    if tree is None:return None
    stack=[(tree,False)];built={}
    while stack:
        node,ready=stack.pop();r,left,right=node
        if ready:
            built[r]=(r+offset,None if left is None else built.pop(left[0]),None if right is None else built.pop(right[0]));stats['face_payload_shift_nodes']+=1
        else:
            stack.append((node,True))
            if right is not None:stack.append((right,False))
            if left is not None:stack.append((left,False))
    return built[tree[0]]


def evaluate(tree,p,q,stats):
    value=0;stack=[(tree,0,len(p),0)]
    while stack:
        node,i,j,d=stack.pop()
        if node is None:
            assert i==j;value+=q[i]*d;stats['face_output_gap_visits']+=1
        else:
            r,left,right=node;assert i<=r<j
            value+=p[r]*(d+1);stats['face_output_key_visits']+=1
            stack.extend(((right,r+1,j,d+1),(left,i,r,d+1)))
    return value


class Prepared:
    def __init__(self,p,q,stats=None):
        stats=Counter() if stats is None else stats
        assert p and len(q)==len(p)+1 and all(isinstance(x,int) and x>=0 for x in (*p,*q))
        self.p=tuple(p);self.q=tuple(q);self.n=len(p);self.mass=sum(p)+sum(q)
        oracle=Oracle(p,q);self.plan=oracle.partition();self.layers=oracle.layers;self.value=oracle.value
        stats.update(oracle.counts());stats['face_partition_queries']+=self.plan['queries']
        stats['face_base_items']+=2*self.n+1
        # The witnesses and core data are released after the forced partition
        # is extracted. Retained preparation data is linear in n.
    def refine(self,p,q,delta,stats=None):
        stats=Counter() if stats is None else stats;n=self.n;delta=Fraction(delta)
        assert delta>0 and len(p)==n and len(q)==n+1
        assert all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
        error=sum(abs(x-delta*y) for x,y in zip((*p,*q),(*self.p,*self.q)))
        stats['face_fixed_error_items']+=2*n+1
        if (n-1)*error>=delta:
            value,tree=knuth_fallback(p,q,stats);stats['face_certificate_rejections']+=1
            return dict(cost=value,tree=tree,method='knuth',blocks=[(0,n)])
        forced=self.plan['forced'];blocks=set(self.plan['blocks']);stats['face_forced_keys']+=len(forced)
        stack=[(0,n,False)];built={}
        while stack:
            i,j,ready=stack.pop()
            if i==j:continue
            if (i,j) in blocks:
                _,tree=knuth_fallback(p[i:j],q[i:j+1],stats)
                built[i,j]=shifted(tree,i,stats);stats['face_ambiguous_blocks']+=1;stats['face_payload_keys']+=j-i
            else:
                r=forced[i,j]
                if ready:built[i,j]=(r,built.pop((i,r),None),built.pop((r+1,j),None))
                else:stack.extend(((i,j,True),(r+1,j,False),(i,r,False)))
        tree=built[0,n];value=evaluate(tree,p,q,stats)
        return dict(cost=value,tree=tree,method='face',blocks=self.plan['blocks'],coarse_mass=self.mass,delta=delta,error=error,unique_coarse=self.plan['unique'],layers=self.layers)


def solve(p,q,stats=None,delta=None):
    stats=Counter() if stats is None else stats;n=len(p)
    assert len(q)==n+1 and all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
    if not n:return dict(cost=0,tree=None,method='empty',blocks=[])
    top=max((*p,*q));cert=None
    candidates=[Fraction(delta)] if delta is not None else ([Fraction(top,m) for m in range(1,17)] if top else [Fraction(1)])
    for scale in candidates:
        cert=certificate(p,q,scale,stats)
        if cert is not None:break
    if cert is None:
        value,tree=knuth_fallback(p,q,stats);stats['face_certificate_rejections']+=1
        return dict(cost=value,tree=tree,method='knuth',blocks=[(0,n)])
    prepared=Prepared(cert['p'],cert['q'],stats)
    return prepared.refine(p,q,cert['delta'],stats)
