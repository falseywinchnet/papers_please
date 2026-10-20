"""Exact mixed OBST by periodic phase and interval length.

For a joint period b, all b phases and lengths through n use exactly
b*(2*n-1) root candidates. Reconstruction emits every key and gap depth.
Arbitrary inputs are accepted: their joint period may be n+1.
"""
from collections import Counter


def joint_period(p,q,stats=None):
    stats=Counter() if stats is None else stats
    n=len(p)
    if len(q)!=n+1 or any(x<0 for x in p) or any(x<0 for x in q):
        raise ValueError('Expected n nonnegative key weights and n+1 gap weights.')
    if not n:return 1
    word=[(p[i],q[i],q[i+1]) for i in range(n)]
    pi=[0]*n
    for i in range(1,n):
        j=pi[i-1]
        while True:
            stats['period_signature_comparisons']+=1
            if word[i]==word[j]:j+=1;break
            if not j:break
            j=pi[j-1]
        pi[i]=j
    b=n-pi[-1]
    # A proper signature period forces the gap closure. At b=n the
    # two endpoint gaps have never been compared by the signature word.
    if b==n and q[n]!=q[0]:b=n+1
    stats['period_signature_entries']+=n
    return b


class PeriodicOBST:
    def __init__(self,key_period,gap_period,n,stats=None):
        self.stats=Counter() if stats is None else stats
        self.p=list(key_period);self.q=list(gap_period);self.b=len(self.p);self.n=n
        if not self.b or len(self.q)!=self.b or n<0 or any(x<0 for x in self.p+self.q):
            raise ValueError('Expected nonempty equal-length nonnegative periods and n>=0.')
        b=self.b
        self.prefix=[0]
        for t in range(n+b):
            self.prefix.append(self.prefix[-1]+self.p[t%b]+self.q[t%b])
            self.stats['periodic_mass_prefix_entries']+=1
        self.costs=[[0]*b];self.roots=[[-1]*b]
        for length in range(1,n+1):
            costs=[];roots=[];candidates=0
            for a in range(b):
                lo=0 if length==1 else self.roots[length-1][a]
                hi=0 if length==1 else 1+self.roots[length-1][(a+1)%b]
                assert 0<=lo<=hi<length
                best=None;root=None
                for r in range(lo,hi+1):
                    value=self.costs[r][a]+self.costs[length-r-1][(a+r+1)%b]
                    if best is None or value<best:best=value;root=r
                    candidates+=1
                mass=self.prefix[a+length]-self.prefix[a]+self.q[(a+length)%b]
                costs.append(best+mass);roots.append(root)
            assert candidates==(b if length==1 else 2*b)
            self.stats['periodic_root_candidates']+=candidates
            self.stats['periodic_states']+=b
            self.costs.append(costs);self.roots.append(roots)
        self.stats['periodic_stored_cost_entries']+=(n+1)*b
        self.stats['periodic_stored_root_entries']+=(n+1)*b

    def value(self,i=0,j=None):
        if j is None:j=self.n
        assert 0<=i<=j<=self.n
        return self.costs[j-i][i%self.b]

    def reconstruct(self,start_phase=0):
        """An ordered child-array tree and key/gap depths, without recursion."""
        n=self.n;b=self.b;a0=start_phase%b
        left=[-1]*n;right=[-1]*n;key_depth=[0]*n;gap_depth=[0]*(n+1)
        root=-1;todo=[(0,n,-1,0,0)]
        while todo:
            i,j,parent,side,depth=todo.pop()
            if i==j:
                gap_depth[i]=depth;self.stats['periodic_reconstructed_gaps']+=1
                continue
            r=i+self.roots[j-i][(a0+i)%b]
            if parent<0:root=r
            elif side==0:left[parent]=r
            else:right[parent]=r
            key_depth[r]=depth+1;self.stats['periodic_reconstructed_keys']+=1
            todo.append((r+1,j,r,1,depth+1));todo.append((i,r,r,0,depth+1))
        return dict(root=root,left=left,right=right,key_depth=key_depth,gap_depth=gap_depth)


def solve(p,q,stats=None):
    stats=Counter() if stats is None else stats
    p=list(p);q=list(q);n=len(p);b=joint_period(p,q,stats)
    pp=(p+[0])[:b];qq=q[:b]
    solver=PeriodicOBST(pp,qq,n,stats)
    return solver.value(),solver.reconstruct(),solver
