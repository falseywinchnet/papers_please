#!/usr/bin/env python3
"""Exact sparse-rank family and clipped-ruler comparison, diagnostic stage."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import hashlib,json,subprocess,sys

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[];last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def evaluate(p,v,d):
  nonlocal last
  proc.stdin.write(' '.join(map(str,[len(p),len(v),*p,*v]))+'\n');proc.stdin.flush();last=json.loads(proc.stdout.readline())
  return last['tails'][d-1]
 for d in (1,2,3,4,5,8,12):
  for m in (2,3,4,7):
   g=2*d;C=(m+1)*g;n=2*C;c=C-1;x=C-3*d;y=C
   p=[int(i+1 in (x,y)) for i in range(n)]
   v=[int((r+1)%g==0) for r in range(c)]
   tail=evaluate(p,v,d);assert tail==m-1
   rows.append(dict(kind='spaced',d=d,m=m,n=n,c=c,tail=tail));stats['spaced_generic_controls']+=1
 for t in (2,3,4):
  d=2**(t-1)
  for h in (t+1,t+2,t+3):
   C=2**h;c=C-1;n=2*C;x=C-3*d;y=C
   p=[int(i+1 in (x,y)) for i in range(n)]
   ruler=[((r+1)&-(r+1)).bit_length()-1 for r in range(c)]
   tails=[]
   for clip in (t-1,t,h-1):tails.append(evaluate(p,[min(clip,v) for v in ruler],d))
   row=dict(kind='clipped',t=t,h=h,d=d,m=C//(2*d)-1,n=n,tails=tails,increment=tails[1]-tails[0]);rows.append(row)
   print(row,flush=True)
 proc.stdin.close();assert proc.wait()==0
 files=('spaced_rank_tail.py','template_tail_probe.cpp')
 out=dict(scope='Exact spaced-rank family and exploratory clipping increments; generic subsequence controls only.',rows=rows,checks=stats,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/spaced_rank_tail.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
