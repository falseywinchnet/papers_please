#!/usr/bin/env python3
"""Exact mixed OBST using a nonlinear ordered-reference inversion corridor.

A linear prefix-envelope fit supplies a strictly increasing reference with
unit exchange margin. A separate baseline certificate proves that the
original optimum has minimum internal path length. Rejected inputs use
ordinary full Knuth. No timings or sampled success gate are used.
"""
from collections import Counter
from fractions import Fraction
from complete import parameters,from_lengths
from trimmed_height import knuth_fallback,balanced
from coarse_face import evaluate


def model(p,q,stats):
    n=len(p);h,S,s=parameters(n);z=S-s
    low=min(q);Eq=sum(x-low for x in q)
    stats['exchange_gap_fit_items']+=n+1
    plans=[]
    for reverse in (False,True):
        pp=p[::-1] if reverse else p;last=None;Ep=0
        for x in pp:
            last=x if last is None else max(x,last+1)
            Ep+=last-x;stats['exchange_key_fit_items']+=1
        V=h*Ep+Eq;D=V.numerator//V.denominator if isinstance(V,Fraction) else V
        plans.append(dict(reversed=reverse,key_error=Ep,gap_error=Eq,gain_bound=V,
                          inversion_budget=D,state_bound=S+1+min(s*z,D*z.bit_length())))
    return min(plans,key=lambda x:(x['gain_bound'],x['reversed']))


def optimize(p,q,fit,stats):
    n=len(p);h,S,s=parameters(n);z=S-s;D=fit['inversion_budget']
    pp=p[::-1] if fit['reversed'] else p;qq=q[::-1] if fit['reversed'] else q
    previous=[0];oldlo=0;parents=[];lo=0
    stats['exchange_shape_states']+=1
    for g in range(S):
        # On layer g+1, both (g+1-e) and (s-e) decrease with e.
        lo=max(lo,g+1-z)
        while (g+1-lo)*(s-lo)>D:
            lo+=1;stats['exchange_lower_bound_increments']+=1
        hi=min(g+1,s)
        current=[None]*(hi-lo+1);pred=bytearray([2])*(hi-lo+1)
        d=h-((g+1 & -(g+1)).bit_length()-1)
        for index,value in enumerate(previous):
            e=oldlo+index;i=g+e
            for x in (0,1):
                after=e+x;stats['exchange_considered_transitions']+=1
                if not lo<=after<=hi:continue
                v=value+((h+1)*(pp[i]+qq[i]+qq[i+1]) if x else h*qq[i])
                if g<S-1:v+=d*pp[i+x]
                dest=after-lo;stats['exchange_admitted_transitions']+=1
                if current[dest] is None or v<current[dest]:current[dest]=v;pred[dest]=x
        assert all(x is not None for x in current)
        parents.append((lo,pred));previous=current;oldlo=lo
        stats['exchange_shape_states']+=len(current);stats['exchange_layer_bounds']+=1
    value=previous[s-oldlo];e=s;choices=[]
    for lo,pred in reversed(parents):
        x=pred[e-lo];assert x<2;choices.append(x);e-=x
    choices.reverse();lengths=[]
    for g,x in enumerate(choices):
        if x:lengths.append(h+1)
        if g<S-1:lengths.append(h-((g+1 & -(g+1)).bit_length()-1))
    assert len(lengths)==n and stats['exchange_shape_states']<=fit['state_bound']
    if fit['reversed']:lengths.reverse();stats['exchange_reflected_lengths']+=n
    tree=from_lengths(lengths);stats['exchange_output_keys']+=n
    assert evaluate(tree,p,q,stats)==value
    return value,tree


def solve(p,q,stats=None):
    stats=Counter() if stats is None else stats;n=len(p)
    assert len(q)==n+1 and all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
    if not n:return dict(cost=0,tree=None,method='empty')
    a=min(p);b=min(q);E=sum(x-a for x in p)+sum(x-b for x in q)
    stats['exchange_global_gate_items']+=2*n+1
    if not E:
        tree=balanced(0,n);value=evaluate(tree,p,q,stats);stats['exchange_uniform_output_keys']+=n
        return dict(cost=value,tree=tree,method='uniform')
    if E and a+b<=(n-1)*E:
        stats['exchange_global_gate_rejections']+=1
        value,tree=knuth_fallback(p,q,stats)
        return dict(cost=value,tree=tree,method='knuth')
    fit=model(p,q,stats);value,tree=optimize(p,q,fit,stats)
    stats['exchange_certified_solves']+=1
    return dict(cost=value,tree=tree,method='exchange_corridor',model=fit,
                global_certificate=dict(key_baseline=a,gap_baseline=b,residual_mass=E))
