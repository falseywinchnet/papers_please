"""Finite Monge slot-window products for arbitrary nonnegative key runs.

The complete constructor handles a prescribed height and equal internal gap
weights (arbitrary endpoint gaps). It does not impose a height certificate
for unrestricted optimality, and rejects unequal internal gaps explicitly.
"""
from collections import Counter
from core_monge import Monge,multiply
from rank_transfer import runs
from mixed_slots import repair

def ruler(c,stats):
 v=[0]*(c+1);F=[0]*(c+1)
 for t in range(1,c+1):
  v[t]=0 if t%2 else v[t//2]+1;F[t]=F[t-1]+v[t];stats['slot_ruler_entries']+=1
 return v,F

def run_factor(v,F,w,m,K,stats):
 c=len(v)-1;assert w>=0 and m>=1 and K>0
 top=[K*m];score=0
 for b in range(1,c+1):
  d=2
  for _ in range(v[b]):
   score+=b//d<=m;d*=2;stats['slot_prefix_threshold_updates']+=1
  top.append(K*max(m-b,0)-w*score);stats['slot_input_boundary_pairs']+=1
 left=[K*(m+a)+w*F[a] for a in range(c+1)]
 entries=[(a,a+m,K) for a in range(max(0,c-m))]
 d=2
 while (m+1)*d<=c:
  if w:
   for k in range(1,c//d-m+1):entries.append((k*d-1,(k+m)*d-1,w));stats['slot_threshold_core_terms']+=1
  d*=2;stats['slot_factor_levels']+=1
 stats['slot_input_core_terms']+=len(entries)
 T=Monge(top,left,entries,stats);assert T.k<=2*c
 return T

class Product:
 def __init__(self,T,left=None,right=None,witness=None,block=None):
  self.T=T;self.left=left;self.right=right;self.witness=witness;self.block=block

def slot_transfer(weights,h,stats=None):
 if stats is None:stats=Counter()
 assert weights and h>=1 and all(w>=0 for w in weights)
 c=2**h-1;v,F=ruler(c,stats);blocks=runs(weights);K=1+(h-1)*sum(weights)
 def build(a,b):
  if b-a==1:
   w,m=blocks[a];return Product(run_factor(v,F,w,m,K,stats),block=(w,m))
  mid=(a+b)//2;left=build(a,mid);right=build(mid,b);T,wit=multiply(left.T,right.T)
  stats['slot_products']+=1;stats['slot_product_input_cores']+=left.T.k+right.T.k;stats['slot_product_output_cores']+=T.k
  return Product(T,left,right,wit)
 root=build(0,len(blocks));r=len(blocks);assert root.T.k<=2*r*(1<<((r-1).bit_length()))*c
 return root,K,v

def selected_slots(root,v,a,b,stats):
 assert b-a>=sum(m for w,m in leaves(root))
 out=[];stack=[(root,a,b)];levels=(len(v)-1).bit_length()
 while stack:
  node,a,b=stack.pop();stats['slot_traceback_nodes']+=1
  if node.block is None:
   k=node.witness.query(a,b);stack.append((node.right,k,b));stack.append((node.left,a,k));continue
  _,m=node.block;assert b-a>=m
  counts=[0]*levels
  for t in range(a+1,b+1):counts[v[t]]+=1;stats['slot_leaf_bucket_visits']+=1
  needed=m;cut=len(counts)-1
  while needed>counts[cut]:needed-=counts[cut];cut-=1;stats['slot_leaf_level_scans']+=1
  for t in range(a+1,b+1):
   if v[t]>cut:out.append(t)
   elif v[t]==cut and needed:out.append(t);needed-=1
   stats['slot_leaf_output_scans']+=1
  assert needed==0
 return out

def leaves(root):
 if root.block is not None:return [root.block]
 return leaves(root.left)+leaves(root.right)

def solve(p,q,h,stats=None):
 assert p and len(q)==len(p)+1 and all(w>=0 for w in (*p,*q)) and h>=1
 if stats is None:stats=Counter()
 n=len(p);c=2**h-1
 if n>c:return None
 if n==1:return dict(cost=p[0]+q[0]+q[1],tree=(0,None,None),slots=[2**(h-1)],runs=1,height=h,stats=stats)
 b=q[1]
 if any(x!=b for x in q[1:n]):raise ValueError('The slot-run constructor requires equal internal gap weights.')
 weights=[x+b for x in p];weights[0]=p[0]+q[0];weights[-1]=p[-1]+q[-1]
 stats['slot_normalized_keys']+=n
 root,K,v=slot_transfer(weights,h,stats);slots=selected_slots(root,v,0,c,stats);assert len(slots)==n
 reward=sum(w*v[t] for w,t in zip(weights,slots));value=root.T.value_reference(0,c)
 stats['slot_final_value_core_visits']+=root.T.k;assert value==-reward
 tree=repair(slots,h,stats)
 return dict(cost=h*sum(weights)+value+b*n,tree=tree,slots=slots,runs=len(runs(weights)),height=h,stats=stats)
