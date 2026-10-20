#!/usr/bin/env python3
"""Audit a two-key exact full-ruler tail and the sharp clipping-error scale."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json,subprocess,sys
from aggregate_core_audit import layers


def two_score(i,j,C,x,y,v,stats):
 c=C-1;e=j-i-c;assert e>=0
 rs=[X-i for X in (x,y) if i<X<=j];ans=0
 for r in rs:
  for u in range(max(1,r-e),min(c,r)+1):
   ans=max(ans,v[u]);stats['one_rank_candidates']+=1
 if len(rs)==2:
  r,s=rs
  for u in range(max(1,r-e),min(c,r)+1):
   for z in range(max(u+1,s-e),min(c,u+s-r,s)+1):
    ans=max(ans,v[u]+v[z]);stats['two_rank_candidates']+=1
 stats['two_key_scores']+=1
 return ans


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[];compiled=None
 proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 for a in range(4):
  d=2**a
  for b in range(3,7):
   Q=2**b;C=d*Q;c=C-1;h=a+b;n=2*C;x=C-3*d;y=C;k=c+d
   v=[0]+[(r&-r).bit_length()-1 for r in range(1,C)]
   low=[min(z,a) for z in v];high=[max(0,z-a) for z in v]
   coarse=[0]+[(r&-r).bit_length()-1 for r in range(1,Q)]
   intervals=[(i,i+k,1) for i in range(n-k+1)]+[(i+1,i+k,-1) for i in range(n-k)]+[(0,n,-1)]
   sums=[0,0,0];cache={}
   def cs(i,j):
    if (i,j) not in cache:cache[i,j]=two_score(i,j,Q,Q-3,Q,coarse,stats)
    return cache[i,j]
   for i,j,sign in intervals:
    values=[two_score(i,j,C,x,y,w,stats) for w in (v,low,high)]
    assert values[0]==values[1]+values[2],(a,b,i,j,values)
    stats['compatible_score_decompositions']+=1
    for r,value in enumerate(values):sums[r]+=sign*value
    if (i,j)==(0,n):mapped=cs(0,2*Q)
    elif j-i==k:
     z=i//d;mapped=cs(z,z+Q) if i%d==0 else cs(z+1,z+Q)
    else:
     z=(i-1)//d;mapped=cs(z+1,z+Q)
    assert values[2]==mapped,(a,b,i,j,values,mapped)
    stats['coarse_score_controls']+=1
   want=5*Q//4-3*b+2
   assert sums==[want,0,want],(a,b,sums,want)
   # Check the closed parity sum independently, including its endpoint cases.
   def V(r):return coarse[r] if 1<=r<Q else 0
   ev=od=0
   for r in range(-2,Q-2):
    delta=max(V(r)+V(r+3),V(r)+V(r+2),V(r-1)+V(r+2))-V(r-1)-V(r+2)
    if r%2:od+=delta
    else:ev+=delta
   assert ev==Q-b-2 and od==Q//4-b+4 and cs(0,2*Q)==b
   stats['parity_sum_controls']+=1
   if n<=128:
    p=[int(i+1 in (x,y)) for i in range(n)]
    for template,wanttail in ((v,want),(low,0)):
     proc.stdin.write(' '.join(map(str,[n,c,*p,*template[1:]]))+'\n');proc.stdin.flush();compiled=json.loads(proc.stdout.readline())
     assert compiled['tails'][d-1]==wanttail;stats['generic_tail_controls']+=1
   if n<=64:
    for scale,gaps in ((1,[0]*(n+1)),(7,[i%3 for i in range(n+1)])):
     p=[scale*int(i+1 in (x,y)) for i in range(n)];W=sum(p)+sum(gaps)
     A=list(layers(p,gaps,h,(h+1)*W+1,stats))[-1]
     total=sum(A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1] for i in range(n) for j in range(i+c+d,n))
     assert total==scale*want;stats['original_mixed_layer_controls']+=1
   if n==16:
    p=[int(i+1 in (x,y)) for i in range(n)]
    for i,j,_ in intervals:
     best=0
     for chosen in combinations(range(i,j),c):
      best=max(best,sum(p[z]*v[r+1] for r,z in enumerate(chosen)));stats['literal_subsequences']+=1
     assert best==two_score(i,j,C,x,y,v,stats);stats['literal_interval_controls']+=1
   rows.append(dict(a=a,b=b,d=d,Q=Q,h=h,n=n,key_positions_one_based=[x,y],full_tail=want,clipped_tail=0,removed_reward=Q-b-1,verification='two-key score enumeration; generic/all-root only where separately counted'))
   print(a,b,want,flush=True)
 for fixture in json.loads((root/'results/spaced_rank_tail.json').read_text())['rows']:
  if fixture['kind']!='spaced':continue
  d,m=fixture['d'],fixture['m'];C=2*d*(m+1);n=2*C;c=C-1;k=c+d;x=C-3*d;y=C
  v=[int(r>0 and r%(2*d)==0) for r in range(C)]
  first=sum(two_score(i,i+k,C,x,y,v,stats) for i in range(n-k+1))
  second=sum(two_score(i+1,i+k,C,x,y,v,stats) for i in range(n-k))
  full=two_score(0,n,C,x,y,v,stats)
  assert (first,second,full)==(C-3*d+m+1,C-3*d,2)
  assert first-second-full==fixture['tail']==m-1
  stats['spaced_boundary_sum_controls']+=1
  if n==12:
   p=[int(i+1 in (x,y)) for i in range(n)]
   for i,j in [(i,i+k) for i in range(n-k+1)]+[(i+1,i+k) for i in range(n-k)]+[(0,n)]:
    vals=[sum(p[z]*v[r+1] for r,z in enumerate(chosen)) for chosen in combinations(range(i,j),c)]
    assert max(vals)==two_score(i,j,C,x,y,v,stats)
    stats['literal_spaced_subsequences']+=len(vals);stats['literal_spaced_scores']+=1
 proc.stdin.close();assert proc.wait()==0
 # Larger rows evaluate the proved formulas only.
 large=[dict(a=b,b=b,d=2**b,Q=2**b,n=2**(2*b+1),full_tail=5*2**b//4-3*b+2,removed_reward=2**b-b-1,verification='closed form only') for b in (8,16,32,64)]
 files=('ruler_clipping_sharp.py','template_tail_probe.cpp','aggregate_core_audit.py','../results/spaced_rank_tail.json')
 out=dict(scope='Exact two-key full-ruler tail and zero clipped tail. Pair-rank enumeration, generic subsequence, literal subset, and original mixed-layer controls are separate from formula-only rows.',rows=rows,formula_only=large,checks=stats,compiled_counts=compiled['counts'],source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/ruler_clipping_sharp.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
