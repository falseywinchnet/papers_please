#!/usr/bin/env python3
"""Falsification probe: density mass outside a capacity band, full mixed weights."""
from collections import Counter
from pathlib import Path
from fractions import Fraction
import hashlib,json,random


def evaluate(p,q,stats,all_roots=False):
 n=len(p);W=sum(p)+sum(q);L=n.bit_length();M=(L+2)*W+1
 pre=[0]
 for a,b in zip(p,q[1:]):pre.append(pre[-1]+a+b)
 old=[[M*max(j-i,0) for j in range(n+1)] for i in range(n+1)]
 rows=[];best=Fraction(0);winner=None
 for h in range(1,L):
  c=2**h-1;cur=[[0]*(n+1) for _ in range(n+1)];roots=[[0]*(n+1) for _ in range(n+1)]
  for k in range(1,n+1):
   for i in range(n-k+1):
    j=i+k;lo=i if all_roots or k==1 else roots[i][j-1];hi=j-1 if all_roots or k==1 else roots[i+1][j]
    value,r=min((old[i][r]+old[r+1][j],r) for r in range(lo,hi+1))
    cur[i][j]=value+pre[j]-pre[i]+q[i];roots[i][j]=r
    stats['states']+=1;stats['root_candidates']+=hi-lo+1
  mass=[0]*(n+1);support=[0]*(n+1)
  for i in range(n):
   for j in range(i+1,n):
    delta=cur[i][j+1]+cur[i+1][j]-cur[i][j]-cur[i+1][j+1]
    assert delta>=0;stats['density_checks']+=1
    if j-i!=c:mass[abs(j-i-c)]+=delta;support[abs(j-i-c)]+=delta>0
  for d in range(n-1,0,-1):mass[d]+=mass[d+1];support[d]+=support[d+1]
  for d in sorted(set([1,c,max(1,c//2),*range(1,min(c+1,17)),*[2**t for t in range(L)]])):
   if d>n:continue
   ratio=Fraction(mass[d]*d,W*(L*d+c)) if W else Fraction(0)
   row=dict(h=h,c=c,d=d,mass=mass[d],support=support[d],ratio=[ratio.numerator,ratio.denominator])
   rows.append(row)
   if ratio>best:best=ratio;winner=row
  old=cur
 stats['evaluations']+=1
 return best,dict(n=n,W=W,p=p,q=q,maximum_ratio=[best.numerator,best.denominator],winner=winner,rows=rows)


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(30119);rows=[];best=Fraction(0);winner=None
 def check(name,p,q):
  nonlocal best,winner
  value,row=evaluate(p,q,stats)
  if len(p)<=16:
   _,ref=evaluate(p,q,stats,True);assert row==ref;stats['all_root_controls']+=1
  row['family']=name;rows.append(row)
  if value>best:best=value;winner=row
 for n in (4,7,8,15,16,31,32,63,64,127,128,255,256):
  fixtures=[]
  for pos in sorted(set((0,n//4,n//2,n-1))):
   p=[0]*n;p[pos]=1;fixtures.append(('single_key',p,[0]*(n+1)))
   q=[0]*(n+1);q[pos]=1;fixtures.append(('single_gap',[0]*n,q))
  fixtures.extend([('uniform',[1]*n,[1]*(n+1)),('alternating_keys',[int(i%2==0) for i in range(n)],[0]*(n+1)),
    ('positive_alternating',[1+int(i%2==0) for i in range(n)],[1]*(n+1)),
    ('odd_ramp',[2*i+1 for i in range(n)],[0]*(n+1))])
  m=max(1,int(n**.5));p=[0]*n
  for i in range(m):p[(n-m)//2+i]=2*i+1
  fixtures.append(('centered_odd_ramp',p,[0]*(n+1)))
  for t in range(8):
   w=[0]*(2*n+1)
   for _ in range(n):w[rng.randrange(len(w))]+=1
   fixtures.append(('random_units',w[:n],w[n:]))
  for name,p,q in fixtures:check(name,p,q)
  print(n,'max ratio',str(best),winner['winner'],flush=True)
 for n in (16,32,64):
  w=[0]*(2*n+1)
  for _ in range(n):w[rng.randrange(len(w))]+=1
  value,current=evaluate(w[:n],w[n:],stats)
  for t in range(200):
   nxt=w[:];a=rng.choice([i for i,x in enumerate(nxt) if x]);b=rng.randrange(len(w));nxt[a]-=1;nxt[b]+=1
   val,row=evaluate(nxt[:n],nxt[n:],stats)
   if val>=value:w=nxt;value=val;current=row
   if val>best:best=val;winner=row
  current['family']='fixed_mass_search';rows.append(current)
  print('search',n,str(best),flush=True)
 report=dict(scope='Falsification and direction only; no upper-bound theorem claimed.',
  tested_expression='outside mass / (W*(L+c/d)); outside means |j-i-c|>=d, excluding capacity line',
  counts=stats,maximum_ratio=[best.numerator,best.denominator],winner=winner,rows=rows,
  source_sha256={'core_tail_probe.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 (root/'results/core_tail_probe.json').write_text(json.dumps(report,indent=2)+'\n')
 print(dict(stats),flush=True)
if __name__=='__main__':main()
