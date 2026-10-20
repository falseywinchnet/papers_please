"""Finite Monge chains for coupled block rewards; no full OBST solver claim."""
from collections import Counter, deque
from core_monge import Monge, multiply
from band_dominance import band_matrix, prefix_matrix
from plateau_core import ruler_block_rewards


def balanced_product(matrices, stats):
    assert matrices
    def build(lo, hi):
        if hi-lo == 1:
            return matrices[lo]
        mid=(lo+hi)//2
        left=build(lo,mid);right=build(mid,hi)
        out,witness=multiply(left,right)
        del witness
        stats['chain_products']+=1
        stats['chain_product_input_cores']+=left.k+right.k
        stats['chain_product_output_cores']+=out.k
        return out
    return build(0,len(matrices))


def chain_dominance(functions,gaps,stats=None):
    """T(A,B)=-max sum f_t(u_t), u_0<=A,u_last>=B,
    0<=u_(t+1)-u_t<=gaps[t]. Equality is on B<=A+sum(gaps).
    Every completion entry is finite and explicitly determined.
    """
    if stats is None:stats=Counter()
    r=len(functions);assert r>=2 and len(gaps)==r-1
    n=len(functions[0]);assert n and all(len(f)==n for f in functions)
    assert all(g>=0 for g in gaps)
    K=1+sum(max(f)-min(f) for f in functions)
    factors=[prefix_matrix(n,K,stats)]
    for t,g in enumerate(gaps):
        # Each unary is charged once, including the final unary.
        F=functions[t];G=functions[t+1] if t==r-2 else [0]*n
        Q,_=band_matrix(F,G,g,stats,K)
        factors.append(Q)
    factors.append(prefix_matrix(n,K,stats))
    out=balanced_product(factors,stats)
    depth=(len(factors)-1).bit_length()
    assert out.k <= (1<<depth)*2*r*(n-1)
    return out


def literal_chain(functions,gaps,stats=None):
    """Independent exact DP, using only feasible states, for all A,B.
    None denotes infeasibility. No sparse-product code is used.
    """
    if stats is None:stats=Counter()
    n=len(functions[0]);out=[]
    for A in range(n):
        cur=[functions[0][u] if u<=A else None for u in range(n)]
        for f,g in zip(functions[1:],gaps):
            nxt=[None]*n;queue=deque()
            for v in range(n):
                while queue and queue[0]<v-g:queue.popleft();stats['oracle_queue_pops']+=1
                if cur[v] is not None:
                    while queue and cur[queue[-1]]<=cur[v]:queue.pop();stats['oracle_queue_pops']+=1
                    queue.append(v);stats['oracle_queue_pushes']+=1
                if queue:nxt[v]=cur[queue[0]]+f[v]
                stats['oracle_states']+=1
            cur=nxt
        best=None;row=[None]*n
        for B in range(n-1,-1,-1):
            if cur[B] is not None:best=cur[B] if best is None else max(best,cur[B])
            row[B]=best;stats['oracle_suffix_states']+=1
        out.append(row)
    return out


def block_functions(h,lengths,stats=None):
    if stats is None:stats=Counter()
    c=2**h-1;P=sum(lengths);assert P<=c and all(m>0 for m in lengths)
    N=c-P+1;functions=[];offset=0
    for m in lengths:
        functions.append(ruler_block_rewards(c,m,stats)[offset:offset+N]);offset+=m
    return functions


def complete_block_core(n,h,z,lengths,gaps,stats=None):
    """Ordinary above-capacity cells whose four intervals retain all blocks.
    Blocks have common unit key weight; arbitrary gap weights cancel.
    """
    if stats is None:stats=Counter()
    assert len(lengths)>=2 and len(gaps)==len(lengths)-1
    P=sum(lengths);G=sum(gaps);c=2**h-1
    assert all(m>0 for m in lengths) and all(g>=0 for g in gaps)
    assert 0<=z and z+P+G<=n
    if P>c or c>=n:return {}
    T=chain_dominance(block_functions(h,lengths,stats),gaps,stats);out={}
    for a,b,d in T.entries:
        i=z-a-1;j=c+z+G-b-1
        if 0<=i<z and z+P+G<=j<n and j-i>c:out[i,j]=d
        stats['chain_coordinate_filters']+=1
    return out
