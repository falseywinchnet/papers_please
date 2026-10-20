#!/usr/bin/env python3
"""Probe fixed tiles whose endpoints cut replicated positive blocks."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,random,subprocess,sys
from aggregate_core_audit import layers

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(42131);stats=Counter();rows=[];last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(s,p,tag):
  nonlocal last
  n=8*s;h=s.bit_length()+1;w=p+[0]*(n+1)
  proc.stdin.write(' '.join(map(str,[n,h,0,5*s,s,*w]))+'\n');proc.stdin.flush();last=json.loads(proc.stdout.readline())
  return dict(s=s,n=n,h=h,kind=tag,p=p,**last,ratio=[last['core'],s+last['mass']])
 for s in (8,16,32,64,128):
  best=None;structured=[]
  def retain(row):
   nonlocal best
   if best is None or Fraction(*row['ratio'])>Fraction(*best['ratio']):best=row
  for base in (2,4,8):
   d=s//base
   for k in range(24):
    coarse=[0]*(8*base)
    for j in range(6*base):coarse[j]=(rng.randrange(2) if k<12 else rng.randrange(4))
    coarse[rng.randrange(base)]=1;coarse[rng.randrange(5*base,6*base)]=1
    p=[x for x in coarse for _ in range(d)]
    row=evaluate(s,p,f'replicated:{base}:{k}');retain(row)
    if k in (0,12):structured.append(row)
  p=best['p'].copy();current=Fraction(*best['ratio'])
  for it in range(400 if s<=32 else 200):
   q=p.copy();active=[j for j,x in enumerate(q) if x];x=rng.randrange(6*s);action=rng.randrange(4)
   if action==0 or not active:q[x]+=1
   elif action==1:q[rng.choice(active)]-=1
   elif action==2:
    y=rng.choice(active);q[y]-=1;q[x]+=1
   else:
    y=rng.choice(active);q[x]+=q[y];q[y]=0
   row=evaluate(s,q,'mutation');retain(row);r=Fraction(*row['ratio'])
   if r>=current or rng.random()<0.03:p=q;current=r
   if it%100==99:p=best['p'].copy();current=Fraction(*best['ratio'])
  rows.append(dict(s=s,best=best,structured=structured));print(s,best['ratio'],flush=True)
 for block in rows:
  if block['s']>16:continue
  for row in [block['best'],*block['structured']]:
   p=row['p'];n=len(p);s=row['s'];h=row['h'];A=list(layers(p,[0]*(n+1),h,(n+1)*sum(p)+1,stats))[-1]
   ds=[A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1] for i in range(s) for j in range(5*s,6*s)]
   assert sum(x>0 for x in ds)==row['core'] and sum(ds)==row['density_mass'];stats['independent_tiles']+=1
 proc.stdin.close();assert proc.wait()==0
 files=('endpoint_amplification_probe.py','pair_amplification_probe.cpp','aggregate_core_audit.py')
 out=dict(scope='Endpoint-cut and unequal-weight block amplification search; finite ratios are not upper-bound proofs.',seed=42131,rows=rows,compiled_counts=last['counts'],checks=stats,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/endpoint_amplification_probe.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
