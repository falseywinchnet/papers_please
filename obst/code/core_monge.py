#!/usr/bin/env python3
"""Condensed Monge min-plus multiplication, with exact witnesses.

Implements the compression/split/staircase/decompression construction of
Gawrychowski, Gorbachev, Kociumaka, ESA 2025 (arXiv:2408.04613v2).
Their algorithm and theorem are prior work. No dense matrix is allocated.
Witness maps here are ordinary integer arrays, not succinct bitvectors;
their aggregate storage can have an extra logarithmic factor.
"""
from collections import Counter


class Monge:
    """Top row, left column, and positive discrete second differences."""
    def __init__(self, top, left, entries, stats):
        self.top=list(top); self.left=list(left); self.stats=stats
        self.p=len(left); self.q=len(top)
        assert self.p and self.q and top[0]==left[0]
        # Two bucket passes provide row/column ordered lists in linear work.
        cols=[[] for _ in range(self.q-1)]
        rows=[[] for _ in range(self.p-1)]
        stats['boundary_and_bucket_slots']+=2*(self.p+self.q)-2
        for i,j,v in entries:
            assert 0<=i<self.p-1 and 0<=j<self.q-1 and v>0
            cols[j].append((i,v));stats['core_visits']+=1
        for j,items in enumerate(cols):
            for i,v in items:
                rows[i].append((j,v));stats['core_visits']+=1
        self.rows=[];self.cols=[[] for _ in range(self.q-1)];self.entries=[]
        for i,items in enumerate(rows):
            merged=[]
            for j,v in items:
                if merged and merged[-1][0]==j:
                    merged[-1]=(j,merged[-1][1]+v)
                else:merged.append((j,v))
                stats['core_visits']+=1
            self.rows.append(merged)
            for j,v in merged:
                self.cols[j].append((i,v));self.entries.append((i,j,v))
                stats['core_records_built']+=1
        self.k=len(self.entries)

    def row(self,i):
        delta=[0]*self.q
        self.stats['boundary_sweep_slots']+=2*self.q
        for a,b,v in self.entries:
            if a<i:delta[b]+=v
            self.stats['core_visits']+=1
        result=[];running=0
        for j,x in enumerate(self.top):
            result.append(self.left[i]+x-self.top[0]-running)
            running+=delta[j]
        return result

    def col(self,j):
        delta=[0]*self.p
        self.stats['boundary_sweep_slots']+=2*self.p
        for a,b,v in self.entries:
            if b<j:delta[a]+=v
            self.stats['core_visits']+=1
        result=[];running=0
        for i,x in enumerate(self.left):
            result.append(self.top[j]+x-self.left[0]-running)
            running+=delta[i]
        return result

    def right(self,i,j,value):
        """Adjacent entry (i,j+1); one core column is scanned."""
        total=0
        for a,v in self.cols[j]:
            self.stats['adjacent_core_visits']+=1
            if a<i:total+=v
        self.stats['adjacent_steps']+=1
        return value+self.top[j+1]-self.top[j]-total

    def up(self,i,j,value):
        """Entry (i,j) from (i+1,j); one core row is scanned."""
        total=0
        for b,v in self.rows[i]:
            self.stats['adjacent_core_visits']+=1
            if b<j:total+=v
        self.stats['adjacent_steps']+=1
        return value-self.left[i+1]+self.left[i]+total

    def select(self, rr, cc):
        """Any increasing nonempty row/column subsets, in linear input work."""
        assert rr and cc
        rm=edge_map(self.p,rr);cm=edge_map(self.q,cc)
        self.stats['selection_map_slots']+=self.p+self.q
        topfull=self.row(rr[0]);leftfull=self.col(cc[0]);entries=[]
        for i,j,v in self.entries:
            self.stats['core_visits']+=1
            if rm[i]>=0 and cm[j]>=0:entries.append((rm[i],cm[j],v))
        return Monge([topfull[j] for j in cc],[leftfull[i] for i in rr],entries,self.stats)

    def value_reference(self,i,j):
        """Slow inspection only. Never called by multiplication or OBST."""
        return self.left[i]+self.top[j]-self.top[0]-sum(v for a,b,v in self.entries if a<i and b<j)


def edge_map(size,chosen):
    out=[-1]*size
    for k,(a,b) in enumerate(zip(chosen,chosen[1:])):
        for i in range(a,b):out[i]=k
    return out


def group_map(size,chosen):
    assert chosen[0]==0
    out=[0]*size
    for k,a in enumerate(chosen):
        b=chosen[k+1] if k+1<len(chosen) else size
        for i in range(a,b):out[i]=k
    return out


class Witness:
    __slots__=('rowmap','colmap','inner','cut','border','left','right','base','stats')
    def __init__(self,rowmap,colmap,inner,stats,base=None,cut=None,border=None,left=None,right=None):
        self.rowmap=rowmap;self.colmap=colmap;self.inner=inner;self.stats=stats
        self.base=base;self.cut=cut;self.border=border;self.left=left;self.right=right
        stats['witness_integer_slots']+=len(rowmap)+len(colmap)+len(inner)+(len(border) if border else 0)
        stats['witness_nodes']+=1

    def query(self,i,j):
        self.stats['witness_query_nodes']+=1
        i=self.rowmap[i];j=self.colmap[j]
        if self.base is not None:k=self.base
        elif j<=self.border[i]:k=self.left.query(i,j)
        else:k=self.cut+self.right.query(i,j)
        return self.inner[k]


def compress(a,b):
    assert a.q==b.p
    stats=a.stats
    rr=[0]+[i+1 for i,x in enumerate(a.rows) if x]
    cc=[0]+[j+1 for j,x in enumerate(b.cols) if x]
    bounds=[0]+[j+1 for j in range(a.q-1) if a.cols[j] or b.rows[j]]+[a.q]
    ss=[]
    for lo,hi in zip(bounds,bounds[1:]):
        best=lo;value=a.top[lo]+b.left[lo]
        for j in range(lo+1,hi):
            v=a.top[j]+b.left[j];stats['inner_representative_comparisons']+=1
            if v<value:best,value=j,v
        ss.append(best)
    stats['compression_dimension_scans']+=a.p+a.q+b.q
    aa=a.select(rr,ss);bb=b.select(ss,cc)
    assert aa.k==a.k and bb.k==b.k
    assert aa.p<=aa.k+1 and bb.q<=bb.k+1 and aa.q<=aa.k+bb.k+1
    return aa,bb,rr,cc,ss


def merge_products(a,b):
    """Minimum of left/right products separated by a monotone staircase."""
    assert a.p==b.p and a.q==b.q
    p,q=a.p,a.q;stats=a.stats
    i=p-1;j=-1
    # Only the valid corners of the moving 2x2 square are retained.
    ga={(0,1):a.left[i]};gb={(0,1):b.left[i]}
    border=[-1]*p;entries=[]
    def horizontal(matrix,g):
        out={}
        for row in (0,1):
            if (row,1) in g:
                out[row,0]=g[row,1]
                if j+2<q:out[row,1]=matrix.right(i+row,j+1,g[row,1])
        return out
    def vertical(matrix,g):
        out={}
        for col in (0,1):
            if (0,col) in g:
                out[1,col]=g[0,col]
                if i>0:out[0,col]=matrix.up(i-1,j+col,g[0,col])
        return out
    while i>=0:
        stats['staircase_steps']+=1
        if i<p-1 and 0<=j<q-1:
            vals={key:min(ga[key],gb[key]) for key in ((0,0),(0,1),(1,0),(1,1))}
            v=vals[0,1]+vals[1,0]-vals[0,0]-vals[1,1]
            assert v>=0
            if v:entries.append((i,j,v))
            stats['border_density_evaluations']+=1
        if j+1<q and ga[0,1]<=gb[0,1]:
            ga=horizontal(a,ga);gb=horizontal(b,gb);j+=1
        else:
            border[i]=j
            ga=vertical(a,ga);gb=vertical(b,gb);i-=1
    assert all(border[i]>=border[i+1] for i in range(p-1))
    for i,j,v in a.entries:
        stats['core_visits']+=1
        if j<border[i+1]:entries.append((i,j,v))
    for i,j,v in b.entries:
        stats['core_visits']+=1
        if j>border[i]:entries.append((i,j,v))
    top=[min(x,y) for x,y in zip(a.top,b.top)]
    left=[min(x,y) for x,y in zip(a.left,b.left)]
    stats['merge_boundary_cells']+=p+q
    return Monge(top,left,entries,stats),border


def multiply(a,b,depth=0):
    """Condensed min-plus product and exact leftmost witnesses."""
    assert a.stats is b.stats and a.q==b.p
    stats=a.stats;stats['product_calls']+=1
    stats['maximum_product_depth']=max(stats['maximum_product_depth'],depth)
    aa,bb,rr,cc,ss=compress(a,b)
    rowmap=group_map(a.p,rr);colmap=group_map(b.q,cc)
    if aa.p==1 and bb.q==1:
        value,k=min((x+y,k) for k,(x,y) in enumerate(zip(aa.top,bb.left)))
        stats['scalar_candidates']+=aa.q
        c=Monge([value],[value],[],stats)
        witness=Witness(rowmap,colmap,ss,stats,base=k)
    else:
        weights=[0]*(aa.q-1)
        for _,j,_ in aa.entries:weights[j]+=1;stats['core_visits']+=1
        for i,_,_ in bb.entries:weights[i]+=1;stats['core_visits']+=1
        total=aa.k+bb.k;prefix=0;cut=1
        for m in range(1,aa.q):
            stats['split_index_scans']+=1
            if prefix>total//2:break
            cut=m;prefix+=weights[m-1]
        al=aa.select(list(range(aa.p)),list(range(cut)))
        bl=bb.select(list(range(cut)),list(range(bb.q)))
        ar=aa.select(list(range(aa.p)),list(range(cut,aa.q)))
        br=bb.select(list(range(cut,bb.p)),list(range(bb.q)))
        assert al.k+bl.k<=total//2 and ar.k+br.k<=total//2
        cl,wl=multiply(al,bl,depth+1);cr,wr=multiply(ar,br,depth+1)
        c,border=merge_products(cl,cr)
        witness=Witness(rowmap,colmap,ss,stats,cut=cut,border=border,left=wl,right=wr)
    # Decompress output dimensions; dropped rows/columns differ by constants.
    top=[c.top[colmap[j]]+b.top[j]-b.top[cc[colmap[j]]] for j in range(b.q)]
    left=[c.left[rowmap[i]]+a.left[i]-a.left[rr[rowmap[i]]] for i in range(a.p)]
    entries=[(rr[i+1]-1,cc[j+1]-1,v) for i,j,v in c.entries]
    stats['decompression_boundary_cells']+=a.p+b.q
    stats['core_visits']+=len(c.entries)
    result=Monge(top,left,entries,stats)
    assert result.k<=2*(a.k+b.k)
    return result,witness
