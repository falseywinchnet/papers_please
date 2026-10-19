"""Exact range-maximum representation of all unimodal above-capacity layers.

Key weights may be arbitrary nonnegative reals; gaps are arbitrary nonnegative.
The below-capacity part and unrestricted optimal-tree certification are outside
this component. No dense interval table is constructed.
"""
from collections import Counter
from plateau_core import range_max_core


def unimodal_peak(p,stats=None):
    if stats is None:stats=Counter()
    assert p
    peak=0;falling=False
    for i,w in enumerate(p):
        if w<0:raise ValueError('Key weights must be nonnegative.')
        if i:
            stats['unimodality_comparisons']+=1
            if w<p[i-1]:falling=True
            elif w>p[i-1] and falling:raise ValueError('Key weights are not unimodal.')
        if w>p[peak]:peak=i
    return peak


def dominating_window(p,indices,peak=None):
    """Proof witness: a contiguous word componentwise dominates this subsequence."""
    if peak is None:peak=unimodal_peak(p)
    assert all(0<=x<len(p) for x in indices)
    assert all(a<b for a,b in zip(indices,indices[1:]))
    k=sum(x<=peak for x in indices)
    start=peak-k+1
    assert 0<=start<=len(p)-len(indices)
    return start


def ruler_windows(p,stats=None):
    """All perfect-ruler window arrays, in O(n log(n+1)) total arithmetic work."""
    if stats is None:stats=Counter()
    n=len(p);previous=[0]*(n+1);h=1;c=1
    stats['window_base_entries']+=n+1
    while c<=n:
        shift=1<<(h-1)
        values=[]
        for a in range(n-c+1):
            values.append(previous[a]+previous[a+shift]+(h-1)*p[a+shift-1])
            stats['ruler_window_updates']+=1
        yield h,values
        previous=values;h+=1;c=2*c+1


class RangeMaximum:
    def __init__(self,values,stats):
        self.stats=stats;self.size=1
        while self.size<len(values):self.size*=2
        self.values=values
        self.tree=[None]*(2*self.size)
        for i in range(len(values)):self.tree[self.size+i]=i
        for i in range(self.size-1,0,-1):
            self.tree[i]=self.better(self.tree[2*i],self.tree[2*i+1])
            stats['unimodal_range_build_nodes']+=1
        stats['unimodal_range_allocated_slots']+=len(self.tree)
    def better(self,a,b):
        if a is None:return b
        if b is None:return a
        self.stats['unimodal_range_value_comparisons']+=1
        if self.values[a]>self.values[b]:return a
        if self.values[b]>self.values[a]:return b
        return min(a,b)
    def query(self,a,b):
        assert 0<=a<=b<len(self.values)
        a+=self.size;b+=self.size+1;best=None
        while a<b:
            if a%2:best=self.better(best,self.tree[a]);a+=1
            if b%2:b-=1;best=self.better(best,self.tree[b])
            a//=2;b//=2;self.stats['unimodal_range_query_levels']+=1
        self.stats['unimodal_range_queries']+=1
        return self.values[best],best


class UnimodalSpanIndex:
    """O(1) unimodality tests after a single scan of arbitrary key weights."""
    def __init__(self,p,stats=None):
        self.n=len(p);self.stats=Counter() if stats is None else stats
        self.bad=[];last_fall=-1;bad=-1
        for j in range(self.n-1):
            if p[j]>p[j+1]:last_fall=j
            elif p[j]<p[j+1]:bad=max(bad,last_fall)
            self.bad.append(bad);self.stats['unimodal_span_index_entries']+=1
    def query(self,a,b):
        assert 0<=a<=b<=self.n
        self.stats['unimodal_span_queries']+=1
        return b-a<=1 or self.bad[b-2]<a


class WindowEnvelope:
    """Contiguous-window upper costs for arbitrary keys; exact on unimodal spans.

The cores belong to this envelope. certified_cores retains exactly its
entries with unimodal outer spans, and equals the original core on that set.
"""
    def __init__(self,p,q=None,stats=None):
        self.stats=Counter() if stats is None else stats
        self.p=list(p);self.n=len(p)
        assert self.n and all(x>=0 for x in p)
        self.span=UnimodalSpanIndex(p,self.stats)
        self.q=[0]*(self.n+1) if q is None else list(q)
        assert len(self.q)==self.n+1 and all(x>=0 for x in self.q)
        self.pp=[0];self.qp=[0]
        for x in p:self.pp.append(self.pp[-1]+x);self.stats['unimodal_mass_prefix_entries']+=1
        for x in self.q:self.qp.append(self.qp[-1]+x);self.stats['unimodal_mass_prefix_entries']+=1
        self.windows={};self.ranges={};self.cores={};self.certified_cores={}
        for h,values in ruler_windows(p,self.stats):
            c=(1<<h)-1
            self.windows[h]=values;self.ranges[h]=RangeMaximum(values,self.stats)
            self.cores[h]={(a,c+b-1):d for a,b,d in range_max_core(values,self.stats)}
            assert len(self.cores[h])<=max(0,self.n-c-1)
            self.stats['unimodal_core_outputs']+=len(self.cores[h])
            self.certified_cores[h]={(i,j):d for (i,j),d in self.cores[h].items() if self.span.query(i,j+1)}
    def score(self,h,i,j):
        c=(1<<h)-1
        assert h in self.windows and 0<=i<j<=self.n and j-i>=c
        return self.ranges[h].query(i,j-c)
    def upper_layer(self,h,i,j,M):
        reward,start=self.score(h,i,j);c=(1<<h)-1
        mass=self.pp[j]-self.pp[i]+self.qp[j+1]-self.qp[i]
        return M*(j-i-c)+h*mass-reward,start

    def layer(self,h,i,j,M):
        if not self.span.query(i,j):raise ValueError('This interval is not certified unimodal.')
        return self.upper_layer(h,i,j,M)


class UnimodalAbove(WindowEnvelope):
    """Exact cores and above-capacity interval values for a globally unimodal input."""
    def __init__(self,p,q=None,stats=None):
        if stats is None:stats=Counter()
        self.peak=unimodal_peak(p,stats)
        super().__init__(p,q,stats)
        assert self.cores==self.certified_cores
