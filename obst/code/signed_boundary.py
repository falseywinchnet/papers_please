"""Recover integer gap weights from value-only signed endpoint response.

The exact oracle is a specified interface, not supplied by a faster general
OBST algorithm. LineOracle is the separately proved convex-chain restriction.
"""
from fractions import Fraction
from collections import Counter


def chain_costs(p,q,stats=None):
    stats=Counter() if stats is None else stats
    n=len(p);assert n>=1 and len(q)==n+1
    W=sum(p)+sum(q)
    C=[sum((i+1)*x for i,x in enumerate(p))+q[0]+n*q[-1]+sum((j+1)*q[j] for j in range(1,n))]
    if n>1:
        delta=2*(p[0]+q[0])+q[1]-W
        for r in range(1,n):
            C.append(C[-1]+delta);stats['signed_chain_updates']+=1
            if r<n-1:delta+=2*p[r]+q[r]+q[r+1]
    assert all(C[r-1]-2*C[r]+C[r+1]>=0 for r in range(1,n-1))
    return C


class LineOracle:
    def __init__(self,p,q,stats=None):
        self.stats=Counter() if stats is None else stats
        self.n=len(p);self.W=sum(p)+sum(q);self.T=4*(self.n+1)*(self.W+2)
        self.C=chain_costs(p,q,self.stats)
    def __call__(self,x,y):
        assert y==-self.T
        t=x+self.T;assert abs(t)<=self.W+2
        lo=0;hi=self.n-1
        while lo<hi:
            mid=(lo+hi)//2;self.stats['signed_line_comparisons']+=1
            if self.C[mid+1]-self.C[mid]+t<0:lo=mid+1
            else:hi=mid
        return self.C[lo]+(lo+1)*t-self.T*(self.n+1)


def recover_gaps(p,W,q0,oracle,stats=None):
    stats=Counter() if stats is None else stats
    n=len(p);assert n>=1 and isinstance(W,int) and isinstance(q0,int) and all(isinstance(x,int) and x>=0 for x in p)
    if n==1:return [q0,W-p[0]-q0]
    initial_queries=stats['signed_recovery_queries']
    M=n+1;T=4*M*(W+2);C=[None]*n
    def query(t0):
        t0=Fraction(t0);B=t0.denominator;t=t0+Fraction(1,B*M)
        value=Fraction(oracle(-T+t,-T))+T*M
        z=value*B*M;assert z.denominator==1
        a=int(z)%M;assert 1<=a<=n
        c=value-a*t;assert c.denominator==1
        stats['signed_recovery_queries']+=1
        stats['signed_largest_denominator']=max(stats['signed_largest_denominator'],B*M)
        return a-1,int(c)
    r,c=query(W+1);assert r==0;C[0]=c
    r,c=query(-W-1);assert r==n-1;C[-1]=c
    todo=[(0,n-1)]
    while todo:
        l,r=todo.pop()
        if r-l<=1:continue
        slope=Fraction(C[l]-C[r],r-l);k,c=query(slope)
        if c+(k+1)*slope==C[l]+(l+1)*slope:
            for j in range(l+1,r):
                v=C[l]-(j-l)*slope;assert v.denominator==1
                C[j]=int(v);stats['signed_collinear_fills']+=1
        else:
            assert l<k<r and C[k] is None;C[k]=c
            todo.append((l,k));todo.append((k,r));stats['signed_strict_splits']+=1
    q=[q0,W+C[1]-C[0]-2*(p[0]+q0)]
    for r in range(1,n-1):q.append(C[r-1]-2*C[r]+C[r+1]-2*p[r]-q[r])
    q.append(W-sum(p)-sum(q));assert len(q)==n+1 and all(x>=0 for x in q)
    stats['signed_recovered_gaps']+=len(q)
    assert stats['signed_recovery_queries']-initial_queries<=n
    return q
