"""Full mixed forward transitions with a scalar prefix carry.

Endpoint dominance is required. Each transition uses O(h^2 D^2) arithmetic
and dictionary operations on a D-node input, without generic min merges.
The bound does not control diagram growth over all n transitions.
"""
from collections import Counter
from slot_dag_skyline import SkylineDiagram
from slot_vector import normalize
from slot_records import sparse_repair


def finite_min(*values):
    finite=[x for x in values if x is not None]
    return min(finite) if finite else None


class ForwardDiagram(SkylineDiagram):
    def first(self,ref):
        return None if ref is None or self.first_values[ref[1]] is None else ref[0]+self.first_values[ref[1]]

    def replace_first(self,ref,value,depth):
        self.stats['forward_replace_visits']+=1
        if depth==0:return None if value is None else (value,0)
        left,right=self.children(ref)
        return self.make(depth,self.replace_first(left,value,depth-1),right)

    def transition(self,ref,weight,gap,context_observer=None):
        summaries={};contexts={};templates={0:None}
        def template(d):
            if d not in templates:
                low=template(d-1)
                templates[d]=self.make(d,low,self.replace_first(low,-(weight+gap)*(d-1),d-1))
            return templates[d]
        # Summary excludes the block's first point, whose global valuation
        # need not equal the local zero convention.
        def summary(r,d):
            self.stats['forward_summary_calls']+=1
            if r is None or d==0:return None
            node=r[1]
            if node not in summaries:
                self.stats['forward_summary_expansions']+=1
                left,right=self.children((0,node));middle=self.first(right)
                summaries[node]=finite_min(summary(left,d-1),summary(right,d-1),
                                           None if middle is None else middle-gap*(d-1))
            value=summaries[node]
            return None if value is None else r[0]+value
        def build(r,d,p):
            self.stats['forward_calls']+=1
            if d==0:return None
            if r is None or (p is not None and p<=r[0]):
                self.stats['forward_pruned_blocks']+=1
                return None if p is None else self.offset(template(d),p)
            base,node=r;relative=None if p is None else p-base
            key=node,relative
            if key not in contexts:
                self.stats['forward_contexts']+=1
                left,right=self.children((0,node));middle=self.first(right)
                carry=finite_min(relative,None if left is None else left[0],middle)
                boundary=finite_min(None if relative is None else relative-gap*(d-1),summary(left,d-1))
                if boundary is not None:boundary-=weight*(d-1)
                low=build(left,d-1,relative);high=build(right,d-1,carry)
                contexts[key]=self.make(d,low,self.replace_first(high,boundary,d-1))
            return self.offset(contexts[key],base)
        result=build(ref,self.h,self.first(ref))
        if context_observer is not None:context_observer(contexts,summaries)
        return result


def solve(p,q,h,stats=None,observer=None):
    stats=Counter() if stats is None else stats
    w,g,constant=normalize(p,q);n=len(w)
    if n>(1<<h)-1:return None
    manager=ForwardDiagram(h,stats);old=manager.point(h,0)
    history=[old];stages=[]
    for k,weight in enumerate(w):
        new=manager.transition(old,weight,g[k])
        if observer is not None:observer(k+1,manager,new)
        stages.append(manager.reachable([new]));history.append(new);old=new
    value,b=manager.predecessor(old,1<<h);slots=[b]
    for k in range(n-1,0,-1):
        _,b=manager.predecessor(history[k],b,g[k]);slots.append(b)
    slots.reverse();tree=sparse_repair(slots,h,stats)
    stats['dag_all_nodes']=len(manager.nodes);stats['dag_history_nodes']=manager.reachable(history)
    return dict(cost=h*(sum(w)+sum(g))+value+constant,tree=tree,slots=slots,
                stage_nodes=stages,height=h)
