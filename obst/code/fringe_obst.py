"""Full mixed OBST with a periodic middle and arbitrary boundary fringes.

The exact central oracle is extended through online concave LWS columns.
A prescribed middle of length m and period b, with d=n-m fringe keys,
takes O(mb+nd) arithmetic work and space. Both endpoints are supported.
"""
from collections import Counter
from periodic_obst import PeriodicOBST,joint_period,solve as periodic_solve
from concave_lws import concave_lws


def extend_column(N,old_cost,mass,stats):
    # Reverse suffix lengths: s<t corresponds to root r=N-s-1 in [N-t,N).
    def weight(s,t):
        stats['fringe_transition_queries']+=1
        return old_cost(N-t,N-s-1)+mass(N-t)
    F,pred=concave_lws(N,weight,stats)
    values=[F[N-i] for i in range(N+1)]
    roots=[N-pred[N-i]-1 for i in range(N)]+[-1]
    stats['fringe_boundary_states']+=N
    return values,roots


def longest_middle(p,q,b,stats=None):
    stats=Counter() if stats is None else stats
    n=len(p);assert 1<=b<n
    left=0;best=None
    for i in range(b,n):
        stats['fringe_period_signature_checks']+=1
        if (p[i],q[i],q[i+1])!=(p[i-b],q[i-b],q[i-b+1]):left=i-b+1
        elif i+1-left>b and (best is None or i+1-left>best[1]-best[0]):best=(left,i+1)
    return best


class FringeOBST:
    def __init__(self,p,q,left,right,b,stats=None):
        self.stats=Counter() if stats is None else stats
        self.p=list(p);self.q=list(q);self.n=len(p);self.left=left;self.right=right;self.b=b
        n=self.n;m=right-left
        assert len(q)==n+1 and all(x>=0 for x in p) and all(x>=0 for x in q)
        assert 0<=left<right<=n and 1<=b<=m
        pp=p[left:left+b];qq=q[left:left+b]
        for t in range(m):
            assert p[left+t]==pp[t%b];self.stats['fringe_middle_key_checks']+=1
        for t in range(m+1):
            assert q[left+t]==qq[t%b];self.stats['fringe_middle_gap_checks']+=1
        self.base=PeriodicOBST(pp,qq,m,self.stats)
        self.prefix=[0]
        for k in range(n):self.prefix.append(self.prefix[-1]+p[k]+q[k])
        self.stats['fringe_mass_prefix_entries']+=n+1
        self.columns={};self.rows={}
        for j in range(right+1,n+1):
            vals,roots=extend_column(j-left,lambda a,r:self.value(left+a,left+r),
                                    lambda a:self.mass(left+a,j),self.stats)
            self.columns[j]=(vals,[left+r if r>=0 else -1 for r in roots])
            self.stats['fringe_right_extensions']+=1
        for i in range(left-1,-1,-1):
            vals,roots=extend_column(n-i,lambda a,r:self.value(n-r,n-a),
                                    lambda a:self.mass(i,n-a),self.stats)
            self.rows[i]=(vals,[n-r-1 if r>=0 else -1 for r in roots])
            self.stats['fringe_left_extensions']+=1
        self.stats['fringe_stored_entries']+=2*sum(len(v) for v,r in self.columns.values())
        self.stats['fringe_stored_entries']+=2*sum(len(v) for v,r in self.rows.values())

    def mass(self,i,j):return self.prefix[j]-self.prefix[i]+self.q[j]
    def value(self,i=0,j=None):
        if j is None:j=self.n
        assert 0<=i<=j<=self.n
        if i==j:return 0
        if i<self.left:return self.rows[i][0][self.n-j]
        if j>self.right:return self.columns[j][0][i-self.left]
        return self.base.costs[j-i][(i-self.left)%self.b]
    def root(self,i,j):
        assert i<j
        if i<self.left:return self.rows[i][1][self.n-j]
        if j>self.right:return self.columns[j][1][i-self.left]
        return i+self.base.roots[j-i][(i-self.left)%self.b]
    def reconstruct(self):
        n=self.n;left=[-1]*n;right=[-1]*n;kd=[0]*n;gd=[0]*(n+1)
        top=-1;todo=[(0,n,-1,0,0)]
        while todo:
            i,j,parent,side,depth=todo.pop()
            if i==j:gd[i]=depth;self.stats['fringe_reconstructed_gaps']+=1;continue
            r=self.root(i,j)
            if parent<0:top=r
            elif side:left[parent]=r
            else:right[parent]=r
            kd[r]=depth+1;self.stats['fringe_reconstructed_keys']+=1
            todo.append((r+1,j,r,0,depth+1));todo.append((i,r,r,1,depth+1))
        return dict(root=top,left=left,right=right,key_depth=kd,gap_depth=gd)


def solve(p,q,stats=None,max_period=None):
    stats=Counter() if stats is None else stats
    p=list(p);q=list(q);n=len(p);whole=joint_period(p,q,stats)
    B=min(max(0,n-1),n.bit_length() if max_period is None else max_period)
    best=(n*whole,None);stats['fringe_planner_period_limit']=B
    if whole>B:
        for b in range(1,B+1):
            span=longest_middle(p,q,b,stats)
            if span is not None:
                l,r=span;m=r-l;proxy=m*b+n*(n-m)
                if proxy<best[0]:best=(proxy,(l,r,b))
    stats['fringe_selected_proxy']=best[0]
    if best[1] is None:
        value,tree,solver=periodic_solve(p,q,stats);stats['fringe_whole_period_route']+=1
    else:
        l,r,b=best[1];solver=FringeOBST(p,q,l,r,b,stats)
        value=solver.value();tree=solver.reconstruct();stats['fringe_extension_route']+=1
    return value,tree,solver
