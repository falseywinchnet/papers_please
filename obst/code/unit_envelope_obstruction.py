#!/usr/bin/env python3
"""Explicit interaction cells survive deletion of every unit-support diagonal."""
from pathlib import Path
from collections import Counter
import hashlib,json
from aggregate_core_audit import layers,partition
from ruler_clipping_sharp import two_score
from rank_reward_tail import scores
from unit_support_envelope import envelope

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
 for t in range(3,11):
  s=2**t;n=8*s;C=4*s;c=C-1;h=t+2;X=3*s+3;Y=4*s+2
  p=[int(i+1 in (X,Y)) for i in range(n)]
  v=[0]+[(r&-r).bit_length()-1 for r in range(1,C)]
  A=list(layers(p,[0]*(n+1),h,(h+1)*2+1,stats))[-1] if n<=128 else None
  S=scores(p,v[1:],stats)[0] if n<=128 else None
  if n<=128:assert (0,5*s) in partition(n,c)[0][s]
  assert 4*s+1>c and 2*s+1<=c<=6*s-1
  cells=[]
  for r in range(2,t):
   i=s+3-2**r;j=5*s+2**(r-1)
   assert 0<=i<s and 5*s<=j<6*s and not envelope(i,j,h)
   vals=[]
   for a,b in ((i,j),(i+1,j+1),(i,j+1),(i+1,j)):
    value=two_score(a,b,C,X,Y,v,stats)
    u=X-a-2*s;w=3*s-(Y+c-b)
    closed=t+max(u.bit_length()-1,1+w.bit_length()-1)
    assert value==closed,(s,r,a,b,value,closed)
    if S is not None:assert value==S[a][b];stats['generic_score_controls']+=1
    vals.append(value);stats['explicit_score_formulas']+=1
   assert vals[0]+vals[1]-vals[2]-vals[3]==1
   if A is not None:
    assert A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]==1;stats['original_density_controls']+=1
   cells.append(dict(i=i,j=j,r=r,density=1));stats['explicit_density_witnesses']+=1
  assert len(cells)==t-2
  rows.append(dict(s=s,n=n,h=h,key_positions_one_based=[X,Y],tile=[0,5*s,s],local_mass=2,proved_off_envelope_cells=cells,verification='independent feasible-rank enumeration; generic and original-layer controls only at n<=128'))
  print(s,len(cells),flush=True)
 files=('unit_envelope_obstruction.py','unit_support_envelope.py','ruler_clipping_sharp.py','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Exact positive-density witnesses outside the support envelope of every unit outcome. The lower bound is log2(side)-2 at local mass two; no exact total-support formula is asserted.',checks=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/unit_envelope_obstruction.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
