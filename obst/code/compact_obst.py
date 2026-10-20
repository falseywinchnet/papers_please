#!/usr/bin/env python3
"""Full mixed-weight optimal BST via condensed Monge penalty layers.

The compact product implements the cited ESA 2025 algorithm. No full interval
cost or root table is built. Ordinary witness arrays replace succinct maps,
so this implementation's witness storage can have an extra logarithmic factor.
"""
from collections import Counter
from core_monge import Monge,multiply
from penalty_layers import fib_limit
from research import check_weights


def solve(p,q,early_stop=True,observer=None):
    check_weights(p,q);n=len(p);stats=Counter();layers=[]
    if not n:return 0,None,dict(stats),layers
    w=sum(p)+sum(q);L=n.bit_length()
    H=min(n,fib_limit(w)+(0 if all(x>0 for x in p) else L))
    M=(H+1)*w+1;P=4*n*M+4*w+1
    prefix=[0]
    singles=[]
    for i in range(n):
        prefix.append(prefix[-1]+p[i]+q[i+1])
        singles.append(p[i]+q[i]+q[i+1])
    stats['input_weight_visits']+=2*n+1
    stats['prefix_and_singleton_cells']+=2*n
    old=Monge([M*j for j in range(n+1)],[P*i for i in range(n+1)],
              [(i,i,P+M) for i in range(n)],stats)
    if observer is not None:observer(0,old,None)
    witnesses=[]
    for h in range(1,H+1):
        aa=old.select(list(range(n+1)),list(range(n)))
        bb=old.select(list(range(1,n+1)),list(range(n+1)))
        product,wit=multiply(aa,bb)
        entries=[]
        for i,j,v in product.entries:
            stats['layer_conversion_core_visits']+=1
            if j>=i+2:entries.append((i,j,v))
        for i in range(n):
            entries.append((i,i,P+singles[i]))
            if i+1<n:
                v=(M if h==1 else min(singles[i],singles[i+1]))-q[i+1]
                assert v>=0
                if v:entries.append((i,i+1,v))
        top=[0]+[product.top[j]+prefix[j]+q[0] for j in range(1,n+1)]
        current=Monge(top,[P*i for i in range(n+1)],entries,stats)
        stats['layer_conversion_boundary_cells']+=2*n+1
        stats['completed_layers']+=1
        stats['maximum_layer_core']=max(stats['maximum_layer_core'],current.k)
        stats['maximum_product_core']=max(stats['maximum_product_core'],product.k)
        witnesses.append(wit)
        if observer is not None:observer(h,current,wit)
        equal=False
        if early_stop:
            # A whole condensed-table fixed point, not merely equal top cost.
            stats['fixed_point_boundary_checks']+=n+1
            equal=current.top==old.top and current.k==old.k
            if equal:
                for x,y in zip(current.entries,old.entries):
                    stats['fixed_point_core_checks']+=1
                    if x!=y:equal=False;break
        layers.append(dict(h=h,full_value=current.top[n],completed_core=current.k,
                           product_core=product.k,fixed_point=equal))
        old=current
        if equal:
            stats['fixed_point_terminations']+=1
            break
    h=len(witnesses)
    # Iterative reconstruction avoids Python recursion limits for skew trees.
    values=[];stack=[(0,n,h,None)]
    while stack:
        i,j,budget,r=stack.pop()
        if i==j:
            values.append(None);continue
        assert budget>0,'nonempty penalized terminal survived'
        if r is not None:
            right=values.pop();left=values.pop()
            values.append((r,left,right));stats['constructed_keys']+=1
        else:
            r=witnesses[budget-1].query(i,j)
            assert i<=r<j
            stack.extend(((i,j,budget,r),(r+1,j,budget-1,None),(i,r,budget-1,None)))
    assert len(values)==1
    return old.top[n],values[0],dict(stats),layers
