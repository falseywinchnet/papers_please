#!/usr/bin/env python3
"""Independent audit of the weighted alternating-cluster tail and derivatives."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random
from rank_reward_tail import scores,tails
from rank_matching_repair import matching
from key_tail_sensitivity import directional


def check(h,w,stats,derivatives=False):
 C=2**h;K=len(w);assert K>=3 and C>=4*K
 n=2*C;c=C-1;x=C-3*(K-1);k=c+K;b=n-k;mu=min(w);N=(x+1)//2-1
 p=[0]*n
 for r,a in enumerate(w):p[x+3*r]=a
 v=[r%2==0 for r in range(1,C)]
 S,_=scores(p,v,stats);Q,_=matching(p,[1]*((c-1)//2),stats,True);assert S==Q;stats['independent_vectors']+=1
 T=tails(S,c,stats);assert T[K]==N*mu;stats['weighted_tail_formulas']+=1
 for i in range(b):
  delta=S[i][i+k]-S[i+1][i+k]
  if i<x-1:expected=mu if (x-i)%2 else 0
  elif i==x-1:expected=w[0]
  else:expected=p[i+1]
  assert delta==expected,(h,w,i,delta,expected);stats['endpoint_formulas']+=1
 assert S[0][n]==sum(w) and S[b][n]==sum(p[b+1:]);stats['terminal_formulas']+=2
 if derivatives:
  minimizers=[r for r,a in enumerate(w) if a==mu]
  for r in range(K):
   g=directional(p,v,x+3*r,stats)[K];expected=N if minimizers==[r] else 0
   assert g==expected;stats['coordinate_derivative_formulas']+=1
  z=p.copy()
  for r in range(K):z[x+3*r]+=1
  Z,_=scores(z,v,stats);assert tails(Z,c,stats)[K]-T[K]==N;stats['joint_increment_formulas']+=1
 return dict(h=h,C=C,K=K,n=n,x=x,weights=w,tail=N*mu,tail_coefficient=N,P=sum(w))


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(37231);rows=[]
 for w in product(range(3),repeat=3):check(4,list(w),stats,True)
 for h in range(4,8):
  C=2**h
  for K in sorted({3,4,C//8,C//4}):
   if K<3:continue
   for w in [[1]*K,[1]+[2]*(K-1),list(range(1,K+1)),[rng.randrange(10) for _ in range(K)]]:
    rows.append(check(h,w,stats,h<=5))
 for r in range(2,5):
  K=2**r;h=2*r;C=K*K;n=2*C;w=[K,3*K]+[2*K]*(K-2)
  if h<=6:row=check(h,w,stats,False);row['verification']='generic and matching controls'
  else:row=dict(h=h,C=C,K=K,n=n,tail=((C-3*K+4)//2-1)*K,verification='proved formula only')
  N=(C-3*K+4)//2-1;assert sum(w)==n
  row.update(input_mass=n,unique_minimum=K,derivative=N,ratio_to_proposed_key_scale=[N*K,K+C]);rows.append(row)
 for r in (8,16,32,64):
  K=2**r;C=K*K;N=(C-3*K+4)//2-1
  rows.append(dict(h=2*r,C=C,K=K,n=2*C,input_mass=2*C,unique_minimum=K,tail=N*K,derivative=N,ratio_to_proposed_key_scale=[N*K,K+C],verification='proved formula only'))
 files=('weighted_cluster_tail.py','key_tail_sensitivity.py','rank_matching_repair.py','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Closed-form weighted alternating-cluster tails and exact coordinate/joint derivatives. The pointwise sensitivity obstruction concerns the alternating template; it does not refute the full-ruler sensitivity target or the aggregate tail bound.',checks=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/weighted_cluster_tail.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
