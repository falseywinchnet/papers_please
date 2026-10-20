#!/usr/bin/env python3
"""Search local tile support divided by side plus inclusive outcome mass."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random,subprocess,sys
from aggregate_core_audit import layers,partition


def independent(p,q,stats):
 n=len(p);N=1<<(n-1).bit_length();L=n.bit_length();W=sum(p)+sum(q);p=p+[0]*(N-n);q=q+[0]*(N-n);M=(N+1)*W+1;out=[]
 for h,A in enumerate(layers(p,q,L-1,M,stats)):
  if not h:continue
  ts,_=partition(N,2**h-1);best=Fraction(0)
  for s,anchors in ts.items():
   for a,b in anchors:
    core=sum(A[i][j+1]+A[i+1][j]>A[i][j]+A[i+1][j+1] for i in range(a,a+s) for j in range(b,b+s))
    mass=sum(p[a:b+s])+sum(q[a:b+s+1]);best=max(best,Fraction(core,s+mass));stats['independent_tiles']+=1
  out.append(best)
 return out


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(38117);stats=Counter();best=None;rows=[];last=None
 engine=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(w,control=False):
  nonlocal last,best
  n=(len(w)-1)//2;engine.stdin.write(str(n)+'\n'+' '.join(map(str,w))+'\n');engine.stdin.flush();last=json.loads(engine.stdout.readline());r=last['winner'];ratio=Fraction(r['core'],r['denominator']);row=dict(n=n,W=sum(w),weights=w.copy(),winner=r,ratio=[ratio.numerator,ratio.denominator])
  if control:
   assert independent(w[:n],w[n:],stats)==[Fraction(a['core'],a['denominator']) for a in last['layers']];stats['independent_inputs']+=1
  if best is None or ratio>Fraction(*best['ratio']):best=row;print('new best',n,row['ratio'],r,flush=True)
  return ratio,row
 for n in (8,15,16,31,32,63,64,127,128,255,256,511,512,1024):
  fixtures=[]
  for gap in (False,True):
   for x in (n//4,n//2,n//2+1):
    w=[0]*(2*n+1);w[(n if gap else 0)+x]=1;fixtures.append(w)
  for mode in range(6):
   w=[0]*(2*n+1)
   for i in range(n):
    if mode==0:w[i]=w[n+i]=1
    elif mode==1:w[i]=i%2
    elif mode==2:w[n+i]=i%2
    elif mode==3:w[i]=int(i%3==0)
    elif mode==4:w[i]=int(i%5==0)
    else:w[n+i]=int(i%3==0)
   fixtures.append(w)
  m=1<<(n.bit_length()//2-1);w=[0]*(2*n+1)
  for i in range(m):w[(n-m)//2+i]=2*i+1
  fixtures.append(w)
  for target in (max(1,n//8),n//2,n,2*n):
   for _ in range(4):
    w=[0]*(2*n+1);positions=list(range(2*n+1)) if _<2 else rng.sample(range(2*n+1),max(1,int(target**.5)))
    for _ in range(target):w[rng.choice(positions)]+=1
    fixtures.append(w)
  local=None
  for w in fixtures:
   rr,row=evaluate(w,n<=16)
   if local is None or rr>Fraction(*local['ratio']):local=row
  rows.append(dict(mode='structured',**local))
 for n,steps in ((32,1500),(64,2000),(128,2000),(256,1000),(512,500)):
  for mode in ('mixed','keys','gaps'):
   choices=list(range(2*n+1)) if mode=='mixed' else (list(range(n)) if mode=='keys' else list(range(n,2*n+1)))
   w=[0]*(2*n+1)
   for _ in range(n):w[rng.choice(choices)]+=1
   rr,local=evaluate(w);current=rr
   for it in range(steps):
    q=w.copy();a=rng.choice([i for i,v in enumerate(q) if v]);b=rng.choice(choices);q[a]-=1;q[b]+=1
    r,row=evaluate(q)
    if r>=current or rng.random()<0.025:w=q;current=r
    if r>Fraction(*local['ratio']):local=row
    if it%250==249:w=local['weights'].copy();current=Fraction(*local['ratio'])
   evaluate(local['weights'],n<=64);rows.append(dict(mode=mode,**local));print('search complete',n,mode,local['ratio'],flush=True)
 engine.stdin.close();assert engine.wait()==0
 files=('tile_boundary_probe.cpp','tile_boundary_probe.py','aggregate_core_audit.py')
 out=dict(scope='Falsification search for K_tile=O(side+inclusive outcome mass), with exact positive-density support. No upper bound inferred from finite ratios.',seed=38117,checks=stats,compiled_counts=last['counts'],winner=best,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/tile_boundary_probe.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
