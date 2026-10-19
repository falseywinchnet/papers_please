#!/usr/bin/env python3
"""Independent all-root controls and operational scaling for capacity bands."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers
from capacity_band import solve,reconstruct
from research import cost


def audit(p,q,stats):
 n=len(p);H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
 dense=list(layers(p,q,H,M,stats))
 for d in sorted(set((0,1,2,4,8,n))):
  result=solve(p,q,d,H,stats);assert result['penalty']==M
  for level in result['layers']:
   h=level['h']
   for k in range(level['lo'],level['hi']+1):
    for i,v in enumerate(level['cost'][k-level['lo']]):assert v==dense[h][i][i+k];stats['entry_checks']+=1
  last=result['layers'][-1]
  if last['lo']<=n<=min(last['hi'],last['c']):
   tree=reconstruct(result);assert cost(tree,p,q)==dense[last['h']][0][n];stats['tree_checks']+=1
 stats['inputs']+=1


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(31319)
 for n in range(1,4):
  for w in product((0,1),repeat=2*n+1):audit(list(w[:n]),list(w[n:]),stats)
 for n in (4,5,7,8,15,16,31,32):
  for _ in range(12):audit([rng.randrange(16) for _ in range(n)],[rng.randrange(16) for _ in range(n+1)],stats)
  audit([1<<i for i in range(n)],[1<<min(i,n-i) for i in range(n+1)],stats)
 scales=[]
 for h in (6,8,10,12):
  for d in (0,1,4,16):
   n=(1<<h)-1-d;p=[100+rng.randrange(4) for _ in range(n)];q=[100+rng.randrange(4) for _ in range(n+1)];cc=Counter()
   result=solve(p,q,d,h,cc);tree=reconstruct(result);value=cost(tree,p,q)
   assert value==result['layers'][-1]['cost'][n-result['layers'][-1]['lo']][0]
   cc['output_keys']=n;scales.append(dict(n=n,h=h,width=d,cost=value,counts=cc,independent_reference=False))
   print(n,d,dict(cc),flush=True)
 files=['capacity_band.py','check_capacity_band.py','aggregate_core_audit.py','research.py']
 report=dict(scope='Exact band entries checked against independent all-root layers; large scale rows check reconstruction and operation counts only.',checks=stats,scales=scales,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/capacity_band.json').write_text(json.dumps(report,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
