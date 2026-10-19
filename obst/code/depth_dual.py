#!/usr/bin/env python3
"""Experimental Lagrangian bound for ordered mixed-weight depth sequences.

All costs and multipliers use exact integer fixed-point arithmetic. A bound
at ANY multiplier vector is valid; optimizing the dual is heuristic.
An affine-price tail permits an exact shortened oracle, independently of
the unknown optimal BST height. See DEPTH_DUAL.md for the projection lemma.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from research import cost, cubic, knuth, unordered_huffman
from sparse import FAMILIES, weights, SparseSolver

SCALE = 1024


def oracle(p,q,prices,scale=SCALE):
    """O(n^2) at full height, using prefix/suffix minima, not O(n^3).

    prices[d] multiplies G_d + K_(d+1) - 2*K_d, d>=1;
    prices[0] multiplies K_1-1. Adjacent key lengths must differ.
    """
    n=len(p)
    if not n:
        return 0,[],[0]
    h=len(prices)-1
    previous=[None]+[(p[0]+q[0])*b*scale+prices[b-1]-prices[b]
                     for b in range(1,h+1)]
    parents=[]
    for i in range(1,n):
        pref=[None]*(h+1)
        best=None
        for b in range(1,h+1):
            pref[b]=best
            candidate=(previous[b],b)
            if best is None or candidate<best:
                best=candidate
        suff=[None]*(h+1)
        best=None
        for b in range(h,0,-1):
            suff[b]=best
            candidate=(previous[b]+q[i]*b*scale+prices[b],b)
            if best is None or candidate<best:
                best=candidate
        current=[None]*(h+1)
        pred=[None]*(h+1)
        for b in range(1,h+1):
            options=[]
            if pref[b] is not None:
                v,a=pref[b]
                options.append((v+q[i]*b*scale+prices[b],a))
            if suff[b] is not None:
                options.append(suff[b])
            v,a=min(options)
            current[b]=v+p[i]*b*scale+prices[b-1]-2*prices[b]
            pred[b]=a
        previous=current
        parents.append(pred)
    value,last=min((previous[b]+q[n]*b*scale+prices[b]-prices[0],b)
                   for b in range(1,h+1))
    lengths=[last]
    for pred in reversed(parents):
        lengths.append(pred[lengths[-1]])
    lengths.reverse()
    gaps=[lengths[0]]+[max(a,b) for a,b in zip(lengths,lengths[1:])]+[lengths[-1]]
    keys=Counter(lengths)
    external=Counter(gaps)
    violation=[keys[1]-1]+[external[d]+keys[d+1]-2*keys[d]
                           for d in range(1,h+1)]
    direct=scale*(sum(w*l for w,l in zip(p,lengths))
                  +sum(w*l for w,l in zip(q,gaps)))
    direct+=sum(a*b for a,b in zip(prices,violation))
    assert direct==value
    return value,lengths,violation


def unique_root_oracle(p,q,prices,scale=SCALE,return_marginals=False):
    """Two chain passes evaluate every forced-root bound in O(nH).

    Exactly one key has length1. Every other key has length at least2.
    """
    n=len(p)
    h=len(prices)-1
    if not n:
        return 0,[],[0]

    def prefixes(pp,qq):
        closes=[(qq[0]*scale+prices[1],None)]
        parents=[]
        previous=None
        for i in range(n-1):
            pred=[None]*(h+1)
            current=[None]*(h+1)
            if i==0:
                for b in range(2,h+1):
                    current[b]=(pp[0]+qq[0])*b*scale+prices[b-1]-prices[b]
            else:
                pref,suff=[None]*(h+1),[None]*(h+1)
                best=None
                for b in range(2,h+1):
                    pref[b]=best
                    if previous[b] is not None:
                        c=(previous[b],b)
                        if best is None or c<best: best=c
                best=None
                for b in range(h,1,-1):
                    suff[b]=best
                    if previous[b] is not None:
                        c=(previous[b]+qq[i]*b*scale+prices[b],b)
                        if best is None or c<best: best=c
                for b in range(2,h+1):
                    options=[]
                    if pref[b] is not None:
                        v,a=pref[b]
                        options.append((v+qq[i]*b*scale+prices[b],a))
                    if suff[b] is not None:
                        options.append(suff[b])
                    if options:
                        v,a=min(options)
                        current[b]=v+pp[i]*b*scale+prices[b-1]-2*prices[b]
                        pred[b]=a
            options=[(current[b]+qq[i+1]*b*scale+prices[b],b)
                     for b in range(2,h+1) if current[b] is not None]
            closes.append(min(options) if options else None)
            parents.append(pred)
            previous=current
        return closes,parents

    left,lp=prefixes(p,q)
    right,rp=prefixes(p[::-1],q[::-1])
    root_values=[]
    for r in range(n):
        if left[r] is None or right[n-r-1] is None:
            continue
        root_values.append((left[r][0]+right[n-r-1][0]
                            +p[r]*scale-2*prices[1],r))
    value,r=min(root_values)

    def reconstruct(k,closes,parents):
        if k==0: return []
        out=[closes[k][1]]
        for i in range(k-1,0,-1):
            out.append(parents[i][out[-1]])
        return list(reversed(out))

    ls=reconstruct(r,left,lp)+[1]+list(reversed(reconstruct(n-r-1,right,rp)))
    gs=[ls[0]]+[max(a,b) for a,b in zip(ls,ls[1:])]+[ls[-1]]
    k,g=Counter(ls),Counter(gs)
    v=[k[1]-1]+[g[d]+k[d+1]-2*k[d] for d in range(1,h+1)]
    direct=scale*(sum(a*b for a,b in zip(p,ls))+sum(a*b for a,b in zip(q,gs)))
    direct+=sum(a*b for a,b in zip(prices,v))
    assert direct==value and ls.count(1)==1
    if return_marginals:
        by_root=dict((r,val) for val,r in root_values)
        assert len(by_root)==n
        return value,ls,v,[by_root[r] for r in range(n)]
    return value,ls,v


def optimize(p,q,ub,iterations=300,unique_root=False):
    n=len(p)
    # Exact uniform-weight dual suggests this initialization. Multipliers
    # remain arbitrary valid integers on nonuniform data.
    ap=sum(p)*SCALE//max(1,n)
    aq=sum(q)*SCALE//(n+1)
    amplitude=(ap+aq)*(1<<n.bit_length())
    cutoff=min(n,n.bit_length()+2)
    height=min(n,cutoff+3)
    slope=min(p,default=0)*SCALE
    head=[ap*(d-1)+(amplitude>>d) for d in range(cutoff+1)]
    def extend(values):
        return values+[values[-1]+slope*(d-cutoff)
                       for d in range(cutoff+1,height+1)]
    starts=[head,[0]*(cutoff+1)]
    evaluate=unique_root_oracle if unique_root else oracle
    head=max(starts,key=lambda values:evaluate(p,q,extend(values))[0])
    best=None
    best_it=0
    divisor=1
    root_best=None
    def root_stats():
        return (dict(root_candidates=sum(x<ub*SCALE for x in root_best))
                if root_best is not None else {})
    # Polyak-style ascent towards a feasible upper bound; no convergence claim.
    for it in range(iterations):
        prices=extend(head)
        if unique_root:
            value,lengths,v,marginals=evaluate(p,q,prices,return_marginals=True)
            root_best=(marginals if root_best is None else
                       [max(a,b) for a,b in zip(root_best,marginals)])
            certificate=min(root_best)
        else:
            value,lengths,v=evaluate(p,q,prices)
            certificate=value
        if best is None or certificate>best:
            best,best_it=certificate,it
        assert value<=ub*SCALE
        if best==ub*SCALE:
            return best,dict(iterations=it+1,best_iteration=best_it,
                             zero_violation=not any(v),upper_certified=True,
                             oracle_height=height,cutoff=cutoff,oracle_calls=it+3,
                             **root_stats())
        norm=sum(a*a for a in v)
        if norm==0:
            return best,dict(iterations=it+1,best_iteration=best_it,
                             zero_violation=True,lengths=lengths,
                             oracle_height=height,cutoff=cutoff,oracle_calls=it+3,
                             **root_stats())
        gradient=v[:cutoff]+[sum(v[cutoff:])]
        norm=sum(a*a for a in gradient)
        if norm==0:
            return best,dict(iterations=it+1,best_iteration=best_it,
                             zero_violation=False,zero_gradient=True,
                             oracle_height=height,cutoff=cutoff,oracle_calls=it+3,
                             **root_stats())
        if it>best_it and (it-best_it)%25==0:
            divisor*=2
        step=max(1,(ub*SCALE-value)//(norm*divisor))
        head=[a+step*b for a,b in zip(head,gradient)]
    return best,dict(iterations=iterations,best_iteration=best_it,
                     zero_violation=False,oracle_height=height,cutoff=cutoff,
                     oracle_calls=iterations+2,**root_stats())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--iterations',type=int,default=300)
    parser.add_argument('--max-n',type=int,default=64)
    parser.add_argument('--unique-root',action='store_true')
    args=parser.parse_args()
    rng=random.Random(0xD3F7)
    enumeration_rng=random.Random(0xD3F700)
    enumeration_checks=0
    for n in range(1,6):
        vectors=[]
        for ls in itertools.product(range(1,n+1),repeat=n):
            if any(a==b for a,b in zip(ls,ls[1:])):
                continue
            gs=(ls[0],)+tuple(max(a,b) for a,b in zip(ls,ls[1:]))+(ls[-1],)
            k,g=Counter(ls),Counter(gs)
            v=(k[1]-1,)+tuple(g[d]+k[d+1]-2*k[d] for d in range(1,n+1))
            vectors.append((ls,gs,v))
        for _ in range(10):
            p=[enumeration_rng.randrange(20) for _ in range(n)]
            q=[enumeration_rng.randrange(20) for _ in range(n+1)]
            prices=[enumeration_rng.randrange(-50000,50001) for _ in range(n+1)]
            brute=min(SCALE*(sum(a*b for a,b in zip(p,ls))+
                             sum(a*b for a,b in zip(q,gs)))+
                      sum(a*b for a,b in zip(prices,v)) for ls,gs,v in vectors)
            assert oracle(p,q,prices)[0]==brute
            root_brute=min(SCALE*(sum(a*b for a,b in zip(p,ls))+
                                  sum(a*b for a,b in zip(q,gs)))+
                           sum(a*b for a,b in zip(prices,v))
                           for ls,gs,v in vectors if ls.count(1)==1)
            assert unique_root_oracle(p,q,prices)[0]==root_brute
            enumeration_checks+=1
    tested=0
    for n in range(1,11):
        for trial in range(100):
            p=[rng.randrange(20) for _ in range(n)]
            q=[rng.randrange(20) for _ in range(n+1)]
            opt,t=cubic(p,q)
            exact_roots=[sum(p)+sum(q)+cubic(p[:r],q[:r+1])[0]
                         +cubic(p[r+1:],q[r+1:])[0] for r in range(n)]
            for _ in range(5):
                prices=[rng.randrange(-5000,5001) for _ in range(n+1)]
                value,_,_=oracle(p,q,prices)
                assert value<=opt*SCALE,(p,q,prices,value,opt)
                root_value,_,_,marginals=unique_root_oracle(p,q,prices,return_marginals=True)
                assert value<=root_value<=opt*SCALE
                assert all(a<=b*SCALE for a,b in zip(marginals,exact_roots))
                tested+=1
    benchmark_rng_state=rng.getstate()
    projected=0
    for n in range(5,26):
        for _ in range(50):
            p=[rng.randrange(1,21) for _ in range(n)]
            q=[rng.randrange(20) for _ in range(n+1)]
            cutoff=rng.randrange(1,n-2)
            slope=rng.randrange(min(p)*SCALE+1)
            head=[rng.randrange(-50000,50001) for _ in range(cutoff+1)]
            full=head+[head[-1]+slope*(d-cutoff) for d in range(cutoff+1,n+1)]
            a,_,_=oracle(p,q,full)
            b,_,_=oracle(p,q,full[:cutoff+4])
            assert a==b,(p,q,head,slope,a,b)
            a,_,_=unique_root_oracle(p,q,full)
            b,_,_=unique_root_oracle(p,q,full[:cutoff+4])
            assert a==b,(p,q,head,slope,a,b,'unique-root')
            projected+=1
    rng.setstate(benchmark_rng_state)
    rows=[]
    for n in (8,16,32,64,128,256):
        if n>args.max_n:
            break
        for family in FAMILIES:
            p,q=weights(n,family,rng)
            opt,_,_=knuth(p,q)
            solver=SparseSolver(p,q)
            ub,_=solver.upper(0,n)
            solver.upper.cache_clear()
            lb,stats=optimize(p,q,ub,args.iterations,args.unique_root)
            mass=sum(p)+sum(q)
            huffman=unordered_huffman(p,q)
            assert lb<=opt*SCALE<=ub*SCALE
            row=dict(n=n,family=family,opt=opt,upper=ub,
                     dual_scaled=lb,scale=SCALE,huffman=huffman,
                     dual_gap=(opt-lb/SCALE)/mass if mass else 0,
                     huffman_gap=(opt-huffman)/mass if mass else 0,
                     oracle_cells=(2 if args.unique_root else 1)*n*
                                  stats['oracle_height']*stats['oracle_calls'],**stats)
            rows.append(row)
            print(n,family,round(row['dual_gap'],4),round(row['huffman_gap'],4),
                  row.get('root_candidates','-'),flush=True)
    filename='depth_dual_unique_root.json' if args.unique_root else 'depth_dual_truncated.json'
    target=Path(__file__).resolve().parents[1]/'results'/filename
    target.write_text(json.dumps(dict(random_bound_checks=tested,
                                     projection_checks=projected,
                                     enumeration_checks=enumeration_checks,
                                     unique_root=args.unique_root,
                                     rows=rows),indent=2)+'\n')


if __name__=='__main__':
    main()
