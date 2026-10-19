#!/usr/bin/env python3
"""Probe sparse repeated clusters for multi-level amplification of total tails."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,subprocess,sys
from capacity_interaction import profile


def score(r):return Fraction(r['winner']['numerator'],r['winner']['denominator'])


def main():
 root=Path(__file__).resolve().parents[1];proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 rows=[];stats=Counter();count=0;last={}
 for n in (64,128,256,512,1024,2048):
  best=None;seen=set();cases=0
  for D in (2,4,8,16,32,64):
   for step in (D-1,D+1):
    for m in sorted({max(2,D//2),D,2*D}):
     span=(m-1)*step+1
     if span>n:continue
     for shift in (0,1):
      start=(n-span)//2+shift
      if start+span>n:continue
      for kind in ('keys','mixed'):
       w=[0]*(2*n+1)
       for k in range(m):
        x=start+k*step;w[x if kind=='keys' or k%2==0 else n+x]=1
       key=tuple(w)
       if key in seen:continue
       seen.add(key);proc.stdin.write(str(n)+' '+' '.join(map(str,w))+'\n');proc.stdin.flush()
       row=json.loads(proc.stdout.readline());last=row['counts'];count+=1;cases+=1
       row.update(cluster=dict(D=D,step=step,m=m,start=start,kind=kind))
       if best is None or score(row)>score(best):best=row
  rows.append(best);print(n,cases,'max',str(score(best)),best['cluster'],best['winner'],flush=True)
 proc.stdin.close();assert proc.wait()==0
 for row in rows:
  if row['n']<=128:
   h=row['winner']['h'];d=row['winner']['d'];a=profile(row['weights'],stats)[h-1]
   assert a['tail'][d]==row['winner']['mass'];stats['winner_controls']+=1
 win=max(rows,key=score);r=score(win)
 files=('cluster_tail_search.py','core_tail_search.cpp','capacity_interaction.py','aggregate_core_audit.py')
 result=dict(scope='Repeated sparse-cluster diagnostic of O(W(L+c/d)); no upper-bound or asymptotic claim from finite maxima.',
 evaluated_inputs=count,maximum_ratio=[r.numerator,r.denominator],winner=win,rows=rows,optimized_counts=last,independent_checks=stats,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/cluster_tail_search.json').write_text(json.dumps(result,indent=2)+'\n');print('complete',count,str(r),flush=True)
if __name__=='__main__':main()
