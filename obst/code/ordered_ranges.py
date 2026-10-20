#!/usr/bin/env python3
"""Full interval/root-range oracle for certified left/right-filled shapes.

The index stores dyadic-stride prefix sums, never an interval table or a
Monge core. Baseline dominance and the ordered expansion exchange are
checked before accepting a coarse input.
"""
from collections import Counter
from fractions import Fraction


def certificate(p,q,stats):
    n=len(p);a=min(p);b=min(q)
    E=sum(x-a for x in p)+sum(x-b for x in q)
    stats['ordered_certificate_items']+=2*n+1
    if E and a+b<=(n-1)*E:return None
    h=(n+1).bit_length()-1
    for reverse in (False,True):
        pp=p[::-1] if reverse else p;qq=q[::-1] if reverse else q
        ok=True
        for i in range(n-1):
            d=pp[i]-pp[i+1];stats['ordered_exchange_checks']+=1
            if max(d,h*d)>qq[i+2]-qq[i]:ok=False;break
        if ok:return dict(reverse=reverse,key_baseline=a,gap_baseline=b,residual_mass=E)
    return None


class OrderedRanges:
    def __init__(self,p,q,stats=None):
        self.stats=Counter() if stats is None else stats;self.n=len(p)
        assert self.n and len(q)==self.n+1
        assert all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
        self.plan=certificate(p,q,self.stats)
        if self.plan is None:raise ValueError('Ordered-shape certificate not satisfied')
        self.reverse=self.plan['reverse'];p=list(p[::-1] if self.reverse else p);q=list(q[::-1] if self.reverse else q)
        self.p=p;self.q=q;self.pp=[0];self.qq=[0]
        for x in p:self.pp.append(self.pp[-1]+x)
        for x in q:self.qq.append(self.qq[-1]+x)
        self.stats['ordered_prefix_items']+=2*self.n+1
        self.dyadic=[]
        for d in range(self.n.bit_length()):
            stride=1<<d;row=[]
            for k,x in enumerate(p):
                row.append(x+(row[k-stride] if k>=stride else 0))
                self.stats['ordered_dyadic_items']+=1
            self.dyadic.append(row)
        self.base=self
    def ruler(self,offset,step_log,lo,hi,stats):
        if lo>hi:return 0
        result=0
        for d in range(hi.bit_length()):
            power=1<<d;first=((lo+power-1)//power)*power;last=(hi//power)*power
            stats['ordered_ruler_terms']+=1
            if first>last:continue
            first_index=offset+(first<<step_log);last_index=offset+(last<<step_log)
            stride=1<<(d+step_log);row=self.dyadic[d+step_log]
            result+=row[last_index]-(row[first_index-stride] if first_index>=stride else 0)
            stats['ordered_stride_queries']+=1
        return result
    def query(self,i,j,stats=None):
        stats=self.stats if stats is None else stats
        assert 0<=i<=j<=self.n;stats['ordered_interval_queries']+=1
        if i==j:return 0
        if self.reverse:i,j=self.n-j,self.n-i
        m=j-i;h=(m+1).bit_length()-1;c=(1<<h)-1;s=m-c
        reward=self.ruler(i-1,1,1,min(s,c),stats)+self.ruler(i+s-1,0,s+1,c,stats)
        keys=(h+1)*(self.pp[j]-self.pp[i])-reward
        gaps=h*(self.qq[j+1]-self.qq[i])+self.qq[i+2*s]-self.qq[i]
        return keys+gaps
    def pivot(self,i,j):
        m=j-i;h=(m+1).bit_length()-1;c=(1<<h)-1;s=m-c
        offset=(1<<(h-1))-1+min(s,1<<(h-1))
        return j-1-offset if self.reverse else i+offset
    def root_cost(self,i,j,r,stats):
        stats['ordered_root_cost_calls']+=1
        return self.query(i,r,stats)+self.query(r+1,j,stats)
    def minimum(self,i,j,lo,hi,stats):
        assert i<=lo<hi<=j
        r=max(lo,min(hi-1,self.pivot(i,j)));stats['ordered_range_queries']+=1
        return self.root_cost(i,j,r,stats)
    def below(self,i,j,threshold,stats,valid=None):
        lo,hi=(i,j) if valid is None else valid
        assert i<=lo<=hi<=j
        if lo==hi:return
        pivot=max(lo,min(hi-1,self.pivot(i,j)))
        stats['ordered_threshold_queries']+=1
        if self.root_cost(i,j,pivot,stats)>threshold:return
        a,b=lo,pivot
        while a<b:
            mid=(a+b)//2;stats['ordered_threshold_comparisons']+=1
            if self.root_cost(i,j,mid,stats)<=threshold:b=mid
            else:a=mid+1
        start=a;a,b=pivot,hi-1
        while a<b:
            mid=(a+b+1)//2;stats['ordered_threshold_comparisons']+=1
            if self.root_cost(i,j,mid,stats)<=threshold:a=mid
            else:b=mid-1
        for r in range(start,a+1):
            stats['ordered_emitted_roots']+=1
            yield r
