#!/usr/bin/env python3
"""Attack U_d <= const P(max v + sum v/d) for general rank templates."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json,random,subprocess,sys
from itertools import combinations

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(39213);stats=Counter();rows=[];best=None;last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(p,v):
  nonlocal last,best
  proc.stdin.write(' '.join(map(str,[len(p),len(v),*p,*v]))+'\n');proc.stdin.flush();last=json.loads(proc.stdout.readline())
  ratio=Fraction(last['numerator'],last['denominator']);row=dict(p=p.copy(),v=v.copy(),d=last['d'],tail=last['tail'],ratio=[ratio.numerator,ratio.denominator])
  if best is None or ratio>Fraction(*best['ratio']):best=row;print('best',len(p),row,flush=True)
  return ratio,row
 for n,steps in ((16,2400),(32,2400),(64,1800),(128,800)):
  c=n//2-1
  for mode in ('binary','general','ruler'):
   p=[0]*n
   for _ in range(n):p[rng.randrange(n)]+=1
   v=[int(i%2==1) for i in range(c)] if mode=='binary' else [((i+1)&-(i+1)).bit_length()-1 for i in range(c)]
   current,local=evaluate(p,v)
   for it in range(steps):
    pp=p.copy();vv=v.copy()
    if mode=='ruler' or rng.randrange(2):
     a=rng.choice([i for i,x in enumerate(pp) if x]);b=rng.randrange(n);pp[a]-=1;pp[b]+=1
    elif mode=='binary':
     a=rng.choice([i for i,x in enumerate(vv) if x]);b=rng.choice([i for i,x in enumerate(vv) if not x]);vv[a]=0;vv[b]=1
    else:
     a=rng.choice([i for i,x in enumerate(vv) if x]);b=rng.randrange(c);vv[a]-=1;vv[b]+=1
    r,row=evaluate(pp,vv)
    if r>=current or rng.random()<.035:p=pp;v=vv;current=r
    if r>Fraction(*local['ratio']):local=row
    if it%300==299:p=local['p'].copy();v=local['v'].copy();current=Fraction(*local['ratio'])
   rows.append(dict(mode=mode,n=n,**local));print('done',n,mode,local['ratio'],flush=True)
 # Literal subsequences independently audit the n=16 retained examples.
 for row in rows:
  if row['n']!=16:continue
  p,v,d=row['p'],row['v'],row['d'];n=len(p);c=len(v);k=c+d
  def score(i,j):
   values=[]
   for inds in combinations(range(i,j),c):
    values.append(sum(p[x]*a for x,a in zip(inds,v)));stats['literal_subsequences']+=1
   stats['literal_scores']+=1
   return max(values)
  U=sum(score(i,i+k) for i in range(n-k+1))-sum(score(i+1,i+k) for i in range(n-k))-score(0,n)
  assert U==row['tail'];stats['literal_tail_controls']+=1
 proc.stdin.close();assert proc.wait()==0
 files=('template_tail_probe.py','template_tail_probe.cpp')
 out=dict(scope='General-template width-sensitive upper-tail falsification. Finite ratios give no upper bound.',seed=39213,winner=best,rows=rows,checks=stats,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/template_tail_probe.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
