#!/usr/bin/env python3
"""Full mixed-weight height optimizer using a split dyadic skeleton.

The split-height/Monge approach is prior Karpinski--Larmore--Rytter work.
This implementation uses explicit aligned tilings and SMAWK matrix minima,
with a separate certificate against taller trees. A divide-and-conquer
matrix search is retained as an independent implementation control.
"""
from bisect import bisect_left, bisect_right
from collections import Counter
import json
from pathlib import Path
import random
import sys

from complete import from_lengths, minimum_ipl, residual_huffman
from research import cost, cubic, knuth, label, shapes, unordered_huffman
from sparse import Counted, FAMILIES, weights


def short_tables(p,q,height,stats):
    n=len(p)
    prefix=[0]
    for a,b in zip(p,q[1:]): prefix.append(prefix[-1]+a+b)
    def mass(i,j): return q[i]+prefix[j]-prefix[i]
    costs=[[[0] for _ in range(n+1)]]
    roots=[None]
    for h in range(1,height+1):
        cap=min(n,(1<<h)-1)
        oldcap=(1<<(h-1))-1
        previous=costs[-1]
        current=[[0]+[None]*min(cap,n-i) for i in range(n+1)]
        root=[[None]*(min(cap,n-i)+1) for i in range(n+1)]
        for length in range(1,cap+1):
            for i in range(n-length+1):
                j=i+length
                low=max(i,j-1-oldcap)
                high=min(j-1,i+oldcap)
                if length>1:
                    low=max(low,root[i][length-1])
                    high=min(high,root[i+1][length-1])
                assert low<=high
                best=None
                for r in range(low,high+1):
                    value=previous[i][r-i]+previous[r+1][j-r-1]
                    stats['short_root_candidates']+=1
                    if best is None or value<best:
                        best,root[i][length]=value,r
                current[i][length]=best+mass(i,j)
                stats['short_states']+=1
        costs.append(current)
        roots.append(root)
    return costs,roots,mass


def smawk(row_ids,column_ids,entry):
    """Leftmost row minima in a totally monotone matrix."""
    result={}
    def visit(rows,columns):
        if not rows: return
        reduced=[]
        for col in columns:
            while reduced and entry(rows[len(reduced)-1],col)<entry(rows[len(reduced)-1],reduced[-1]):
                reduced.pop()
            if len(reduced)<len(rows): reduced.append(col)
        visit(rows[1::2],reduced)
        indices={c:i for i,c in enumerate(reduced)}
        low=0
        for pos in range(0,len(rows),2):
            high=indices[result[rows[pos+1]]] if pos+1<len(rows) else len(reduced)-1
            row=rows[pos]
            best=reduced[low]
            value=entry(row,best)
            for offset in range(low+1,high+1):
                col=reduced[offset]
                other=entry(row,col)
                if other<value: best,value=col,other
            result[row]=best
            low=high
    visit(row_ids,column_ids)
    return result


def height_optimum(p,q,height,method='smawk'):
    n=len(p)
    assert n>=1 and (1<<height)>=n+1
    # One more lower level trades cheaper short-table work for fewer
    # matrix searches. The split stays within a constant of H/2.
    lower=min(height,height//2+1)
    upper=height-lower
    blocks=1<<upper
    capacity=1<<lower
    stats=Counter()
    sentinel=(height+1)*(sum(p)+sum(q))+1
    tables,roots,mass=short_tables(p,q,lower,stats)
    small=tables[-1]
    values=[{} for _ in range(blocks+1)]
    parents=[{} for _ in range(blocks+1)]
    values[0][0]=0

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
        row_cost={i:values[b][i]+(p[i-1]*key_depth if i else 0) for i in rows}

        # One grid block contains an arbitrary height-limited lower tree.
        # Row additions preserve the Monge property of its interval costs.
        def columns(first,last,lo,hi):
            if first>last: return
            j=(first+last)//2
            begin=max(lo,bisect_left(rows,j-capacity))
            end=min(hi,bisect_right(rows,j-1)-1)
            best=None
            choice=None
            for a in range(begin,end+1):
                i=rows[a]
                value=row_cost[i]+small[i][j-i-1]+upper*mass(i,j-1)
                stats['top_matrix_queries']+=1
                if best is None or value<best:
                    best,choice=value,a
            assert choice is not None,(b,j,rows,lo,hi)
            i=rows[choice]
            update(b+1,j,best,(b,i,'block'))
            columns(first,j-1,lo,choice)
            columns(j+1,last,choice,hi)

        first,last=rows[0]+1,min(n+1,rows[-1]+capacity)
        if method=='divide':
            columns(first,last,0,len(rows)-1)
        else:
            assert method=='smawk'
            def entry(j,i):
                # Ordered distance padding is essential: tied infinity
                # cells need not form a totally monotone rectangular matrix.
                if i<j-capacity:
                    stats['top_padding_queries']+=1
                    return sentinel+j-capacity-i
                if i>=j:
                    stats['top_padding_queries']+=1
                    return sentinel+i-j+1
                stats['top_matrix_queries']+=1
                return row_cost[i]+small[i][j-i-1]+upper*mass(i,j-1)
            winners=smawk(list(range(first,last+1)),rows,entry)
            for j,i in winners.items():
                assert i<j<=i+capacity
                update(b+1,j,entry(j,i),(b,i,'block'))

        # A shallower gap can skip several grid blocks. Width one is
        # already represented by a zero-key lower tree above.
        width=2
        while b%width==0 and b+width<=blocks:
            depth=upper-(width.bit_length()-1)
            for i in rows:
                update(b+width,i+1,row_cost[i]+q[i]*depth,(b,i,'gap'))
                stats['coarse_gap_transitions']+=1
            width*=2
    stats['top_states']+=len(values[-1])
    result=values[-1][n+1]
    lengths=[None]*n

    def put(i,j,h,depth):
        if i==j: return
        r=roots[h][i][j-i]
        lengths[r]=depth+1
        put(i,r,h-1,depth+1)
        put(r+1,j,h-1,depth+1)

    b,j=blocks,n+1
    while b:
        oldb,i,kind=parents[b][j]
        if oldb:
            lengths[i-1]=upper-((oldb & -oldb).bit_length()-1)
        if kind=='block': put(i,j-1,lower,upper)
        b,j=oldb,i
    assert j==0 and all(x is not None and 1<=x<=height for x in lengths)
    tree=from_lengths(lengths)
    assert cost(tree,p,q)==result
    stats.update(height_limit=height,lower_height=lower,upper_blocks=blocks,
                 reconstructed_keys=n,actual_height=max(lengths))
    return result,tree,stats


def tall_minimum_ipl(n,required_height):
    """Minimum IPL among n-key trees with external height >= required_height.

    Force one path, then fill the remaining available nodes breadth first.
    None means the requested height is impossible.
    """
    if required_height>n: return None
    remaining=n-required_height
    value=required_height*(required_height-1)//2
    depth=1
    expanded=0
    while remaining:
        free=(1 if depth<required_height else 2 if depth==required_height else 0)
        free+=2*expanded
        expanded=min(remaining,free)
        value+=depth*expanded
        remaining-=expanded
        depth+=1
    return value


def attempt(p,q,extra_height=1):
    n=len(p)
    if not n: return 0,None,Counter(certified=1)
    height=n.bit_length()+extra_height
    # Do not build a large abstract tree for tiny inputs.
    height=min(n,height)
    candidate,tree,stats=height_optimum(p,q,height)
    outside=tall_minimum_ipl(n,height+1)
    stats['candidate']=candidate
    if outside is None:
        stats['certified']=1
        return candidate,tree,stats
    a,b=min(p),min(q)
    comparisons=Counter()
    ps=[v.value for v in sorted((Counted(w,comparisons) for w in p),reverse=True)]
    qs=[v.value for v in sorted((Counted(w,comparisons) for w in q),reverse=True)]
    stats['bound_sort_comparisons']=comparisons['bound_weight_comparisons']
    residual=residual_huffman(ps,qs,a,b,stats)
    bound=(a+b)*outside+(a+2*b)*n+residual
    stats.update(tall_minimum_ipl=outside,tall_excess=outside-minimum_ipl(n),
                 exclusion_bound=bound,certified=int(candidate<=bound))
    return candidate if candidate<=bound else None,tree,stats


def solve(p,q,extra_height=1):
    value,tree,stats=attempt(p,q,extra_height)
    if value is None:
        value,tree,scans=knuth(p,q)
        stats.update(fallback_states=len(p)*(len(p)+1)//2,fallback_root_candidates=scans)
    return value,tree,dict(stats)


def height_cubic(p,q,height):
    """Independent all-root recurrence, including every interval."""
    n=len(p)
    old=[[0 if i==j else None for j in range(n+1)] for i in range(n+1)]
    levels=[old]
    for h in range(1,height+1):
        new=[[0 if i==j else None for j in range(n+1)] for i in range(n+1)]
        for i in range(n):
            for j in range(i+1,n+1):
                choices=[old[i][r]+old[r+1][j] for r in range(i,j)
                         if old[i][r] is not None and old[r+1][j] is not None]
                if choices:
                    new[i][j]=min(choices)+sum(p[i:j])+sum(q[i:j+1])
        levels.append(new)
        old=new
    return levels


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0x5A117)
    shape_checks=height_checks=0
    for n in range(1,9):
        ts=[label(s)[0] for s in shapes(n)]
        def height(t):
            return 0 if t is None else 1+max(height(t[1]),height(t[2]))
        hs=[height(t) for t in ts]
        ipls=[cost(t,[1]*n,[0]*(n+1))-n for t in ts]
        for h in range(1,n+2):
            actual=[x for x,y in zip(ipls,hs) if y>=h]
            assert tall_minimum_ipl(n,h)==(min(actual) if actual else None)
            height_checks+=1
        for _ in range(25):
            p=[rng.randrange(20) for _ in range(n)]
            q=[rng.randrange(20) for _ in range(n+1)]
            for h in range(n.bit_length(),min(n,n.bit_length()+2)+1):
                value,tree,_=height_optimum(p,q,h)
                assert value==min(cost(t,p,q) for t,th in zip(ts,hs) if th<=h)
                assert cost(tree,p,q)==value
                shape_checks+=1
    full_checks=certified=height_dp_checks=short_checks=0
    for n in range(1,41):
        for trial in range(50):
            base=(0,10,1000)[trial%3]
            p=[base+rng.randrange(30) for _ in range(n)]
            q=[base+rng.randrange(30) for _ in range(n+1)]
            true,_=cubic(p,q)
            value,tree,stats=solve(p,q)
            assert value==true==cost(tree,p,q)
            if trial%4==0:
                h=stats['height_limit']
                direct=height_cubic(p,q,h)
                assert direct[h][0][n]==stats['candidate']
                divided,dt,_=height_optimum(p,q,h,method='divide')
                assert divided==stats['candidate']==cost(dt,p,q)
                height_dp_checks+=1
                short,_,_=short_tables(p,q,stats['lower_height'],Counter())
                for level,table in enumerate(short):
                    for i,row in enumerate(table):
                        for length,v in enumerate(row):
                            assert v==direct[level][i][i+length]
                            short_checks+=1
            certified+=stats.get('certified',0)
            full_checks+=1
    family_checks=0
    for n in (0,1,2,3,7,15,31,63):
        for family in FAMILIES:
            p,q=weights(n,family,rng) if n else ([],[rng.randrange(20)])
            value,tree,_=solve(p,q)
            assert value==cubic(p,q)[0]==cost(tree,p,q)
            family_checks+=1
    print('Verified',shape_checks,'height optima,',height_checks,
          'tall IPL minima,',full_checks,'full inputs;',certified,'certificates;',
          height_dp_checks,'height-DP and',short_checks,'short-table comparisons',flush=True)
    rows=[]
    for n in (128,256,384,512,768,1000,1024,1536,2048):
        for family in ('near_uniform','random','geometric','gap_spike'):
            p,q=weights(n,family,rng)
            true,_,scans=knuth(p,q)
            trials=[]
            for extra in (0,1,2):
                value,tree,stats=attempt(p,q,extra)
                assert stats['candidate']>=true
                if value is not None: assert value==true==cost(tree,p,q)
                trials.append(dict(stats))
            rows.append(dict(n=n,family=family,optimum=true,trials=trials,
                             knuth_states=n*(n+1)//2,knuth_root_candidates=scans))
            print(n,family,'cert',[x['certified'] for x in trials],
                  'exact height candidates',[x['candidate']==true for x in trials],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'split_height.json'
    out.write_text(json.dumps(dict(shape_checks=shape_checks,height_checks=height_checks,
                                   full_checks=full_checks,certified_checks=certified,
                                   height_dp_checks=height_dp_checks,short_checks=short_checks,
                                   family_checks=family_checks,
                                   rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
