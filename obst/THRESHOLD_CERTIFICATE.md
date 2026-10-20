# Threshold runs, dyadic ranks, and a linear mixed-weight certificate

Research and exposition: **OpenAI Codex Sydney**. Problem selection and
sponsorship: Joshuah Rainstar. This is an exact, scoped constructor for
the full key-and-gap objective. The unrestricted subquadratic problem remains
open; no priority claim is made.

## 1. Exact indicator optimum

Let an ordered binary external tree have N leaves. Give H of them weight one
and the others weight zero, and let R be the number of contiguous zero runs,
including runs at the endpoints. For H>0 its minimum weighted external path
length is exactly

    E(H) + R,
    E(H) = (floor(log2 H)+2) H - 2^(floor(log2 H)+1).

For H=0 the optimum is zero. Here E(H) is the ordinary minimum external path
length of H unit-weight leaves, with E(1)=0.

For the lower bound, remove every maximal zero-only subtree. Each lies within
one zero run, and every run contains at least one such subtree. The parent of
each removed subtree has a selected descendant in its other child, since
otherwise the removed subtree was not maximal. Suppressing the resulting
unary nodes decreases the selected-depth sum by at least one per removed
subtree. The remaining full H-leaf tree costs at least E(H), so the original
cost is at least E(H)+R.

For the upper bound, begin with an optimal H-leaf unit tree. Assign each
interior zero run to the selected leaf immediately to its left. Assign an
initial zero run to the first selected leaf's left and a final zero run to
the last selected leaf's right. Each leaf has at most one assigned right run,
and only the first can also have a left run. Replace the leaf by a small
ordered tree accommodating the assigned zero-only subtrees. One assigned run
increases its selected depth by one; two runs increase it by two. Every
zero-only subtree has arbitrary required size and zero cost. The total is
E(H)+R, with all original leaves and their order preserved.

## 2. Arbitrary gap weights

For nonnegative q=(q_0,...,q_(N-1)), write Q=max q. At threshold t in (0,Q],
let H_t count weights at least t and R_t count runs of weights below t.
Layering the preceding lower bound gives, for every tree shape,

    gap_cost(T,q) >= G(q) = integral_0^Q [E(H_t)+R_t] dt.

Equality need not hold: different thresholds may prefer incompatible trees.
For q=(100,10,1,10), G=152 whereas the alphabetic optimum is 153.

The order-dependent term has a scan formula:

    D(q) = integral R_t dt
         = Q-q_0 + sum_(i=1)^(N-1) max(q_(i-1)-q_i,0)
         = Q-(q_0+q_(N-1))/2 + (1/2) sum |q_i-q_(i-1)|.

If q_[r] denotes the r-th largest weight, the remaining term is

    F(q) = sum_(r=2)^N (ceil(log2 r)+1) q_[r],
    G(q) = F(q)+D(q).

This follows from E(r)-E(r-1)=ceil(log2 r)+1 for r>=2 and E(1)=0.
The identity can be understood by ordinary finite layer sums; integrals do
not require numerical integration or approximation.

### Computing F without sorting

For a current multiset of M>1 weights, let k be the largest power of two
strictly less than M. All ranks k+1,...,M have coefficient log2(k)+2.
Use deterministic median-of-five selection to retain the k largest weights,
charge that coefficient times the sum of the discarded weights, and repeat
on the retained multiset. A single retained weight contributes zero.

After the first step every retained size halves. The sizes processed are
M,k,k/2,...,2, whose sum is less than 3M. Each selection, partition, sum, and
copy takes linear work in its own size. Thus F and G take O(N) arithmetic
work and O(N) auxiliary space for arbitrary weights. Selection is the
standard deterministic linear-selection method, not a new primitive. Only
groups of at most five are sorted in the implementation.

A cheaper scan-only formula is used when checked multiplicities permit it.
Put h=floor(log2 N), S=2^h, s=N-S, beta=min q. If at least S/2 weights equal
Q and at least s equal beta, then

    F(q)=(h+1) sum q - S Q + s beta.

For beta<t<=Q the selected count is between S/2 and S, on which E(H) is the
affine function (h+1)H-S. The contribution below beta is beta E(N).
The formula also holds for uniform weights and N=1. This multiplicity test
only selects a cheaper evaluation method; it is not an optimality test.

## 3. Key bound and linear recognition of equality

For any mixed BST the key contribution is at least

    K(p)=sum_(r=1)^n p_[r] floor(log2(r)+1).

The coefficient is bit_length(r). At most 2^d-1 nodes can have comparison
length at most d, and rearrangement pairs larger weights with shorter
lengths. The gap bound is valid for every shape, so

    OPT(p,q) >= K(p)+G(q).

A candidate tree's equality with K can be checked without sorting p. Let H
be its number of positive-weight keys, and let d_i be comparison lengths.
Equality holds if and only if both conditions hold:

1. The sum of d_i over positive keys equals sum_(r=1)^H bit_length(r).
2. Every positive weight at a shallower depth is at least every positive
   weight at a deeper depth.

The sorted positive lengths dominate the capacity profile componentwise.
All positive weights are strictly positive, so any excess length makes the
rearranged cost strictly larger. Equality of the unweighted sums forces the
exact capacity profile. The second condition is exactly equality in the
rearrangement step. One traversal collects the sum and per-depth minima and
maxima; adjacent nonempty levels suffice to test the second condition. H=0
is vacuous. Zeros may occupy deeper parts of the tree.

## 4. Full construction and its precise scope

`threshold_complete.attempt(p,q)` constructs the max-Cartesian tree on key
weights, using the standard monotone stack and leftmost priority for ties.
It then checks key equality and gap equality. When both hold, the returned
tree is globally optimal for the original mixed objective. All keys are
reconstructed, including zero-weight keys. Traversal and reconstruction are
iterative, so linear-height candidates require no recursive Python calls.

Screening, successful construction, and auxiliary space are O(n), including
input validation, candidate construction, the general gap formula, equality
checks, and output. These are arithmetic/comparison-operation bounds, not
bit-complexity or machine-instruction bounds. Arbitrarily large integers
increase the cost of arithmetic operations.

`solve` uses exact Knuth DP on failure; `portfolio_solve` first tries the
previous profile certificate, then this certificate, and then the earlier
signature/affine portfolio. Their unrestricted
worst case remains quadratic. A rejected candidate need not be suboptimal.
Ties can hide other attaining trees: p=(1,1,1), q=(1,1,1,1) has a balanced
attaining tree of cost 13, but the chosen Cartesian tree is a chain.
For p=(2,1,1), q=(100,10,1,10), the bound is 158 and the full optimum 160.

If all p_i are positive and pairwise distinct, the attempt is a complete
recognizer of attainment of K+G: any attaining tree orders weights by depth,
so every parent has greater weight than its children. The inorder max-heap
is then the unique Cartesian tree. This recognizes bound attainment, not
all cases where the candidate happens to be optimal.

## 5. A positive family with many key and gap levels

Start with a perfect skeleton of S-1 keys, S=2^h. Its bottom slots have depth
h and indices 0,...,S-1. Expand any s odd slots to cherries, where
0<=s<=S/2. There are n=S-1+s keys. Give every even slot gap weight Q>0,
every unexpanded odd slot an arbitrary weight in [beta,Q], and both gaps
of each expanded slot weight beta, where 0<beta<=Q.

For beta<t<=Q every even slot is selected. Selected gaps are at depth h;
if H are selected, the zero runs number S-H. Since S/2<=H<=S,

    E(H)+(S-H)=hH,

which is exactly the candidate's selected-depth sum. For 0<t<=beta, all
N=S+s gaps are selected and this minimum-path-length shape attains E(N).
Thus the single candidate attains every threshold optimum and hence G.

Give all keys positive weights strictly decreasing between depth layers,
with arbitrary values within each layer. The candidate attains K and has
strictly decreasing ancestor weights, so the Cartesian construction recovers
it. This proves O(n) full optimal construction for the family. Both key and
gap alphabets may have Theta(n) distinct values; gap order need not be
alternating, and no large common baseline is required. The solver receives
only p and q, without a tree, slot pattern, or other witness.

The key and gap vectors may also be scaled independently by any positive
factors: both component equalities persist. The theorem imposes no dominance
condition between the total key mass and the total gap mass.

For the checked family, s=S/4, beta=1, Q=n^2+2, unexpanded odd slot j has
weight j+2, and key i of comparison length d_i has weight

    p_i=(h+2-d_i)(n+1)+i.

All n key weights are distinct; there are S/4+2 distinct gap weights. Key
weights are O(n log n), gap weights O(n^2), and both have O(log n) bits.
At n=327679, full cost is 253331707448885247, with 655322 Cartesian
comparisons, 327679 candidate-key visits, 327680 candidate-gap visits,
327680 gap-bound scan items, and 327679 output keys. No interval-DP cells
or selection calls are used on this scan-formula family.

## 6. Independent evidence and prior work

The independent threshold probe preceded the production constructor. It
checks all 1022 binary leaf patterns through eight keys, across 862118
indicator/tree inequalities, and finds equality with the exhaustive minimum
for every pattern. It also checks 20560 weighted tree inequalities and key
equality characterizations, and 1200 mixed cubic-DP controls.

The constructor harness checks 3000 inputs against independent cubic and
Knuth recurrences, including 2610 literal exhaustive controls, and checks
another 3000 portfolio solves. It retains 885 accepted certificates, 927
key-profile rejections, and 1188 gap-profile rejections. It independently
checks 21844 gap vectors against explicit threshold sums and sorted-rank
sums, 36 positive multilevel fixtures against Knuth, six scaling fixtures
through 327679 keys, and a 20000-key chain with positive key and gap cost.
Twenty selection scaling controls cover random, ascending, descending,
duplicate, and organ-pipe weights through 100000 gaps. Source hashes and
all logical work counters are stored in the two corresponding JSON files.

The binary indicator subproblem is a lemma for the full mixed certificate;
it does not replace the original objective with alphabetic coding.
Cartesian construction, rearrangement, layer decomposition, and deterministic
linear selection are standard tools. Order-sensitive total-variation terms
also occur in prior alphabetic-code upper bounds, including the literature
reviewed by Bruno, De Prisco, De Santis, and Vaccaro (arXiv:2407.16443).
The present derivation is a lower bound and an equality certificate, but
that distinction is not evidence of mathematical priority. Targeted searches
have not settled novelty. The unrestricted mixed-weight problem remains open.

References: Blum et al., *Time bounds for selection*, JCSS 7 (1973),
448-461, doi:10.1016/S0022-0000(73)80033-9; Vuillemin, *A unifying look at
data structures*, CACM 23 (1980), 229-239; Bruno et al., *Bounds and Algorithms
for Alphabetic Codes and Binary Search Trees*, arXiv:2407.16443.

## 7. Matched full construction and routing evidence

`threshold_complete_matched.json` retains 80 matched trials and 400 complete
constructions: five solvers in five cyclic orders, eight families, n=639
and n=1279, exact Python integers on M4/Python 3.9.6/macOS 26.5 arm64.
All costs agree, with direct tree-cost checks outside the timed regions.
At n=1279, median paired ratios are:

| Family | Portfolio / Knuth | Portfolio / previous | Standalone / Knuth |
|---|---:|---:|---:|
| Positive multilevel | 0.00601 | 0.00565 | 0.00562 |
| Gap-bound rejection | 1.07108 | 1.00181 | 1.02028 |
| Uniform tied keys | 0.00200 | 1.05368 | 0.99477 |
| Previous profile | 0.00713 | 0.88792 | 1.00479 |
| Ordinary random | 1.03464 | 1.00206 | 0.99130 |
| Geometric | 1.02515 | 0.96564 | 1.04512 |
| Four signatures | 0.04686 | 1.14112 | 0.99806 |
| Affine | 0.04371 | 1.16128 | 1.01041 |

An initial candidate-first route nearly doubled uniform-route time and added
roughly 50% on old profile fixtures. The final portfolio tests the old profile
certificate first. Counter checks verify zero Cartesian-candidate visits on
those old successes, and the full correctness harness passed again afterward.
Failed certificates still add work; the standalone constructor forfeits old
fast paths. All observations, including regressions, remain in the raw data.

During the final run a read-only host observation reported load averages
25.31, 16.11, 13.19. These are not isolated-machine measurements. Identical
kernels vary substantially, and five observations per row do not establish
precise speedups. Subunit old-route ratios are not saved algorithmic work.
The proved linear bounds and logical operation counts are the scaling evidence.
