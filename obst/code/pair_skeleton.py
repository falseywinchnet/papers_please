#!/usr/bin/env python3
"""Coupled excluded-class bounds for two internal selected gaps.

The first possible violating depth sum has exactly one extra comparison on
the selected paths. Enumerate its constant-size skeleton, retaining all key
and gap weights in order-free payload-forest relaxations. Deeper violations
use a separate tail bound. This is an exact certificate, not a heuristic.
"""
from collections import Counter
from functools import lru_cache

from core_exclusion import solve as previous_solve
from heavy_core import Counted, fits, intervals, tri, uniform_tree
from mass_frontier import solve as frontier_solve
from research import check_weights, cost, knuth, label, shapes


def forest_bound(p, q, stats):
    """Optimal unordered mixed forest, with len(q)-len(p) equal-depth roots."""
    assert len(q) > len(p)
    sc = Counter()
    ps = [x.value for x in sorted(Counted(w, sc) for w in p)]
    leaves = [x.value for x in sorted(Counted(w, sc) for w in q)]
    stats['forest_sort_comparisons'] += sc['selection_sort_comparisons']
    stats['forest_input_items'] += len(p)+len(q)
    merged = []
    i = j = 0

    def pop():
        nonlocal i, j
        if i < len(leaves) and j < len(merged):
            stats['forest_queue_comparisons'] += 1
        if i < len(leaves) and (j == len(merged) or leaves[i] <= merged[j]):
            v = leaves[i]
            i += 1
        else:
            v = merged[j]
            j += 1
        return v

    answer = 0
    for w in ps:
        total = w+pop()+pop()
        assert not merged or total >= merged[-1]
        merged.append(total)
        answer += total
        stats['forest_contractions'] += 1
    assert len(leaves)-i+len(merged)-j == len(q)-len(p)
    return answer


def depths(tree, n):
    keys, gaps = [0]*n, [0]*(n+1)

    def walk(t, lo=0, d=0):
        if t is None:
            gaps[lo] = d
            return
        r, a, b = t
        keys[r] = d+1
        walk(a, lo, d+1)
        walk(b, r+1, d+1)
    walk(tree)
    return keys, gaps


@lru_cache(None)
def skeleton_profiles(m, selected, insertion):
    """All first-violating profiles, with one extra key in a light interval."""
    core = [i+(i >= insertion) for i in range(m)]
    selected_aug = [g+(g > insertion) for g in selected]
    result = []
    for shape in shapes(m+1):
        tree = label(shape)[0]
        if fits(tree, set(core)):
            continue
        kl, gd = depths(tree, m+1)
        if sum(gd[g] for g in selected_aug) != m+2:
            continue
        hole_min = min(gd[insertion], gd[insertion+1])
        assert hole_min >= kl[insertion]
        ordinary = tuple(gd[t+(t > insertion)] if t != insertion else hole_min
                         for t in range(m+1))
        result.append((tuple(kl[i] for i in core),
                       tuple(gd[g] for g in selected_aug), ordinary,
                       kl[insertion]))
    return tuple(result)


def pair_data(n, gaps):
    a, b = sorted(gaps)
    assert 0 < a < b < n
    anchors = sorted({a-1, a, b-1, b})
    blocks = list(intervals(n, anchors))
    selected = tuple(blocks.index((g, g)) for g in (a, b))
    return (a, b), anchors, blocks, selected


def excluded_bound(p, q, gaps, stats):
    gaps, anchors, blocks, selected = pair_data(len(p), gaps)
    m = len(anchors)
    theta = min(q[g] for g in gaps)
    residual_q = q.copy()
    for g in gaps:
        residual_q[g] = 0
    residual_lower = forest_bound(p, residual_q, stats)
    tail = 2*sum(q[g] for g in gaps)+(m-1)*theta+residual_lower
    regions = {}
    for t, (i, j) in enumerate(blocks):
        if t in selected:
            continue
        ps, qs = p[i:j], q[i:j+1]
        mass = sum(ps)+sum(qs)
        ordinary = forest_bound(ps, qs, stats)
        if ps:
            remaining = ps.copy()
            largest = max(remaining)
            remaining.remove(largest)
            two = forest_bound(remaining, qs, stats)
            stats['bridge_maximum_items'] += len(ps)
        else:
            largest = two = None
        regions[t] = (mass, ordinary, largest, two)
    first = None
    records = []
    for insertion, (mass, _, largest, two) in regions.items():
        if largest is None:
            continue
        profiles = skeleton_profiles(m, selected, insertion)
        for kl, gd, hd, bridge_length in profiles:
            value = sum(p[a]*d for a, d in zip(anchors, kl))
            value += sum(q[g]*d for g, d in zip(gaps, gd))
            for t, (w, ordinary, _, _) in regions.items():
                if t == insertion:
                    value += bridge_length*largest+hd[t]*(w-largest)+two
                else:
                    value += hd[t]*w+ordinary
            first = value if first is None else min(first, value)
            stats['skeleton_profiles_checked'] += 1
        records.append(dict(block=insertion, profiles=len(profiles)))
    stats['residual_lower_bound'] = residual_lower
    stats['tail_lower_bound'] = tail
    stats['first_level_lower_bound'] = first
    stats['skeleton_regions'] = records
    basic = 2*sum(q[g] for g in gaps)+(m-2)*theta+residual_lower
    stats['basic_lower_bound'] = basic
    result = max(basic, tail if first is None else min(first, tail))
    stats['excluded_lower_bound'] = result
    return result


def closed_candidate(p, q, gaps, stats, kernel='frontier', balanced=False):
    _, anchors, blocks, _ = pair_data(len(p), gaps)
    payload, cq = [], []
    relative = 0

    def midpoint(i, j):
        if i == j:
            return None
        r = (i+j)//2
        stats['witness_payload_keys'] += 1
        return r, midpoint(i, r), midpoint(r+1, j)

    def shift(t, offset):
        if t is None:
            return None
        r, a, b = t
        stats['payload_relabelled_keys'] += 1
        return r+offset, shift(a, offset), shift(b, offset)

    for i, j in blocks:
        ps, qs = p[i:j], q[i:j+1]
        if balanced:
            tree = midpoint(0, j-i)
            value = cost(tree, ps, qs)
        else:
            result = uniform_tree(ps, qs, stats)
            if result is not None:
                value, tree = result
            elif kernel == 'knuth':
                value, tree, scans = knuth(ps, qs)
                stats['payload_short_states'] += tri(j-i)
                stats['payload_root_candidates'] += scans
            else:
                value, tree, counts = frontier_solve(ps, qs)
                for k, v in counts.items():
                    stats['payload_'+k] += v
        relative += value
        cq.append(sum(ps)+sum(qs))
        payload.append(shift(tree, i))
    value, tree, scans = knuth([p[i] for i in anchors], cq)
    stats['closed_core_states'] += tri(len(anchors))
    stats['closed_core_root_candidates'] += scans

    def expand(t, lo=0):
        if t is None:
            return payload[lo]
        r, a, b = t
        stats['closed_core_reconstructed_keys'] += 1
        return anchors[r], expand(a, lo), expand(b, r+1)
    tree = expand(tree)
    assert value+relative == cost(tree, p, q)
    return value+relative, tree


def solve(p, q, kernel='frontier', refine=False, gaps=None):
    check_weights(p, q)
    assert kernel in ('frontier', 'knuth')
    stats = Counter()
    direct = uniform_tree(p, q, stats)
    if direct is not None:
        stats['global_uniform'] = 1
        return *direct, dict(stats)
    if gaps is None:
        first = second = None
        for g in range(1, len(p)):
            stats['gap_selection_items'] += 1
            item = (q[g], -g)
            if first is None or item > first:
                first, second = item, first
            elif second is None or item > second:
                second = item
        if second is not None and second[0] > 0:
            gaps = (-first[1], -second[1])
    if gaps is not None:
        gaps, anchors, _, _ = pair_data(len(p), gaps)
        stats['selected_gaps'] = gaps
        stats['core_keys'] = len(anchors)
        if len(anchors) == len(p):
            value, tree = closed_candidate(p, q, gaps, stats, kernel)
            stats['whole_core'] = 1
            return value, tree, dict(stats)
        lower = excluded_bound(p, q, gaps, stats)
        witness, _ = closed_candidate(p, q, gaps, stats, kernel, balanced=True)
        stats['witness_cost'] = witness
        if witness <= lower or refine:
            value, tree = closed_candidate(p, q, gaps, stats, kernel)
            stats['closed_candidate_cost'] = value
            if value <= lower:
                stats['certified_core'] = 1
                stats['refinement_rescued'] = int(witness > lower)
                return value, tree, dict(stats)
        stats['certificate_failed'] = 1
    value, tree, counts = previous_solve(p, q, kernel)
    for k, v in counts.items():
        stats['fallback_'+k] = v
    stats['fallback_calls'] = 1
    return value, tree, dict(stats)
