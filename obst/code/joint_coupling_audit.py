#!/usr/bin/env python3
"""Exact small-alphabet, depth-profile, and normalization controls."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from joint_merge_probe import candidate,oracle,enumerated
from research import cubic,cost
from threshold_probe import key_bound,threshold_bound


def profile_key_cost(p,pd):
    if not p:return 0
    prefix=[0]
    for x in sorted(p,reverse=True):prefix.append(prefix[-1]+x)
    total=prefix[-1];value=total
    for t in range(1,max(pd)):
        A=sum(d<=t for d in pd)
        value+=total-prefix[A]
    return value


def main():
    checks=Counter();rows=[];failures=[];rng=random.Random(317208)
    for alphabet in ((0,1),(1,2)):
        for n in range(8):
            row=Counter(n=n,low=alphabet[0],high=alphabet[1])
            for count in range(n+1):
                p=[alphabet[0]]*count+[alphabet[1]]*(n-count)
                for q in itertools.product(alphabet,repeat=n+1):
                    expected,witness=oracle(p,q);got=candidate(p,q)
                    row['cases']+=1
                    if not got['valid'] or got['value']!=expected:
                        row['invalid' if not got['valid'] else 'suboptimal']+=1
                        if len(failures)<8:failures.append(dict(p=p,q=q,optimum=expected,candidate=got))
                    else:row['exact']+=1
                    if len(set(p))<=1:
                        shifted=[x+(p[0] if p else 0) for x in q]
                        assert got['valid'] and got['value']==expected==cubic([0]*n,shifted)[0]-(p[0] if p else 0)*n
                        checks['constant_key_shift_controls']+=1
            rows.append(dict(row));print(dict(row),flush=True)
    for n in range(10):
        p=[rng.randrange(40) for _ in range(n)]
        for tree,pd,qd in enumerated(n):
            assert profile_key_cost(p,pd)==sum(x*y for x,y in zip(sorted(p,reverse=True),sorted(pd)))
            assert sum(qd)-sum(pd)==n
            checks['profile_and_depth_identity_controls']+=1
    for n in range(1,21):
        for trial in range(20):
            p=[rng.randrange(1,30) for _ in range(n)];q=[rng.randrange(1,30) for _ in range(n+1)]
            lower=key_bound(p)+threshold_bound(q);opt,tree=cubic(p,q);merge=candidate(p,q)
            for a in sorted({-min(q),0,min(p),rng.randrange(-min(q),min(p)+1)}):
                pp=[x-a for x in p];qq=[x+a for x in q]
                assert key_bound(pp)+threshold_bound(qq)-a*n==lower
                assert cubic(pp,qq)[0]-a*n==opt==cost(tree,pp,qq)-a*n
                shifted=candidate(pp,qq)
                assert shifted['qd']==merge['qd'] and shifted['valid']==merge['valid']
                assert shifted['charges']-a*n==merge['charges']
                assert [x['pair_margin'] for x in shifted['trace']]==[x['pair_margin'] for x in merge['trace']]
                if merge['valid']:assert shifted['value']-a*n==merge['value']
                checks['transfer_invariance_controls']+=1
    result=dict(seed=317208,checks=dict(checks),small_alphabets=rows,failures=failures,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('joint_coupling_audit.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    (Path(__file__).resolve().parents[1]/'results'/'joint_coupling_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('checks',dict(checks),flush=True)


if __name__=='__main__':main()
