#!/usr/bin/env python3
"""Exact full OBST from a Fibonacci subtree-mass frontier.

The Fibonacci approach follows Hirschberg--Larmore--Molodowitch; the
short-interval/top-skeleton construction is Larmore/Karpinski--Larmore--Rytter.
We use the separately proved mixed-weight bound W/F_(d+1), not 2W/F_(d+3):
the latter fails already for p=[1,1], q=[1,100,1] at depth one in this model.
We compare their uniform width envelope with a variable interval contour.
All arithmetic is exact, all key and gap weights retain their order.
"""
from collections import Counter
import json
from pathlib import Path
import random
import sys

from complete import from_lengths
from research import check_weights, cost, cubic, knuth, label, shapes
from sparse import FAMILIES, weights
from split_height import smawk


def mass_function(p,q):
    prefix=[0]
    for a,b in zip(p,q[1:]): prefix.append(prefix[-1]+a+b)
    return lambda i,j:q[i]+prefix[j]-prefix[i]


def contour(n,mass,numerator,denominator,stats):
    """Maximal nonempty intervals with denominator*mass <= numerator.

    Empty intervals are always allowed, even if their sole gap is heavy.
    Nonnegative weights imply a nondecreasing endpoint sequence.
    """
    ends=[]
    j=0
    for i in range(n+1):
        j=max(i,j)
        while j<n:
            stats['contour_mass_checks']+=1
            if denominator*mass(i,j+1)>numerator: break
            j+=1
        ends.append(j)
    assert all(i<=ends[i]<=n for i in range(n+1))
    assert all(a<=b for a,b in zip(ends,ends[1:]))
    return ends


def select_plan(p,q,mode,stats):
    n=len(p)
    mass=mass_function(p,q)
    total=sum(p)+sum(q)
    best=n*(n+1)//2
    chosen=(0,[n]*(n+1))
    # F_(d+1), starting at depth zero. At depth zero the full table
    # is feasible and its direct Knuth implementation needs no top search.
    f,g=1,1
    d=1
    while n*(1<<d)<best:
        f,g=g,f+g
        ends=contour(n,mass,total,f,stats)
        width=max(e-i for i,e in enumerate(ends))
        if mode=='uniform': ends=[min(n,i+width) for i in range(n+1)]
        states=sum(e-i for i,e in enumerate(ends))
        estimate=states+n*(1<<d)
        stats['parameter_levels']+=1
        if estimate<best:
            best=estimate
            chosen=d,ends
        d+=1
    upper,ends=chosen
    stats.update(selected_depth=upper,selected_width=max(e-i for i,e in enumerate(ends)),
                 selected_short_states=sum(e-i for i,e in enumerate(ends)),
                 selected_work_proxy=best)
    return upper,ends


def interval_tables(p,q,ends,stats):
    """Knuth recurrence restricted to a hereditary monotone contour.

    Bucket only existing cells by length. Scanning every i for every length
    would lose the O(number of cells) bound on nonuniform contours.
    """
    n=len(p)
    mass=mass_function(p,q)
    tables=[[0]+[None]*(ends[i]-i) for i in range(n+1)]
    roots=[[None]*(ends[i]-i+1) for i in range(n+1)]
    buckets=[[] for _ in range(n+1)]
    for i,e in enumerate(ends):
        for length in range(1,e-i+1):
            buckets[length].append(i)
            stats['interval_bucket_entries']+=1
    for length,starts in enumerate(buckets[1:],1):
        for i in starts:
            j=i+length
            low=i if length==1 else roots[i][length-1]
            high=j-1 if length==1 else roots[i+1][length-1]
            best=None
            for r in range(low,high+1):
                value=tables[i][r-i]+tables[r+1][j-r-1]
                stats['short_root_candidates']+=1
                if best is None or value<best:
                    best,roots[i][length]=value,r
            tables[i][length]=best+mass(i,j)
            stats['short_states']+=1
    assert stats['short_root_candidates']<=3*stats['short_states']
    return tables,roots,mass


def frontier_optimum(p,q,ends,upper,method='smawk',audit=False):
    """Exact optimum with each depth-upper subtree inside its local contour.

    Does not by itself assert unrestricted optimality. Arbitrary contours
    may have no feasible tree; returns None in that case.
    """
    n=len(p)
    assert len(ends)==n+1 and all(i<=e<=n for i,e in enumerate(ends))
    assert all(a<=b for a,b in zip(ends,ends[1:]))
    stats=Counter()
    small,roots,mass=interval_tables(p,q,ends,stats)
    blocks=1<<upper
    sentinel=(upper+n+1)*(sum(p)+sum(q))+1
    values=[{} for _ in range(blocks+1)]
    parents=[{} for _ in range(blocks+1)]
    values[0][0]=0
    left=[0]*(n+2)
    i=0
    for j in range(1,n+2):
        while ends[i]+1<j: i+=1
        left[j]=i
        stats['band_boundary_scans']+=1

    def update(b,j,value,parent):
        if j not in values[b] or value<values[b][j]:
            values[b][j]=value
            parents[b][j]=parent

    for b in range(blocks):
        rows=[i for i in range(n+1) if i in values[b]]
        stats['top_row_scans']+=n+1
        stats['top_states']+=len(values[b])
        if not rows: continue
        key_depth=0 if not b else upper-((b & -b).bit_length()-1)
        rowcost={i:values[b][i]+(p[i-1]*key_depth if i else 0) for i in rows}
        # Variable widths can leave holes in reachable rows and columns.
        # Keep exactly output columns covered by at least one feasible row.
        columns=[]
        reach=0
        for j in range(1,n+2):
            if j-1 in rowcost: reach=max(reach,ends[j-1]+1)
            if j<=reach: columns.append(j)
            stats['top_column_scans']+=1

        def entry(j,i):
            if i<left[j]:
                stats['top_padding_queries']+=1
                return sentinel+left[j]-i
            if i>=j:
                stats['top_padding_queries']+=1
                return sentinel+i-j+1
            stats['top_matrix_queries']+=1
            return rowcost[i]+small[i][j-i-1]+upper*mass(i,j-1)

        if method=='smawk': winners=smawk(columns,rows,entry)
        else:
            assert method=='brute'
            winners={j:min((i for i in rows if left[j]<=i<j),key=lambda i:entry(j,i))
                     for j in columns}
        for j,i in winners.items():
            assert left[j]<=i<j
            value=entry(j,i)
            if audit:
                brute=min((rowcost[a]+small[a][j-a-1]+upper*mass(a,j-1),a)
                          for a in rows if left[j]<=a<j)
                assert (value,i)==brute,(b,j,i,brute)
                stats['audited_top_minima']+=1
            update(b+1,j,value,(b,i,'block'))
        width=2
        while b%width==0 and b+width<=blocks:
            depth=upper-(width.bit_length()-1)
            for i in rows:
                update(b+width,i+1,rowcost[i]+q[i]*depth,(b,i,'gap'))
                stats['coarse_gap_transitions']+=1
            width*=2
    stats['top_states']+=len(values[-1])
    if n+1 not in values[-1]: return None,None,stats
    value=values[-1][n+1]
    lengths=[None]*n

    def put(i,j,depth):
        if i==j: return
        r=roots[i][j-i]
        lengths[r]=depth+1
        put(i,r,depth+1)
        put(r+1,j,depth+1)

    b,j=blocks,n+1
    while b:
        oldb,i,kind=parents[b][j]
        if oldb: lengths[i-1]=upper-((oldb & -oldb).bit_length()-1)
        if kind=='block': put(i,j-1,upper)
        b,j=oldb,i
    assert j==0 and all(x is not None for x in lengths)
    tree=from_lengths(lengths)
    assert value==cost(tree,p,q)
    stats.update(reconstructed_keys=n,actual_height=max(lengths,default=0))
    return value,tree,stats


def solve(p,q,mode='adaptive',audit=False):
    check_weights(p,q)
    assert mode in ('adaptive','uniform')
    n=len(p)
    if not n: return 0,None,dict(selected_depth=0,short_states=0)
    stats=Counter()
    upper,ends=select_plan(p,q,mode,stats)
    if not upper:
        value,tree,scans=knuth(p,q)
        stats.update(short_states=n*(n+1)//2,short_root_candidates=scans,
                     direct_knuth=1,reconstructed_keys=n)
    else:
        value,tree,counts=frontier_optimum(p,q,ends,upper,audit=audit)
        assert value is not None,(p,q,mode,upper,ends)
        stats.update(counts)
    return value,tree,dict(stats)


def admissible(t,ends,upper,i=0,j=None,depth=0):
    if j is None: j=len(ends)-1
    if t is None: return True
    if depth==upper: return j<=ends[i]
    r,a,b=t
    return (admissible(a,ends,upper,i,r,depth+1)
            and admissible(b,ends,upper,r+1,j,depth+1))


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0xF1B0C017)
    shape_checks=table_checks=full_checks=audited=mass_checks=0
    # Preserve the failure of the initially imported mass normalization.
    cp,cq=[1,1],[1,100,1]
    bad_value,bad_tree=cubic(cp,cq)
    assert bad_value==206 and sum(cp)+sum(cq)==104
    child=bad_tree[1] or bad_tree[2]
    assert child is not None
    bad_mass=cp[child[0]]+cq[child[0]]+cq[child[0]+1]
    assert bad_mass==102 and 3*bad_mass>2*(sum(cp)+sum(cq))
    # Arbitrary nondecreasing contours, including holes in diagonal lengths,
    # prove more about the engine than tests of Fibonacci contours alone.
    for n in range(1,9):
        ts=[label(s)[0] for s in shapes(n)]
        for trial in range(30):
            p=[rng.randrange(10) for _ in range(n)]
            q=[rng.randrange(10) for _ in range(n+1)]
            ends=[n]*(n+1)
            for i in range(n-1,-1,-1): ends[i]=rng.randrange(i,ends[i+1]+1)
            tables,_,_=interval_tables(p,q,ends,Counter())
            for i,e in enumerate(ends):
                for j in range(i+1,e+1):
                    assert tables[i][j-i]==cubic(p[i:j],q[i:j+1])[0]
                    table_checks+=1
            for upper in range(4):
                expected=min((cost(t,p,q) for t in ts if admissible(t,ends,upper)),default=None)
                value,tree,c=frontier_optimum(p,q,ends,upper,audit=True)
                assert value==expected,(p,q,ends,upper,value,expected)
                if value is not None: assert cost(tree,p,q)==value
                audited+=c['audited_top_minima']
                shape_checks+=1
    for n in range(1,41):
        for trial in range(30):
            if trial<13: p,q=weights(n,FAMILIES[trial],rng)
            else:
                p=[rng.randrange(30) for _ in range(n)]
                q=[rng.randrange(30) for _ in range(n+1)]
            expected=cubic(p,q)[0]
            # Check the mass guarantee directly on an independently
            # optimized tree, at every internal depth, including ties/zeros.
            _,oracle_tree=cubic(p,q)
            mass=mass_function(p,q)
            total=sum(p)+sum(q)
            def check_subtrees(t,i,j,f=1,g=1):
                nonlocal mass_checks
                if t is None: return
                assert f*mass(i,j)<=total,(p,q,t,i,j,f)
                mass_checks+=1
                r,a,b=t
                check_subtrees(a,i,r,g,f+g)
                check_subtrees(b,r+1,j,g,f+g)
            check_subtrees(oracle_tree,0,n)
            for mode in ('adaptive','uniform'):
                value,tree,c=solve(p,q,mode,audit=True)
                assert value==expected==cost(tree,p,q),(n,trial,mode)
                audited+=c.get('audited_top_minima',0)
                full_checks+=1
    print('Verified',shape_checks,'shape classes,',table_checks,'interval cells,',
          full_checks,'full solves,',audited,'top minima,',mass_checks,'subtree bounds',flush=True)
    rows=[]
    for n in (128,256,512,768,1024,1536,2048):
        for family in ('near_uniform','random','geometric','log_uniform','spike','gap_spike','keys_only','gaps_only'):
            p,q=weights(n,family,rng)
            expected,_,scans=knuth(p,q)
            runs={}
            for mode in ('adaptive','uniform'):
                value,tree,c=solve(p,q,mode)
                assert value==expected==cost(tree,p,q)
                runs[mode]=c
            rows.append(dict(n=n,family=family,optimum=expected,counts=runs,
                             knuth_states=n*(n+1)//2,knuth_root_candidates=scans))
            print(n,family,[(m,runs[m]['selected_depth'],runs[m]['short_states']) for m in runs],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'mass_frontier.json'
    out.write_text(json.dumps(dict(shape_checks=shape_checks,table_checks=table_checks,
                                   full_checks=full_checks,audited_top_minima=audited,
                                   mass_checks=mass_checks,
                                   rejected_bound_counterexample=dict(p=cp,q=cq,optimum=bad_value,
                                      total_mass=104,depth_one_internal_mass=102),rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
