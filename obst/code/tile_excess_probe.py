#!/usr/bin/env python3
"""Maximize local support minus input mass; evidence, never an upper-bound proof."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,math,random,subprocess,sys
from aggregate_core_audit import layers,partition

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(521019);rows=[];stats=Counter();last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(h,s,above,w):
  nonlocal last
  proc.stdin.write(' '.join(map(str,[h,s,above,*w]))+'\n');proc.stdin.flush();last=json.loads(proc.stdout.readline())
  return dict(h=h,side=s,above=bool(above),weights=w.copy(),**last)
 def metric(row):return row['core']-row['mass']
 for h,s,steps in [(5,4,700),(5,8,700),(6,8,700),(6,16,700),(7,8,500),(7,16,500),(7,32,500),(8,16,350),(8,32,350),(8,64,350),(9,32,180),(9,64,180)]:
  for above in (0,1):
   C=2**h;b=C+s if above else C-2*s;n=b+s
   for mode in ('keys','gaps','mixed'):
    pos=list(range(n)) if mode=='keys' else list(range(n,2*n+1)) if mode=='gaps' else list(range(2*n+1))
    fixtures=[]
    for kind in range(6):
     w=[0]*(2*n+1)
     if kind<2:
      for _ in range(s*(kind+1)):w[rng.choice(pos)]+=1
     elif kind==2:
      m=max(2,int(math.sqrt(s)));a=n//2-m//2
      for j in range(m):w[(n if mode=='gaps' else 0)+a+j]=2*j+1
     elif kind==3:
      for i in pos:w[i]=int(i%2==0)
     elif kind==4:
      for j in range(s):w[(n if mode=='gaps' else 0)+n//2-s//2+j]=1
     else:
      for _ in range(max(2,s//4)):w[rng.choice(pos)]+=rng.randrange(1,5)
     fixtures.append(w)
    candidates=[evaluate(h,s,above,w) for w in fixtures];best=max(candidates,key=metric);current=best;w=best['weights'].copy()
    for it in range(steps):
     v=w.copy();active=[x for x in pos if v[x]];act=rng.randrange(12)
     if act<3 or not active:v[rng.choice(pos)]+=1
     elif act<6:v[rng.choice(active)]-=1
     elif act<10:
      x=rng.choice(active);y=(x+rng.choice([-s,-2,-1,1,2,s])) if rng.random()<.7 else rng.choice(pos)
      if y not in pos:y=rng.choice(pos)
      v[x]-=1;v[y]+=1
     elif act==10:
      x=rng.choice(active);v[x]=0
     else:
      x=rng.choice(active);y=rng.choice(pos);v[x],v[y]=v[y],v[x]
     row=evaluate(h,s,above,v);delta=metric(row)-metric(current);temperature=.3+1.7*(1-(it%100)/100)
     if delta>=0 or rng.random()<math.exp(delta/temperature):w=v;current=row
     if (metric(row),row['core'])>(metric(best),best['core']):best=row
     if it%100==99:w=best['weights'].copy();current=best
    best['mode']=mode;best.pop('counts');best['excess']=metric(best);best['excess_over_side']=[best['excess'],s];rows.append(best)
    print('winner',h,s,above,mode,best['core'],best['mass'],'excess',best['excess'],flush=True)
 proc.stdin.close();assert proc.wait()==0
 # Independent all-root checks of every small winner, including literal tile support.
 for row in rows:
  h,s,above=row['h'],row['side'],row['above'];C=2**h;b=C+s if above else C-2*s;n=b+s
  if n>96:continue
  w=row['weights'];p,q=w[:n],w[n:];A=list(layers(p,q,h,(h+2)*sum(w)+1,stats))[-1]
  ds=[A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1] for i in range(s) for j in range(b,b+s)]
  assert sum(x>0 for x in ds)==row['core'];assert sum(ds)==row['density_mass'];assert sum(w)==row['mass']
  N=1<<(n-1).bit_length();assert (0,b) in partition(N,C-1)[0][s];stats['independent_winner_tiles']+=1
 files=['tile_excess_probe.py','tile_excess_probe.cpp','aggregate_core_audit.py']
 out=dict(scope='Fixed accepted tiles, variable integer mass; objective core minus mass. Finite outcomes do not prove a uniform local bound.',seed=521019,rows=rows,compiled_counts=last['counts'],independent_counts=stats,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/tile_excess_probe.json').write_text(json.dumps(out,indent=2)+'\n')
 print('independent',dict(stats),flush=True)
if __name__=='__main__':main()
