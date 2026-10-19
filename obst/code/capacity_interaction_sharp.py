#!/usr/bin/env python3
"""Independent controls for the sharp width-one interaction family."""
from collections import Counter
from pathlib import Path
import hashlib,json
from capacity_interaction import profile
from aggregate_core_audit import layers


def single_full(x,n,h):
 c=2**h-1;lo=max(1,c+x+1-n);hi=min(c,x+1)
 reward=max(t for t in range(h) if (lo+2**t-1)//2**t<=hi//2**t)
 return h-reward


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
 for h in range(2,7):
  C=2**h;n=2*C;w=[int(x%2==0) for x in range(n)]+[0]*(n+1)
  a=profile(w,stats)[h-1];unit_full=sum(single_full(x,n,h) for x in range(0,n,2))
  assert unit_full==2*C-h-1
  unit_potential=0;unit_tail=0
  if h<=4:
   for x in range(0,n,2):
    e=[0]*(2*n+1);e[x]=1;b=profile(e,stats)[h-1]
    assert b['full']==single_full(x,n,h)
    unit_potential+=b['potentials'];unit_tail+=b['tail'][1];stats['unit_full_checks']+=1
   assert unit_potential==a['potentials']
   assert a['tail'][1]-unit_tail==(h-3)*C+2*h+2
   stats['independent_interaction_checks']+=1
  assert a['full']==(h-1)*C+h+1
  assert a['tail'][1]==C*(C-2)
  assert a['full']-unit_full==(h-3)*C+2*h+2;stats['family_formula_checks']+=1
  rows.append(dict(h=h,n=n,P=C,total_tail=a['tail'][1],full_residual=a['full'],unit_full=unit_full,
                   interaction=(h-3)*C+2*h+2,bound=(h-1)*C,
                   verification='all-root family and all weighted unit inputs' if h<=4 else 'all-root family; unit full costs use proved slot formula'))
 # The hW allowance for arbitrary widths would also have an optimal coefficient.
 for h in range(2,7):
  C=2**h;n=2*C;w=[1]*n+[0]*(n+1);a=profile(w,stats)[h-1];d=C//2
  assert a['tail'][d]==(h-1)*n+h-(C-1);stats['wide_family_checks']+=1
  # Unit-key tails vanish here: every classified pair has distance <= C/2-1.
 for h in (8,16,32,64,128):
  C=2**h
  rows.append(dict(h=h,n=2*C,P=C,total_tail=C*(C-2),full_residual=(h-1)*C+h+1,
                   unit_full=2*C-h-1,interaction=(h-3)*C+2*h+2,bound=(h-1)*C,
                   verification='closed-form evaluation only'))
 files=('capacity_interaction_sharp.py','capacity_interaction.py','aggregate_core_audit.py')
 result=dict(scope='Explicit sharpness formulas, independent all-root controls, and separately labeled formula-only rows.',
 checks=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/capacity_interaction_sharp.json').write_text(json.dumps(result,indent=2)+'\n')
 print(dict(stats),flush=True)
if __name__=='__main__':main()
