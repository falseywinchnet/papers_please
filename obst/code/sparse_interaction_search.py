#!/usr/bin/env python3
"""Target sparse weights missed by dense fixed-mass starts; diagnostic only."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib,json,random,subprocess,sys
from capacity_interaction import profile


def score(row):return Fraction(row['excess'],row['denominator'])


def main():
 root=Path(__file__).resolve().parents[1];binary=sys.argv[1];rng=random.Random(33220)
 proc=subprocess.Popen([binary],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 rows=[];counts={};evaluations=0;stats=Counter();best=Fraction(0);winner=None
 for n in (8,16,32,64,128,256,512):
  cases=[];seen=set()
  def add(entries,label):
   w=[0]*(2*n+1)
   for x,v in entries:w[x]+=v
   key=tuple(w)
   if key not in seen:seen.add(key);cases.append((w,label))
  if n<=64:
   for a,b in combinations(range(2*n+1),2):add(((a,1),(b,1)),'exhaustive-unit-pair')
  for gap in sorted({1,2,3,n//4,n//2,*[2**k+delta for k in range(n.bit_length()) for delta in (-1,0,1) if 0<2**k+delta<n]}):
   for x in sorted({0,1,n//4,n//2,max(0,n//2-gap),n-gap-1}):
    if x+gap>=n:continue
    for a,b in ((1,1),(1,2),(2,1),(1,7),(7,1)):
     for kind in ('keys','gaps','mixed'):
      first=x if kind!='gaps' else n+x
      second=x+gap if kind=='keys' else n+x+gap
      add(((first,a),(second,b)),'structured-pair')
  for _ in range(150):
   size=rng.randrange(2,9);indices=rng.sample(range(2*n+1),size)
   add([(x,rng.randrange(1,9)) for x in indices],'random-sparse')
  best_n=None
  for w,label in cases:
   proc.stdin.write(str(n)+' '+' '.join(map(str,w))+'\n');proc.stdin.flush();row=json.loads(proc.stdout.readline())
   assert row['weights']==w;counts=row['counts'];evaluations+=1
   if best_n is None or score(row)>score(best_n):best_n=row.copy();best_n['family']=label
   if winner is None or score(row)>best:
    best=score(row);winner=row.copy();winner['family']=label
  rows.append(best_n)
  print(n,'inputs',len(cases),'max',str(score(best_n)),'overall',str(best),flush=True)
 proc.stdin.close();assert proc.wait()==0
 # Independent all-root checks of every retained size winner through 64 keys.
 for row in rows:
  n=row['n']
  if n>64:continue
  w=row['weights'];h=row['h'];d=row['d'];a=profile(w,stats)[h-1];unit=0
  for x,v in enumerate(w):
   if v:
    e=[0]*(2*n+1);e[x]=1;unit+=v*profile(e,stats)[h-1]['tail'][d]
  assert row['mass']==a['tail'][d] and row['unit_mass']==unit
  stats['winner_controls']+=1
 files=('sparse_interaction_search.py','core_interaction_search.cpp','capacity_interaction.py','aggregate_core_audit.py')
 result=dict(scope='Sparse-input falsification of the unproved all-width hW interaction allowance; finite outcomes do not prove a bound.',
 evaluated_inputs=evaluations,maximum_ratio=[best.numerator,best.denominator],winner=winner,rows=rows,
 counts_including_unit_profiles=counts,independent_checks=stats,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/sparse_interaction_search.json').write_text(json.dumps(result,indent=2)+'\n');print('complete',evaluations,str(best),flush=True)
if __name__=='__main__':main()
