#!/usr/bin/env python3
"""Full mixed OBST with range-sensitive shape certificates.

Perfect sizes use the sharp universal box threshold. Other sizes use
shortening capacities, independent of total residual mass. The existing
nonlinear exchange corridor optimizes the original costs after acceptance;
rejection uses full exact Knuth. Arithmetic is integer or Fraction.
"""
from collections import Counter
from fractions import Fraction
from exchange_corridor import model,optimize
from trimmed_height import balanced,knuth_fallback
from coarse_face import evaluate


def shape_certificate(p,q,stats):
    n=len(p)
    if not n:return dict(accepted=True,kind='empty',threshold=0)
    a=min(p);b=min(q);P=max(p)-a;Q=max(q)-b
    E=sum(x-a for x in p)+sum(x-b for x in q)
    L=n.bit_length();K=(1<<L)-L-1;G=0 if L==1 else 1<<(L-1)
    options=[((n-1)*E,'total_mass'),(P*K+Q*G,'range_capacity')]
    if n+1==1<<L:options.append((P*(n-L)+(Q if n>1 else 0),'perfect_box'))
    threshold,kind=min(options,key=lambda item:(item[0],item[1]))
    stats['range_certificate_items']+=2*n+1
    return dict(accepted=a+b>=threshold,kind=kind,threshold=threshold,
                key_baseline=a,gap_baseline=b,key_range=P,gap_range=Q,
                residual_mass=E,height=L,key_capacity=K,gap_capacity=G)


def solve(p,q,stats=None):
    stats=Counter() if stats is None else stats;n=len(p)
    assert len(q)==n+1 and all(isinstance(x,(int,Fraction)) and x>=0 for x in (*p,*q))
    cert=shape_certificate(p,q,stats)
    if not n:return dict(cost=0,tree=None,method='empty',certificate=cert)
    if cert['accepted']:
        if cert['residual_mass']==0 or n+1==1<<n.bit_length():
            tree=balanced(0,n);value=evaluate(tree,p,q,stats)
            stats['range_direct_output_keys']+=n
            return dict(cost=value,tree=tree,method='range_direct',certificate=cert)
        fit=model(p,q,stats);value,tree=optimize(p,q,fit,stats)
        stats['range_certified_corridors']+=1
        return dict(cost=value,tree=tree,method='range_corridor',model=fit,certificate=cert)
    stats['range_certificate_rejections']+=1
    value,tree=knuth_fallback(p,q,stats)
    return dict(cost=value,tree=tree,method='knuth',certificate=cert)
