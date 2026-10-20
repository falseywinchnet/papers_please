"""Full mixed DAG construction with O(h) skyline predecessor queries.

The prefix arithmetic is the checkpoint-58 construction. Nonnegative weights
imply endpoint dominance, allowing traceback without mask/add/range operations.
"""
from collections import Counter
from slot_dag import Diagram
from slot_vector import normalize
from slot_records import sparse_repair


class SkylineDiagram(Diagram):
    def __init__(self,h,stats=None):
        super().__init__(h,stats)
        self.first_values=[0]

    def make(self,depth,left,right):
        ref=super().make(depth,left,right)
        if len(self.nodes)>len(self.first_values):
            assert len(self.nodes)==len(self.first_values)+1
            _,l,_=self.nodes[-1]
            value=None if l is None or self.first_values[l[1]] is None else l[0]+self.first_values[l[1]]
            self.first_values.append(value)
            self.stats['skyline_first_value_nodes']+=1
        return ref

    def predecessor(self,ref,stop,gap=0):
        """Minimize F(a)-gap*min(v(a),v(stop)) for 0<=a<stop.

        Requires the actual prefix endpoint dominance property. With stop=2^h
        and gap=0 this finds the global minimum. Ties choose the earliest
        skyline candidate, not necessarily the earliest minimizing address.
        """
        assert 0<stop<=1<<self.h and gap>=0
        e=(stop&-stop).bit_length()-1
        zero=None if ref is None or self.first_values[ref[1]] is None else ref[0]+self.first_values[ref[1]]
        best=None if zero is None else (zero,0)
        pos=0;bits=stop-1
        for d in range(self.h-1,-1,-1):
            self.stats['skyline_path_steps']+=1
            left,right=self.children(ref)
            if bits>>d&1:
                pos+=1<<d;ref=right
                if ref is not None and self.first_values[ref[1]] is not None:
                    value=ref[0]+self.first_values[ref[1]]-gap*min(d,e)
                    candidate=(value,pos)
                    best=candidate if best is None else min(best,candidate)
                    self.stats['skyline_candidates']+=1
            else:ref=left
        return best


def solve(p,q,h,stats=None,observer=None):
    stats=Counter() if stats is None else stats
    w,g,constant=normalize(p,q);n=len(w)
    if n>(1<<h)-1:return None
    manager=SkylineDiagram(h,stats)
    old=manager.point(h,0);history=[old];stages=[]
    masks=[manager.mask(d) for d in range(h)] if any(g) else []
    for k,weight in enumerate(w):
        if g[k]==0:
            reward=manager.valuation_function([-weight*d for d in range(h)])
            new=manager.add(manager.prefix(old,h),reward,h)
        else:
            new=None
            for d in range(h):
                subset=manager.add(old,masks[d],h)
                reward=manager.valuation_function([-weight*e-g[k]*min(d,e) for e in range(h)])
                candidate=manager.add(manager.prefix(subset,h),reward,h)
                new=manager.minimum(new,candidate,h)
                stats['dag_gap_classes']+=1
        if observer is not None:observer(k+1,manager,new)
        stages.append(manager.reachable([new]));history.append(new);old=new
    before=stats.copy();nodes_before=len(manager.nodes)
    value,b=manager.predecessor(old,1<<h);slots=[b]
    for k in range(n-1,0,-1):
        _,b=manager.predecessor(history[k],b,g[k]);slots.append(b)
    slots.reverse()
    assert len(manager.nodes)==nodes_before
    assert stats['skyline_path_steps']-before['skyline_path_steps']==n*h
    stats['skyline_trace_new_nodes']=len(manager.nodes)-nodes_before
    tree=sparse_repair(slots,h,stats)
    stats['dag_all_nodes']=len(manager.nodes)
    stats['dag_history_nodes']=manager.reachable(history)
    return dict(cost=h*(sum(w)+sum(g))+value+constant,tree=tree,slots=slots,
                stage_nodes=stages,height=h)
