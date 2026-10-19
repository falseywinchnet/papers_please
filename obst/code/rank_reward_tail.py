#!/usr/bin/env python3
"""Exact audit of upper-tail rank-reward stability and ruler clipping."""
from collections import Counter
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers


def scores(p,v,stats,witness=False):
 n=len(p);c=len(v);S=[[None]*(n+1) for _ in range(n+1)];R={}
 for i in range(n-c+1):
  dp=[None]*(c+1);dp[0]=0;seq=[None]*(c+1);seq[0]=()
  for j in range(i+1,n+1):
   for r in range(min(c,j-i),0,-1):
    if dp[r-1] is None:continue
    candidate=dp[r-1]+p[j-1]*v[r-1];stats['matching_candidates']+=1
    path=seq[r-1]+(j-1,) if witness else None
    if dp[r] is None or candidate>dp[r] or (witness and candidate==dp[r] and path<seq[r]):
     dp[r]=candidate
     if witness:seq[r]=path
   if j-i>=c:
    S[i][j]=dp[c];stats['score_entries']+=1
    if witness:R[i,j]=seq[c]
 return S,R


def tails(S,c,stats):
 n=len(S)-1;tail=[0]*(n+1)
 for i in range(n):
  for j in range(i+c+1,n):
   d=S[i][j]+S[i+1][j+1]-S[i][j+1]-S[i+1][j];assert d>=0
   tail[j-i-c]+=d;stats['upper_densities']+=1
 for d in range(n-1,0,-1):tail[d]+=tail[d+1]
 return tail


def small_audit(p,v,stats):
 n=len(p);c=len(v);P=sum(p);S,R=scores(p,v,stats,True)
 for i,j in R:
  choices=list(combinations(range(i,j),c));best=max(sum(p[x]*a for x,a in zip(t,v)) for t in choices)
  path=min(t for t in choices if sum(p[x]*a for x,a in zip(t,v))==best)
  assert (S[i][j],R[i,j])==(best,path);stats['literal_intervals']+=1;stats['literal_subsets']+=len(choices)
  if j-i>c:
   assert all(a<=b<=z for a,b,z in zip(R[i,j-1],R[i,j],R[i+1,j]));stats['path_monotonicity_checks']+=c
 base=tails(S,c,stats)
 for r in range(c):
  for delta in (1,5):
   vv=v.copy();vv[r]+=delta;T,_=scores(p,vv,stats);tt=tails(T,c,stats)
   for d in range(1,n+1):
    change=tt[d]-base[d]
    assert -2*P*delta<=change<=P*delta,(p,v,r,delta,d,change)
    stats['coordinate_stability_checks']+=1
 stats['small_inputs']+=1


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(34220);stats=Counter()
 for n in range(2,7):
  c=min(3,n-1)
  for p in product((0,1),repeat=n):
   for v in ([0]*c,[1]*c,[i%2 for i in range(c)]):small_audit(list(p),v,stats)
 for n in (7,8,9,10):
  for _ in range(15):
   c=rng.randrange(1,n);small_audit([rng.randrange(8) for _ in range(n)],[rng.randrange(5) for _ in range(c)],stats)
 rows=[];maxperiodic=Fraction(0);winner=None
 for h in range(3,8):
  C=2**h;c=C-1;n=2*C;v=[(r&-r).bit_length()-1 for r in range(1,C)]
  fixtures=[('uniform',[1]*n),('alternating',[int(i%2==0) for i in range(n)]),
            ('two-keys',[int(i in (C-5,C)) for i in range(n)]),('ramp',[i+1 for i in range(n)])]
  for block in (1,2,3,4,5,8,16):
   fixtures.append(('phase-alternating',[int((i+i//block)%2==0) for i in range(n)]))
  for _ in range(4):fixtures.append(('random',[rng.randrange(8) for _ in range(n)]))
  for name,p in fixtures:
   P=sum(p);S,_=scores(p,v,stats);base=tails(S,c,stats)
   if h==3:
    q=[rng.randrange(4) for _ in range(n+1)];M=(h+2)*(P+sum(q))+1
    A=list(layers(p,q,h,M,stats))[-1]
    for i in range(n):
     for j in range(i+c+1,n):
      assert A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]==S[i][j]+S[i+1][j+1]-S[i][j+1]-S[i+1][j]
      stats['mixed_layer_checks']+=1
   for t in range(h):
    vv=[min(a,t) for a in v];Q,_=scores(p,vv,stats);cut=tails(Q,c,stats)
    error=2**(h-t)-(h-t)-1;assert sum(a-b for a,b in zip(v,vv))==error
    for d in range(1,n+1):
     assert base[d]<=cut[d]+P*error;stats['clipping_checks']+=1
    if t and 2**t<n and P:
     d=2**t;ratio=Fraction(cut[d],t*P);stats['periodic_diagnostics']+=1
     if ratio>maxperiodic:
      maxperiodic=ratio;winner=dict(h=h,n=n,t=t,d=d,p=p,tail=cut[d],P=P,ratio=[ratio.numerator,ratio.denominator],family=name)
  rows.append(dict(h=h,n=n,inputs=len(fixtures)))
  print(h,'periodic diagnostic maximum',str(maxperiodic),flush=True)
 files=('rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Finite audit of the proved rank-coordinate stability, nonnegative densities, and ruler clipping formulas. The separate diagnostic candidate U_clipped(d)<=tP for d>=2^t is false; its counterexample is retained.',
 checks=stats,rows=rows,periodic_candidate_maximum=[maxperiodic.numerator,maxperiodic.denominator],periodic_candidate_winner=winner,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/rank_reward_tail.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
