#!/usr/bin/env python3
"""Target large tiles near capacity, avoiding small-tile objective plateaus."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json,random,subprocess,sys
from aggregate_core_audit import layers,partition


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(38219);best=None;last=None;rows=[];stats=Counter()
 engine=subprocess.Popen([sys.argv[1],'4'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(w):
  nonlocal best,last
  n=(len(w)-1)//2;engine.stdin.write(str(n)+'\n'+' '.join(map(str,w))+'\n');engine.stdin.flush();last=json.loads(engine.stdout.readline());a=last['winner'];r=Fraction(a['core'],a['denominator']);row=dict(n=n,W=sum(w),weights=w.copy(),winner=a,ratio=[r.numerator,r.denominator])
  if best is None or r>Fraction(*best['ratio']):best=row;print('new best',n,row['ratio'],a,flush=True)
  return r,row
 for n,steps in ((64,2000),(128,2000),(256,1500),(512,700)):
  for mode in ('mixed','keys','gaps'):
   positions=list(range(2*n+1)) if mode=='mixed' else (list(range(n)) if mode=='keys' else list(range(n,2*n+1)))
   for W in (n//4,n):
    w=[0]*(2*n+1)
    for _ in range(W):w[rng.choice(positions)]+=1
    current,local=evaluate(w)
    for it in range(steps):
     q=w.copy();a=rng.choice([i for i,v in enumerate(q) if v]);b=rng.choice(positions);q[a]-=1;q[b]+=1
     r,row=evaluate(q)
     if r>=current or rng.random()<0.04:w=q;current=r
     if r>Fraction(*local['ratio']):local=row
     if it%300==299:w=local['weights'].copy();current=Fraction(*local['ratio'])
    rows.append(dict(mode=mode,**local));print('done',n,mode,W,local['ratio'],flush=True)
 # Independent all-root controls on every retained size-64 winner.
 for row in rows:
  if row['n']!=64:continue
  n=row['n'];p=row['weights'][:n];q=row['weights'][n:];win=row['winner'];h=win['h']
  if not h:continue
  A=list(layers(p,q,h,(n+1)*sum(row['weights'])+1,stats))[-1];a=win['a'];b=win['b'];s=win['side']
  count=sum(A[i][j+1]+A[i+1][j]>A[i][j]+A[i+1][j+1] for i in range(a,a+s) for j in range(b,b+s))
  assert count==win['core'];assert sum(p[a:b+s])+sum(q[a:b+s+1])==win['mass'];assert (a,b) in partition(n,2**h-1)[0][s];stats['independent_winner_tiles']+=1
 engine.stdin.close();assert engine.wait()==0
 files=('tile_capacity_support.cpp','tile_capacity_support.py','aggregate_core_audit.py')
 out=dict(scope='Capacity-adjacent tile-support diagnostic with side at least four and capacity at least four sides. Fixed-mass mutations do not certify an upper bound.',seed=38219,winner=best,rows=rows,checks=stats,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/tile_capacity_support.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
