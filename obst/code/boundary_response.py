#!/usr/bin/env python3
"""Exact small boundary envelopes and a quadratic explicit-facet family.

Research harness, not a new full-OBST solver. All polyhedral arithmetic is
rational. A boundary response adds nonnegative weights to the endpoint gaps.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import random

from pair_skeleton import depths
from research import cost, cubic, knuth, label, shapes


@lru_cache(None)
def profiles(n):
    return tuple((t, *depths(t, n)) for t in (label(s)[0] for s in shapes(n)))


def planes(p, q):
    result = {}
    for _, kl, gd in profiles(len(p)):
        value = sum(a*b for a, b in zip(p, kl))+sum(a*b for a, b in zip(q, gd))
        key = gd[0], gd[-1]
        result[key] = min(result.get(key, value), value)
    return tuple((a, b, c) for (a, b), c in sorted(result.items()))


def clip(poly, a, b, c):
    """Intersect convex polygon with a*x+b*y<=c, using exact rationals."""
    out = []
    for u, v in zip(poly, poly[1:]+poly[:1]):
        fu, fv = a*u[0]+b*u[1]-c, a*v[0]+b*v[1]-c
        if fu <= 0:
            out.append(u)
        if (fu < 0 < fv) or (fv < 0 < fu):
            t = fu/(fu-fv)
            out.append((u[0]+t*(v[0]-u[0]), u[1]+t*(v[1]-u[1])))
    return out


def envelope(items, n):
    """Canonical affine pieces with positive-area regions in x,y>=0.

    All finite line intersections have coordinates <=2*n*max|c| in
    absolute value (integer determinant is at least one). This larger box
    intersects every full-dimensional cell, including unbounded cells.
    """
    limit = Fraction(4*max(1, n)*max(1, max(abs(c) for _, _, c in items))+1)
    kept = []
    for a, b, c in items:
        poly = [(Fraction(0), Fraction(0)), (limit, Fraction(0)),
                (limit, limit), (Fraction(0), limit)]
        for d, e, f in items:
            poly = clip(poly, a-d, b-e, f-c)
            if len(poly) < 3:
                break
        area = sum(u[0]*v[1]-u[1]*v[0] for u, v in zip(poly, poly[1:]+poly[:1]))
        if area:
            kept.append((a, b, c))
    assert kept
    return tuple(kept)


def one_side(m):
    p, probes = [], []
    w, mass = 4*m, 0
    for _ in range(m):
        p.append(w)
        mass += w
        probes.append(2*mass+2*m)
        w *= 8
    q = [1]*(m+1)
    return p, q, probes


def product_family(m):
    p, q, probes = one_side(m)
    outside_mass_max = 2*sum(p)+2*m+2+2*probes[-1]
    center = (2*m+2)*outside_mass_max
    return p+[center]+p[::-1], [1]*(2*m+2), probes


def hinge_response(m, x):
    p, _, _ = one_side(m)
    base = sum((m-i)*w for i, w in enumerate(p))+m+m*(m+1)//2
    return base+m*x-sum(max(0, x-(w-p[0])) for w in p[1:])


class FactoredFamily:
    """O(m)-space response for the entire quadrant, including reconstruction.

    This is the explicit geometric witness family, not a general OBST solver.
    """
    def __init__(self, m):
        self.m = m
        self.p, self.q, self.probes = product_family(m)
        ps = self.p[:m]
        self.c0 = sum((m-i)*w for i, w in enumerate(ps))+m+m*(m+1)//2
        self.thresholds = [w-ps[0] for w in ps[1:]]
        self.prefix = [0]
        for w in self.thresholds:
            self.prefix.append(self.prefix[-1]+w)
        self.mass = sum(self.p)+sum(self.q)
        self.right_mass = self.mass-ps[0]-1
        self.a = self.c0-m*ps[0]-m-1
        self.b = self.p[m]+2*(sum(ps)-ps[0])+2*m+2*self.a

    def hinge(self, x, counts):
        lo, hi = 0, len(self.thresholds)
        while lo < hi:
            mid = (lo+hi)//2
            counts['threshold_comparisons'] += 1
            if self.thresholds[mid] <= x:
                lo = mid+1
            else:
                hi = mid
        return self.c0+(self.m-lo)*x+self.prefix[lo], lo

    def evaluate(self, x, y, counts):
        hx, jx = self.hinge(x, counts)
        hy, jy = self.hinge(y, counts)
        candidates = (hx+hy, self.right_mass+y+self.a+hy,
                      self.right_mass+y+self.b,
                      self.right_mass+x+self.a+hx,
                      self.right_mass+x+self.b)
        value, case = min((v, i) for i, v in enumerate(candidates))
        counts['outer_minimum_comparisons'] += 4
        return self.mass+x+y+value, case, jx, jy

    def solve(self, x, y, counts):
        value, case, jx, jy = self.evaluate(x, y, counts)
        m = self.m

        def node(i, left=None, right=None):
            counts['constructed_keys'] += 1
            return i, left, right

        def chain(mirror=False):
            t = None
            for k in range(1, m):
                t = node(2*m-k, None, t) if mirror else node(k, t, None)
            return t

        def side(j, mirror=False):
            t = None
            for k in range(1, j+1):
                t = node(2*m-k, None, t) if mirror else node(k, t, None)
            t = node(2*m, t, None) if mirror else node(0, None, t)
            for k in range(j+1, m):
                t = node(2*m-k, None, t) if mirror else node(k, t, None)
            return t

        if case == 0:
            tree = node(m, side(jx), side(jy, True))
        elif case == 1:
            tree = node(0, None, node(m, chain(), side(jy, True)))
        elif case == 2:
            tree = node(0, None, node(2*m, node(m, chain(), chain(True)), None))
        elif case == 3:
            tree = node(2*m, node(m, side(jx), chain(True)), None)
        else:
            tree = node(2*m, node(0, None, node(m, chain(), chain(True))), None)
        return value, tree


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a+b
    return a


def all_optimal_depths(p, q):
    vals = [(sum(a*b for a, b in zip(p, kl))+sum(a*b for a, b in zip(q, gd)),
             (gd[0], gd[-1])) for _, kl, gd in profiles(len(p))]
    best = min(v for v, _ in vals)
    return best, {d for v, d in vals if v == best}


def collision_search():
    groups = {}
    checked = 0
    contexts = [(([a] if a else []), ([b] if b else []))
                for a, b in itertools.product((0, 1, 4, 16, 64), repeat=2) if a or b]
    contexts += [(list(a), list(b)) for a, b in itertools.product(
        ((1, 16), (16, 1), (4, 4), (64, 4), (4, 64)), repeat=2)]
    for n in (3, 4):
        for v in itertools.product(range(1, 5), repeat=2*n-1):
            p, q = list(v[:n]), [1, *v[n:], 1]
            env = envelope(planes(p, q), n)
            signature = (n, sum(p)+sum(q), q[0], q[-1], env)
            if signature in groups:
                oldp, oldq = groups[signature]
                for a, b in contexts:
                    pp, qq = a+p+b, [1]*len(a)+q+[1]*len(b)
                    op, oq = a+oldp+b, [1]*len(a)+oldq+[1]*len(b)
                    current, _ = cubic(pp, qq)
                    old, _ = cubic(op, oq)
                    checked += 1
                    if current != old:
                        return dict(p=p, q=q, other_p=oldp, other_q=oldq,
                                    envelope=env, mass=signature[1], context=[a, b],
                                    cost=current, other_cost=old, checked=checked)
            else:
                groups[signature] = p, q
    return dict(no_collision_found=True, groups=len(groups), context_checks=checked)


def fixed_collision():
    """Verify the reduced example without relying on envelope clipping."""
    p = [1, 1, 2, 3]
    qs = ([1, 4, 2, 1, 1], [1, 4, 1, 2, 1])
    common = ((1, 2, 45), (1, 3, 42), (2, 1, 43), (2, 2, 36), (3, 1, 39))
    data = []
    for q in qs:
        items = planes(p, q)
        assert set(common) <= set(items)
        for a, b, c in items:
            # Every discarded plane is pointwise dominated on the quadrant
            # by one common plane: no numerical convex-hull claim is needed.
            assert any(d <= a and e <= b and f <= c for d, e, f in common)
        fullp, fullq = [7, 1]+p+[1, 7], [1, 1]+q+[1, 1]
        direct = [cost(t, fullp, fullq) for t, _, _ in profiles(8)]
        value, tree = cubic(fullp, fullq)
        assert value == min(direct) == cost(tree, fullp, fullq) == knuth(fullp, fullq)[0]
        root_values = [min(v for (t, _, _), v in zip(profiles(8), direct) if t[0] == r)
                       for r in range(8)]
        data.append(dict(p=p, q=q, planes=items, full_p=fullp, full_q=fullq,
                         optimum=value, root_values=root_values, tree=tree,
                         enumerated_shapes=len(direct)))
    assert [x['optimum'] for x in data] == [101, 100]
    assert all(sum(x['p'])+sum(x['q']) == 16 for x in data)
    return dict(common_envelope=common, instances=data)


def main():
    rng = random.Random(0xB0A2D)
    counts = Counter()
    for n in range(1, 8):
        for trial in range(25):
            p = [rng.randrange(10) for _ in range(n)]
            q = [rng.randrange(10) for _ in range(n+1)]
            items = planes(p, q)
            env = envelope(items, n)
            if q[0] and q[-1]:
                mass = sum(p)+sum(q)
                for a, b, _ in env:
                    assert a == 1 or fib(a-1)*q[0] <= mass
                    assert b == 1 or fib(b-1)*q[-1] <= mass
                    counts['bounded_endpoint_depth_planes'] += 1
            for x, y in [(0, 0), (1, 3), (17, 41), (10000, 2), (2, 10000)]:
                qq = q.copy(); qq[0] += x; qq[-1] += y
                expected, _ = cubic(p, qq)
                assert min(a*x+b*y+c for a,b,c in items) == expected
                assert min(a*x+b*y+c for a,b,c in env) == expected
                counts['envelope_queries'] += 1
    rows = []
    for m in range(1, 17):
        p, q, probes = product_family(m)
        factored = FactoredFamily(m)
        seen = set()
        lp, lq, _ = one_side(m)
        for j, x in enumerate(probes):
            assert lp[0]+1+x > sum(lp[1:j+1])+j+1
            for k in range(j+1, m):
                assert lp[k]+1 > sum(lp[:k])+x+k+1
                counts['strict_endpoint_inequalities'] += 1
        test_x = [0, 1, probes[-1]*100]
        for w in lp[1:]:
            test_x.extend((w-lp[0]-1, w-lp[0], w-lp[0]+1))
        for x in test_x:
            qq = lq.copy(); qq[0] += x
            assert cubic(lp, qq)[0] == hinge_response(m, x)
            counts['hinge_queries'] += 1
        for j, x in enumerate(probes):
            for k, y in enumerate(probes):
                qq = q.copy(); qq[0] += x; qq[-1] += y
                value, tree, scans = knuth(p, qq)
                expected = (m-j+1, m-k+1)
                assert tree[0] == m
                assert cost(tree, p, qq) == value
                _, gd = depths(tree, len(p))
                assert (gd[0], gd[-1]) == expected
                # The central-root decomposition is independently checked.
                lp, lq, _ = one_side(m)
                rq = lq.copy(); lq[0] += x; rq[-1] += y
                left, _ = cubic(lp, lq)
                right, _ = cubic(lp[::-1], rq)
                assert value == sum(p)+sum(qq)+left+right
                assert value == sum(p)+sum(qq)+hinge_response(m, x)+hinge_response(m, y)
                fc = Counter()
                fv, ft = factored.solve(x, y, fc)
                assert fv == value == cost(ft, p, qq)
                assert fc['constructed_keys'] == len(p)
                counts.update(fc)
                counts['product_queries'] += 1
                counts['knuth_root_candidates'] += scans
                if m <= 4:
                    brute, ds = all_optimal_depths(p, qq)
                    assert brute == value and ds == {expected}
                    counts['all_shapes_unique_depth_pair'] += 1
                if m <= 8:
                    assert cubic(p, qq)[0] == value
                    counts['full_cubic_queries'] += 1
                seen.add(expected)
        assert len(seen) == m*m
        tail = factored.b-factored.a-hinge_response(m, 0)-sum(factored.thresholds)
        assert tail > probes[-1]
        external = []
        for j, y in enumerate(probes):
            x = 2*(factored.mass+y)
            external.extend(((x, y, (1, m-j+2)), (y, x, (m-j+2, 1))))
        y = tail+1
        x = 2*(factored.mass+y)
        external.extend(((x, y, (1, 2)), (y, x, (2, 1))))
        for x, y, expected in external:
            qq = q.copy(); qq[0] += x; qq[-1] += y
            fc = Counter()
            value, tree = factored.solve(x, y, fc)
            assert value == cost(tree, p, qq) == knuth(p, qq)[0]
            _, gd = depths(tree, len(p))
            assert (gd[0], gd[-1]) == expected
            assert fc['constructed_keys'] == len(p)
            seen.add(expected)
            counts.update(fc)
            counts['external_piece_queries'] += 1
        assert len(seen) == m*m+2*m+2
        for x, y in [(0, 0), (tail-1, tail), (tail, tail+1),
                     (tail*100, tail*101)]+[(rng.randrange(4*tail), rng.randrange(4*tail)) for _ in range(20)]:
            qq = q.copy(); qq[0] += x; qq[-1] += y
            fc = Counter()
            value, tree = factored.solve(x, y, fc)
            assert value == cost(tree, p, qq) == knuth(p, qq)[0]
            assert fc['constructed_keys'] == len(p)
            counts.update(fc)
            counts['global_factored_queries'] += 1
        row = dict(m=m, n=len(p), exposed_depth_pairs=len(seen),
                   maximum_weight_bits=max(p).bit_length(), probes=probes)
        if m <= 4:
            env = envelope(planes(p, q), len(p))
            assert len(env) == m*m+2*m+2
            row['full_quadrant_affine_pieces'] = len(env)
            row['envelope'] = env
        rows.append(row)
        print('product', m, row.get('full_quadrant_affine_pieces'), len(seen), flush=True)
    collision = collision_search()
    print('collision', collision, flush=True)
    reduced = fixed_collision()
    print('reduced collision', [x['optimum'] for x in reduced['instances']], flush=True)
    source = Path(__file__)
    target = source.parents[1]/'results'/'boundary_response.json'
    target.write_text(json.dumps(dict(seed=0xB0A2D, counts=counts, rows=rows,
        collision=collision, reduced_collision=reduced,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest()), indent=2)+'\n')


if __name__ == '__main__':
    main()
