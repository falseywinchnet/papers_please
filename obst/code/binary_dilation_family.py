#!/usr/bin/env python3
"""Large original-layer support controls for replicated binary patterns."""
from pathlib import Path
import hashlib,json,subprocess,sys

def main():
 root=Path(__file__).resolve().parents[1];rows=[];last=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 for s in (8,16,32):
  n=8*s
  patterns={'pair':[int(i in (3*s+2,4*s+1)) for i in range(n)],
   'alternating':[int(3*s<=i<5*s and i%2==0) for i in range(n)],
   'three_blocks':[int(any(a<=i<a+max(1,s//4) for a in (3*s+1,4*s,5*s-s//4))) for i in range(n)]}
  for name,p in patterns.items():
   base=None
   for d in (1,2,4):
    N=d*n;side=d*s;h=side.bit_length()+1;fine=[x for x in p for _ in range(d)]
    w=fine+[0]*(N+1)
    proc.stdin.write(' '.join(map(str,[N,h,0,5*side,side,*w]))+'\n');proc.stdin.flush();last=json.loads(proc.stdout.readline())
    if base is None:base=last
    assert last['core']==base['core'] and last['density_mass']==base['density_mass']
    assert last['mass']==d*base['mass']
    if d>1:assert last['off_core']==last['core']
    rows.append(dict(coarse_s=s,n=N,d=d,pattern=name,coarse_p=p,**last))
   print(s,name,base['core'],base['mass'],flush=True)
 proc.stdin.close();assert proc.wait()==0
 files=('binary_dilation_family.py','pair_amplification_probe.cpp')
 out=dict(scope='Original-layer monotone-root controls of exact core and density-mass invariance under binary replication. Small independent all-root controls are recorded separately in binary_dilation_audit.json.',rows=rows,compiled_counts=last['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/binary_dilation_family.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
