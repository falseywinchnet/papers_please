#!/usr/bin/env python3
"""Two endpoint prices for a valid full mixed OBST lower-bound certificate.

All LP vertices and separation cuts are exact. A bounded number of cuts
does not imply that the maximum has been found. Integer-cost rounding is
used only for integer original inputs. Rejection falls back to Knuth.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd
from shifted_alphabetic import alphabetic,tree_cost
from research import knuth


def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def upper_vertex(cuts,L,R,stats):
    """Maximize z under supporting planes and box; integer Cramer's rule."""
    rows=[(-u,-v,1,c) for u,v,c in cuts]+[(-1,0,0,0),(1,0,0,L),(0,-1,0,0),(0,1,0,R)]
    best=None
    for aa,bb,cc in combinations(rows,3):
        stats['lp_vertex_triples']+=1
        den=det3(aa,bb,cc)
        if not den:continue
        columns=list(zip(aa,bb,cc));rhs=columns[3]
        nums=[det3(rhs,columns[1],columns[2]),det3(columns[0],rhs,columns[2]),det3(columns[0],columns[1],rhs)]
        if den<0:den=-den;nums=[-z for z in nums]
        if best and nums[2]*best[3]<best[2]*den:continue
        feasible=True
        for A,B,C,D in rows:
            stats['lp_constraint_checks']+=1
            if A*nums[0]+B*nums[1]+C*nums[2]>D*den:feasible=False;break
        if feasible and (best is None or nums[2]*best[3]>best[2]*den):best=(*nums,den)
    assert best is not None
    return tuple(Fraction(z,best[3]) for z in best[:3])


def oracle(p,q,a,x,y,stats):
    n=len(p);L=p[0]+q[0];R=p[-1]+q[-1]
    x=Fraction(x);y=Fraction(y);scale=x.denominator*y.denominator//gcd(x.denominator,y.denominator)
    X=int(x*scale);Y=int(y*scale)
    pp=[X]+[(v-a)*scale for v in p[1:-1]]+[Y]
    qq=[L*scale-X]+[(v+a)*scale for v in q[1:-1]]+[R*scale-Y]
    assert min(pp+qq)>=0
    stats['oracle_transform_items']+=2*n+1
    stats['oracle_validation_items']+=2*n+1
    gap,tree,counts=alphabetic(qq)
    stats.update({'alphabetic_'+k:v for k,v in counts.items()});stats['oracle_calls']+=1
    class Weighted:
        __slots__=('i',)
        def __init__(self,i):self.i=i
        def __lt__(self,other):
            stats['key_sort_comparisons']+=1
            return (-pp[self.i],self.i)<(-pp[other.i],other.i)
    order=sorted(Weighted(i) for i in range(n));lengths=[0]*n
    stats['rank_wrapper_items']+=n;stats['rank_assignments']+=n;stats['key_sum_items']+=n
    for j,item in enumerate(order):lengths[item.i]=(j+1).bit_length()
    key=sum(v*d for v,d in zip(pp,lengths));qd=[0]*(n+1)
    todo=[(tree,0,n,0)]
    while todo:
        t,lo,hi,d=todo.pop()
        if t is None:assert lo==hi;qd[lo]=d;stats['depth_gap_visits']+=1
        else:
            r,l,rr=t;todo.extend(((l,lo,r,d+1),(rr,r+1,hi,d+1)));stats['depth_key_visits']+=1
    bx=lengths[0]-qd[0];by=lengths[-1]-qd[-1]
    intercept=sum((v-a)*d for v,d in zip(p[1:-1],lengths[1:-1]))+L*qd[0]+R*qd[-1]+sum((v+a)*d for v,d in zip(q[1:-1],qd[1:-1]))-a*n
    value=Fraction(key+gap,scale)-a*n
    assert value==intercept+bx*x+by*y
    stats['intercept_sum_items']+=2*n-3
    full=tree_cost(tree,p,q,stats)
    return value,(bx,by,intercept),full,tree


def attempt(p,q,budget=None,stop_on_certificate=True):
    n=len(p);stats=Counter()
    if n<3:
        v,t,scans=knuth(p,q);stats['tiny_root_candidates']=scans;stats['certified']=1
        return v,t,stats,dict(lower=Fraction(v),upper=Fraction(v),max_complete=True,history=[])
    if len(q)!=n+1 or any(type(v) is not int or v<0 for v in p+q):raise ValueError('nonnegative integer original weights required')
    stats['input_validation_items']+=2*n+1;stats['interior_min_items']+=n-2
    a=min(p[1:-1]);L=p[0]+q[0];R=p[-1]+q[-1]
    if budget is None:budget=max(2,n.bit_length())
    x=Fraction(max(0,p[0]-a));y=Fraction(max(0,p[-1]-a))
    cuts=set();history=[];best=None;candidate=None;candidate_tree=None;upper=None;complete=False
    for iteration in range(budget):
        value,plane,cost,tree=oracle(p,q,a,x,y,stats)
        if best is None or value>best:best=value
        if candidate is None or cost<candidate:candidate=cost;candidate_tree=tree
        history.append(dict(x=x,y=y,lower=value,plane=plane,candidate=cost))
        assert best<=candidate
        certified=(candidate*best.denominator-best.numerator<best.denominator)
        if certified and stop_on_certificate:break
        cuts.add(plane)
        xx,yy,upper=upper_vertex(cuts,L,R,stats)
        assert upper>=best
        if upper==best:complete=True;break
        x,y=xx,yy
    certified=(candidate*best.denominator-best.numerator<best.denominator)
    stats.update(dict(input_keys=n,shift=a,certified=int(certified),max_complete=int(complete),cut_count=len(cuts)))
    metadata=dict(lower=best,upper=upper,max_complete=complete,history=history)
    return (candidate,candidate_tree,stats,metadata) if certified else (None,None,stats,metadata)


def solve(p,q,budget=None):
    v,t,s,meta=attempt(p,q,budget)
    if v is None:
        v,t,scans=knuth(p,q);s['fallback_dense_states']=len(p)*(len(p)+1)//2;s['fallback_root_candidates']=scans
    return v,t,s,meta
