#!/usr/bin/env python3
"""Root-range min-plus products without repeated full boundary arrays.

For a finite square Monge matrix C, index min_r C(i,r)+C(r+1,j)
on every node of a balanced hierarchy of root ranges. Each density is
assigned to at most one range per depth in each factor.
"""
from collections import Counter
from core_monge import Monge,multiply


class PrefixIndex:
    def __init__(self,matrix):
        self.top=matrix.top;self.left=matrix.left;self.width=matrix.q
        self.stats=matrix.stats;self.nodes=[(0,0,0)];self.versions=[0]
        for row in matrix.rows:
            root=self.versions[-1]
            for j,value in row:root=self.add(root,0,self.width,j,value)
            self.versions.append(root);self.stats['range_index_versions']+=1
    def add(self,node,lo,hi,j,value):
        left,right,total=self.nodes[node]
        if hi-lo>1:
            mid=(lo+hi)//2
            if j<mid:left=self.add(left,lo,mid,j,value)
            else:right=self.add(right,mid,hi,j,value)
        self.nodes.append((left,right,total+value));self.stats['range_index_nodes']+=1
        return len(self.nodes)-1
    def query(self,i,j,stats=None):
        stats=self.stats if stats is None else stats
        node=self.versions[i];lo=0;hi=self.width;total=0
        while node and lo<j:
            stats['range_index_query_nodes']+=1
            left,right,value=self.nodes[node]
            if hi<=j:total+=value;break
            mid=(lo+hi)//2
            if j<=mid:node=left;hi=mid
            else:total+=self.nodes[left][2];node=right;lo=mid
        stats['range_entry_queries']+=1
        return self.left[i]+self.top[j]-self.top[0]-total


def floor_index(values,x,stats):
    lo=0;hi=len(values)
    while lo<hi:
        mid=(lo+hi)//2;stats['range_coordinate_comparisons']+=1
        if values[mid]<=x:lo=mid+1
        else:hi=mid
    return lo-1


class Coordinate:
    def __init__(self,value,stats):self.value=value;self.stats=stats
    def __lt__(self,other):
        self.stats['range_sort_comparisons']+=1
        return self.value<other.value


def unique_sorted(values,stats):
    result=[]
    for item in sorted(Coordinate(x,stats) for x in values):
        if not result or result[-1]!=item.value:result.append(item.value)
        stats['range_unique_items']+=1
    return result


class Node:
    pass


class RootRanges:
    def __init__(self,matrix):
        assert matrix.p==matrix.q and matrix.p>=2
        self.n=matrix.p-1;self.stats=matrix.stats;self.base=PrefixIndex(matrix)
        self.nodes=[];self.core_by_depth=Counter()
        ea=[x for x in matrix.entries if x[1]<self.n-1]
        eb=[x for x in matrix.entries if x[0]>=1]
        self.stats['range_initial_core_scans']+=2*matrix.k
        self.root=self.build(0,self.n,ea,eb,0)
    def build(self,lo,hi,ea,eb,depth):
        stats=self.stats;node=Node();node.lo=lo;node.hi=hi
        node.rr=unique_sorted([0]+[a+1 for a,b,v in ea],stats)
        node.cc=unique_sorted([0]+[b+1 for a,b,v in eb],stats)
        node.rowbase=[self.base.query(i,lo) for i in node.rr]
        node.colbase=[self.base.query(lo+1,j) for j in node.cc]
        aa=Monge(self.base.top[lo:hi],node.rowbase,
                 [(floor_index(node.rr,a,stats),b-lo,v) for a,b,v in ea],stats)
        bb=Monge(node.colbase,self.base.left[lo+1:hi+1],
                 [(a-lo-1,floor_index(node.cc,b,stats),v) for a,b,v in eb],stats)
        product,witness=multiply(aa,bb)
        node.product_core=product.k;node.index=PrefixIndex(product)
        assert node.product_core<=len(ea)+len(eb)
        self.core_by_depth[depth]+=len(ea)+len(eb)
        stats['range_factor_core_entries']+=len(ea)+len(eb)
        stats['range_product_core_entries']+=node.product_core
        stats['range_inner_slots']+=hi-lo;stats['range_product_nodes']+=1
        self.nodes.append(node)
        del aa,bb,product,witness
        node.left=node.right=None
        if hi-lo>1:
            mid=(lo+hi)//2;al=[];ar=[];bl=[];br=[]
            for entry in ea:
                a,b,v=entry;stats['range_partition_core_visits']+=1
                if b<mid-1:al.append(entry)
                elif b>=mid:ar.append(entry)
            for entry in eb:
                a,b,v=entry;stats['range_partition_core_visits']+=1
                if a<mid:bl.append(entry)
                elif a>=mid+1:br.append(entry)
            node.left=self.build(lo,mid,al,bl,depth+1)
            node.right=self.build(mid,hi,ar,br,depth+1)
        return node
    def value(self,node,i,j,stats):
        x=floor_index(node.rr,i,stats);y=floor_index(node.cc,j,stats)
        stats['range_minimum_queries']+=1
        return (node.index.query(x,y,stats)+self.base.query(i,node.lo,stats)-node.rowbase[x]
                +self.base.query(node.lo+1,j,stats)-node.colbase[y])
    def below(self,i,j,threshold,stats,valid=None):
        """Yield exactly the qualifying root positions, in increasing order."""
        lo,hi=(i,j) if valid is None else valid
        stack=[self.root]
        while stack:
            node=stack.pop();stats['range_enumeration_nodes']+=1
            if node.hi<=lo or hi<=node.lo:
                stats['range_disjoint_prunes']+=1;continue
            if self.value(node,i,j,stats)>threshold:
                stats['range_threshold_prunes']+=1;continue
            if node.hi-node.lo==1:
                stats['range_emitted_roots']+=1;yield node.lo
            else:stack.extend((node.right,node.left))
