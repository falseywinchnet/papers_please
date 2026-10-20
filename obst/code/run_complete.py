#!/usr/bin/env python3
"""Exact shape optimization by runs of (p_i, q_i+q_(i+1)).

Block rewards telescope in skeleton rank. Monotone deques evaluate all
boundary transfers, and Hirschberg-style recomputation reconstructs in linear
space. A separate existing mixed residual bound certifies full optimality.
"""
from collections import Counter,deque

from complete import parameters,minimum_ipl,from_lengths,residual_huffman
from research import check_weights,cost,knuth
from sparse import Counted


def signature_runs(p,q,stats):
    blocks=[]
    for i,a in enumerate(p):
        c=q[i]+q[i+1];stats['signature_items']+=1
        if blocks and blocks[-1][2:]==(a,c):
            start,_,_,_=blocks[-1];blocks[-1]=(start,i+1,a,c)
        else:blocks.append((i,i+1,a,c))
    stats['signature_runs']=len(blocks)
    return blocks


def limits(L,t,u):
    """Possible skeleton counts in a nonempty block with boundary bits t,u."""
    low=((L+1)//2 if t else L//2+1) if u else (L//2 if t else (L+1)//2)
    return low,L-(1-u)


def block_word(L,m,t,u):
    low,high=limits(L,t,u);assert low<=m<=high
    z=L-m
    if u:
        word=([1] if not t else [])+[0,1]*z+[1]*(m-z-(not t))
    elif t:
        word=[1]*(m-z+1)+[0]+[1,0]*(z-1)
    else:
        word=[1]*(m-z)+[1,0]*z
    assert len(word)==L
    return word


def transfer(previous,L,U,backward,stats):
    """Four sliding-window maxima, preserving both last-key boundary bits."""
    width=len(U);current=[[None]*width for _ in (0,1)]
    stats['block_transfers']+=1;stats['transfer_profile_slots']+=2*width
    for t in (0,1):
        for u in (0,1):
            low,high=limits(L,t,u)
            if low>high:continue
            src=previous[u if backward else t]
            dst=current[t if backward else u];queue=deque();cursor=0
            for j in range(width):
                lo,hi=(j+low,j+high) if backward else (j-high,j-low)
                hi=min(hi,width-1)
                while cursor<=hi:
                    v=src[cursor]
                    if v is not None:
                        v=v+U[cursor] if backward else v-U[cursor]
                        while queue:
                            stats['deque_value_comparisons']+=1
                            if queue[-1][1]>v:break
                            queue.pop();stats['deque_dominated_pops']+=1
                        queue.append((cursor,v));stats['deque_pushes']+=1
                    cursor+=1;stats['source_positions_scanned']+=1
                while queue and queue[0][0]<lo:
                    queue.popleft();stats['deque_expired_pops']+=1
                stats['transfer_window_queries']+=1
                if queue:
                    v=queue[0][1]-U[j] if backward else queue[0][1]+U[j]
                    if dst[j] is None or v>dst[j]:dst[j]=v
    return current


def sweep(blocks,left,right,lo,hi,boundary,backward,bits,stats):
    width=hi-lo+1;previous=[[None]*width for _ in (0,1)]
    stats['max_sweep_width']=max(stats['max_sweep_width'],width)
    r,t=boundary;previous[t][r-lo]=0
    order=range(right-1,left-1,-1) if backward else range(left,right)
    for b in order:
        start,end,a,c=blocks[b]
        U=[(2*a+c)*r-a*bits[r] for r in range(lo,hi+1)]
        stats['potential_terms']+=width
        previous=transfer(previous,end-start,U,backward,stats)
    return previous


def optimize_shape(p,q,blocks=None):
    check_weights(p,q);n=len(p);stats=Counter(input_keys=n)
    if blocks is None:blocks=signature_runs(p,q,stats)
    stats['shape_blocks']=len(blocks)
    if not n:return 0,None,stats
    h,S,s=parameters(n);m=S-1;bits=[0]*(m+1)
    for r in range(1,m+1):bits[r]=bits[r//2]+(r&1)
    stats['popcount_terms']=m+1
    base=(h+1)*sum(p)+h*sum(q)+sum(q[i]+q[i+1] for i in range(n))
    stats['base_key_terms']=n;stats['base_gap_terms']=n+1;stats['base_pair_terms']=n
    word=[]
    if not s:
        word=[1]*n;stats['fixed_shape']=1
        best=sum((1+(r&-r).bit_length()-1)*p[r-1]+q[r-1]+q[r] for r in range(1,n+1))
    elif len(blocks)==1:
        _,_,a,c=blocks[0]
        u=next(u for u in (0,1) if limits(n,1,u)[0]<=m<=limits(n,1,u)[1])
        word=block_word(n,m,1,u);best=(2*a+c)*m-a*bits[m]
        stats['single_block']=1
    else:
        final=sweep(blocks,0,len(blocks),0,m,(0,1),False,bits,stats)
        best,u=max((final[u][m],u) for u in (0,1) if final[u][m] is not None)
        del final
        def recover(left,right,r0,t0,r1,t1):
            stats['traceback_nodes']+=1
            if right-left==1:
                start,end,a,c=blocks[left]
                word.extend(block_word(end-start,r1-r0,t0,t1))
                stats['traceback_leaf_keys']+=end-start
                return (2*a+c)*(r1-r0)-a*(bits[r1]-bits[r0])
            mid=(left+right)//2
            forward=sweep(blocks,left,mid,r0,r1,(r0,t0),False,bits,stats)
            reverse=sweep(blocks,mid,right,r0,r1,(r1,t1),True,bits,stats)
            selected=None
            for j in range(r1-r0+1):
                for t in (0,1):
                    stats['traceback_split_checks']+=1
                    a,b=forward[t][j],reverse[t][j]
                    if a is not None and b is not None:
                        if selected is None or a+b>selected[0]:selected=(a+b,r0+j,t)
            assert selected is not None
            value,r,t=selected
            # Release both profiles before recursing: no profile stack.
            del forward,reverse
            lv=recover(left,mid,r0,t0,r,t);rv=recover(mid,right,r,t,r1,t1)
            assert lv+rv==value
            return value
        assert recover(0,len(blocks),0,1,m,u)==best
    assert len(word)==n and sum(word)==m
    lengths=[];r=0;last=1
    for x in word:
        assert x or last
        if x:r+=1;lengths.append(h-((r&-r).bit_length()-1))
        else:lengths.append(h+1)
        last=x
    tree=from_lengths(lengths);value=base-best
    assert cost(tree,p,q)==value
    stats['constructed_keys']=n;stats['direct_cost_keys']=n;stats['direct_cost_gaps']=n+1
    return value,tree,stats


def sorted_weights(p,q,blocks,stats):
    """Only O(k) weighted records: each constant adjacent-gap sum alternates."""
    ps=[];qs=[]
    for start,end,a,c in blocks:
        L=end-start;ps.append((a,L));qs.append((q[start],(L+1)//2))
        if L>1:qs.append((q[start+1],L//2))
    qs.append((q[-1],1))
    result=[]
    for records in (ps,qs):
        counts=Counter()
        ordered=sorted((Counted(z,counts) for z in records),reverse=True)
        stats['sort_record_comparisons']+=counts['bound_weight_comparisons']
        stats['sort_records']+=len(records)
        values=[]
        for z in ordered:
            v,L=z.value;values.extend([v]*L)
        stats['sorted_items']+=len(values);result.append(values)
    return result


def attempt(p,q,*,preflight=True):
    check_weights(p,q);n=len(p);stats=Counter(input_keys=n)
    if not n:return 0,None,Counter(input_keys=0,certified=1)
    blocks=signature_runs(p,q,stats);ps,qs=sorted_weights(p,q,blocks,stats)
    a,b=ps[-1],qs[-1];H=residual_huffman(ps,qs,a,b,stats)
    lower=(a+b)*(minimum_ipl(n)+1)+(a+2*b)*n+H
    h,S,s=parameters(n)
    class_lower=sum(v*(i+1).bit_length() for i,v in enumerate(ps))
    class_lower+=h*sum(qs)+(sum(qs[-2*s:]) if s else 0)
    stats['nonminimal_lower_bound']=lower;stats['residual_lower_bound']=H
    stats['class_profile_terms']=2*n+1;stats['class_profile_lower_bound']=class_lower
    if preflight and class_lower>lower:
        stats['preflight_rejected']=stats['global_gate_rejected']=1
        return None,None,stats
    value,tree,sc=optimize_shape(p,q,blocks)
    del sc['input_keys'];stats.update(sc);stats['candidate_cost']=value
    if value<=lower:stats['certified']=1;return value,tree,stats
    stats['global_gate_rejected']=1
    return None,None,stats


def solve(p,q,*,preflight=True):
    value,tree,stats=attempt(p,q,preflight=preflight)
    if value is None:
        value,tree,scans=knuth(p,q);n=len(p)
        stats['fallback_dense_states']=n*(n+1)//2
        stats['fallback_root_candidates']=scans;stats['fallback_constructed_keys']=n
    return value,tree,stats


def portfolio_solve(p,q):
    """Cheap structural routing; keep the standalone linear-space kernel."""
    check_weights(p,q);n=len(p);routing=Counter()
    blocks=signature_runs(p,q,routing);k=len(blocks)
    # This measured policy is not a correctness premise. Above the cap,
    # quadratic fallback is still O(n*k), since k>n/32.
    cap=max(16,n//32)
    if k>cap:
        from ramp_complete import solve as affine_solve
        value,tree,stats,_=affine_solve(p,q)
        route='route_to_affine'
    else:
        value,tree,stats=solve(p,q)
        route='route_to_runs'
    stats['routing_signature_items']=routing['signature_items']
    stats['routing_runs']=k;stats['routing_cap']=cap;stats[route]=1
    return value,tree,stats


def make_fixture(n,k,rng,baseline=True):
    if not n:return [],[0]
    k=min(n,max(1,k));p=[];q=[rng.randrange(n*n+1)]
    for j in range(k):
        start=j*n//k;end=(j+1)*n//k;L=end-start
        a=rng.randrange(n*n+1);x=q[-1];y=rng.randrange(n*n+1)
        p.extend([a]*L)
        q.extend(y if i%2 else x for i in range(1,L+1))
    M=max(p+q+[1]);B=4*(n+1)**2*M if baseline else 0
    return [B+v for v in p],[B+v for v in q]
