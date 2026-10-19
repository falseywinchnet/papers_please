#!/usr/bin/env python3
"""Harness for complete mixed run-vector construction; no timing evidence."""
from collections import Counter
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
import hashlib,json,random
from slot_vector import solve,normalize,operations
from aggregate_core_audit import layers
from slot_run_audit import verify_tree
from research import shapes,label,cost
from slot_run import slot_transfer


def literal_prefix(w,g,v,end,last,stats):
    best=None
    for ss in combinations(range(1,last),end-1):
        ss=ss+(last,)
        reward=sum(w[i]*v[t] for i,t in enumerate(ss))+sum(g[i]*min(v[ss[i-1]],v[ss[i]]) for i in range(1,end))
        val=-reward
        if best is None or val<best:best=val
        stats['vector_literal_prefix_selections']+=1
    return best


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(541019)
    def observer(k,m,old,new,back,w,g,v,K):
        c=len(v)-1;end=k+m
        for b in range(end,c+1):
            ref=literal_prefix(w,g,v,end,b,stats)
            assert new[b]==ref;stats['vector_prefix_entry_controls']+=1
            a=back[b];assert old[a] is not None and b-a>=m
            # Independent literal run selection or one-key gap transition.
            if m==1:chosen=old[a]-w[k]*v[b]-g[k]*min(v[a],v[b])
            else:
                chosen=old[a]-w[k]*(v[b]+max(sum(v[t] for t in ss) for ss in combinations(range(a+1,b),m-1)))
            assert chosen==new[b];stats['vector_predecessor_controls']+=1
    # Every mixed binary input through four keys, two feasible heights where affordable.
    for n in range(1,5):
        for ww in product((0,1),repeat=2*n+1):
            p=list(ww[:n]);q=list(ww[n:]);H=n.bit_length()+1
            original=list(layers(p,q,H,(H+1)*sum(ww)+1,stats))
            w,g,constant=normalize(p,q)
            for shape in shapes(n):
                tree=label(shape)[0]
                assert cost(tree,p,q)==cost(tree,w,g)+constant;stats['vector_shape_gauge_controls']+=1
            for h in range(1,H+1):
                result=solve(p,q,h,stats,observer if h<=3 else None)
                if n>2**h-1:assert result is None;stats['vector_capacity_controls']+=1;continue
                assert result['cost']==original[h][0][n]
                assert verify_tree(result['tree'],p,q,h,stats)==result['cost'];stats['vector_original_tree_controls']+=1
            stats['vector_binary_inputs']+=1
    print('binary',dict(stats),flush=True)
    # Entire forced-end finite factors, independently compared to the prior
    # condensed window factor and checked for nonnegative four-corner densities.
    for h in range(2,6):
        c=2**h-1
        for m in (2,3,c,c+2):
            for w in (0,1,Fraction(5,3)):
                node,K,v=slot_transfer([w]*(m-1),h,stats)
                B=[[K*max(m-b+a,0)-w*(v[b]+sum(min(m-1,(b-1)//2**t-a//2**t) for t in range(1,h))) for b in range(1,c+1)] for a in range(c+1)]
                for a in range(c+1):
                    for b in range(1,c+1):
                        assert B[a][b-1]==node.T.value_reference(a,b-1)-w*v[b]
                        stats['vector_finite_factor_controls']+=1
                for a in range(c):
                    for j in range(c-1):
                        assert B[a][j+1]+B[a+1][j]-B[a][j]-B[a+1][j+1]>=0
                        stats['vector_factor_monge_cells']+=1
    # Deliberately mixed, rational, geometric and run-rich inputs, all-root references.
    for n in (5,7,8,12,16,24,32):
        for trial in range(12):
            if trial==0:p=[2**i for i in range(n)];q=[2**(n-i) for i in range(n+1)]
            elif trial==1:p=[2]*n;q=[1+(i%3==0) for i in range(n+1)]
            elif trial==2:p=[1+(i//3)%2 for i in range(n)];q=[3]*(n+1);q[n//2]=9
            elif trial==3:p=[0]*n;q=[rng.randrange(5) for _ in range(n+1)]
            elif trial in (4,5):
                levels=[Fraction(rng.randrange(8),2) for _ in range(3)]
                p=[levels[min(2,3*i//n)] for i in range(n)];base=Fraction(rng.randrange(4),3);q=[base]*(n+1)
                for i in (n//4,3*n//4):q[i]+=Fraction(rng.randrange(1,6),2)
                q[0]=Fraction(1,3);q[-1]=Fraction(7,2)
            else:p=[Fraction(rng.randrange(8),2) for _ in range(n)];q=[Fraction(rng.randrange(8),3) for _ in range(n+1)]
            H=n.bit_length()+1;original=list(layers(p,q,H,(H+1)*(sum(p)+sum(q))+1,stats))
            for h in range(n.bit_length(),H+1):
                result=solve(p,q,h,stats)
                assert result['cost']==original[h][0][n]
                assert verify_tree(result['tree'],p,q,h,stats)==result['cost'];stats['vector_original_tree_controls']+=1
            stats['vector_mixed_inputs']+=1
    print('mixed',dict(stats),flush=True)
    # Large full constructions with independently checked output, no large all-root oracle.
    large=[]
    for h in (8,10,12,14):
        c=2**h-1;n=c//2+1
        for kind in ('uniform','three_runs','three_runs_gap_exceptions'):
            p=[4]*n if kind=='uniform' else [1 if i<n//3 else 7 if i<2*n//3 else 2 for i in range(n)]
            q=[3]*(n+1)
            if kind.endswith('exceptions'):
                for i in (n//5,n//2,4*n//5):q[i]+=5
                q[0]=1;q[-1]=8
            counts=Counter();result=solve(p,q,h,counts)
            assert verify_tree(result['tree'],p,q,h,counts)==result['cost']
            if kind=='uniform':assert result['cost']==7*sum(i.bit_length() for i in range(1,n+1))+3*n
            large.append(dict(n=n,h=h,kind=kind,**{k:result[k] for k in ('cost','runs','gap_exceptions','stages')},counts=counts,verification='Full constructor and independent output-tree order/height/cost; uniform rows also have closed minimum-IPL optimum'))
            print('large',h,kind,result['stages'],counts['vector_run_entry_queries'],flush=True)
    files=['slot_vector.py','slot_vector_audit.py','concave_lws.py','mixed_slots.py','aggregate_core_audit.py','slot_run_audit.py','research.py','slot_run.py','core_monge.py','rank_transfer.py','block_chain.py']
    out=dict(scope='Complete prescribed-height construction with arbitrary mixed nonnegative weights; complexity adapts to transformed key runs and internal-gap exceptions. No unrestricted-height certificate.',seed=541019,counts=stats,large=large,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_vector_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
