#!/usr/bin/env python3
"""Side-specific variable-mass falsification search, with all-root controls.

This searches a proposed local support inequality; it proves no upper bound.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random,subprocess,sys
from aggregate_core_audit import layers,partition


def main():
 root=Path(__file__).resolve().parents[1]; rng=random.Random(39107)
 stats=Counter(); rows=[]; best=None; last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(w,side):
  nonlocal last,best
  n=(len(w)-1)//2
  proc.stdin.write(' '.join(map(str,[n,side,*w]))+'\n');proc.stdin.flush()
  last=json.loads(proc.stdout.readline());r=last['winner']
  ratio=Fraction(r['core'],r['denominator'])
  row=dict(n=n,W=sum(w),side=side,weights=w.copy(),winner=r,ratio=[ratio.numerator,ratio.denominator])
  if best is None or ratio>Fraction(*best['ratio']):
   best=row;print('best',n,side,row['ratio'],r,flush=True)
  return ratio,row
 for n,steps in ((32,1400),(64,1400),(128,1000),(256,600)):
  seeds=[]
  for filename in ('tile_boundary_probe.json','tile_capacity_support.json'):
   for row in json.loads((root/'results'/filename).read_text())['rows']:
    if row['n']==n:seeds.append(row['weights'])
  for side in (4,8,16,32):
   if side>n//4:continue
   for mode in ('keys','gaps','mixed'):
    positions=list(range(n)) if mode=='keys' else list(range(n,2*n+1)) if mode=='gaps' else list(range(2*n+1))
    fixtures=[]
    for kind in range(4):
     w=[0]*(2*n+1)
     if kind==0:
      for _ in range(2*side):w[rng.choice(positions)]+=1
     elif kind==1:
      m=max(2,int(side**.5));start=n//2-m//2
      for i in range(m):w[(n if mode=='gaps' else 0)+start+i]=2*i+1
     elif kind==2:
      for i in positions:w[i]=int(i%2==0)
     else:
      for _ in range(side):w[rng.choice(positions)]+=rng.randrange(1,4)
     fixtures.append(w)
    for w in seeds:
     if all(not x or i in positions for i,x in enumerate(w)):fixtures.append(w)
    local=None
    for w in fixtures:
     r,row=evaluate(w,side)
     if local is None or r>Fraction(*local['ratio']):local=row
    w=local['weights'].copy();current=Fraction(*local['ratio'])
    for it in range(steps):
     q=w.copy();win=local['winner'];a,b=win['a'],win['b']+side
     active=[i for i in positions if q[i]]
     inside=[i for i in positions if (a<=i<b if i<n else a<=i-n<=b)]
     if not inside:inside=positions
     action=rng.randrange(10)
     if action<3 or not active:q[rng.choice(inside)]+=1
     elif action<6:q[rng.choice(active)]-=1
     elif action<9:
      x=rng.choice(active);y=rng.choice(inside);q[x]-=1;q[y]+=1
     else:
      x=rng.choice(active);y=rng.choice(inside);q[y]+=q[x];q[x]=0
     r,row=evaluate(q,side)
     if r>=current or rng.random()<0.025:w=q;current=r
     if r>Fraction(*local['ratio']):local=row
     if it%200==199:
      w=local['weights'].copy();current=Fraction(*local['ratio'])
    rows.append(dict(mode=mode,**local));print('done',n,side,mode,local['ratio'],flush=True)
 # Independent dense all-root recurrence and literal tile counting.
 for row in rows:
  if row['n']>64:continue
  n=row['n'];p=row['weights'][:n];q=row['weights'][n:];h=row['winner']['h']
  if not h:continue
  A=list(layers(p,q,h,(n+1)*sum(row['weights'])+1,stats))[-1]
  win=row['winner'];a,b,s=win['a'],win['b'],win['side']
  assert (a,b) in partition(n,2**h-1)[0][s]
  support=sum(A[i][j+1]+A[i+1][j]>A[i][j]+A[i+1][j+1] for i in range(a,a+s) for j in range(b,b+s))
  assert support==win['core'];assert sum(p[a:b+s])+sum(q[a:b+s+1])==win['mass']
  stats['independent_winner_tiles']+=1
 proc.stdin.close();assert proc.wait()==0
 files=('tile_support_frontier.py','tile_support_frontier.cpp','aggregate_core_audit.py')
 out=dict(scope='Variable-integer-mass, fixed-side local support falsification. Finite ratios are not an upper-bound proof.',seed=39107,winner=best,rows=rows,checks=stats,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/tile_support_frontier.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
