#!/usr/bin/env python3
"""Falsification search for width-sensitive clipped-ruler upper tails."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random,subprocess,sys
from rank_reward_tail import scores,tails


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(35019);stats=Counter();proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True);last={};best={};rows=[]
 def evaluate(p,h,t,control=False):
  nonlocal last
  n=len(p);C=2**h;c=C-1;v=[min((r&-r).bit_length()-1,t) for r in range(1,C)];P=sum(p)
  proc.stdin.write(' '.join(map(str,[n,c]+p+v))+'\n');proc.stdin.flush();a=json.loads(proc.stdout.readline());last=a['counts']
  if control:
   S,_=scores(p,v,stats);T=tails(S,c,stats);assert a['tail']==T;stats['independent_vectors']+=1
  if not P:return Fraction(0),None
  d=max(range(1,n+1),key=lambda d:Fraction(a['tail'][d]*d,P*(t*d+C)))
  value=Fraction(a['tail'][d]*d,P*(t*d+C));row=dict(n=n,h=h,t=t,c=c,d=d,mass=a['tail'][d],support=a['support'][d],P=P,p=p.copy(),ratio=[value.numerator,value.denominator])
  if t not in best or value>Fraction(*best[t]['ratio']):best[t]=row
  return value,row
 for n in range(4,11):
  for p in product((0,1),repeat=n):evaluate(list(p),2,1,n<=7)
 for n in (16,32,64,128,256):
  for h in sorted({max(2,(n.bit_length()-1)//2),n.bit_length()-2}):
   if 2**h-1>=n:continue
   for t in sorted({1,min(2,h-1),h-1}):
    fixtures=[[1]*n,[i+1 for i in range(n)],[int(i%2==0) for i in range(n)]]
    for step in (2,3,4,5,7,8,9,15,16,17):
     for phase in (0,1):fixtures.append([int((i+phase)%step==0) for i in range(n)])
    C=2**h
    for m in (2,4,8,16):
     for step in (3,5,9,17):
      span=(m-1)*step+1
      if span<=n:
       start=(n-span)//2;fixtures.append([int(i>=start and (i-start)%step==0 and (i-start)//step<m) for i in range(n)])
    for p in fixtures:evaluate(p,h,t,n<=32)
    for mode in ('dense','sparse'):
     p=[1]*n if mode=='dense' else [0]*n
     if mode=='sparse':
      for _ in range(n):p[rng.randrange(n)]+=1
     value,row=evaluate(p,h,t)
     local=row
     for iteration in range(600 if n<=128 else 200):
      q=p.copy()
      if rng.randrange(10)==0:
       q=[0]*n
       for _ in range(n):q[rng.randrange(n) if mode=='dense' else rng.choice([n//2-3,n//2,n//2+3])]+=1
      else:
       a=rng.choice([i for i,x in enumerate(q) if x]);b=rng.randrange(n);amount=rng.randint(1,q[a]);q[a]-=amount;q[b]+=amount
      vv,rr=evaluate(q,h,t)
      if vv>=value or rng.randrange(100)==0:p=q;value=vv
      if Fraction(*rr['ratio'])>Fraction(*local['ratio']):local=rr
     rows.append(dict(mode=mode,**local))
   print('size',n,'h',h,'maxima',{t:str(Fraction(*r['ratio'])) for t,r in best.items()},flush=True)
 for r in best.values():
  if r['n']<=128:evaluate(r['p'],r['h'],r['t'],True)
 proc.stdin.close();assert proc.wait()==0
 files=('periodic_tail_probe.py','periodic_tail_probe.cpp','rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Diagnostic only: tests U_d(v_clipped) / [P(t+(c+1)/d)], not a proved bound.',seed=35019,winners=list(best.values()),rows=rows,optimized_counts=last,independent_checks=stats,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/periodic_tail_probe.json').write_text(json.dumps(result,indent=2)+'\n');print('complete',last,dict(stats),flush=True)
if __name__=='__main__':main()
