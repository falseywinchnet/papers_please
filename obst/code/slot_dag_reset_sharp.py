#!/usr/bin/env python3
"""Exact tight reset-path family on arbitrary diagrams, outside the OBST domain."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json
from slot_dag_forward import ForwardDiagram
from slot_dag_reset_audit import certify


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
    for m in list(range(1,17))+[24,32,48,64]:
        h=2*m;N=2**m;manager=ForwardDiagram(h);ref=(0,0)
        coefficients=[-2**j for j in range(m)]+[-Fraction(2**(j+1)-1,m+1) for j in range(m)]
        for d,c in enumerate(coefficients,1):ref=manager.make(d,ref,manager.offset(ref,c))
        assert manager.reachable([ref])==h+1
        _,row=certify(manager,ref,1,1,stats)
        assert row['contexts']==3*m*(m+1)//2
        expected_make=m*(7*m*m+15*m+2)//6
        assert row['counts']['dag_make_calls']==expected_make
        assert row['counts']['forward_replace_visits']==expected_make
        assert row['max_carries_per_node']==m+1
        # This explicit violation proves the family is not an actual prefix.
        assert manager.value(ref,N)>manager.value(ref,N-1)
        checks=0
        xs=range(N) if m<=6 else [0,1,N-1]+[2**j for j in range(m)]
        for x in xs:
            ys=range(N) if m<=6 else [0,1,N//2,N-2,N-1]
            for y in ys:
                assert manager.value(ref,N*x+y)==-Fraction(2*x-bin(x).count('1'),m+1)-y
                checks+=1
        rows.append(dict(m=m,height=h,input_nodes=h+1,expected_contexts=3*m*(m+1)//2,
                         expected_make_calls=expected_make,value_controls=checks,
                         domain='Not realizable as an OBST prefix: F(2^m)>F(2^m-1) violates endpoint dominance',**{k:v for k,v in row.items() if k!='input_nodes'}))
        print(m,row['contexts'],expected_make,flush=True)
    files=['slot_dag_reset_sharp.py','slot_dag_reset_audit.py','slot_dag_forward.py',
           'slot_dag_skyline.py','slot_dag.py','slot_vector.py','slot_records.py']
    result=dict(scope='Closed-form sharpness of the mechanical carry recursion on arbitrary compact inputs; explicit violation excludes this family from actual OBST prefixes',
                counts=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_reset_sharp.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
