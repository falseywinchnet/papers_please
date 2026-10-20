#!/usr/bin/env python3
"""Independent subsequence and original-layer controls for binary dilation."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import hashlib,json,random
from rank_reward_tail import scores
from aggregate_core_audit import layers

def nu(x):return (x&-x).bit_length()-1

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(41119);stats=Counter();rows=[]
 # Both restrictions in the identity are necessary, even for binary keys.
 for word,c,wrong in (([1,1,1,0,0,0,0,0],7,0),([1,1,1,1],3,2)):
  choices=list(combinations(range(len(word)),c))
  got=max(sum(word[k]*nu(r+1) for r,k in enumerate(seq)) for seq in choices)
  assert got==1 and got!=wrong;stats['scope_counterexamples']+=1
  stats['literal_scope_subsequences']+=len(choices)
 # Componentwise saturation is tested for arbitrary nonnegative rank rewards.
 for n in range(2,8):
  for mask in range(1<<n):
   p=[(mask>>k)&1 for k in range(n)]
   for c in range(1,n+1):
    v=[rng.randrange(5) for _ in range(c)];target=min(sum(p),c)
    allscore=[];saturated=[]
    for seq in combinations(range(n),c):
     val=sum(p[k]*r for k,r in zip(seq,v));allscore.append(val)
     if sum(p[k] for k in seq)==target:saturated.append(val)
     stats['literal_saturation_subsequences']+=1
    assert max(allscore)==max(saturated);stats['saturation_controls']+=1
 for n,h in ((8,2),(12,3),(16,3)):
  c=2**h-1
  fixtures=[[int(i in xs) for i in range(n)] for xs in ((n//2,), (n//2-2,n//2+1),tuple(range(n//2-2,n//2+2))) if len(xs)<=c]
  for _ in range(4):
   xs=rng.sample(range(n),rng.randrange(1,min(n,c)+1));fixtures.append([int(i in xs) for i in range(n)])
  for p in fixtures:
   S,_=scores(p,[nu(r) for r in range(1,c+1)],stats)
   for d in (2,4):
    N=d*n;H=h+nu(d);C=d*(c+1)-1;P=[x for x in p for _ in range(d)]
    T,_=scores(P,[nu(r) for r in range(1,C+1)],stats)
    q=[rng.randrange(4) for _ in range(N+1)]
    A=list(layers(P,q,H,(H+1)*(sum(P)+sum(q))+1,stats))[-1] if N<=32 else None
    tested={}
    for a in range(N):
     for b in range(a+C,N+1):
      if a%d and p[a//d]:continue
      if b%d and p[b//d]:continue
      aa=(a+d-1)//d;bb=b//d;m=sum(p[aa:bb])
      assert bb-aa>=c and m<=c
      expected=m*(d-1)+S[aa][bb]
      assert T[a][b]==expected,(n,h,p,d,a,b,T[a][b],expected)
      tested[a,b]=expected;stats['dilation_score_controls']+=1
      if A is not None:
       original=(b-a-C)*((H+1)*(sum(P)+sum(q))+1)+H*(sum(P[a:b])+sum(q[a:b+1]))-expected
       assert A[a][b]==original;stats['mixed_original_entry_controls']+=1
    count=0
    for i in range(N):
     for j in range(i+C+1,N):
      corners=((i,j),(i+1,j+1),(i,j+1),(i+1,j))
      if not all(x in tested for x in corners):continue
      D=T[i][j]+T[i+1][j+1]-T[i][j+1]-T[i+1][j]
      if i%d==0 and j%d==d-1:
       a=i//d;b=(j+1)//d-1
       expected=S[a][b]+S[a+1][b+1]-S[a][b+1]-S[a+1][b]
      else:expected=0
      assert D==expected;stats['dilation_density_controls']+=1;count+=int(D>0)
      if D:assert ((j-i-C+1)&(j-i-C))!=0;stats['off_envelope_controls']+=1
      if A is not None:
       assert A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]==D;stats['mixed_original_density_controls']+=1
    rows.append(dict(n=n,h=h,p=p,d=d,fine_n=N,score_controls=len(tested),positive_controlled_cells=count,original_all_root=N<=32))
  print(n,h,len(fixtures),flush=True)
 files=('binary_dilation_audit.py','rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Independent finite controls of the separately proved binary-block dilation identity, including arbitrary nonnegative gap weights in original-layer controls. Endpoint cuts through positive blocks and intervals with more than coarse capacity many positive blocks are outside the theorem.',checks=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/binary_dilation_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
