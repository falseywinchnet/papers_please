#!/usr/bin/env python3
"""Independent controls and exact dense-core family for rank transfers."""
from collections import Counter
from itertools import product,combinations
from pathlib import Path
from fractions import Fraction
import hashlib,json,random
from rank_transfer import transfer,transfer_run_list,literal_transfer,runs
from block_chain import chain_dominance,literal_chain,complete_block_core
from aggregate_core_audit import layers


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(441904)
    # All finite products are tested, not only their feasible submatrices.
    for n in range(1,6):
        fixtures=list(product((0,1,3),repeat=n))
        for weights in fixtures:
            c=7;T,K=transfer(weights,c,stats);blocks=runs(weights)
            F=[sum((r&-r).bit_length()-1 for r in range(1,t+1)) for t in range(c+1)]
            oracle=literal_transfer(weights,c,stats)
            dense=[[0 if u==v else None for v in range(c+1)] for u in range(c+1)]
            for w,m in blocks:
                factor=[[K*(max(u-v,0)+max(v-u-m,0))+w*(F[u]-F[v]) for v in range(c+1)] for u in range(c+1)]
                nxt=[[min(dense[u][x]+factor[x][v] for x in range(c+1) if dense[u][x] is not None) for v in range(c+1)] for u in range(c+1)]
                stats['dense_finite_product_candidates']+=sum(x is not None for row in dense for x in row)*(c+1)
                dense=nxt
            for u in range(c+1):
                for v in range(c+1):
                    assert T.value_reference(u,v)==dense[u][v]
                    stats['finite_transfer_entry_controls']+=1
                    if oracle[u][v] is not None:
                        assert oracle[u][v]==dense[u][v]
                        stats['feasible_transfer_entry_controls']+=1
                        t=v-u
                        best=max(sum(weights[x]*(((u+k)&-(u+k)).bit_length()-1) for k,x in enumerate(ts,1)) for ts in combinations(range(n),t))
                        assert best==-oracle[u][v]
                        from math import comb
                        stats['literal_transfer_subsequences']+=comb(n,t)
                        stats['literal_transfer_entry_controls']+=1
            stats['exhaustive_transfer_inputs']+=1
        print('exhaustive',n,flush=True)
    for n in (3,5,8,12):
        for _ in range(8):
            p=[Fraction(rng.randrange(8),rng.randrange(1,6)) for i in range(n)]
            T,K=transfer(p,7,stats);oracle=literal_transfer(p,7,stats)
            for u in range(8):
                for v in range(u,min(7,u+n)+1):
                    assert T.value_reference(u,v)==oracle[u][v]
                    stats['rational_transfer_entry_controls']+=1
            stats['rational_transfer_inputs']+=1
    # Original all-root mixed layers, for arbitrary keys and nonzero gaps.
    for n in (4,7,8,12,16,24,32):
        for trial in range(10):
            if trial==0:p=list(range(n))
            elif trial==1:p=[1<<min(i,n-1-i) for i in range(n)]
            elif trial==2:p=[7+(i%3==0) for i in range(n)]
            elif trial==3:p=[rng.randrange(5)]*n
            else:p=[rng.randrange(8) for i in range(n)]
            q=[rng.randrange(5) for _ in range(n+1)];H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
            for h,A in enumerate(layers(p,q,H,M,stats)):
                c=2**h-1
                if not h or c>n:continue
                intervals={(0,n)}
                for _ in range(5):
                    i=rng.randrange(n-c+1);j=rng.randrange(i+c,n+1);intervals.add((i,j))
                for i,j in sorted(intervals):
                    T,K=transfer(p[i:j],c,stats)
                    S=-T.value_reference(0,c)
                    assert A[i][j]==M*(j-i-c)+h*(sum(p[i:j])+sum(q[i:j+1]))-S
                    stats['original_layer_score_controls']+=1
            stats['mixed_transfer_inputs']+=1
        print('mixed',n,flush=True)
    # Genuine finite chains of arbitrary signed functions, including a dense square.
    for N in (2,3,5,8,12):
        for r in (2,3,4,6):
            for _ in range(5):
                fs=[[rng.randrange(-9,10) for u in range(N)] for t in range(r)]
                gs=[rng.randrange(max(1,N//r+1)) for t in range(r-1)]
                T=chain_dominance(fs,gs,stats);oracle=literal_chain(fs,gs,stats)
                for a in range(N):
                    for b in range(N):
                        if oracle[a][b] is not None:
                            assert T.value_reference(a,b)==-oracle[a][b]
                            stats['generic_chain_score_controls']+=1
                stats['generic_chain_inputs']+=1
    chain_rows=[]
    for s in (1,2,4,8,16):
        r=2*s+1;N=2*s+1
        fs=[list(range(N)) for _ in range(r-1)]+[[-(r-1)*u for u in range(N)]]
        gs=[1]*(r-1);oracle=literal_chain(fs,gs,stats)
        T=chain_dominance(fs,gs,stats)
        for A in range(N):
            for B in range(N):
                d=max(B-A,0)
                assert oracle[A][B]==-d*(d+1)//2
                assert T.value_reference(A,B)==d*(d+1)//2
                stats['dense_chain_formula_entries']+=1
        core={(a,b):d for a,b,d in T.entries}
        for a in range(s):
            for b in range(s,2*s):
                assert core[a,b]==1;stats['dense_chain_square_cells']+=1
        chain_rows.append(dict(s=s,factors=r,N=N,square_core=s*s,verification='literal feasible-state DP and condensed product'))
        print('dense chain',s,flush=True)
    # Exact weighted-ramp transfer family. Product controls grow beyond literal subsets.
    ramp_rows=[]
    for h in range(3,9):
        c=2**h-1;r=2**(h-1);p=list(range(1,r+1));s=r//2;local=Counter()
        T,K=transfer(p,c,local);F=[sum((j&-j).bit_length()-1 for j in range(1,t+1)) for t in range(c+1)]
        G=[sum(j*((j&-j).bit_length()-1) for j in range(1,t+1)) for t in range(c+1)]
        oracle=literal_transfer(p,c,local) if h<=6 else None
        for u in range(c+1):
            for v in range(u,min(c,u+r)+1):
                expected=-((r-v)*(F[v]-F[u])+G[v]-G[u])
                assert T.value_reference(u,v)==expected
                if oracle is not None:assert oracle[u][v]==expected;local['independent_ramp_dp_entries']+=1
                local['ramp_formula_entry_controls']+=1
        core={(a,b):d for a,b,d in T.entries}
        strict=0
        for u in range(c):
            for v in range(u+1,min(c,u+r)):
                expected=((u+1)&-(u+1)).bit_length()-1
                assert core.get((u,v),0)==expected
                strict+=expected>0;local['ramp_density_controls']+=1
        expected_core=sum(min(r-1,c-1-u) for u in range(1,c-1,2))
        assert strict==expected_core
        assert T.k==strict+c+max(0,c-r)
        square=sum(core.get((u,v),0)>0 for u in range(s) for v in range(s,2*s))
        assert square==s*(s//2)
        ramp_rows.append(dict(h=h,c=c,keys=r,W=r*(r+1)//2,s=s,square_core=square,strict_transfer_core=strict,completed_transfer_core=T.k,counts=dict(local),verification='condensed product and closed-form density; independent subsequence DP also used' if oracle is not None else 'condensed product and closed-form density; no independent large DP'))
        print('ramp',h,strict,square,flush=True)
    # Many equal blocks are checked against original mixed layers as a separate use.
    for n in (12,16,24,32):
        for _ in range(8):
            r=rng.randrange(3,min(7,n//2));lengths=[1]*r;gaps=[rng.randrange(2) for _ in range(r-1)]
            budget=max(0,n-r-sum(gaps)-2*max(1,n//5))
            for t in range(r):
                extra=min(budget,rng.randrange(3));lengths[t]+=extra;budget-=extra
            z=rng.randrange(n-sum(lengths)-sum(gaps)+1);p=[0]*n;start=z
            for t,m in enumerate(lengths):
                p[start:start+m]=[1]*m;start+=m+(gaps[t] if t<r-1 else 0)
            end=start;q=[rng.randrange(4) for _ in range(n+1)];H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
            for h,A in enumerate(layers(p,q,H,M,stats)):
                c=2**h-1
                if not h or c>=n:continue
                got=complete_block_core(n,h,z,lengths,gaps,stats)
                want={}
                for i in range(z):
                    for j in range(max(i+c+1,end),n):
                        d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                        if d:want[i,j]=d
                        stats['many_block_density_controls']+=1
                assert got==want;stats['many_block_support_sets']+=1
            stats['many_block_inputs']+=1
    files=('rank_transfer.py','rank_transfer_audit.py','block_chain.py','band_dominance.py','core_monge.py','plateau_core.py','aggregate_core_audit.py')
    result=dict(scope='Finite arbitrary-key rank transfers, many-block interior representation, and explicit dense transfer squares. These are not original-interval-core counterexamples or a full OBST solver.',checks=dict(stats),chain_rows=chain_rows,ramp_rows=ramp_rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/rank_transfer_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(stats),flush=True)
if __name__=='__main__':main()
