#!/usr/bin/env python3
"""Structured adversaries and all-band exact controls; no upper-bound certification."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random,subprocess,sys
from aggregate_core_audit import layers


def reference(w,checks):
 n=(len(w)-1)//2;L=n.bit_length();W=sum(w);M=(L+2)*W+1;result=[]
 for h,A in enumerate(layers(w[:n],w[n:],L-1,M,checks)):
  if not h:continue
  c=2**h-1;mass=[0]*(n+1);support=[0]*(n+1)
  for i in range(n):
   for j in range(i+1,n):
    v=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert v>=0
    d=abs(j-i-c)
    if d:mass[d]+=v;support[d]+=v>0
  for d in range(n-1,0,-1):mass[d]+=mass[d+1];support[d]+=support[d+1]
  best=dict(h=h,c=c,d=1,mass=0,support=0,numerator=0,denominator=1);value=Fraction(0)
  for d in range(1,n+1):
   num=mass[d]*d;den=W*(L*d+c) if W else 1;ratio=Fraction(num,den)
   if ratio>value:best=dict(h=h,c=c,d=d,mass=mass[d],support=support[d],numerator=num,denominator=den);value=ratio
  result.append(best)
 checks['vectors']+=1;return result


def patterns(n):
 for pos in (0,n//2,n//2+1,n-1):
  w=[0]*(2*n+1);w[pos]=1;yield 'single_key_'+str(pos),w
 rng=random.Random(31119+n)
 yield 'near_uniform',[100+rng.randrange(4) for _ in range(2*n+1)]
 yield 'geometric_mixed',[1<<rng.randrange(16) for _ in range(2*n+1)]
 for distance in sorted(set([1,2,3,4,max(1,n//8),n//4,n//2])):
  for mode in ('keys','gaps','mixed'):
   w=[0]*(2*n+1)
   for t in range(0,n,distance):
    pos=t if mode=='keys' or mode=='mixed' and (t//distance)%2 else n+t
    w[pos]=1
   yield mode+'_comb_'+str(distance),w
 for m in (2,4,8,16):
  if m>n:continue
  for values in ('equal','ramp','geometric','ruler'):
   for spacing in ('cluster','spread'):
    w=[0]*(2*n+1)
    for t in range(m):
     i=(n-m)//2+t if spacing=='cluster' else (t+1)*n//(m+1)
     w[i]=1 if values=='equal' else 2*t+1 if values=='ramp' else 1<<t if values=='geometric' else ((t+1)&-(t+1)).bit_length()
    yield values+'_'+spacing+'_'+str(m),w
 for position in (n//4,n//2,3*n//4):
  for a,b in ((1,1),(1,16),(16,1),(1,256)):
   w=[0]*(2*n+1);w[position]=a;w[min(n-1,position+max(1,n//8))]=b
   yield 'two_keys_'+str((position,a,b)),w
 yield 'uniform',[1]*(2*n+1)
 yield 'positive_alternating',[1+int(i%2==0) for i in range(n)]+[1]*(n+1)


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(31119);checks=Counter();rows=[]
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 best=Fraction(0);winner=None
 def record(row,name,audit):
  nonlocal best,winner
  row['family']=name
  if audit:assert row['layers']==reference(row['weights'],checks)
  r=row['winner'];value=Fraction(r['numerator'],r['denominator'])
  if winner is None or value>best:best=value;winner=row
  rows.append(row)
 for n in (2,3,4,5,8,15,16,31,32,63,64,127,128,255,256,512,1024):
  fixtures=list(patterns(n)) if n>=16 else [('random',[rng.randrange(8) for _ in range(2*n+1)]) for t in range(10)]
  for name,w in fixtures:
   proc.stdin.write(' '.join(map(str,[n,*w]))+'\n');proc.stdin.flush();row=json.loads(proc.stdout.readline());record(row,name,n<=16)
  print(n,'best',str(best),winner['family'],winner['winner'],flush=True)
 proc.stdin.close();assert proc.wait()==0
 structured_counts=rows[-1]['counts'];search_counts=Counter()
 for n in (16,32,64,128,256,512):
  for start in range(3):
   seed=31119+10*n+start;steps=max(200,1000*min(64,n)//n)
   row=json.loads(subprocess.check_output([sys.argv[1],str(n),str(steps),str(seed)],text=True))
   row.update(seed=seed,steps=steps);search_counts.update(row['counts']);record(row,'fixed_mass_search',n<=32)
   print('search',n,start,str(best),flush=True)
 files=['core_tail_search.cpp','core_tail_search.py','aggregate_core_audit.py']
 report=dict(scope='Diagnostic only: no universal tail bound follows from finite search.',
 objective='max over every early layer and every integer d>=1 of outside mass / (W*(L+c/d))',
 maximum_ratio=[best.numerator,best.denominator],winner=winner,checks=checks,structured_counts=structured_counts,search_counts=search_counts,rows=rows,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/core_tail_search.json').write_text(json.dumps(report,indent=2)+'\n');print(dict(checks),flush=True)
if __name__=='__main__':main()
