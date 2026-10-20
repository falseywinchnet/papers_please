#!/usr/bin/env python3
"""Linear two-level depth-profile construction with a global component bound.

All unsuccessful paths use exact Knuth. The reachability representation is
four interval endpoints at high-key boundaries, not an n-by-rank table.
"""
from collections import Counter
from complete import parameters,minimum_ipl,from_lengths,residual_huffman
from research import check_weights,cost,knuth


def shifted(interval):
    return None if interval is None else (interval[0]+1,interval[1]+1)


def joined(a,b):
    if a is None:return b
    if b is None:return a
    assert max(a[0],b[0])<=min(a[1],b[1])+1
    return min(a[0],b[0]),max(a[1],b[1])


def contains(state,r,stats):
    stats['membership_queries']+=1
    if r<0:return False
    interval=state[r%2]
    return interval is not None and interval[0]<=r//2<=interval[1]


def choices(L,target,followed_by_high):
    """Possible incoming rank and a representative low word, at most two."""
    end=target-int(followed_by_high)
    if L==0:yield end,[]
    elif L==1:
        yield end,[0]
        if (end-1)%2==0:yield end-1,[1]
    elif L in (2,3) and (end-1)%2==0:
        yield end-1,([0,1] if L==2 else [0,1,0])


def recognize(pattern,m):
    """Return a valid word of rank m, or None; linear work and space."""
    stats=Counter();a,b=(0,0),None;records=[];L=0
    for high in pattern:
        stats['recognizer_input_keys']+=1
        if not high:L+=1;continue
        records.append((L,a,b));stats['stored_boundaries']+=1
        stats['interval_transitions']+=1
        if L==0:a,b=shifted(b),a
        elif L==1:
            a,b=shifted(joined(a,b)),a
            stats['interval_unions']+=1
        elif L in (2,3):a,b=shifted(a),None
        else:a,b=None,None
        if a is None and b is None:
            stats['dead_prefix']=1
            return None,stats
        if a is not None and b is not None:
            assert a[0]-b[0] in (0,1) and a[1]-b[1] in (0,1)
        L=0
    chosen=next(((r,w) for r,w in choices(L,m,False) if contains((a,b),r,stats)),None)
    if chosen is None:return None,stats
    r,w=chosen;pieces=[w]
    for L,a,b in reversed(records):
        selected=next(((r0,w) for r0,w in choices(L,r,True) if contains((a,b),r0,stats)),None)
        assert selected is not None
        r,w=selected;pieces.append(w+[1]);stats['traceback_boundaries']+=1
    assert r==0
    word=[x for piece in reversed(pieces) for x in piece]
    assert len(word)==len(pattern) and sum(word)==m
    stats['word_output_keys']=len(word)
    return word,stats


def attempt(p,q,*,certify=True):
    check_weights(p,q);n=len(p);stats=Counter(input_keys=n,validation_input_weights=2*n+1)
    if not n:return 0,None,stats+Counter(certified=int(certify))
    levels=[];counts=[]
    for v in p:
        stats['key_classification_items']+=1
        if not levels or v not in levels:
            levels.append(v);counts.append(0)
            if len(levels)>2:
                stats['unsupported_keys']=1;return None,None,stats
        counts[levels.index(v)]+=1
    for i,v in enumerate(q):
        stats['gap_classification_items']+=1
        if v!=q[i%2]:stats['unsupported_gaps']=1;return None,None,stats
    h,S,s=parameters(n);m=S-1
    ordered=sorted(zip(levels,counts),reverse=True)
    hi=ordered[0][0];H=ordered[0][1]
    if s and len(levels)==2 and not S//2-1<=H<=m:
        stats['unsupported_high_count']=1;return None,None,stats
    ps=[v for v,count in ordered for _ in range(count)]
    stats['sorted_weight_records']=len(ordered);stats['expanded_weight_items']=n
    value=sum(v*(i+1).bit_length() for i,v in enumerate(ps))
    value+=h*sum(q)+s*(q[0]+q[1]);stats['profile_cost_terms']=2*n+1
    stats['global_profile_lower_bound']=value
    if not s:
        word=[1]*n;stats['fixed_shape_keys']=n
    elif len(levels)==1:
        word=[0,1]*s+[1]*(m-s);stats['uniform_shape_keys']=n
    else:
        pattern=[int(v==hi) for v in p];stats['pattern_items']=n
        word,sc=recognize(pattern,m);stats.update(sc)
        if word is None:stats['profile_unattained']=1;return None,None,stats
    lengths=[];r=0;last=1
    for x in word:
        assert x or last
        if x:r+=1;lengths.append(h-((r&-r).bit_length()-1))
        else:lengths.append(h+1)
        last=x
    tree=from_lengths(lengths);actual=cost(tree,p,q)
    stats['constructed_keys']=n;stats['direct_cost_keys']=n;stats['direct_cost_gaps']=n+1
    if s:assert actual==value
    # A perfect skeleton has one shape, even if it misses the free profile.
    value=actual;stats['candidate_cost']=value
    if certify:
        profile=stats['global_profile_lower_bound']
        assert value>=profile
        if value==profile:
            stats['certified']=stats['profile_certified']=1
        else:
            # Only the unique perfect shape can miss the free key profile.
            assert not s
            gap_records=sorted(((q[0],(n+2)//2),(q[1],(n+1)//2)),reverse=True)
            qs=[v for v,count in gap_records for _ in range(count)]
            stats['sorted_weight_records']+=2;stats['expanded_weight_items']+=n+1
            a,b=ps[-1],qs[-1];bound=residual_huffman(ps,qs,a,b,stats)
            lower=(a+b)*(minimum_ipl(n)+1)+(a+2*b)*n+bound
            stats['nonminimal_lower_bound']=lower;stats['residual_lower_bound']=bound
            stats['mixed_gate_calls']=1
            if value>lower:stats['gate_rejected']=1;return None,None,stats
            stats['certified']=stats['mixed_certified']=1
    return value,tree,stats


def solve(p,q):
    value,tree,stats=attempt(p,q)
    if value is None:
        value,tree,scans=knuth(p,q)
        stats['fallback_dense_states']=len(p)*(len(p)+1)//2
        stats['fallback_root_candidates']=scans
        stats['fallback_constructed_keys']=len(p)
    return value,tree,stats


def portfolio_solve(p,q):
    """Try the linear profile route, then preserve the preceding portfolio."""
    value,tree,stats=attempt(p,q)
    if value is None:
        from run_complete import portfolio_solve as previous
        value,tree,counts=previous(p,q)
        stats['route_to_previous']=1
        for key,v in counts.items():stats['previous_'+key]=v
    else:stats['route_to_profile']=1
    return value,tree,stats
