#!/usr/bin/env python3
"""Matched full screening attempts on arbitrary 256-bit mixed weights."""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from coarse_screen import solve
from research import knuth,cost


def main():
    rng=random.Random(692020);rows=[]
    for n in (32,64,128,256):
        p=[rng.getrandbits(256)+1 for _ in range(n)]
        q=[rng.getrandbits(256)+1 for _ in range(n+1)]
        expected,tree,scans=knuth(p,q)
        assert cost(tree,p,q)==expected
        for b in (1,16,n.bit_length()**2,n.bit_length()**3):
            stats=Counter();result=solve(p,q,stats,precision=b)
            assert result['cost']==expected==cost(result['tree'],p,q)
            assert result['coarse_mass']<=b*(2*n+1)
            assert result['coarse_core']<=n+n.bit_length()*result['coarse_mass']
            assert stats['range_product_nodes']==2*n-1
            rows.append(dict(n=n,precision=b,p=p,q=q,cost=str(expected),
                             method=result['method'],states=result.get('states'),arcs=result.get('arcs'),
                             coarse_mass=result['coarse_mass'],coarse_core=result['coarse_core'],
                             coarse_height=result['coarse_height'],fine_height=result['fine_height'],
                             delta=str(result['delta']),input_max_bits=max((*p,*q)).bit_length(),
                             preparation=result['preparation_counts'],query=result['query_counts'],
                             complete_counts=dict(stats),reference_knuth_candidates=scans))
            print(n,b,result['method'],result.get('states'),result.get('arcs'),flush=True)
    root=Path(__file__).resolve().parents[1]
    files=('coarse_screen_scale.py','root_ranges.py','coarse_screen.py','core_monge.py',
           'compact_obst.py','trimmed_height.py','research.py','coarse_face.py')
    out=dict(seed=692020,scope='Matched complete exact constructions at four coarse precisions; arbitrary wide weights, full Knuth controls and every failed route retained',
             rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/coarse_screen_scale.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
