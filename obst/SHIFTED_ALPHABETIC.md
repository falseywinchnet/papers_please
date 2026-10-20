# Shifted alphabetic certificates for full mixed OBSTs

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. Hu--Tucker alphabetic construction, rearrangement, and
the internal/external path-length identity are established ingredients.
Priority for the certificate and explicit family is not established. This
is an exact shortcut with quadratic fallback, not an unrestricted solution.

## Bound and best admissible uniform transfer

Let K(p) be the key-capacity bound, A(q) the exact ordered alphabetic gap
optimum, M(n) the minimum sum of n unit key comparison lengths, and E(n+1)
the minimum sum of n+1 unit gap depths. Then E(n+1)=M(n)+n.
For any -min(q)<=a<=min(p), the full mixed cost of every fixed tree obeys

    C(T;p-a,q+a) = C(T;p,q) + an.

Consequently

    L(a) = K(p-a) + A(q+a) - an <= OPT(p,q).

Write m=min(p), with m=0 for no keys. The strongest L(a) on this entire
admissible interval is L(m). Indeed, uniform subtraction preserves key
ranks, so K(p-a)=K(p)-a M(n), and

    L(a) = K(p) + min_T [sum_i q_i d_i(T) + a(sum_i d_i(T)-E(n+1))].

Every affine term has nonnegative slope. Their pointwise minimum is
nondecreasing (and concave), so its maximum is at a=m. In particular
L(m)>=K(p)+A(q)>=K(p)+G(q), where G is the preceding threshold bound.
The exact alphabetic optimum A changes shape as a varies; this is why it
can improve although K+G is invariant under the same transfer.

Compute an alphabetic optimum T for q+m, then evaluate the original full
ordered cost C(T;p,q). If that cost equals L(m), T is globally optimal.
No key is permuted and no key weight is omitted from the returned cost.
Equivalently, T must also attain K(p-m) with the original residual key
positions. Rejection can miss a different tied alphabetic optimum, and
even a globally optimal candidate may fail equality. It is not a complete
recognizer of mixed optimality or of bound attainment.

The strict merge counterexample from JOINT_MERGE_OBSTRUCTION.md has
K(p)+G(q)=208, K(p)+A(q)=212, L(1)=213, and OPT=213. The shifted alphabetic
tree is the full optimum. This repairs that example by a valid lower bound;
the rejected mixed merge rule still returns an invalid lower estimate 214.

## Full implementation and arithmetic complexity

`shifted_alphabetic.alphabetic` implements the classical compatible-merge
construction of Hu and Tucker, with two later implementation ingredients:
leftist heaps and a priority queue with stale-event removal. A live group
contains internal items between two consecutive unmerged original leaves,
including those boundary leaves as possible partners. Its best pair is
among at most four items: two boundary leaves and two heap minima.
Removing a boundary leaf melds its incident groups. Each merge consumes
two items and creates one internal item. Original-leaf depths are recovered
from the merge tree and reconstructed in alphabetic order with a stack.

There are O(n) groups, merges, leaf removals, and priority events. Leftist
heap melds and priority operations take O(log(n+1)) time each. Reconstruction,
full cost evaluation, and fixed scans are linear; sorting the residual
key weights takes O(n log(n+1)). Therefore the complete certificate and
successful full construction take O(n log(n+1)) arithmetic work and O(n)
space. There are no interval-DP cells on acceptance. `solve` falls back to
the independent Knuth implementation on rejection, preserving exactness
and the quadratic unrestricted worst case. The earlier portfolio is not
modified or silently replaced by this standalone route.

Tie handling is explicit without n-bit symbolic weights. For the mathematical
perturbation assign infinitesimal secondary weight 2^i to original leaf i.
Active items partition the original leaves. At equal primary mass, two
individual items compare by their largest original-leaf index. For two
candidate pairs, compare the larger of their two largest indices, then the
smaller. If the pairs share an item, it cancels; otherwise the largest
differing leaf decides the perturbation order. These two indices therefore
exactly reproduce the symbolic sum comparison among active pairs. Stale
queue events are discarded before use. The representation stores O(log n)
bit indices, rather than materializing exponentially valued tie weights.

Counters separately record key-sort comparisons, heap-item comparisons,
priority-entry comparisons, heap meld calls, events, stale events, groups,
merges, cost visits, reconstruction, and preprocessing. Tuple comparisons
are logical comparisons, not individual machine instructions. Arithmetic
on large input weights has additional bit costs.

## A positive nonuniform family outside the old capacity certificate

Let r=2^h and n=7r-1. Repeat the original gap vector

    (18,2,13,3,17,1,2)

r times. Build a perfect skeleton with r leaves and put the six-key tree
from the strict counterexample into each leaf. Each gadget has key
comparison lengths (2,4,3,1,2,3) and gap depths (2,4,4,3,2,3,3), before
the skeleton's h-depth shift. Give every deepest key weight 1. Give the
other keys arbitrary positive residuals above 1 that decrease between
depth layers. There are 6r-1 residual-positive keys; their comparison-length
profile attains the key-capacity minimum.

For a concrete integer family with many distinct keys, set

    p_i = 1,                                  if l_i=h+4,
    p_i = 1 + (h+4-l_i)(n+1) + i,              otherwise.

There are 6r distinct key weights and six distinct gap weights. The maximum
key weight is O(n log n), so all weights have O(log n) bits. Both key and
gap weights are strictly positive; the common key minimum is just 1.

It remains to prove the candidate alphabetic-optimal for q+1. In every
block the shifted gaps are (19,3,14,4,18,2,3). Compatible merging performs
the local stages 2+3=5, 3+14=17, 17+4=21, and 18+5=23. Every stage finishes
in every block before a larger stage begins; cross-block alternatives do
not undercut these costs. This leaves, per block, an original leaf 19 and
internal items 21 and 23. For even r, the original leaves pair at cost 38
before any other remaining pair can be cheaper, removing all barriers.
The remaining Huffman merges pair 21s to 42s and 23s to 46s, leaving r/2
copies of twice (19,21,23). Repeat the doubling reduction until the final
triple, where 19+21=40 and 40+23=63. For r=1 those last two merges are
already compatible. All equal-cost choices within a stage give the same
item depths.

Thus the shifted alphabetic depth vector is exactly h plus the gadget
vector, repeated r times. The alphabetic cost is r(169+63h). Reconstruction
recovers the stated skeleton/gadget tree. Its residual keys attain K(p-1),
so the full original tree is certified in O(n log n) arithmetic work.
The chosen residual magnitudes can vary arbitrarily within the depth-order
condition; no key/gap dominance assumption is used in this equality proof.

Its original key contribution exceeds K(p) by exactly r: the r unit keys
are one level deeper than their capacity slots, while the other keys
already attain their residual optimum. Hence no tree with the original
key-capacity equality and this exact total can witness the old K+G bound.
The old key-capacity test rejects this candidate for every r. This is a
proved strict extension beyond the earlier simultaneous-capacity families,
while retaining all original nonuniform mixed weights.

## Independent checks and results

The independent cubic probe preceded the optimized constructor: 960 mixed
controls, 3629 scalar-transfer checks, and 37500 literal tree inequalities.
It certifies 138 candidates, including 24 whose value strictly exceeds
the earlier K+G bound.

The constructor audit checks all 9840 ternary gap vectors through seven
keys against independent cubic values and the literal compatible-pair
implementation, including exact equality of ordered gap-depth vectors.
There are 960 full mixed solves against cubic and Knuth, including 560
literal exhaustive controls. The suite covers random, near-uniform,
geometric, binary/zero, and constant-key weights: 336 certificates and
624 exact fallbacks; all 279 constant-key cases certify. Eight positive
family sizes through n=895 match Knuth, and the four smallest also match
cubic. A 1199-key skewed tree checks iterative reconstruction/traversal.

Five larger full constructions reach n=229375, with 196608 distinct key
weights and exact cost 2029411090432. The explicit independent family tree,
the reconstructed tree, and the bound have equal cost. The original key
capacity deficit is r=32768. Full counters are retained in
`results/shifted_alphabetic.json`; the production solver receives only p,q,
not the reference family tree.

The separate benchmark compares the standalone shifted constructor,
the previous portfolio, and Knuth in all six orders on seven families at
two sizes. It includes full preprocessing, certification, and reconstruction,
and retains every rejection overhead and old-fast-path regression. Timings
are supporting observations; the proof and counters establish scaling.

There are 84 matched trials and 252 full constructions on Apple M4,
Python 3.9.6, macOS 26.5 arm64. At 895 keys, median paired shifted/Knuth
ratios are 0.07629 for the new family, 1.02507 for random, 1.14523 for
near-uniform, and 1.04554 for geometric inputs. The constant-key control
is 0.05598; that reduction is established prior work. On the previous
profile family this standalone route is 213.67 times slower than the
old portfolio; on the preceding multilevel family at 639 keys it is
12.57 times slower. The earlier portfolio is retained unchanged.
Load averages were 11.57/11.66/13.47 initially and 13.56/12.13/13.54 finally.
Same-process order cycling, six trials per row, and this substantial load
limit timing precision. Raw data are in `shifted_alphabetic_matched.json`.

The root AGENTS.md contains M4 reproduction commands. Result manifests
record source hashes and deterministic seeds. Mathematical novelty and
broad practical superiority remain unproved. The unrestricted subquadratic
or impossibility question is still open.

Prior work: T. C. Hu and A. C. Tucker, *Optimal Computer Search Trees and
Variable-Length Alphabetical Codes*, SIAM J. Applied Mathematics 21(4),
514-532 (1971), https://doi.org/10.1137/0121057. The original paper's
operation bound must not be confused with the heap-based implementation
bound proved here.
