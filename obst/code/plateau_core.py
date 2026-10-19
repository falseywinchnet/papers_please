"""Enumerate ordinary above-capacity densities for one constant key block.

Gap weights may be arbitrary: they cancel in this region. This constructs
only the above-capacity part of a layer core, not a complete OBST solver.
"""
from collections import Counter

def range_max_core(values,stats=None):
 """Nonadjacent strict visibility pairs with their exact density values."""
 if stats is None:stats=Counter()
 stack=[];result=[]
 def emit(i,j,interior):
  stats['visibility_candidates']+=1
  if j-i<2:return
  assert interior is not None
  density=min(values[i],values[j])-interior
  assert density>0
  result.append((i,j,density));stats['visibility_output_pairs']+=1
 for j,x in enumerate(values):
  interior=None
  while stack and values[stack[-1]]<x:
   i=stack.pop();stats['stack_pops']+=1
   emit(i,j,interior);interior=values[i]
  if stack:
   emit(stack[-1],j,interior)
   if values[stack[-1]]==x:stack.pop();stats['stack_pops']+=1
  stack.append(j);stats['stack_pushes']+=1
 return result

def ruler_block_rewards(c,m,stats=None):
 """All sums of m consecutive ruler rewards, in linear arithmetic work."""
 if stats is None:stats=Counter()
 assert 1<=m<=c
 ruler=[0]*(c+1)
 for r in range(1,c+1):
  ruler[r]=0 if r%2 else ruler[r//2]+1;stats['ruler_values']+=1
 total=0
 for r in range(1,m+1):total+=ruler[r];stats['initial_reward_additions']+=1
 result=[total]
 for r in range(1,c-m+1):
  total+=ruler[r+m]-ruler[r];result.append(total);stats['sliding_reward_updates']+=1
 return result

def above_plateau_core(n,h,start,length,weight=1,stats=None):
 """Return {(i,j):density}; keys start,...,start+length-1 have weight.

Coordinates and start are zero-based. A valid terminal penalty is assumed.
The arithmetic work and memory are O(c) when c=2**h-1<n; otherwise the
requested region is empty. No population-count primitive is required.
"""
 if stats is None:stats=Counter()
 assert n>=1 and h>=1 and 0<=start<n and 1<=length<=n-start and weight>=0
 c=2**h-1
 if c>=n or length>c or weight==0:return {}
 values=ruler_block_rewards(c,length,stats);out={}
 for a,b,density in range_max_core(values,stats):
  i=start-b;j=c+start-1-a;stats['coordinate_filters']+=1
  if 0<=i<j<n:out[i,j]=weight*density;stats['core_outputs']+=1
 return out
