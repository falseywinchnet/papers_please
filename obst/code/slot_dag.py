"""Exact mixed slot DP on additive-normalized binary decision diagrams.

No bound on diagram size is assumed. Counters include all intermediate
nodes and recursive operations, not merely the final live representation.
"""
from collections import Counter
from slot_vector import normalize
from slot_records import sparse_repair


class Diagram:
    def __init__(self, h, stats=None):
        self.h = h
        self.stats = Counter() if stats is None else stats
        self.nodes = [(0, None, None)]
        self.maxima = [0]
        self.unique = {}
        self.constants = {0: (0, 0)}
        self.minimum_cache = {}
        self.add_cache = {}
        self.prefix_cache = {}

    def offset(self, ref, value):
        return None if ref is None else (ref[0]+value, ref[1])

    def make(self, depth, left, right):
        self.stats['dag_make_calls'] += 1
        if left is None and right is None:
            return None
        base = min(x[0] for x in (left, right) if x is not None)
        left, right = self.offset(left, -base), self.offset(right, -base)
        key = depth, left, right
        if key not in self.unique:
            self.unique[key] = len(self.nodes)
            self.nodes.append(key)
            maxima = [None if x is None or self.maxima[x[1]] is None
                      else x[0]+self.maxima[x[1]] for x in (left, right)]
            self.maxima.append(None if None in maxima else max(maxima))
            self.stats['dag_created_nodes'] += 1
        return base, self.unique[key]

    def constant(self, depth, value=0):
        if depth not in self.constants:
            low = self.constant(depth-1)
            self.constants[depth] = self.make(depth, low, low)
        return self.offset(self.constants[depth], value)

    def point(self, depth, position, value=0):
        if depth == 0:
            return value, 0
        half = 1 << (depth-1)
        low = self.point(depth-1, position % half, value)
        return self.make(depth, low, None) if position < half else self.make(depth, None, low)

    def children(self, ref):
        if ref is None:
            return None, None
        depth, left, right = self.nodes[ref[1]]
        return self.offset(left, ref[0]), self.offset(right, ref[0])

    def minimum(self, a, b, depth):
        self.stats['dag_min_calls'] += 1
        if a is None: return b
        if b is None: return a
        if a[1] == b[1]: return min(a, b)
        ma, mb = self.maxima[a[1]], self.maxima[b[1]]
        if ma is not None and a[0]+ma <= b[0]:
            self.stats['dag_range_prunes'] += 1
            return a
        if mb is not None and b[0]+mb <= a[0]:
            self.stats['dag_range_prunes'] += 1
            return b
        base = min(a[0], b[0])
        a, b = self.offset(a, -base), self.offset(b, -base)
        if a > b: a, b = b, a
        key = depth, a, b
        if key not in self.minimum_cache:
            self.stats['dag_min_expansions'] += 1
            al, ar = self.children(a); bl, br = self.children(b)
            result = self.make(depth, self.minimum(al, bl, depth-1),
                               self.minimum(ar, br, depth-1))
            self.minimum_cache[key] = result
        return self.offset(self.minimum_cache[key], base)

    def add(self, a, b, depth):
        self.stats['dag_add_calls'] += 1
        if a is None or b is None: return None
        base = a[0]+b[0]
        if depth == 0: return base, 0
        ia, ib = sorted((a[1], b[1])); key = depth, ia, ib
        if key not in self.add_cache:
            self.stats['dag_add_expansions'] += 1
            al, ar = self.children((0, ia)); bl, br = self.children((0, ib))
            self.add_cache[key] = self.make(depth, self.add(al, bl, depth-1),
                                          self.add(ar, br, depth-1))
        return self.offset(self.add_cache[key], base)

    def prefix(self, ref, depth):
        """At b return min_{a<b} ref(a); the empty prefix is infinity."""
        self.stats['dag_prefix_calls'] += 1
        if ref is None or depth == 0: return None
        node = ref[1]
        if node not in self.prefix_cache:
            self.stats['dag_prefix_expansions'] += 1
            left, right = self.children((0, node))
            pl, pr = self.prefix(left, depth-1), self.prefix(right, depth-1)
            if left is not None:
                pr = self.minimum(pr, self.constant(depth-1, left[0]), depth-1)
            self.prefix_cache[node] = self.make(depth, pl, pr)
        return self.offset(self.prefix_cache[node], ref[0])

    def valuation_function(self, values):
        """values[d] at valuation d; slot zero also receives values[0]."""
        # Identical (depth,zero) subproblems must be shared before recursion.
        cache = {}
        def memo(depth, zero):
            key = depth, zero
            if key not in cache:
                if depth == 0: result = zero, 0
                else: result = self.make(depth, memo(depth-1, zero),
                                         memo(depth-1, values[depth-1]))
                cache[key] = result
            return cache[key]
        return memo(self.h, values[0])

    def mask(self, d):
        ref = self.make(d+1, None, self.point(d, 0))
        for depth in range(d+2, self.h+1):
            ref = self.make(depth, ref, ref)
        if d == 0:
            ref = self.minimum(ref, self.point(self.h, 0), self.h)
        return ref

    def value(self, ref, position, depth=None):
        depth = self.h if depth is None else depth
        while ref is not None and depth:
            left, right = self.children(ref); depth -= 1
            ref = right if position & (1 << depth) else left
        return None if ref is None else ref[0]

    def range_min(self, ref, stop, depth=None, start=0):
        """Earliest minimizing position strictly before stop."""
        depth = self.h if depth is None else depth
        self.stats['dag_range_visits'] += 1
        if ref is None or start >= stop: return None
        if depth == 0: return ref[0], start
        left, right = self.children(ref); half = 1 << (depth-1)
        if start+(1 << depth) <= stop:
            # The node's offset is its exact finite minimum.
            if left is not None and left[0] == ref[0]:
                return self.range_min(left, stop, depth-1, start)
            return self.range_min(right, stop, depth-1, start+half)
        a = self.range_min(left, stop, depth-1, start)
        b = self.range_min(right, stop, depth-1, start+half)
        return b if a is None else a if b is None else min(a, b)

    def reachable(self, roots):
        seen = set(); pending = [r[1] for r in roots if r is not None]
        while pending:
            node = pending.pop()
            if node in seen: continue
            seen.add(node)
            _, left, right = self.nodes[node]
            pending.extend(r[1] for r in (left, right) if r is not None)
        return len(seen)


def solve(p, q, h, stats=None, observer=None):
    stats = Counter() if stats is None else stats
    w, g, constant = normalize(p, q); n = len(w)
    if n > (1 << h)-1: return None
    manager = Diagram(h, stats)
    old = manager.point(h, 0); history = [old]; stages = []
    masks = [manager.mask(d) for d in range(h)] if any(g) else []
    for k, weight in enumerate(w):
        if g[k] == 0:
            reward = manager.valuation_function([-weight*d for d in range(h)])
            new = manager.add(manager.prefix(old, h), reward, h)
        else:
            new = None
            for d in range(h):
                subset = manager.add(old, masks[d], h)
                reward = manager.valuation_function([-weight*e-g[k]*min(d,e) for e in range(h)])
                candidate = manager.add(manager.prefix(subset, h), reward, h)
                new = manager.minimum(new, candidate, h)
                stats['dag_gap_classes'] += 1
        if observer is not None: observer(k+1, manager, new)
        stages.append(manager.reachable([new])); history.append(new); old = new
    value, b = manager.range_min(old, 1 << h)
    slots = [b]
    for k in range(n-1, 0, -1):
        e = (b & -b).bit_length()-1
        if g[k] == 0:
            _, a = manager.range_min(history[k], b)
        else:
            choices = []
            for d in range(h):
                subset = manager.add(history[k], masks[d], h)
                best = manager.range_min(subset, b)
                if best is not None: choices.append((best[0]-g[k]*min(d,e), best[1]))
            _, a = min(choices)
        slots.append(a); b = a
    slots.reverse()
    tree = sparse_repair(slots, h, stats)
    stats['dag_all_nodes'] = len(manager.nodes)
    stats['dag_history_nodes'] = manager.reachable(history)
    return dict(cost=h*(sum(w)+sum(g))+value+constant, tree=tree, slots=slots,
                stage_nodes=stages, height=h)
