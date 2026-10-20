#!/usr/bin/env python3
"""Literal proof table for a zero-threshold-tail counterexample."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json
from rank_reward_tail import scores,tails
from aggregate_core_audit import layers


def main():
 root=Path(__file__).resolve().parents[1];p=[0,0,0,0,2,1,1,2,1,0];inputs=[p,[int(x>=1) for x in p],[int(x>=2) for x in p]];stats=Counter();rows=[]
 intervals=[(0,8),(1,9),(2,10),(1,8),(2,9),(0,10)]
 for t in (1,2):
  v=[min((r&-r).bit_length()-1,t) for r in range(1,8)];values=[]
  for w in inputs:
   vals=[]
   for i,j in intervals:
    opts=[sum(w[x]*z for x,z in zip(a,v)) for a in combinations(range(i,j),7)]
    vals.append(max(opts));stats['literal_subsequences']+=len(opts);stats['literal_interval_scores']+=1
   tail=sum(vals[:3])-sum(vals[3:]);S,_=scores(w,v,stats);assert all(S[i][j]==a for (i,j),a in zip(intervals,vals));assert tails(S,7,stats)[1]==tail
   if t==2:
    A=list(layers(w,[0]*11,3,4*sum(w)+1,stats))[-1]
    direct=sum(A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1] for i in range(10) for j in range(i+8,10))
    assert direct==tail;stats['original_layer_controls']+=1
   values.append(vals);rows.append(dict(t=t,p=w,scores=vals,tail=tail))
  assert [sum(a[:3])-sum(a[3:]) for a in values]==[1,0,0]
 files=('nested_tail_example.py','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Literal six-interval score table proving that no multiplicative constant transfers binary threshold tails to the weighted tail, for both the alternating and full height-three ruler templates.',intervals=intervals,rows=rows,checks=stats,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/nested_tail_example.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
