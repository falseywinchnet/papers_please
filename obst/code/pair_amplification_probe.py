#!/usr/bin/env python3
"""Try to amplify the two-key interaction in its fixed maximal tile."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,random,subprocess,sys
from aggregate_core_audit import layers,partition
from unit_support_envelope import envelope

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(41017)
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 rows=[];stats=Counter();last=None
 def evaluate(s,p,tag):
  nonlocal last
  n=8*s;h=s.bit_length()+1;w=p+[0]*(n+1)
  proc.stdin.write(' '.join(map(str,[n,h,0,5*s,s,*w]))+'\n');proc.stdin.flush()
  last=json.loads(proc.stdout.readline())
  return dict(s=s,n=n,h=h,kind=tag,weights=w,**last,ratio=[last['core'],s+last['mass']])
 for s in (8,16,32,64,128):
  n=8*s;best=None;offbest=None;structured=[]
  def retain(row):
   nonlocal best,offbest
   if best is None or Fraction(*row['ratio'])>Fraction(*best['ratio']):best=row
   if offbest is None or Fraction(row['off_core'],s+row['mass'])>Fraction(offbest['off_core'],s+offbest['mass']):offbest=row
  for m in sorted(set([1,2,3,4,max(1,s//8),s//4,s//2,s])):
   for kind in ('paired_block','paired_spread','shared_endpoint','weighted_left','weighted_right'):
    p=[0]*n
    for k in range(m):
     shift=k if kind!='paired_spread' else k*s//m
     x=3*s+2+shift;y=4*s+1+shift
     if kind=='shared_endpoint':y=4*s+1
     p[x]+=k+1 if kind=='weighted_left' else 1
     p[y]+=m-k if kind=='weighted_right' else 1
    row=evaluate(s,p,f'{kind}:{m}');structured.append(row);retain(row)
  # Mutations remain in the region occupied by the paired clusters.
  w=best['weights'][:n];current=Fraction(*best['ratio'])
  for it in range(600 if s<=32 else 250):
   p=w.copy();active=[i for i,x in enumerate(p) if x]
   a=rng.randrange(3*s,5*s);act=rng.randrange(4)
   if not active or act==0:p[a]+=1
   elif act==1:p[rng.choice(active)]-=1
   elif act==2:
    b=rng.choice(active);p[b]-=1;p[a]+=1
   else:
    b=rng.choice(active);p[a]+=p[b];p[b]=0
   row=evaluate(s,p,'mutation');retain(row);ratio=Fraction(*row['ratio'])
   if ratio>=current or rng.random()<0.03:w=p;current=ratio
   if it%100==99:w=best['weights'][:n];current=Fraction(*best['ratio'])
  rows.append(dict(s=s,structured=structured,best=best,offbest=offbest))
  print(s,best['ratio'],best['core'],best['mass'],offbest['off_core'],flush=True)
 # Small all-root checks use neither monotone roots nor prefix support sums.
 for block in rows:
  if block['s']>16:continue
  for row in (block['best'],block['offbest'],block['structured'][0]):
   n=row['n'];s=row['s'];h=row['h'];w=row['weights']
   A=list(layers(w[:n],w[n:],h,(n+1)*sum(w)+1,stats))[-1]
   assert (0,5*s) in partition(n,2**h-1)[0][s]
   ds=[(i,j,A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]) for i in range(s) for j in range(5*s,6*s)]
   assert sum(d>0 for i,j,d in ds)==row['core']
   assert sum(d>0 and not envelope(i,j,h) for i,j,d in ds)==row['off_core']
   assert sum(d for i,j,d in ds)==row['density_mass'];stats['independent_tiles']+=1
 proc.stdin.close();assert proc.wait()==0
 files=('pair_amplification_probe.cpp','pair_amplification_probe.py','aggregate_core_audit.py','unit_support_envelope.py')
 result=dict(scope='Fixed-tile pair amplification falsification; ratios are finite observations, not a general support bound.',seed=41017,rows=rows,checks=stats,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/pair_amplification_probe.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
