#!/usr/bin/env python3
"""Fixed-mass adversarial search on the exact input-key tail derivative."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random,subprocess,sys
from key_tail_sensitivity import directional


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(37119);stats=Counter();rows=[];best=None;last=None
 engine=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(p,h,x,control=False):
  nonlocal last,best
  n=len(p);engine.stdin.write(f'{n} {h} {x}\n'+ ' '.join(map(str,p))+'\n');engine.stdin.flush();last=json.loads(engine.stdout.readline())
  if control:
   v=[(r&-r).bit_length()-1 for r in range(1,2**h)];assert last['derivative']==directional(p,v,x,stats);stats['independent_controls']+=1
  d=max(range(1,n-2**h+1),key=lambda d:Fraction(last['derivative'][d]*d,(h-1)*d+2**h))
  r=Fraction(last['derivative'][d]*d,(h-1)*d+2**h)
  row=dict(n=n,h=h,x=x,d=d,derivative=last['derivative'][d],tail=last['tail'][d],p=p.copy(),ratio=[r.numerator,r.denominator])
  if best is None or r>Fraction(*best['ratio']):best=row
  return r,row
 for n,h,steps in [(16,3,1500),(32,4,2000),(64,5,2000),(128,6,1200),(256,7,300)]:
  nbest=None
  for trial in range(3):
   p=[0]*n
   for _ in range(n):p[rng.randrange(n)]+=1
   x=n//2;r,row=evaluate(p,h,x,n<=32);local=row
   for it in range(steps):
    q=p.copy();xx=x
    if it%5==0:xx=rng.randrange(n//4,3*n//4)
    else:
     a=rng.choice([i for i,w in enumerate(q) if w]);b=rng.randrange(n);q[a]-=1;q[b]+=1
    rr,nrow=evaluate(q,h,xx,it<3 and n<=32)
    if rr>=r or rng.random()<0.02:p,x,r=q,xx,rr
    if rr>Fraction(*local['ratio']):local=nrow
    if it%250==249:p=local['p'].copy();x=local['x'];r=Fraction(*local['ratio'])
   if nbest is None or Fraction(*local['ratio'])>Fraction(*nbest['ratio']):nbest=local
   print('size',n,'trial',trial,'winner',local['ratio'],'derivative',local['derivative'],'width',local['d'],flush=True)
  evaluate(nbest['p'],h,nbest['x'],True);rows.append(nbest)
 engine.stdin.close();assert engine.wait()==0
 files=('key_sensitivity_search.cpp','key_sensitivity_search.py','key_tail_sensitivity.py','rank_matching_repair.py','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Adversarial diagnostic for exact right input-key derivatives; fixed integer mass n. Finite ratios do not prove an upper bound.',seed=37119,rows=rows,winner=best,compiled_counts=last['counts'],checks=stats,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/key_sensitivity_search.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
