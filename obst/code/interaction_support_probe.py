#!/usr/bin/env python3
"""Search support outside every unit-outcome dyadic diagonal."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,subprocess,sys
from aggregate_core_audit import layers,partition
from unit_support_envelope import envelope

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[];best=None;last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(w):
  nonlocal best,last
  n=(len(w)-1)//2;proc.stdin.write(' '.join(map(str,[n,*w]))+'\n');proc.stdin.flush();last=json.loads(proc.stdout.readline())
  r=last['winner'];ratio=Fraction(r['core'],r['denominator']);row=dict(n=n,weights=w,ratio=[ratio.numerator,ratio.denominator],winner=r)
  if best is None or ratio>Fraction(*best['ratio']):best=row;print('best',n,row['ratio'],r,flush=True)
  return row
 for n in (32,64,128,256,512,1024,2048):
  for mode in ('keys','gaps','mixed'):
   local=None
   for gap in sorted(set(x for x in (1,2,3,4,5,7,9,15,17,31,33,int(n**.5),n//8,n//4) if x<n//2)):
    for shift in (-1,0,1):
     y=n//2+shift;x=y-gap;w=[0]*(2*n+1)
     if mode=='keys':w[x]=w[y]=1
     elif mode=='gaps':w[n+x]=w[n+y]=1
     else:w[x]=w[n+y]=1
     row=evaluate(w);row.update(mode=mode,separation=gap,shift=shift)
     if local is None or Fraction(*row['ratio'])>Fraction(*local['ratio']):local=row
   rows.append(local);print('done',n,mode,local['ratio'],local['separation'],local['shift'],flush=True)
 for row in rows:
  if row['n']>64:continue
  n=row['n'];w=row['weights'];win=row['winner'];h=win['h']
  if not h:continue
  A=list(layers(w[:n],w[n:],h,(n+1)*sum(w)+1,stats))[-1];a,b,s=win['a'],win['b'],win['s'] if 's' in win else win['side']
  assert (a,b) in partition(n,2**h-1)[0][s]
  count=sum(A[i][j+1]+A[i+1][j]>A[i][j]+A[i+1][j+1] for i in range(a,a+s) for j in range(b,b+s) if not envelope(i,j,h))
  assert count==win['core'];stats['independent_winner_tiles']+=1
 proc.stdin.close();assert proc.wait()==0
 files=('interaction_support_probe.py','interaction_support_probe.cpp','unit_support_envelope.py','aggregate_core_audit.py')
 out=dict(scope='Two-outcome probe of positive ordinary densities outside the proved unit-outcome envelope. Ratios to local mass are diagnostic only.',rows=rows,winner=best,checks=stats,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/interaction_support_probe.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
