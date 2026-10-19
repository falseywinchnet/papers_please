"""Finite sparse-Monge representation of a two-coordinate band optimum.

Uses the previously implemented ESA 2025 multiplication primitive. This is
an above-capacity interior component, not a full optimal-BST constructor.
"""
from collections import Counter
from core_monge import Monge,multiply
from plateau_core import ruler_block_rewards,range_max_core,above_plateau_core

def band_matrix(F,G,g,stats,K=None):
 n=len(F);assert n and len(G)==n and g>=0
 if K is None:K=1+max(F)-min(F)+max(G)-min(G)
 top=[K*max(v-g,0)-F[0]-G[v] for v in range(n)]
 left=[K*u-F[u]-G[0] for u in range(n)]
 entries=[(i,i,K) for i in range(n-1)]
 entries.extend((i,i+g,K) for i in range(n-1) if i+g<n-1)
 stats['input_boundary_cells']+=2*n;stats['input_core_terms']+=len(entries)
 return Monge(top,left,entries,stats),K

def prefix_matrix(n,K,stats):
 stats['input_boundary_cells']+=2*n;stats['input_core_terms']+=n-1
 return Monge([K*j for j in range(n)],[0]*n,[(i,i,K) for i in range(n-1)],stats)

def dominance(F,G,g,stats=None):
 """Return finite T, with T(A,B)=-max F(u)+G(v) whenever B<=A+g.

The maximization has u<=A, v>=B, 0<=v-u<=g, and 0<=u,v<n.
Values outside the feasible domain are the explicit finite completion.
"""
 if stats is None:stats=Counter()
 Q,K=band_matrix(F,G,g,stats);L=prefix_matrix(len(F),K,stats)
 middle,w=multiply(L,Q);del w
 out,w=multiply(middle,L);del w
 assert out.k<=14*(len(F)-1)
 return out

def two_block_interior(n,h,z,m,g,k,stats=None):
 """Unit blocks [z,z+m), [z+m+g,z+m+g+k); all other keys zero.

Returns only ordinary above-capacity densities whose four intervals
contain both whole blocks. Arbitrary nonnegative gaps cancel there.
"""
 if stats is None:stats=Counter()
 c=2**h-1;assert h>=1 and m>=1 and k>=1 and g>=0 and 0<=z and z+m+g+k<=n
 if c>=n or m+k>c:return {}
 N=c-m-k+1
 F=ruler_block_rewards(c,m,stats)[:N]
 G=ruler_block_rewards(c,k,stats)[m:m+N]
 T=dominance(F,G,g,stats);out={}
 for a,b,D in T.entries:
  i=z-a-1;j=c+z+g-b-1;stats['interior_coordinate_filters']+=1
  if 0<=i<z and z+m+g+k<=j<n and j-i>c:
   out[i,j]=D;stats['interior_core_outputs']+=1
 return out

def range_maximum(values,stats):
 size=1
 while size<len(values):size*=2
 tree=[-1]*(2*size);tree[size:size+len(values)]=values
 for i in range(size-1,0,-1):tree[i]=max(tree[2*i],tree[2*i+1]);stats['range_tree_build_nodes']+=1
 def query(a,b):
  assert 0<=a<=b<len(values)
  a+=size;b+=size+1;best=-1
  while a<b:
   stats['range_query_levels']+=1
   if a%2:best=max(best,tree[a]);a+=1
   if b%2:b-=1;best=max(best,tree[b])
   a//=2;b//=2
  stats['range_queries']+=1
  return best
 return query

def batch_values(T,queries,stats):
 """Offline weighted core-prefix queries, without dense matrix conversion."""
 tree=[0]*(T.q+1);index=0;out={}
 for A,B in sorted(set(queries)):
  while index<T.k and T.entries[index][0]<A:
   _,b,v=T.entries[index];x=b+1
   while x<=T.q:tree[x]+=v;x+=x&-x;stats['prefix_update_nodes']+=1
   index+=1
  total=0;x=B
  while x:total+=tree[x];x-=x&-x;stats['prefix_query_nodes']+=1
  out[A,B]=T.left[A]+T.top[B]-T.top[0]-total;stats['core_value_queries']+=1
 return out

def two_block_above_core(n,h,z,m,g,k,weight=1,stats=None):
 """Entire ordinary above-capacity core for two equal positive blocks.

All other keys are zero; arbitrary nonnegative gaps cancel. The algorithm
uses O(n log(n+1)) work. The reused product stores ordinary witness maps,
so its implemented peak-space guarantee is O(n log(n+1)), not linear.
"""
 if stats is None:stats=Counter()
 assert h>=1 and m>=1 and k>=1 and g>=0 and z>=0 and z+m+g+k<=n and weight>=0
 c=2**h-1
 if c>=n or c==1 or weight==0:return {}
 end=z+m;second=end+g;last=second+k
 candidates=set()
 def add(i,j):
  stats['support_candidate_visits']+=1
  if 0<=i<j<n and j-i>c:candidates.add((i,j))
 for start,length in ((z,m),(second,k)):
  for i,j in above_plateau_core(n,h,start,length,1,stats):add(i,j)
 for boundary in (z,end,second,last):
  i=boundary-1
  if 0<=i<n:
   for j in range(i+c+1,n):add(i,j)
  j=boundary-1
  if 0<=j<n:
   for i in range(max(0,j-c)):add(i,j)
 for d in (c+g-1,c+g):
  if d>c:
   for i in range(max(0,n-d)):add(i,i+d)
 rewards={};queries={}
 for length in set((m,k)):
  if length<=c:
   rewards[length]=ruler_block_rewards(c,length,stats)
   queries[length]=range_maximum(rewards[length],stats)
 for first_length,second_length,start,reflect in ((m,k,z,False),(k,m,n-last,True)):
  if second_length>c:continue
  for a,b,_ in range_max_core(rewards[second_length],stats):
   i=start+first_length-(b-g);j=c+start+first_length+g-a-1
   if reflect:i,j=n-1-j,n-1-i
   add(i,j)
 T=None;N=c-m-k+1
 if N>0:
  T=dominance(rewards[m][:N],rewards[k][m:m+N],g,stats)
  for a,b,_ in T.entries:add(z-a-1,c+z+g-b-1)
 assert len(candidates)<=28*n
 prefix=[0]*(c+1);ruler=[0]*(c+1)
 for r in range(1,c+1):
  ruler[r]=0 if r%2 else ruler[r//2]+1
  prefix[r]=prefix[r-1]+ruler[r];stats['ruler_prefix_entries']+=1
 # Each interval score is either a scalar/range maximum or one sparse core query.
 intervals={(a,b) for i,j in candidates for a,b in ((i,j),(i+1,j+1),(i,j+1),(i+1,j))}
 scores={};pending={}
 for i,j in intervals:
  a=max(0,min(j,end)-max(i,z));b=max(0,min(j,last)-max(i,second));P=a+b
  if P>=c:value=prefix[c]
  elif not P:value=0
  elif not a or not b:
   start,length=(z,m) if a else (second,k)
   if i>=start or j<=start+length:value=prefix[P]
   else:value=queries[length](max(0,c+start-j),min(c-length,start-i))
  elif i>=z and j<=last:value=prefix[a]+prefix[b]
  elif i>=z:value=prefix[a]+queries[k](max(a,c+second-j),min(a+g,c-k))
  elif j<=last:value=prefix[b]+queries[m](max(b,c-z-m+i),min(b+g,c-m))
  else:
   assert T is not None
   pending[i,j]=(min(N-1,z-i),max(0,c+z+g-j));continue
  scores[i,j]=value;stats['direct_interval_scores']+=1
 if pending:
  values=batch_values(T,pending.values(),stats)
  for ij,ab in pending.items():scores[ij]=-values[ab]
 out={}
 for i,j in candidates:
  D=scores[i,j]+scores[i+1,j+1]-scores[i,j+1]-scores[i+1,j]
  assert D>=0
  if D:out[i,j]=weight*D
  stats['constructed_density_evaluations']+=1
 stats['full_above_core_outputs']+=len(out)
 return out
