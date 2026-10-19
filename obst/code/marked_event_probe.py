#!/usr/bin/env python3
"""Experimental one-key compatible-merge event family, NOT an exact solver.

Literal scans and copied states expose the candidate space. Every reconstructed
candidate uses the original positional key weight. Finite agreement does not
prove sufficiency of the event family. No subquadratic implementation is claimed.
"""
from collections import Counter
from joint_merge_probe import from_gap_depths
from research import cost


def pairs(items, weight, stats):
    out = []
    for i, a in enumerate(items):
        stats['pair_outer_items'] += 1
        if a[1] == 'mark':
            continue
        crossed = False
        for j in range(i + 1, len(items)):
            stats['pair_scan_items'] += 1
            b = items[j]
            if b[1] == 'mark':
                crossed = True
                continue
            out.append((a[0] + b[0] + (weight if crossed else 0),
                        a[3] + b[3], i, j, crossed))
            stats['pair_candidates'] += 1
            if b[1] is True:
                break
    return out


def least(events, stats):
    stats['event_order_comparisons'] += max(0, len(events) - 1)
    return min(events)


def merge(items, event, stats):
    z, tag, i, j, crossed = event
    a, b = items[i], items[j]
    stats['copied_state_items'] += len(items)
    items = list(items)
    items[i] = (z, False, (a[2], b[2]), tag)
    del items[j]
    if crossed:
        for k, a in enumerate(items):
            stats['marker_scan_items'] += 1
            if a[1] == 'mark':
                del items[k]
                break
        else:
            raise AssertionError('crossing event without a marker')
    stats['merges'] += 1
    return items


def finish(items, p, q, stats):
    while len(items) > 1:
        items = merge(items, least(pairs(items, 0, stats), stats), stats)
    depths = [0] * len(q)
    todo = [(items[0][2], 0)]
    while todo:
        tree, depth = todo.pop()
        stats['merge_tree_visits'] += 1
        if isinstance(tree, int):
            depths[tree] = depth
        else:
            todo.extend((x, depth + 1) for x in tree)
    tree, valid = from_gap_depths(depths)
    stats['reconstruction_leaf_items'] += len(q)
    if not valid:
        stats['invalid_reconstructions'] += 1
        return None
    stats['full_cost_outcomes'] += len(p) + len(q)
    return cost(tree, p, q), tree, depths


def candidate(q, r, weight, all_crossings=True):
    assert 0 <= r < len(q) - 1 and weight >= 0 and min(q) >= 0
    p = [0] * (len(q) - 1)
    p[r] = weight
    items = [(z, True, i, 1 << i) for i, z in enumerate(q)]
    items.insert(r + 1, (weight, 'mark', None, 0))
    stats = Counter(input_gaps=len(q))
    best = None
    witness = None
    levels = []
    event_step = 0
    while True:
        options = pairs(items, weight, stats)
        crossing = [event for event in options if event[-1]]
        assert crossing
        if not all_crossings:
            crossing = [least(crossing, stats)]
        level = []
        for event in crossing:
            completed = finish(merge(items, event, stats), p, q, stats)
            stats['completed_candidates'] += 1
            level.append((event, completed[0] if completed else None))
            if completed is not None and (best is None or completed[0] < best):
                best = completed[0]
                witness = (event_step, event, completed)
        levels.append(level)
        ordinary = [event for event in options if not event[-1]]
        if not ordinary:
            break
        items = merge(items, least(ordinary, stats), stats)
        event_step += 1
    return dict(cost=best, witness=witness, levels=levels, stats=dict(stats))


def greedy(q, r, weight):
    p = [0] * (len(q) - 1)
    p[r] = weight
    items = [(z, True, i, 1 << i) for i, z in enumerate(q)]
    items.insert(r + 1, (weight, 'mark', None, 0))
    stats = Counter()
    charge = 0
    while True:
        event = least(pairs(items, weight, stats), stats)
        charge += event[0]
        items = merge(items, event, stats)
        if event[-1]:
            break
    while len(items) > 1:
        event = least(pairs(items, 0, stats), stats)
        charge += event[0]
        items = merge(items, event, stats)
    completed = finish(items, p, q, stats)
    return dict(cost=completed[0] if completed else None, charge=charge,
                tree=completed[1] if completed else None, stats=dict(stats))
