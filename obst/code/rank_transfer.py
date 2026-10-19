"""Finite Monge transfers for arbitrary nonnegative key weights.

A transfer entry (u,v) chooses v-u keys and assigns them ruler ranks u+1..v.
This is a representation of above-capacity scores, not a full BST solver.
"""
from collections import Counter
from core_monge import Monge
from block_chain import balanced_product


def prefix_rewards(c,stats):
    ruler=[0]*(c+1);F=[0]*(c+1)
    for k in range(1,c+1):
        ruler[k]=0 if k%2 else ruler[k//2]+1
        F[k]=F[k-1]+ruler[k]
        stats['transfer_ruler_entries']+=1
    return F


def runs(weights):
    out=[]
    for w in weights:
        assert w>=0
        if out and out[-1][0]==w:out[-1]=(w,out[-1][1]+1)
        else:out.append((w,1))
    return out


def run_factor(F,weight,length,K,stats):
    c=len(F)-1
    assert length>=1 and weight>=0 and K>0
    top=[K*max(v-length,0)-weight*F[v] for v in range(c+1)]
    left=[K*u+weight*F[u] for u in range(c+1)]
    core=[(u,u,K) for u in range(c)]
    core.extend((u,u+length,K) for u in range(c-length))
    stats['transfer_input_boundary_entries']+=2*(c+1)
    stats['transfer_input_core_terms']+=len(core)
    return Monge(top,left,core,stats)


def transfer_run_list(blocks,c,stats=None):
    if stats is None:stats=Counter()
    assert c>=1 and blocks and all(w>=0 and m>=1 for w,m in blocks)
    F=prefix_rewards(c,stats)
    K=1+F[c]*sum(w for w,m in blocks)
    factors=[run_factor(F,w,m,K,stats) for w,m in blocks]
    out=balanced_product(factors,stats)
    r=len(blocks)
    assert out.k<=(1<<((r-1).bit_length()))*2*r*c
    return out,K


def transfer(weights,c,stats=None):
    assert weights
    return transfer_run_list(runs(weights),c,stats)


def literal_transfer(weights,c,stats=None):
    """Independent subsequence DP for every feasible pair of ranks.
    Invalid entries remain None; no completion/product machinery is used.
    """
    if stats is None:stats=Counter()
    out=[[None]*(c+1) for _ in range(c+1)]
    for u in range(c+1):
        best=[None]*(c-u+1);best[0]=0
        for w in weights:
            for t in range(c-u,0,-1):
                if best[t-1] is not None:
                    rank=u+t;reward=w*((rank&-rank).bit_length()-1)
                    value=best[t-1]+reward
                    if best[t] is None or value>best[t]:best[t]=value
                stats['transfer_dp_candidates']+=1
        for t,value in enumerate(best):
            if value is not None:out[u][u+t]=-value
    return out
