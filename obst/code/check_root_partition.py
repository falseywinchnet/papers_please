#!/usr/bin/env python3
"""Full mixed controls for the root/nonroot certificate and exact fallback."""
from collections import Counter
import hashlib,json,random
from pathlib import Path
from root_partition import attempt,solve,normalize
from root_partition_probe import bound
from root_partition_family import family
from endpoint_prices import attempt as priced
from research import cubic,knuth
from joint_merge_probe import enumerated
from shifted_alphabetic import tree_cost


def main():
    rng=random.Random(317219);checks=Counter();examples={}
    for n in tuple(range(9))+(12,20,32,64):
        for trial in range(80):
            kind=trial%5
            if kind==0:p=[rng.randrange(21) for _ in range(n)];q=[rng.randrange(21) for _ in range(n+1)]
            elif kind==1:p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
            elif kind==2:p=[1<<rng.randrange(13) for _ in range(n)];q=[1<<rng.randrange(13) for _ in range(n+1)]
            elif kind==3:p=[rng.randrange(2) for _ in range(n)];q=[rng.randrange(2) for _ in range(n+1)]
            else:p=[rng.randrange(1,20)]*n;q=[rng.randrange(1,20) for _ in range(n+1)]
            expected=cubic(p,q)[0];assert expected==knuth(p,q)[0]
            value,tree,stats=solve(p,q)
            assert value==expected==tree_cost(tree,p,q)
            checks['full_solves']+=1
            checks['certified' if stats['certified'] else 'fallback']+=1
            if n<=8:
                assert min((sum(v*d for v,d in zip(p,pd))+sum(v*d for v,d in zip(q,qd))
                            for _,pd,qd in enumerated(n)),default=0)==expected
                checks['literal_controls']+=1
            if n>=3:
                pp,qq,constant=normalize(p,q,Counter())
                independent,meta=bound(pp,qq)
                if stats['partition_evaluated']:
                    assert stats['global_lower_bound']==independent-constant
                    assert stats['fixed_root_lower_bound']==meta['fixed']-constant
                    assert stats['nonroot_lower_bound']==meta['nonroot']-constant
                else:
                    assert independent-constant==expected
                checks['independent_bound_controls']+=1
                old,_,_,oldmeta=priced(p,q,budget=100,stop_on_certificate=False)
                assert oldmeta['max_complete']
                if stats['global_lower_bound']>oldmeta['lower']:
                    checks['stronger_than_max_transfer']+=1
                    examples.setdefault('stronger',dict(p=p,q=q,optimum=expected,lower=stats['global_lower_bound'],old_lower=str(oldmeta['lower'])))
                if stats['certified'] and old is None:checks['rescued_price_rejection']+=1
                if old is not None and not stats['certified']:checks['lost_price_certificate']+=1
        print(n,dict(checks),flush=True)
    for h in range(3,9):
        p,q=family(h);value,tree,stats=solve(p,q)
        assert value==knuth(p,q)[0] and stats['certified']
        checks['family_controls']+=1
    result=dict(seed=317219,checks=dict(checks),examples=examples,
      source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest()
       for f in ('check_root_partition.py','root_partition.py','root_partition_probe.py','root_partition_family.py',
                 'endpoint_prices.py','shifted_alphabetic.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    (Path(__file__).resolve().parents[1]/'results'/'root_partition.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
