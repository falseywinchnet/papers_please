"""Full mixed OBST on additive diagrams excluding each block's first entry.

A node stores left interior, midpoint scalar, and right interior. Boundary
assembly is constant work; reset paths give O(h(D+1)) work per update.
All-stage diagram growth remains open. None denotes positive infinity.
"""
from collections import Counter
from slot_vector import normalize
from slot_records import nu


def finite_min(*values):
    finite=[v for v in values if v is not None]
    return min(finite) if finite else None


class PuncturedDiagram:
    def __init__(self,h,stats=None):
        self.h=h;self.stats=Counter() if stats is None else stats
        self.nodes=[];self.unique={}

    def offset(self,ref,amount):return None if ref is None else (ref[0]+amount,ref[1])

    def make(self,depth,left,middle,right):
        self.stats['punctured_make_calls']+=1
        base=finite_min(None if left is None else left[0],middle,None if right is None else right[0])
        if base is None:return None
        key=depth,self.offset(left,-base),None if middle is None else middle-base,self.offset(right,-base)
        if key not in self.unique:
            self.unique[key]=len(self.nodes);self.nodes.append(key);self.stats['punctured_created_nodes']+=1
        return base,self.unique[key]

    def children(self,ref):
        if ref is None:return None,None,None
        base,node=ref;_,l,c,r=self.nodes[node]
        return self.offset(l,base),None if c is None else c+base,self.offset(r,base)

    def from_values(self,values):
        assert len(values)==1<<self.h
        def visit(a,d):
            if d==0:return None
            mid=a+(1<<(d-1))
            return self.make(d,visit(a,d-1),values[mid],visit(mid,d-1))
        return visit(0,self.h)

    def from_standard(self,old,ref):
        cache={}
        def visit(r):
            if r is None:return None
            base,node=r;d=old.nodes[node][0]
            if d==0:return None
            if node not in cache:
                l,rr=old.children((0,node))
                cache[node]=self.make(d,visit(l),old.first(rr),visit(rr))
            return self.offset(cache[node],base)
        return visit(ref)

    def value(self,ref,position):
        if position==0:return None
        d=self.h
        while ref is not None:
            l,c,r=self.children(ref);d-=1;mid=1<<d
            if position==mid:return c
            if position<mid:ref=l
            else:position-=mid;ref=r
        return None

    def reachable_set(self,roots):
        seen=set();pending=[r[1] for r in roots if r is not None]
        while pending:
            node=pending.pop()
            if node in seen:continue
            seen.add(node);_,l,_,r=self.nodes[node]
            pending.extend(x[1] for x in (l,r) if x is not None)
        return seen

    def reachable(self,roots):return len(self.reachable_set(roots))

    def transition(self,ref,weight,gap,first=None,observer=None):
        contexts={};summaries={};templates={0:None}
        def template(d):
            self.stats['punctured_template_calls']+=1
            if d not in templates:
                low=template(d-1)
                templates[d]=self.make(d,low,-(weight+gap)*(d-1),low)
            return templates[d]
        def summary(r):
            self.stats['punctured_summary_calls']+=1
            if r is None:return None
            base,node=r
            if node not in summaries:
                self.stats['punctured_summary_expansions']+=1
                d=self.nodes[node][0];l,c,rr=self.children((0,node))
                summaries[node]=finite_min(summary(l),None if c is None else c-gap*(d-1),summary(rr))
            return None if summaries[node] is None else base+summaries[node]
        def build(r,d,p):
            self.stats['punctured_build_calls']+=1
            if d==0:return None
            if r is None or (p is not None and p<=r[0]):
                self.stats['punctured_pruned_blocks']+=1
                return None if p is None else self.offset(template(d),p)
            base,node=r;relative=None if p is None else p-base;key=node,relative
            if key not in contexts:
                self.stats['punctured_contexts']+=1
                l,c,rr=self.children((0,node))
                rightp=finite_min(relative,None if l is None else l[0],c)
                boundary=finite_min(None if relative is None else relative-gap*(d-1),summary(l))
                if boundary is not None:boundary-=weight*(d-1)
                contexts[key]=self.make(d,build(l,d-1,relative),boundary,build(rr,d-1,rightp))
            return self.offset(contexts[key],base)
        result=build(ref,self.h,first)
        if observer is not None:observer(contexts,summaries,templates)
        return result

    def predecessor(self,ref,stop,gap=0):
        assert 0<stop<=1<<self.h and gap>=0
        e=(stop&-stop).bit_length()-1;bits=stop-1;pos=0;best=None
        for d in range(self.h-1,-1,-1):
            self.stats['punctured_trace_steps']+=1
            l,c,r=self.children(ref)
            if bits>>d&1:
                pos+=1<<d;ref=r
                if c is not None:
                    candidate=c-gap*min(d,e),pos
                    best=candidate if best is None else min(best,candidate)
                    self.stats['punctured_trace_candidates']+=1
            else:ref=l
        return best


def sparse_repair(slots, h, stats):
    """Delete unwanted ancestors, enumerated in order without comparison sorting."""
    kept = set()
    for slot in slots:
        x = slot
        while x not in kept:
            kept.add(x); stats['record_ancestor_nodes'] += 1
            d = nu(x)
            if d == h-1: break
            x = x-(1 << d) if x & (1 << (d+1)) else x+(1 << d)
    labels = []; todo = [(1 << (h-1), h-1, False)]
    while todo:
        x, d, ready = todo.pop()
        stats['punctured_ancestor_walk_visits'] += 1
        if ready:
            labels.append(x)
            continue
        if d and x+(1 << (d-1)) in kept:
            todo.append((x+(1 << (d-1)), d-1, False))
        todo.append((x, d, True))
        if d and x-(1 << (d-1)) in kept:
            todo.append((x-(1 << (d-1)), d-1, False))
    assert len(labels) == len(kept)
    count = len(labels)
    index = {x: i+1 for i, x in enumerate(labels)}
    key = [0]+labels; where = dict(index); rank = {x: i for i, x in enumerate(slots)}
    left = [0]*(count+1); right = [0]*(count+1); parent = [0]*(count+1)
    prev = [i-1 for i in range(count+1)]; nxt = [i+1 for i in range(count+1)]; nxt[count] = 0
    root = index[1 << (h-1)]
    for i, x in enumerate(labels, 1):
        d = nu(x)
        if d:
            left[i] = index.get(x-(1 << (d-1)), 0)
            right[i] = index.get(x+(1 << (d-1)), 0)
            if left[i]: parent[left[i]] = i
            if right[i]: parent[right[i]] = i
    for label in labels:
        if label in rank: continue
        node = where[label]
        if left[node] and right[node]:
            dead = nxt[node]; moved = key[dead]
            key[node] = moved; where[moved] = node
            assert not left[dead]
        else: dead = node
        child = left[dead] or right[dead]; par = parent[dead]
        if not par: root = child
        elif left[par] == dead: left[par] = child
        else: assert right[par] == dead; right[par] = child
        if child: parent[child] = par
        a, b = prev[dead], nxt[dead]
        if a > 0: nxt[a] = b
        if b: prev[b] = a
        where[label] = 0; stats['record_deleted_ancestors'] += 1
    stack = [(root, False)]; built = {}
    while stack:
        node, ready = stack.pop()
        if not node: continue
        if ready:
            built[node] = rank[key[node]], built.pop(left[node], None), built.pop(right[node], None)
            stats['record_output_nodes'] += 1
        else: stack.extend(((node, True), (right[node], False), (left[node], False)))
    return built[root]


def solve(p,q,h,stats=None,observer=None):
    stats=Counter() if stats is None else stats
    w,g,constant=normalize(p,q);n=len(w)
    if n>(1<<h)-1:return None
    manager=PuncturedDiagram(h,stats);ref=None;history=[ref];stages=[]
    for k,weight in enumerate(w):
        ref=manager.transition(ref,weight,g[k],0 if k==0 else None)
        if observer is not None:observer(k+1,manager,ref)
        history.append(ref);stages.append(manager.reachable([ref]))
    before=len(manager.nodes);trace=stats['punctured_trace_steps']
    value,b=manager.predecessor(ref,1<<h);slots=[b]
    for k in range(n-1,0,-1):
        _,b=manager.predecessor(history[k],b,g[k]);slots.append(b)
    slots.reverse();assert len(manager.nodes)==before
    assert stats['punctured_trace_steps']-trace==n*h
    tree=sparse_repair(slots,h,stats)
    stats['punctured_all_nodes']=len(manager.nodes);stats['punctured_history_nodes']=manager.reachable(history)
    return dict(cost=h*(sum(w)+sum(g))+value+constant,tree=tree,slots=slots,stage_nodes=stages,height=h)
