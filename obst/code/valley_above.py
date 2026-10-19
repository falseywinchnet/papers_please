"""Exact implicit above-capacity queries for nonincreasing-then-increasing keys.

Preprocessing and storage are O(n log(n+1)); queries use O(log(n+1)) work.
The representation does not enumerate the potentially quadratic core.
"""
from collections import Counter
from unimodal_above import ruler_windows


def valley_floor(p,stats=None):
    stats=Counter() if stats is None else stats
    if not p:raise ValueError('At least one key is required.')
    bottom=0;rising=False
    for i,w in enumerate(p):
        if w<0:raise ValueError('Key weights must be nonnegative.')
        if w<p[bottom]:bottom=i
        if i:
            stats['valley_validation_comparisons']+=1
            if w>p[i-1]:rising=True
            elif w<p[i-1] and rising:raise ValueError('Key weights do not form a valley.')
    return bottom


def largest_end_split(p,i,j,c,bottom,stats=None):
    """Select c largest keys as a prefix and suffix, favoring left ties."""
    stats=Counter() if stats is None else stats
    assert 0<=i<=j<=len(p) and 0<=c<=j-i
    split=max(i,min(bottom,j))
    low=max(0,c-(j-split));high=min(c,split-i)
    while low<high:
        mid=(low+high)//2
        stats['valley_split_comparisons']+=1
        if p[i+mid]>=p[j-c+mid]:low=mid+1
        else:high=mid
    stats['valley_split_queries']+=1
    return low


class RulerPrefixes:
    def __init__(self,p,stats):
        self.p=list(p);self.stats=stats
        self.windows={0:[0]*(len(p)+1)}
        self.windows.update(ruler_windows(p,stats))
        self.powers=[];d=1;k=0
        while d<=len(p):
            self.powers.append((k,d));k+=1;d*=2
        stats['ruler_prefix_stored_entries']+=sum(map(len,self.windows.values()))

    def query(self,start,length):
        assert 0<=start<=len(self.p)-length and length>=0
        result=0
        # Scanning powers avoids an assumed constant-time population-count or log.
        for k,d in reversed(self.powers):
            self.stats['ruler_prefix_bit_steps']+=1
            if length>=d:
                result+=self.windows[k][start]+k*self.p[start+d-1]
                start+=d;length-=d
                self.stats['ruler_prefix_chunks']+=1
        assert length==0
        self.stats['ruler_prefix_queries']+=1
        return result


class ValleyAbove:
    def __init__(self,p,q=None,stats=None):
        self.stats=Counter() if stats is None else stats
        self.p=list(p);self.n=len(p);self.bottom=valley_floor(p,self.stats)
        self.q=[0]*(self.n+1) if q is None else list(q)
        if len(self.q)!=self.n+1 or any(x<0 for x in self.q):
            raise ValueError('There must be n+1 nonnegative gap weights.')
        self.forward=RulerPrefixes(p,self.stats)
        self.backward=RulerPrefixes(list(reversed(p)),self.stats)
        self.pp=[0];self.qp=[0]
        for x in p:self.pp.append(self.pp[-1]+x);self.stats['valley_mass_prefix_entries']+=1
        for x in self.q:self.qp.append(self.qp[-1]+x);self.stats['valley_mass_prefix_entries']+=1

    def score(self,h,i,j):
        c=(1<<h)-1
        assert h>=1 and 0<=i<j<=self.n and j-i>=c
        left=largest_end_split(self.p,i,j,c,self.bottom,self.stats)
        reward=self.forward.query(i,left)+self.backward.query(self.n-j,c-left)
        return reward,((i,i+left),(j-(c-left),j))

    def layer(self,h,i,j,M):
        reward,blocks=self.score(h,i,j);c=(1<<h)-1
        mass=self.pp[j]-self.pp[i]+self.qp[j+1]-self.qp[i]
        return M*(j-i-c)+h*mass-reward,blocks


def dense_valley(s):
    assert s>=4 and s&(s-1)==0
    m=2*s
    return list(range(2*m,0,-2))+list(range(1,2*m,2))


def dense_valley_density(s,i,j):
    assert 0<=i<s and 3*s<=j<4*s
    rank=3*s-(i+j+1)//2
    return (rank&-rank).bit_length()-1
