# Reachable coarse-optimal families: exact size and rotation barriers

The coarse-refinement theorem leaves ambiguous intervals. Two tempting ways
to resolve them are to expand every reachable coarse-optimal subproblem, or
to descend by rotations inside the coarse family. Both have explicit limits.
These results concern those approaches, not the complexity of full OBST.

## An explicit quadratic interval and cubic root-choice family

Let B=2^k, k>=1, and n=6B-1. Every coarse key and gap has weight one, so the
mass is 2n+1. Coarse cost is 2I+3n. Every minimum-internal-path-length tree is
optimal.

Begin with a perfect (4B-1)-key upper skeleton, then expand 2B of its 4B
bottom gaps. Its four depth-two subtrees each have a perfect (B-1)-key upper
skeleton and x_j optional bottom expansions, where 0<=x_j<=B and sum x_j=2B.
For every u,v in [0,B], set x_0=u, x_1=v and distribute 2B-u-v over x_2,x_3.
The second depth-two subtree occupies

    [B+u, 2B-1+u+v).

These are (B+1)^2 distinct nonempty intervals, each occurring in a full
coarse-optimal tree. On such an interval, put i=B+u. The optimal roots are
exactly i+B/2-1+t for

    max(0,v-B/2) <= t <= min(v,B/2).

Thus the selected intervals alone have

    (B+1) sum_(v=0)^B (min(v,B-v)+1) = (B+1)(B/2+1)^2

root triples. Merging equal intervals therefore still leaves Theta(n^2)
interval states and Theta(n^3) root triples in the worst case. A root triple
is an interval together with one optimal root, not a complete tree.

The grammar is the set reached from the full interval by following *every*
optimal root and both children. Optimal substructure proves it is exactly
the set of interval/root triples occurring in full coarse optima. The upper
bounds follow from the total number of intervals and interval/root triples.

## Every counted choice can matter to a fine query

Every coarse-optimal tree can become the unique fine optimum under an
arbitrarily small certified perturbation. For a target T, give key i error
weight epsilon*(n^2+1)^(-depth_T(i)), and give gaps zero error. Root dominance
and induction make T uniquely optimal for the error vector. Since T also
minimizes coarse cost, it uniquely minimizes their positive scaled sum.
Choose epsilon<delta/[n(n-1)] to satisfy the coarse-family certificate.

This uses the established exposing-weight idea. [Onishi and Hoshi (2005)](
https://www.aporc.org/LNOR/5/ISORA2005F20.pdf) study optimality regions for
key-weighted BSTs. The manuscript gives the short mixed-weight argument
explicitly; there is no novelty claim for the general exposing principle.

Each counted triple can therefore be required by some uniquely selected fine
optimum. Different triples may require different perturbations. This supports
a lower bound for an explicitly stored reusable grammar, not for arbitrary
implicit representations or for one fine-input query.

## Holes in root sets and a strict rotation trap

With p=(4,1,4), q=(1,1,1,1), the root-constrained costs are (24,25,24).
Optimal-root extremes do not imply that every intervening root is optimal.

For five keys, take coarse weights all one. There are six optima, corresponding
to choosing two of four bottom gaps of the perfect three-key skeleton. Their
coarse-cost-preserving single-rotation graph has components of sizes two and
four. The root-1/root-3 trees form one edge. The four root-2 trees independently
orient their two-key left and right children.

Write r(L,R) for a rooted tree with zero-based key indices and omit leaf
children. For D>8, take

    p=(D,D+1,D+1,D,D), q=(D,D,D,D,D,D),
    T=1(0,3(2,4)), U=2(1(0,empty),3(empty,4)).

Then C(T)=27D+4 and C(U)=27D+3. All four single rotations from T have costs
27D+5, 29D+3, 29D+5, 33D+6. Hence T is a strict local minimum but is globally
suboptimal. The exact optimum is 27D+3, by the six coarse candidates and the
certificate 4*2<D. Dividing weights by D makes the perturbation arbitrarily
small while all original key and gap weights remain positive.

## Independent evidence

`coarse_face_structure.py` was written as a falsification/verification harness
before proposing any new constructor. It compares reachable sets with literal
optimal-tree enumeration on forty inputs through eight keys (10,275 literal
costs), checks 27 unique exposing perturbations, and verifies four exact-scale
rotation traps. Its all-root reference examines 24,972 interval states and
1,349,726 root candidates.

For B=2,4,8,16,32, all selected intervals and all their optimal roots agree with
the independent recurrence. Each of the 1,493 selected intervals also has an
explicit full optimal-tree witness. Five shuffled, all-distinct fine-weight
inputs satisfy the certificate and have complete Knuth constructions checked
by direct fine and coarse tree costs. Larger rows through B=2^20 evaluate
proved formulas only. The JSON retains every fine input, exact counts, seed
and both source hashes. No timing or empirical exponent is used in the proof.

The next constructive direction must avoid materializing all coarse-optimal
interval choices and must support exchanges beyond one rotation. The previous
common-root theorem remains correct; its ambiguity parameter cannot be
eliminated merely by replacing a payload with its explicit optimal grammar.
