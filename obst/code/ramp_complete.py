#!/usr/bin/env python3
"""Exact minimum-IPL optimization in a certified corridor around an affine fit.

The signed residual profile bounds how much any shape can gain over the
left-filled reference. Affine baseline regret excludes grid states. A separate
existing residual-Huffman gate certifies global optimality; otherwise use Knuth.
Both slopes are robustly inferred and either orientation may be selected.
"""
from collections import Counter

from complete import parameters, minimum_ipl, from_lengths, residual_huffman
from ordered_complete import sorted_desc
from research import check_weights, cost, knuth
from ruler_barrier import construct
from sparse import Counted


def counted_sort(values,stats,name,reverse=False):
    counts=Counter()
    result=[x.value for x in sorted((Counted(v,counts) for v in values),reverse=reverse)]
    stats[name]+=counts['bound_weight_comparisons']
    stats[name+'_items']+=len(result)
    return result


def robust_slope(values,stats):
    """Median of disjoint half-separated secants, rounded to an integer."""
    m=len(values)//2
    if not m:return 0
    differences=[values[i+m]-values[i] for i in range(m)]
    median=counted_sort(differences,stats,'fit_comparisons')[m//2]
    return max(0,(median+m//2)//m)


def fit(p,q,reference,stats):
    n=len(p);h,S,s=parameters(n);z=S-s
    lam=robust_slope(p,stats);mu=robust_slope(q,stats);gamma=lam+2*mu
    dp=[v-lam*i for i,v in enumerate(p)]
    dq=[v-mu*i for i,v in enumerate(q)]
    ps=counted_sort(dp,stats,'profile_comparisons',reverse=True)
    qs=counted_sort(dq,stats,'profile_comparisons',reverse=True)
    lower=sum(v*(i+1).bit_length() for i,v in enumerate(ps))
    lower+=h*sum(qs)+(sum(qs[-2*s:]) if s else 0)
    residual_reference=cost(reference,dp,dq)
    stats['reference_cost_keys']+=n;stats['reference_cost_gaps']+=n+1
    V=residual_reference-lower
    assert V>=0
    D=min(s*z,V//gamma) if gamma else s*z
    bound=S+1+min(s*z,D*z.bit_length())
    if not V:bound=S+1
    return dict(key_slope=lam,gap_slope=mu,gamma=gamma,gain_bound=V,
                inversion_budget=D,state_upper_bound=bound,
                residual_reference=residual_reference,profile_lower_bound=lower)


def potential_prefix(S,lam,mu,stats):
    prefix=[0];bits=[0]
    for g in range(S):
        # bit_count is absent from the M4's Python 3.9. Build popcounts linearly.
        if g:bits.append(bits[g//2]+(g&1))
        prefix.append(prefix[-1]+(2*lam+2*mu)*g-lam*bits[g])
        stats['potential_terms']+=1
    return prefix


def state_regret(prefix,s,a,b):
    return prefix[s+a]-prefix[s-b+a]-prefix[s]+prefix[s-b]


def reflect(tree,n,stats):
    if tree is None:return None
    r,l,z=tree;stats['reflection_nodes']+=1
    return n-1-r,reflect(z,n,stats),reflect(l,n,stats)


def optimize_shape(p,q,state_budget=None):
    """Return the exact class optimum, or None before DP if its budget is large."""
    check_weights(p,q);n=len(p);h,S,s=parameters(n);stats=Counter(input_keys=n)
    reference_counts=Counter();reference=construct(0,n,reference_counts)
    stats['reference_constructed_keys']=n
    if not s:
        value=cost(reference,p,q);stats['fixed_shape']=1
        stats['fixed_cost_keys']=n;stats['fixed_cost_gaps']=n+1
        stats['constructed_keys']=n
        return value,reference,stats,dict(fixed_shape=True)
    fits=[]
    for reverse in (False,True):
        pp,qq=(p[::-1],q[::-1]) if reverse else (p,q)
        model=fit(pp,qq,reference,stats);model['reversed']=reverse
        fits.append(model)
    model=min(fits,key=lambda m:(m['state_upper_bound'],m['inversion_budget'],m['reversed']))
    stats['state_upper_bound']=model['state_upper_bound']
    if state_budget is not None and model['state_upper_bound']>state_budget:
        stats['state_budget_rejected']=1
        return None,None,stats,model
    pp,qq=(p[::-1],q[::-1]) if model['reversed'] else (p,q)
    if model['gain_bound']==0:
        tree=reference;value=cost(tree,pp,qq);stats['profile_attained']=1
        stats['constructed_keys']=n
    else:
        prefix=potential_prefix(S,model['key_slope'],model['gap_slope'],stats)
        previous={0:0};parents=[];stats['shape_states']=1
        for g in range(S):
            current={};pred={}
            d=h-((g+1 & -(g+1)).bit_length()-1)
            for e,value in previous.items():
                i=g+e
                for x in (0,1):
                    after=e+x
                    if not 0<=s-after<=S-g-1:continue
                    stats['candidate_transitions']+=1
                    a=g+1-after;b=s-after
                    regret=state_regret(prefix,s,a,b)
                    stats['regret_queries']+=1
                    assert regret>=model['gamma']*a*b
                    if regret>model['gain_bound']:
                        stats['corridor_rejections']+=1
                        continue
                    v=value+(d*pp[i+x] if g<S-1 else 0)
                    v+=(h+1)*(pp[i]+qq[i]+qq[i+1]) if x else h*qq[i]
                    stats['admitted_transitions']+=1
                    if after not in current or v<current[after]:
                        current[after]=v;pred[after]=(e,x)
            assert current
            stats['shape_states']+=len(current);previous=current;parents.append(pred)
        value=previous[s]
        assert stats['shape_states']<=model['state_upper_bound']
        e=s;choices=[]
        for pred in reversed(parents):
            e,x=pred[e];choices.append(x)
        choices.reverse();lengths=[]
        for g,x in enumerate(choices):
            if x:lengths.append(h+1)
            if g<S-1:lengths.append(h-((g+1 & -(g+1)).bit_length()-1))
        tree=from_lengths(lengths);stats['constructed_keys']=len(lengths)
        assert len(lengths)==n and sum(lengths)-n==minimum_ipl(n)
    if model['reversed']:tree=reflect(tree,n,stats)
    stats['reconstruction_cost_keys']+=n;stats['reconstruction_cost_gaps']+=n+1
    assert cost(tree,p,q)==value
    return value,tree,stats,model


def attempt(p,q,state_budget=None,*,preflight=True):
    check_weights(p,q);n=len(p)
    if not n:
        return 0,None,Counter(input_keys=0,constructed_keys=0,certified=1),dict(fixed_shape=True)
    if not preflight:
        value,tree,stats,model=optimize_shape(p,q,state_budget)
        if value is None:return None,None,stats,model
    proof=Counter()
    ps=sorted_desc(p,proof);qs=sorted_desc(q,proof);a=ps[-1];b=qs[-1]
    residual=residual_huffman(ps,qs,a,b,proof)
    lower=(a+b)*(minimum_ipl(n)+1)+(a+2*b)*n+residual
    proof['nonminimal_lower_bound']=lower;proof['residual_lower_bound']=residual
    if preflight:
        h,S,s=parameters(n)
        class_lower=sum(v*(i+1).bit_length() for i,v in enumerate(ps))
        class_lower+=h*sum(qs)+(sum(qs[-2*s:]) if s else 0)
        proof['class_profile_terms']=2*n+1;proof['class_profile_lower_bound']=class_lower
        if class_lower>lower:
            proof['input_keys']=n;proof['preflight_rejected']=proof['global_gate_rejected']=1
            return None,None,proof,dict(preflight_rejected=True)
        value,tree,stats,model=optimize_shape(p,q,state_budget)
        if value is None:
            stats.update(proof)
            return None,None,stats,model
    stats.update(proof);stats['candidate_cost']=value
    if value<=lower:
        stats['certified']=1
        return value,tree,stats,model
    stats['global_gate_rejected']=1
    return None,None,stats,model


def solve(p,q,*,preflight=True):
    n=len(p)
    budget=max(1,n*max(1,n.bit_length())**2)
    value,tree,stats,model=attempt(p,q,budget,preflight=preflight)
    stats['shape_state_budget']=budget
    if value is None:
        value,tree,scans=knuth(p,q)
        stats['fallback_dense_states']=n*(n+1)//2
        stats['fallback_root_candidates']=scans;stats['fallback_constructed_keys']=n
    return value,tree,stats,model
