#!/usr/bin/env python3
"""Adversarial fixed-mass search for the unproved all-band interaction bound."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random,subprocess,sys
from capacity_interaction import profile


def ratio(row):return Fraction(row['excess'],row['denominator'])


def main():
 root=Path(__file__).resolve().parents[1];binary=sys.argv[1];rng=random.Random(32220)
 proc=subprocess.Popen([binary],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 rows=[];stats=Counter();search_counts=Counter();structured_counts={}
 for n in (2,3,4,5,7,8,16,32,64,128,256):
  basis=[]
  if n<=8:
   for x in range(2*n+1):
    w=[0]*(2*n+1);w[x]=1;basis.append(profile(w,stats))
  fixtures=[('uniform-mixed',[1]*(2*n+1)),('uniform-key',[1]*n+[0]*(n+1)),
            ('uniform-gap',[0]*n+[1]*(n+1)),
            ('alternating-mixed',[1+int(i%2==0) for i in range(n)]+[1]*(n+1))]
  for shift in (0,n//4,n//2):
   for length in (1,max(1,n//8),max(1,n//2)):
    w=[0]*(2*n+1)
    for i in range(shift,min(n,shift+length)):w[i]=2*(i-shift)+1
    fixtures.append(('odd-ramp',w))
  for _ in range(12 if n<=8 else 4):fixtures.append(('random',[rng.randrange(8) for _ in range(2*n+1)]))
  for label,w in fixtures:
   proc.stdin.write(str(n)+' '+' '.join(map(str,w))+'\n');proc.stdin.flush()
   row=json.loads(proc.stdout.readline());assert row['weights']==w;structured_counts=row['counts']
   if n<=8:
    ref=profile(w,stats);best=Fraction(0)
    for h,a in enumerate(ref,1):
     for d in range(1,n+1):
      unit=sum(v*basis[x][h-1]['tail'][d] for x,v in enumerate(w))
      r=Fraction(a['tail'][d]-unit,h*sum(w)) if sum(w) else Fraction(0)
      best=max(best,r)
    assert best==ratio(row),(n,w,best,row)
    if best:
     h=row['h'];d=row['d'];a=ref[h-1]
     assert row['mass']==a['tail'][d]
     assert row['full_excess']==a['full']-sum(v*basis[x][h-1]['full'] for x,v in enumerate(w))
    stats['optimized_vectors']+=1
   row['family']=label;rows.append(row)
  print('structured',n,'max',str(max(map(ratio,rows))),flush=True)
 proc.stdin.close();assert proc.wait()==0
 for n in (16,32,64,128,256):
  for mode in (0,1,2):
   seed=32221+n+mode;steps=1200
   row=json.loads(subprocess.check_output([binary,str(n),str(steps),str(seed),str(mode)],text=True))
   assert sum(row['weights'])==n;row.update(family='search',seed=seed,steps=steps,start_mode=mode)
   rows.append(row);search_counts.update(row['counts'])
   print('search',n,mode,'max',str(ratio(row)),flush=True)
 winner=max(rows,key=ratio)
 result=dict(scope='Falsification search only: T_d(w)<=sum_x w_x*T_d(e_x)+hW remains unproved for d>1.',
 objective='maximize (tail mass minus sum of weighted unit-input tail masses)/(hW) over all early layers and every band width',
 maximum_ratio=[ratio(winner).numerator,ratio(winner).denominator],winner=winner,checks=stats,
 structured_counts=structured_counts,search_counts=search_counts,rows=rows,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in
 ('core_interaction_search.cpp','core_interaction_search.py','capacity_interaction.py','aggregate_core_audit.py')})
 (root/'results/core_interaction_search.json').write_text(json.dumps(result,indent=2)+'\n')
 print('final',result['maximum_ratio'],dict(stats),flush=True)
if __name__=='__main__':main()
