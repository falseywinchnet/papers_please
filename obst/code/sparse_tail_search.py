#!/usr/bin/env python3
"""Sparse and phase-coupled falsification of the original total-tail target."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib,json,random,subprocess,sys
from capacity_interaction import profile


def score(row):
 r=row['winner'];return Fraction(r['numerator'],r['denominator'])


def main():
 root=Path(__file__).resolve().parents[1];binary=sys.argv[1];rng=random.Random(34219)
 proc=subprocess.Popen([binary],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 rows=[];counts={};evaluations=0;stats=Counter();best=Fraction(0);winner=None
 for n in (8,16,32,64,128,256,512,1024):
  cases=[];seen=set()
  def add(w,label):
   key=tuple(w)
   if sum(w) and key not in seen:seen.add(key);cases.append((w,label))
  def sparse(entries,label):
   w=[0]*(2*n+1)
   for x,v in entries:w[x]+=v
   add(w,label)
  if n<=64:
   for a,b in combinations(range(2*n+1),2):sparse(((a,1),(b,1)),'exhaustive-unit-pair')
  for gap in sorted({1,2,3,n//4,n//2,*[2**k+delta for k in range(n.bit_length()) for delta in (-1,0,1) if 0<2**k+delta<n]}):
   for x in sorted({0,1,n//4,n//2,max(0,n//2-gap),n-gap-1}):
    if x+gap>=n:continue
    for a,b in ((1,1),(1,2),(2,1),(1,7),(7,1)):
     for kind in ('keys','gaps','mixed'):
      first=x if kind!='gaps' else n+x;second=x+gap if kind=='keys' else n+x+gap
      sparse(((first,a),(second,b)),'structured-pair')
  for period in (2,3,4,5,7,8,9,15,16,17,31,32):
   if period>n:continue
   for block in (1,2,4,8,16,32):
    if block>n:continue
    for kind in ('keys','gaps','mixed'):
     w=[0]*(2*n+1)
     for x in range(n):
      if (x+(x//block)%2)%period==0:
       w[x if kind=='keys' or (kind=='mixed' and x%2==0) else n+x]=1
     add(w,'phase-comb')
   for width in (1,2,3,4,8):
    w=[0]*(2*n+1)
    for x in range(n):
     if x%period<width:w[x]=1+(x%period)
    add(w,'clustered-ramp')
  for _ in range(120):
   size=rng.randrange(2,min(17,2*n+2));indices=rng.sample(range(2*n+1),size)
   sparse([(x,rng.randrange(1,9)) for x in indices],'random-sparse')
  best_n=None
  for w,label in cases:
   proc.stdin.write(str(n)+' '+' '.join(map(str,w))+'\n');proc.stdin.flush();row=json.loads(proc.stdout.readline())
   assert row['weights']==w;counts=row['counts'];evaluations+=1
   if best_n is None or score(row)>score(best_n):best_n=row.copy();best_n['family']=label
   if winner is None or score(row)>best:best=score(row);winner=row.copy();winner['family']=label
  rows.append(best_n)
  print(n,'inputs',len(cases),'max',str(score(best_n)),'overall',str(best),flush=True)
 proc.stdin.close();assert proc.wait()==0
 for row in rows:
  n=row['n']
  if n>128:continue
  w=row['weights'];h=row['winner']['h'];d=row['winner']['d'];a=profile(w,stats)[h-1]
  assert row['winner']['mass']==a['tail'][d];stats['winner_controls']+=1
 result=dict(scope='Falsification of total tail O(W(L+c/d)) on sparse and coupled phase patterns; no universal upper-bound claim.',
 evaluated_inputs=evaluations,maximum_ratio=[best.numerator,best.denominator],winner=winner,rows=rows,
 optimized_counts=counts,independent_checks=stats,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in
 ('sparse_tail_search.py','core_tail_search.cpp','capacity_interaction.py','aggregate_core_audit.py')})
 (root/'results/sparse_tail_search.json').write_text(json.dumps(result,indent=2)+'\n');print('complete',evaluations,str(best),flush=True)
if __name__=='__main__':main()
