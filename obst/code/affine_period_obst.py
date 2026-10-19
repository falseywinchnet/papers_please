"""Exact full mixed OBST under affine translation, in O(nb) arithmetic work.

p[i+b]=scale*p[i]+offset; q[i+b]=scale*q[i]-offset, scale>0.
Only actual nonnegative input intervals are used. No infinite positive
extension is assumed. The last b-1 lengths use ordinary Knuth diagonals.
"""
from collections import Counter
from fractions import Fraction


def recognize(p,q,b,stats=None):
    stats=Counter() if stats is None else stats
    n=len(p);assert 1<=b<=n
    scale=None
    for i in range(n-b):
        for old,new in ((p[i]+q[i],p[i+b]+q[i+b]),(p[i]+q[i+1],p[i+b]+q[i+b+1])):
            stats['affine_recognition_pairs']+=1
            if old==0:
                if new!=0:return None
            elif scale is None:
                if new<=0:return None
                scale=Fraction(new)/old
                if scale.denominator==1:scale=scale.numerator
            elif new!=scale*old:return None
    if scale is None:scale=1
    offset=scale*q[0]-q[b]
    for i in range(n-b):
        stats['affine_recognition_weights']+=1
        if p[i+b]!=scale*p[i]+offset:return None
    for i in range(n-b+1):
        stats['affine_recognition_weights']+=1
        if q[i+b]!=scale*q[i]-offset:return None
    return scale,offset


class AffinePeriodOBST:
    def __init__(self,p,q,b,scale,offset,stats=None):
        self.stats=Counter() if stats is None else stats
        self.p=list(p);self.q=list(q);self.n=n=len(p);self.b=b;self.scale=scale;self.offset=offset
        if len(q)!=n+1 or scale<=0 or not 1<=b<=max(1,n) or any(x<0 for x in list(p)+list(q)):
            raise ValueError('Expected finite nonnegative mixed weights and a positive affine scale.')
        for i in range(n-b):assert p[i+b]==scale*p[i]+offset
        for i in range(max(0,n-b+1)):assert q[i+b]==scale*q[i]-offset
        self.m=m=n-b+1 if n else 0
        self.powers=[1];self.sums=[0]
        for k in range(n//b+1):
            self.powers.append(self.powers[-1]*scale);self.sums.append(self.sums[-1]+self.powers[-2])
            self.stats['affine_power_entries']+=1
        self.prefix=[0]
        for i in range(n):self.prefix.append(self.prefix[-1]+p[i]+q[i])
        self.costs=[[0]*b];self.roots=[[-1]*b];self.tail_costs={};self.tail_roots={}
        for length in range(1,m+1):
            vals=[];roots=[];count=0
            for a in range(b):
                lo=0 if length==1 else self.roots[length-1][a]
                hi=0 if length==1 else 1+self.roots[length-1][(a+1)%b]
                assert 0<=lo<=hi<length
                best=None;root=None
                for r in range(lo,hi+1):
                    v=self.value(a,a+r)+self.value(a+r+1,a+length)
                    if best is None or v<best:best=v;root=r
                    count+=1
                vals.append(best+self.mass(a,a+length));roots.append(root)
            assert count==b*(1 if length==1 else 2)
            self.stats['affine_phase_candidates']+=count;self.stats['affine_phase_states']+=b
            self.costs.append(vals);self.roots.append(roots)
        for length in range(m+1,n+1):
            vals=[];roots=[];count=0
            for i in range(n-length+1):
                j=i+length;lo=self.root(i,j-1);hi=self.root(i+1,j)
                best=None;root=None
                for r in range(lo,hi+1):
                    v=self.value(i,r)+self.value(r+1,j)
                    if best is None or v<best:best=v;root=r
                    count+=1
                vals.append(best+self.mass(i,j));roots.append(root)
            assert count<=2*n-length
            self.stats['affine_tail_candidates']+=count;self.stats['affine_tail_states']+=len(vals)
            self.tail_costs[length]=vals;self.tail_roots[length]=roots
        self.stats['affine_stored_entries']+=2*((m+1)*b+sum(map(len,self.tail_costs.values())))

    def mass(self,i,j):return self.prefix[j]-self.prefix[i]+self.q[j]
    def value(self,i=0,j=None):
        if j is None:j=self.n
        assert 0<=i<=j<=self.n
        length=j-i
        if not length:return 0
        if length>self.m:return self.tail_costs[length][i]
        k,a=divmod(i,self.b);self.stats['affine_transformed_queries']+=1
        return self.powers[k]*self.costs[length][a]-self.offset*length*self.sums[k]
    def root(self,i,j):
        length=j-i;assert length>0
        if length>self.m:return self.tail_roots[length][i]
        return i+self.roots[length][i%self.b]
    def reconstruct(self):
        n=self.n;left=[-1]*n;right=[-1]*n;kd=[0]*n;gd=[0]*(n+1);top=-1
        todo=[(0,n,-1,0,0)]
        while todo:
            i,j,parent,side,depth=todo.pop()
            if i==j:gd[i]=depth;self.stats['affine_gap_visits']+=1;continue
            r=self.root(i,j)
            if parent<0:top=r
            elif side:left[parent]=r
            else:right[parent]=r
            kd[r]=depth+1;self.stats['affine_key_visits']+=1
            todo.append((r+1,j,r,0,depth+1));todo.append((i,r,r,1,depth+1))
        return dict(root=top,left=left,right=right,key_depth=kd,gap_depth=gd)


def solve(p,q,stats=None,max_period=None):
    stats=Counter() if stats is None else stats
    p=list(p);q=list(q);n=len(p)
    if len(q)!=n+1 or any(x<0 for x in p+q):raise ValueError('Expected nonnegative mixed weights.')
    if not n:
        s=AffinePeriodOBST(p,q,1,1,0,stats);return 0,s.reconstruct(),s
    B=n if max_period is None else min(n,max(0,max_period));chosen=None
    for b in range(1,B+1):
        result=recognize(p,q,b,stats)
        if result is not None:chosen=(b,*result);break
    if chosen is None:chosen=(n,1,q[0]-q[n]);stats['affine_fallback_route']+=1
    else:stats['affine_recognized_route']+=1
    s=AffinePeriodOBST(p,q,*chosen,stats)
    return s.value(),s.reconstruct(),s
