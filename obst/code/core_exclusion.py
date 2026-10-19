#!/usr/bin/env python3
"""Full mixed-weight OBST core certificates with a residual lower bound.

A non-core-closed tree costs at least protected_OPT + theta + residual_LB.
An explicit protected-optimal core with balanced payloads can certify closure
before any exact payload solve. Optional refinement tests the exact closed
candidate. Certificate failure uses the preceding exact full solver.
"""
from collections import Counter
import itertools
from math import isqrt

from complete import residual_huffman
from heavy_core import (Counted, anchors_at, core_solve, intervals,
                        solve as previous_solve, tri, uniform_tree)
from research import check_weights, cost, knuth


def choose_plans(p, q, stats, max_core=None):
    """Two representatives per dyadic core-size band; O(log(n+1)) plans.

    Retain the least Knuth proxy and highest threshold in each band. The
    default cap bounds the sum of protected-core table sizes by O(n log n).
    """
    n = len(p)
    if not n:
        return []
    cap = min(n, isqrt(n*n.bit_length())) if max_core is None else max_core
    outcomes = [x.value for x in sorted(Counted(w, stats) for w in p+q)]
    activation = [x.value for x in sorted(
        Counted((max(p[i], q[i], q[i+1]), i), stats) for i in range(n))]
    parent, size = [-1]*n, [0]*n
    active = block_states = cursor = 0
    cheapest, highest = {}, {}

    def find(i):
        while parent[i] != i:
            stats['selection_find_steps'] += 1
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        nonlocal block_states
        a, b = find(a), find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        block_states += size[a]*size[b]
        parent[b] = a
        size[a] += size[b]
        stats['selection_unions'] += 1

    for threshold, group in itertools.groupby(outcomes):
        while cursor < n and activation[cursor][0] < threshold:
            _, i = activation[cursor]
            parent[i], size[i] = i, 1
            active += 1
            block_states += 1
            cursor += 1
            stats['selection_activations'] += 1
            if i and parent[i-1] >= 0:
                union(i, i-1)
            if i+1 < n and parent[i+1] >= 0:
                union(i, i+1)
        m = n-active
        proxy = tri(m)+block_states
        stats['selection_thresholds'] += 1
        if threshold > 0 and m <= cap and proxy < tri(n):
            band = m.bit_length()-1
            plan = dict(threshold=threshold, core_keys=m, knuth_proxy=proxy)
            if band not in cheapest or proxy < cheapest[band]['knuth_proxy']:
                cheapest[band] = plan
            highest[band] = plan
        # Consume the equal-weight group explicitly, without further sorting.
        for _ in group:
            pass
    stats['selection_items'] = 3*n+1
    stats['protected_core_cap'] = cap
    unique = {x['threshold']: x for x in list(cheapest.values())+list(highest.values())}
    order = sorted(Counted((x['knuth_proxy'], x['threshold']), stats) for x in unique.values())
    stats['candidate_plans'] = len(order)
    return [unique[x.value[1]] for x in order]


def choose_plan(p, q, stats, max_core=None):
    plans = choose_plans(p, q, stats, max_core)
    return plans[0] if plans else None


def protected_witness(p, q, threshold, stats):
    """Return protected optimum and full witness light cost, in O(n+m^2)."""
    n = len(p)
    anchors = anchors_at(p, q, threshold)
    assert anchors
    lp = [w if w < threshold else 0 for w in p]
    lq = [w if w < threshold else 0 for w in q]
    hp = [p[i] if p[i] >= threshold else 0 for i in anchors]
    hq = []
    blocks = list(intervals(n, anchors))
    for i, j in blocks:
        # Nonempty payloads have no selected outcomes, including their gaps.
        hq.append(sum(w for w in q[i:j+1] if w >= threshold))
    protected, tree, scans = knuth(hp, hq)
    stats['protected_states'] += tri(len(anchors))
    stats['protected_root_candidates'] += scans
    stats['protected_cost'] = protected
    stats['residual_items'] += 2*n+1

    def balanced(i, j):
        if i == j:
            return None
        r = (i+j)//2
        stats['witness_payload_keys'] += 1
        return r, balanced(i, r), balanced(r+1, j)

    def expand(t, lo=0):
        if t is None:
            return balanced(*blocks[lo])
        r, a, b = t
        stats['witness_core_keys'] += 1
        return anchors[r], expand(a, lo), expand(b, r+1)

    witness = expand(tree)
    upper = cost(witness, lp, lq)
    stats['witness_light_cost'] = upper
    stats['witness_cost_keys'] += n
    return protected, upper, lp, lq


def sorted_profiles(p, q, stats):
    sc = Counter()
    ps = [x.value for x in sorted((Counted(w, sc) for w in p), reverse=True)]
    qs = [x.value for x in sorted((Counted(w, sc) for w in q), reverse=True)]
    stats['bound_sort_comparisons'] += sc['selection_sort_comparisons']
    return ps, qs


def light_lower(lp, lq, stats, profiles=None, threshold=None):
    # Same established mixed-node order-free relaxation, with separate
    # sorting and two-queue merge counters. No new Huffman theorem is claimed.
    if profiles is None:
        ps, qs = sorted_profiles(lp, lq, stats)
    else:
        residuals = []
        for values in profiles:
            light = [w for w in values if w < threshold]
            residuals.append(light+[0]*(len(values)-len(light)))
            stats['bound_profile_items'] += len(values)
        ps, qs = residuals
    return residual_huffman(ps, qs, 0, 0, stats)


def attempt(p, q, stats, kernel='frontier', refine=False, threshold=None, profiles=None):
    plan = choose_plan(p, q, stats) if threshold is None else dict(
        threshold=threshold, core_keys=len(anchors_at(p, q, threshold)))
    if plan is None:
        stats['no_candidate_core'] += 1
        return None
    theta = plan['threshold']
    stats.update({'plan_'+k: v for k, v in plan.items()})
    protected, upper, lp, lq = protected_witness(p, q, theta, stats)
    lower = light_lower(lp, lq, stats, profiles, theta)
    ceiling = protected+theta+lower
    stats.update(light_lower_bound=lower, exclusion_lower_bound=ceiling)
    witness_passes = upper <= theta+lower
    stats['witness_certificate'] = int(witness_passes)
    if not witness_passes and not refine:
        stats['certificate_failed'] += 1
        return None
    value, tree = core_solve(p, q, theta, kernel, stats)
    stats['closed_candidate_cost'] = value
    if value <= ceiling:
        stats['certified_core'] += 1
        stats['refinement_rescued'] = int(not witness_passes)
        return value, tree
    assert not witness_passes
    stats['certificate_failed'] += 1
    return None


def solve(p, q, kernel='frontier', refine=False):
    check_weights(p, q)
    assert kernel in ('frontier', 'knuth')
    stats = Counter()
    result = uniform_tree(p, q, stats)
    if result is not None:
        stats['global_uniform'] += 1
    else:
        plans = choose_plans(p, q, stats)
        profiles = sorted_profiles(p, q, stats) if plans else None
        attempts = []
        for plan in plans:
            counts = Counter()
            result = attempt(p, q, counts, kernel, False, plan['threshold'], profiles)
            attempts.append(dict(counts))
            if result is not None:
                stats['certified_core'] = 1
                stats['witness_certificate'] = counts['witness_certificate']
                stats['refinement_rescued'] = counts['refinement_rescued']
                break
        # At most one failed exact payload construction, preserving the
        # quadratic general worst case even when refinement is requested.
        if result is None and refine and plans:
            counts = Counter(refinement_attempt=1)
            result = attempt(p, q, counts, kernel, True, plans[0]['threshold'], profiles)
            attempts.append(dict(counts))
            if result is not None:
                stats['certified_core'] = 1
                stats['witness_certificate'] = counts['witness_certificate']
                stats['refinement_rescued'] = counts['refinement_rescued']
        stats['attempts'] = attempts
    if result is None:
        value, tree, old = previous_solve(p, q, kernel)
        for k, v in old.items():
            stats['fallback_'+k] = v
        stats['fallback_calls'] += 1
    else:
        value, tree = result
    assert value == cost(tree, p, q)
    return value, tree, dict(stats)
