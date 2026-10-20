"""Exact mixed OBST using valuation-class records, without expanding 2**h.

Arbitrary nonnegative exact weights are supported. The integer score-range
bound is a separate complexity statement, not a correctness assumption.
"""
from bisect import bisect_right
from collections import Counter
from concave_lws import row_minima
from slot_vector import normalize, operations


def nu(t): return (t & -t).bit_length()-1 if t else 0


class Records:
    def __init__(self, records, h):
        self.records = sorted(records)
        self.classes = [[] for _ in range(h)]
        for a, value, pred in self.records:
            self.classes[nu(a)].append((a, value, pred))
        self.positions = [[a for a, value, pred in group] for group in self.classes]

    def lookup(self, b):
        e = nu(b); j = bisect_right(self.positions[e], b)-1
        assert j >= 0
        a, value, pred = self.classes[e][j]
        return value, pred


def gap_pass(old, w, g, h, stats):
    records = []; c = (1 << h)-1
    for e in range(h):
        base = 1 << e; step = 2*base; best = None; group = []
        for a, value, pred in old.records:
            b = base+step*max(0, (a-base)//step+1)
            stats['record_gap_candidates'] += 1
            if b > c: break
            candidate = value-g*min(nu(a), e)-w*e
            if best is None or candidate < best:
                if group and group[-1][0] == b: group[-1] = (b, candidate, a)
                else: group.append((b, candidate, a))
                best = candidate
        records.extend(group)
    return Records(records, h)


def run_pass(old, k, w, m, h, penalty, stats):
    c = (1 << h)-1
    candidates = [(a, value) for a, value, pred in old.records if a <= c-m]
    columns = [a for a, value in candidates]; values = dict(candidates)
    assert columns

    def entry(b, a):
        stats['record_run_entry_queries'] += 1
        reward = nu(b)
        for t in range(1, h):
            reward += min(m-1, ((b-1) >> t)-(a >> t))
            stats['record_run_threshold_terms'] += 1
        return values[a]+penalty*max(m-b+a, 0)-w*reward

    def query(rows):
        rows = sorted(set(rows))
        if not rows: return {}
        stats['record_search_batches'] += 1
        stats['record_queried_rows'] += len(rows)
        arg = row_minima(rows, columns, entry, stats)
        out = {}
        for b in rows:
            a = arg[b]; assert b-a >= m
            out[b] = (entry(b, a), a)
        return out

    intervals = []; endpoints = []
    for e in range(h):
        base = 1 << e; step = 2*base
        lo = base+step*max(0, (k+m-base+step-1)//step)
        hi = base+step*((c-base)//step)
        if lo <= hi:
            intervals.append((lo, hi, step)); endpoints.extend((lo, hi))
    answers = query(endpoints); records = []; active = []
    for lo, hi, step in intervals:
        left, right = answers[lo], answers[hi]
        records.append((lo, *left))
        assert left[0] >= right[0]
        if left[0] > right[0]: active.append((lo, hi, step, left, right))
    del answers
    while active:
        stats['record_active_intervals'] += len(active)
        pending = []; rows = []
        for lo, hi, step, left, right in active:
            if hi-lo == step:
                records.append((hi, *right))
            else:
                mid = lo+((hi-lo)//step//2)*step
                pending.append((lo, mid, hi, step, left, right)); rows.append(mid)
        answers = query(rows); active = []
        for lo, mid, hi, step, left, right in pending:
            middle = answers[mid]
            assert left[0] >= middle[0] >= right[0]
            if left[0] > middle[0]: active.append((lo, mid, step, left, middle))
            if middle[0] > right[0]: active.append((mid, hi, step, middle, right))
    return Records(records, h)


def select_run(a, b, m, h, stats):
    """Select highest valuations, earliest ties, in O(m+h) arithmetic work."""
    assert b-a >= m
    if m == 1: return [b]
    need = m-1; cut = 0
    for t in range(h-1, -1, -1):
        count = ((b-1) >> t)-(a >> t)
        stats['record_trace_thresholds'] += 1
        if count >= need: cut = t; break
    step = 1 << (cut+1); first_high = (a//step+1)*step
    higher = list(range(first_high, b, step))
    base = 1 << cut
    first_equal = base+step*max(0, (a-base)//step+1)
    equal = [first_equal+j*step for j in range(need-len(higher))]
    # Merge the two already sorted arithmetic progressions, not all slots.
    result = []; i = j = 0
    while i < len(higher) or j < len(equal):
        if j == len(equal) or i < len(higher) and higher[i] < equal[j]:
            result.append(higher[i]); i += 1
        else: result.append(equal[j]); j += 1
        stats['record_trace_output_slots'] += 1
    assert len(result) == need and all(a < t < b for t in result)
    return result+[b]


def sparse_repair(slots, h, stats):
    """Delete only unwanted ancestors; absent branches contain no output key."""
    kept = set()
    for slot in slots:
        x = slot
        while x not in kept:
            kept.add(x); stats['record_ancestor_nodes'] += 1
            d = nu(x)
            if d == h-1: break
            x = x-(1 << d) if x & (1 << (d+1)) else x+(1 << d)
    labels = sorted(kept); count = len(labels)
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


def solve(p, q, h, stats=None, observer=None):
    assert h >= 1
    if stats is None: stats = Counter()
    w, g, constant = normalize(p, q); n = len(w)
    if n > (1 << h)-1: return None
    mass = sum(w)+sum(g); penalty = 1+(h-1)*mass
    old = Records([(0, 0, -1)], h); history = []; ops = operations(w, g)
    for k, m, weight, gap in ops:
        if m == 1:
            new = gap_pass(old, weight, gap, h, stats)
            stats['record_singleton_passes'] += 1
        else:
            assert gap == 0
            new = run_pass(old, k, weight, m, h, penalty, stats)
            stats['record_run_passes'] += 1
        if observer is not None: observer(k, m, old, new)
        stats['record_stored_states'] += len(new.records)
        history.append(new); old = new
    value, b = min((value, b) for b, value, pred in old.records)
    pieces = []
    for (k, m, weight, gap), table in zip(reversed(ops), reversed(history)):
        _, a = table.lookup(b)
        pieces.append(select_run(a, b, m, h, stats)); b = a
    assert b == 0
    slots = [t for piece in reversed(pieces) for t in piece]
    assert len(slots) == n and all(a < b for a, b in zip(slots, slots[1:]))
    reward = sum(x*nu(t) for x, t in zip(w, slots))
    reward += sum(g[i]*min(nu(slots[i-1]), nu(slots[i])) for i in range(1, n))
    assert value == -reward
    tree = sparse_repair(slots, h, stats)
    return dict(cost=h*mass+value+constant, tree=tree, slots=slots, height=h,
                stages=len(ops), stage_records=[len(t.records) for t in history])
