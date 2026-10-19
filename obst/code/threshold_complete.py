#!/usr/bin/env python3
"""Exact mixed OBST via Cartesian candidate and global threshold certificate.

Linear screening and successful construction for arbitrary weights, using
dyadic-rank selection. Failed certificates use an exact prior constructor.
No unrestricted subquadratic claim. All arithmetic is exact integer arithmetic.
"""
from collections import Counter
from complete import minimum_ipl
from research import check_weights,knuth
from sparse import Counted


def select_value(values,k,stats):
    """Standard deterministic median-of-five selection, ascending rank k."""
    a=list(values);stats['selection_copy_items']+=len(a)
    while True:
        stats['selection_input_items']+=len(a)
        if len(a)<=5:
            return sorted(Counted(x,stats) for x in a)[k].value
        medians=[]
        for start in range(0,len(a),5):
            group=sorted(Counted(x,stats) for x in a[start:start+5])
            stats['selection_group_items']+=len(group)
            medians.append(group[len(group)//2].value)
        pivot=select_value(medians,len(medians)//2,stats)
        less=[];greater=[];equal=0
        for x in a:
            stats['selection_partition_items']+=1
            stats['bound_weight_comparisons']+=1
            if x<pivot:less.append(x)
            else:
                stats['bound_weight_comparisons']+=1
                if x>pivot:greater.append(x)
                else:equal+=1
        if k<len(less):a=less
        elif k<len(less)+equal:return pivot
        else:k-=len(less)+equal;a=greater


def ranked_external(q,stats):
    """Sum sorted q_r * (ceil(log2 r)+1), r>=2, in linear work.

    Peel the lowest coefficient block; retained top ranks halve after
    the first iteration. Only constant-size groups are ever sorted.
    """
    current=list(q);value=0;stats['rank_copy_items']+=len(current)
    while len(current)>1:
        N=len(current);k=1<<((N-1).bit_length()-1)
        stats['rank_level_items']+=N
        pivot=select_value(current,N-k,stats)
        top=[]
        for x in current:
            stats['rank_partition_items']+=1;stats['bound_weight_comparisons']+=1
            if x>pivot:top.append(x)
        top.extend([pivot]*(k-len(top)))
        stats['rank_output_items']+=k;stats['rank_sum_items']+=N+k
        value+=(k.bit_length()+1)*(sum(current)-sum(top))
        current=top
    return value


def gap_bound(q,stats):
    """Integral of the exact binary-indicator alphabetic optima."""
    N=len(q);assert N
    h=N.bit_length()-1;S=1<<h;s=N-S
    low=high=q[0];low_count=high_count=0;total=falls=0;previous=q[0]
    for x in q:
        stats['gap_bound_input_items']+=1
        total+=x;falls+=max(previous-x,0);previous=x
        if x<low:low=x;low_count=1
        elif x==low:low_count+=1
        if x>high:high=x;high_count=1
        elif x==high:high_count+=1
    if high_count>=S//2 and low_count>=s:
        ranked=(h+1)*total-S*high+s*low
        stats['gap_linear_formula']=1
    else:
        ranked=ranked_external(q,stats)
        stats['gap_selection_formula']=1
    value=ranked+high-q[0]+falls
    stats['gap_lower_bound']=value
    return value


def attempt(p,q):
    check_weights(p,q);n=len(p)
    stats=Counter(input_keys=n,validation_input_weights=2*n+1)
    if not n:return 0,None,stats+Counter(certified=1)
    left=[-1]*n;right=[-1]*n;stack=[]
    for i,x in enumerate(p):
        last=-1
        while stack:
            stats['cartesian_comparisons']+=1
            if p[stack[-1]]>=x:break
            last=stack.pop();stats['cartesian_pops']+=1
        if stack:right[stack[-1]]=i
        left[i]=last;stack.append(i);stats['cartesian_pushes']+=1
    root=stack[0];todo=[(root,1)];order=[];key_cost=gap_cost=H=length_sum=0
    minimum=[];maximum=[]
    while todo:
        i,d=todo.pop();order.append(i);stats['candidate_key_visits']+=1
        x=p[i];key_cost+=x*d
        if x:
            H+=1;length_sum+=d
            while len(minimum)<d:minimum.append(None);maximum.append(None)
            lo=minimum[d-1];hi=maximum[d-1]
            minimum[d-1]=x if lo is None else min(lo,x)
            maximum[d-1]=x if hi is None else max(hi,x)
        if left[i]<0:gap_cost+=q[i]*d;stats['candidate_gap_visits']+=1
        else:todo.append((left[i],d+1))
        if right[i]<0:gap_cost+=q[i+1]*d;stats['candidate_gap_visits']+=1
        else:todo.append((right[i],d+1))
    stats['positive_keys']=H;stats['positive_length_sum']=length_sum
    if length_sum!=minimum_ipl(H)+H:
        stats['key_profile_rejected']=1;return None,None,stats
    previous=None
    for lo,hi in zip(minimum,maximum):
        stats['key_profile_levels']+=1
        if lo is None:continue
        if previous is not None and previous<hi:
            stats['key_profile_rejected']=1;return None,None,stats
        previous=lo
    lower=gap_bound(q,stats)
    assert gap_cost>=lower
    stats['key_lower_bound']=key_cost
    stats['global_lower_bound']=key_cost+lower
    stats['candidate_cost']=key_cost+gap_cost
    if gap_cost!=lower:
        stats['gap_profile_rejected']=1;return None,None,stats
    built=[None]*n
    for i in reversed(order):
        built[i]=(i,None if left[i]<0 else built[left[i]],None if right[i]<0 else built[right[i]])
        stats['constructed_keys']+=1
    stats['certified']=1
    return key_cost+gap_cost,built[root],stats


def solve(p,q):
    value,tree,stats=attempt(p,q)
    if value is None:
        value,tree,scans=knuth(p,q)
        stats['fallback_dense_states']=len(p)*(len(p)+1)//2
        stats['fallback_root_candidates']=scans
        stats['fallback_constructed_keys']=len(p)
    return value,tree,stats


def portfolio_solve(p,q):
    # Preserve the preceding profile shortcut before paying for another
    # whole candidate. Three distinct key levels reject that classifier
    # immediately on the new positive multilevel family.
    from profile_complete import attempt as profile_attempt
    value,tree,old=profile_attempt(p,q)
    stats=Counter({'previous_profile_'+k:v for k,v in old.items()})
    if value is not None:return value,tree,stats
    value,tree,new=attempt(p,q);stats.update(new)
    if value is None:
        from run_complete import portfolio_solve as previous
        value,tree,old=previous(p,q)
        stats.update({'previous_'+k:v for k,v in old.items()})
    return value,tree,stats
