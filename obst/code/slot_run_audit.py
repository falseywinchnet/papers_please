#!/usr/bin/env python3
"""Independent finite products, literal subsequences, original trees and gap barriers."""
from collections import Counter
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
import hashlib,json,random
from math import comb
from slot_run import slot_transfer,solve
from rank_transfer import runs
from aggregate_core_audit import layers
from research import cost

def nu(t):return (t&-t).bit_length()-1

def direct_factor(a,b,w,m,K,h):
 return K*max(m-b+a,0)-w*sum(min(m,b//2**r-a//2**r) for r in range(1,h))

def reference(weights,a,b,stats):
 dp=[0]+[None]*len(weights)
 for t in range(a+1,b+1):
  for k in range(len(weights),0,-1):
   if dp[k-1] is not None:
    v=dp[k-1]+weights[k-1]*nu(t)
    if dp[k] is None or v>dp[k]:dp[k]=v
   stats['slot_independent_dp_candidates']+=1
 return dp[-1]

def verify_tree(tree,p,q,h,stats):
 n=len(p);seen=[];stack=[(tree,0)]
 while stack:
  t,d=stack.pop()
  if t is None:assert d<=h;continue
  r,l,b=t;assert d<h;seen.append(r);stack.extend([(b,d+1),(l,d+1)]);stats['verified_tree_nodes']+=1
 assert sorted(seen)==list(range(n))
 def walk(t):return [] if t is None else walk(t[1])+[t[0]]+walk(t[2])
 assert walk(tree)==list(range(n));return cost(tree,p,q)

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(531019)
 for n in range(1,6):
  for weights in product((0,1,3),repeat=n):
   h=3;c=7;node,K,v=slot_transfer(weights,h,stats);blocks=runs(weights)
   dense=[[0 if a==b else None for b in range(c+1)] for a in range(c+1)]
   for w,m in blocks:
    Q=[[direct_factor(a,b,w,m,K,h) for b in range(c+1)] for a in range(c+1)]
    stats['finite_dense_product_candidates']+=sum(x is not None for row in dense for x in row)*(c+1)
    dense=[[min(dense[a][t]+Q[t][b] for t in range(c+1) if dense[a][t] is not None) for b in range(c+1)] for a in range(c+1)]
   for a in range(c+1):
    for b in range(c+1):
     assert node.T.value_reference(a,b)==dense[a][b];stats['finite_product_entry_controls']+=1
     if b-a>=n:
      dp=reference(weights,a,b,stats)
      literal=max(sum(w*nu(t) for w,t in zip(weights,ss)) for ss in combinations(range(a+1,b+1),n))
      assert dense[a][b]==-dp==-literal;stats['literal_feasible_entry_controls']+=1
      stats['literal_subsequences']+=comb(b-a,n)
   stats['exhaustive_transfer_inputs']+=1
 print('finite',dict(stats),flush=True)
 # Direct leaf controls include long runs with no feasible entry, fractions and small heights.
 for h in range(1,6):
  c=2**h-1
  for m in (1,2,max(1,c//2),c,c+2):
   w=Fraction(5,3);node,K,v=slot_transfer([w]*m,h,stats)
   for a in range(c+1):
    for b in range(c+1):
     assert node.T.value_reference(a,b)==direct_factor(a,b,w,m,K,h);stats['leaf_completion_controls']+=1
 # Full prescribed-height constructor, including nonzero common internal gaps and arbitrary endpoints.
 for n in (1,2,3,4,5,7,8,12,16,24):
  for trial in range(10):
   if trial==0:p=[1]*n
   elif trial==1:p=[2**i for i in range(n)]
   elif trial==2:p=[0]*n
   else:p=[rng.randrange(7) for _ in range(n)]
   b=Fraction(rng.randrange(4),2);q=[rng.randrange(7)]+[b]*(n-1)+[rng.randrange(7)]
   H=n.bit_length()+1;M=(H+1)*(sum(p)+sum(q))+1;original=list(layers(p,q,H,M,stats))
   for h in range(1,H+1):
    if n>2**h-1:assert solve(p,q,h,stats) is None;stats['capacity_rejections']+=1;continue
    result=solve(p,q,h,stats);assert result['cost']==original[h][0][n]
    assert verify_tree(result['tree'],p,q,h,stats)==result['cost'];stats['original_tree_controls']+=1
   stats['mixed_constructor_inputs']+=1
 try:solve([1,2,3],[0,1,2,0],3)
 except ValueError:stats['unequal_gap_rejections']+=1
 else:raise AssertionError('Unequal internal gaps were accepted')
 print('original',dict(stats),flush=True)
 # A one-gap transition has an exact dense signed checkerboard on fully feasible entries.
 gap_rows=[]
 for s in (2,4,8,16,32,64,128,256,512):
  h=s.bit_length()+1;c=4*s-1;positive=negative=0;mass=0
  def Q(u,v):assert 1<=u<v<=c;return -min(nu(u),nu(v))
  for u in range(1,s+1):
   for v in range(2*s+1,3*s+1):
    D=Q(u,v+1)+Q(u+1,v)-Q(u,v)-Q(u+1,v+1)
    e=u+(u%2);f=v+(v%2);predicted=(-1)**(u+v)*min(nu(e),nu(f))
    assert D==predicted and D!=0;positive+=D>0;negative+=D<0;mass+=abs(D);stats['gap_transition_density_controls']+=1
  assert positive==negative==s*s//2
  gap_rows.append(dict(side=s,height=h,capacity=c,positive=positive,negative=negative,absolute_density_mass=mass,verification='Direct four-entry transition evaluation and proved checkerboard formula'))
 # Large run-based products and complete repaired trees; no large quadratic reference.
 large=[]
 for h in (8,10,12,14):
  c=2**h-1;n=c//2+1
  for kind in ('uniform','three_runs'):
   p=[4]*n if kind=='uniform' else [1 if i<n//3 else 7 if i<2*n//3 else 2 for i in range(n)]
   q=[3]*(n+1);counts=Counter();result=solve(p,q,h,counts)
   assert verify_tree(result['tree'],p,q,h,counts)==result['cost']
   if kind=='uniform':assert result['cost']==7*sum(i.bit_length() for i in range(1,n+1))+3*n
   large.append(dict(n=n,h=h,kind=kind,runs=result['runs'],cost=result['cost'],counts=counts,verification='Full sparse product, witness traceback and independent tree cost/height; uniform rows additionally have the closed minimum-IPL optimum'))
   print('large',h,kind,'runs',result['runs'],'core terms',counts['slot_input_core_terms'],flush=True)
 files=['slot_run.py','slot_run_audit.py','core_monge.py','rank_transfer.py','mixed_slots.py','aggregate_core_audit.py','research.py']
 out=dict(scope='Exact prescribed-height construction for arbitrary keys with equal internal gaps; no unrestricted-height certificate. Separate one-gap checkerboard is a transfer-coordinate barrier, not an interval-core lower bound.',seed=531019,counts=stats,gap_rows=gap_rows,large=large,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/slot_run_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
