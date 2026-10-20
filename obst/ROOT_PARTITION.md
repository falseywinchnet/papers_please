# Root/nonroot coupling beyond every additive separable transfer

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. The full mixed-weight objective remains active. These are
exact certificates and a proved separation from the preceding bound class;
there is no unrestricted subquadratic algorithm or impossibility theorem here.
Mathematical priority has not been established.

## A positional dichotomy with three alphabetic constructions

For arbitrary nonnegative key weights p and gap weights q, let K(p) be the
minimum key-capacity bound and A(q) the exact alphabetic gap optimum. Choose
an index r of a largest key weight w=p_r, and let v be the largest remaining
key weight. Assume n>=2. Write P=sum(p), Q=sum(q), and define

    N_r = K(p) + A(q) + w-v,
    R_r = P+Q + K(p[:r]) + K(p[r+1:])
                  + A(q[:r+1]) + A(q[r+1:]).

Then

    K(p)+A(q) <= min(N_r,R_r) <= OPT(p,q).

Proof for the nonroot case: in any tree whose root is not r, exchange the
weights at r and the root, retaining the tree shape. The exchanged key cost
is at least K(p). If r has comparison length l>=2 and the root weight is u,
the original cost exceeds the exchanged cost by (w-u)(l-1)>=w-v. Adding the
unconstrained alphabetic minimum proves N_r. This exchange is only an argument
for a lower bound; it does not alter the ordered input or construct a BST.

For root r, the recurrence pays P+Q and then the two ordered subproblems.
Separately bounding their keys and gaps gives R_r. The two cases partition
all full trees, so their minimum is a lower bound. Both case bounds are at
least K(p)+A(q): the root-constrained free key placement costs at least K,
and the root-constrained gap tree costs at least A. This domination applies
at the chosen weights; it is not domination of every other reweighting.

The implementation first applies the preceding exact maximal interior
transfer a=min(p[1:-1]), with endpoint residuals max(0,p_0-a) and
max(0,p_(n-1)-a). It subtracts an from every transformed bound. Original
weights remain the objective for all candidate evaluations.

It constructs the global alphabetic optimum and sorts residual keys once.
The subsequences of that order on either side of r give both conditional
capacity sums in one scan. If the first candidate already meets K+A, it
returns immediately. Otherwise two more alphabetic calls construct the
left and right gap optima. It compares the original mixed costs of the
global alphabetic candidate and the tree joining those children at r.
Equality with min(N_r,R_r)-an certifies global optimality. There are at most
three alphabetic calls over a total of 2(n+1) leaves, one key sort, and linear
normalization, rebasing, reconstruction, and cost scans:

    O(n log(n+1)) arithmetic operations and O(n) space.

At n<3, a constant-size exact base case is used. Rejection uses exact Knuth,
so unrestricted worst-case work remains quadratic. The preceding portfolio
and two-price solver are unchanged. This standalone route can reject cases
that a different endpoint price certifies; it is not a universal replacement.

For the published four-key obstruction, maximal normalization gives
p'=(0,0,1,0), q'=(2,3,2,2,2), with additive constant four. Here K=1, A=26,
r=2, w-v=1, N_r=28, and R_r=28. The new full bound is 24, exactly the optimum;
the maximum over the entire preceding additive separable class is only 23.

## An infinite positive family outside the whole preceding class

Let h>=3, N=2^h, n=N-1. In the perfect tree let

    l_i=h-v_2(i+1), r=N/4-1, s=N/2-1,
    C=4hN, w=hN^2/2.

Initially set p_i=1+(h-l_i)N+i+1, then replace

    p_0=p_2=p_(n-1)=1, p_r=w+1.

Set q_j=C+j-1 for 0<=j<N. Every original weight is positive, all weights have
O(log n) bits, there are n-2 distinct key weights, and all n+1 gap weights
are distinct. Only the three bottom keys explicitly set to one coincide.

The maximal interior transfer is a=1. At endpoint prices zero, residual
keys P_i=p_i-1 have their largest value w at r, the next-largest value
v=(h-1/2)N at the perfect root s, and three zero bottom keys. Transformed
gaps are Q_j=C+j. All other residual key weights decrease strictly between
depth layers. The perfect tree attains the conditional nonroot key bound
K(P)+w-v: moving w to the root and v to r attains the free capacity bound.

All transformed gap weights lie between C and C+N-1<2C. With N a power of
two, unrestricted Huffman pairs nodes level by level; the resulting depth
vector is uniformly h. The perfect alphabetic tree attains that unrestricted
minimum, so

    A(Q)=h[CN+N(N-1)/2].

If r is the root, the left and right alphabetic subtrees contain N/4 and
3N/4 gaps. Their minimum unit-weight total depth, including the root, is
Nh+N/4. Consequently, since all Q_j>=C, the root-r alphabetic cost exceeds
A(Q) by at least

    CN/4 - hN(N-1)/2 = w+hN/2 > w-v.

Its conditional key bound is at least K(P), so R_r>N_r. The perfect tree
attains N_r and the new certificate proves it fully optimal in O(n log n).

The exact full cost and deficit of the preceding best separable bound are

    OPT = [(8h^2+6h-7)N^2+(12-5h)N]/2 + 1-3h,
    D   = [hN^2-(2h-1)N]/2.

To derive the cost, use sum l_i=(h-1)N+1,
sum l_i^2=N(h^2-2h+3)-3, and symmetry
sum (i+1)l_i=(N/2)sum l_i. After the three zero-key corrections and the
replacement at r, the perfect residual key cost is
(5h-7)N^2/2+(7-2h)N-3h. Add A(Q) and subtract n.

This deficit survives **every** admissible additive transfer, not just the
chosen normalization. The preceding maximal-face theorem reduces all transfers
to a=1 and endpoint prices x,y. At x=y=0, both zero endpoint keys occupy
capacity slots of length h, and both endpoint gaps also have depth h.
The supporting plane for K+A therefore has both slopes zero and value
K(P)+A(Q). It bounds the price objective everywhere in the endpoint box.
The value is attained at zero, so the entire transfer class has maximum
K(P)+A(Q)-n=OPT-D, strictly below the full optimum.

Twelve full constructions reach n=262143, with 262141 distinct key weights,
262144 distinct gap weights, and exact cost 92530765201355. The preceding
maximum is 91912294498251, leaving deficit 618470703104. The largest run uses
three alphabetic calls, 524285 compatible merges, 13894100 priority comparisons,
17365446 heap-item comparisons, and 1482337 key-sort comparisons. All scans,
heap operations, tree rebasing, and output visits are recorded. There are no
interval-DP cells. Seven sizes through 511 keys match Knuth; three also match
cubic. All larger sizes match a separately constructed perfect tree and the
proved closed form. Six smaller sizes additionally complete the exact
endpoint-price maximum and verify the claimed deficit independently.

## Harness-first evidence and limits

The independent root/nonroot harness precedes the optimized constructor.
Across 840 mixed instances through eight keys it checks 246480 literal
conditioned inequalities, with random, near-uniform, geometric, and zero/binary
weights. The new bound strictly improves K+A in 373 cases and is exact in 324.

The full normalized implementation matches independent cubic, Knuth, and
reconstructed original cost on 1040 instances through 64 keys. Of these,
720 also match literal tree enumeration. There are 800 independent bound
controls, plus six family checks. The route certifies 505, including all
240 constant-size base cases, and falls back on 535. It improves upon the
*completed* maximum transfer bound in 84 cases and rescues 11 price rejections,
but loses 47 price certificates. These are finite suite counts, not distributional
success guarantees. The fixed endpoint choice and candidate tie selection
matter; different valid certificates need not dominate one another.

## A retained diagnostic: one marked merge is not greedily decidable

A separate research probe places a marker at the interior key and charges its
weight when a compatible pair first crosses that marker. Always selecting the
cheapest eligible event fails even on three keys. For residual
p=(0,4,0), q=(8,10,2,18), the marked merge of cost 16 is strictly cheaper than
the two ordinary choices of costs 18 and 20. Its next merge costs 24 instead
of 26 or 34; total charge and reconstructed full cost are 82. The five tree
costs are 80, 96, 92, 82, and 84, so the optimum is 80. Inverting a unit uniform
transfer gives the all-positive full instance p=(1,5,1), q=(7,9,1,17), where
this route returns 79 and the optimum is 77. All primary choices are strict.

The alternative probe performs ordinary merges while the marker remains,
and at every prefix tries activating the cheapest crossing pair, then completes
ordinary compatible merging. All reconstructed trees are evaluated with the
original positional key cost. An invalid reconstructed depth sequence is
rejected. It matched the optimum on 17769 cases: 14769 exhaustive small-alphabet
inputs and 3000 seeded mixed-shape controls through 32 keys. There are 15769
literal-tree oracle checks. In 4134 cases, all eligible crossing choices were
also enumerated, without changing the best result. This is evidence for a
candidate-family conjecture, not a proof or a production solver.

Its objective is not unimodal in the activation prefix. With q=(1,1,1,1),
r=1, and marked weight one, the exact candidate costs are 9,11,9. Thus a
single-valley search is unjustified. The recorded suite contains 6759
nonunimodal sequences, 116 greedy failures, and 65 disagreements between a
greedy merge charge and the reconstructed positional cost. Across all event
attempts, 20800 depth sequences fail reconstruction. The probe retains full
scan/copy/comparison counts; it has no claimed subquadratic complexity.

The root/nonroot certificate above does not depend on this conjecture. It
retains positional coupling through a proved exhaustive case partition.

A strict positive-gap nonunimodality example is q=(17,83,93,11), r=1,
and marked weight 92. The ordinary left merge costs 100, then the right
merge costs 104. Activating before, between, or after them gives costs
500,681,500. The initial forced crossing has mass 268 and its completion
first merges the outer gaps at cost 28. Thus the failure of a single-valley
assumption does not depend on zero weights or a tie between ordinary merges.

## Full-construction timing controls

The matched run has 88 trials and 352 complete constructions: four cyclic
solver orders, eleven families, and two nominal sizes. It includes the new
route, bounded pricing with fallback, the earlier portfolio, and
Knuth. At 511 keys, median paired new/Knuth ratios are 0.25899 on the new
family, 0.12370 on the preceding endpoint family, 1.21721 random, 1.31079
near-uniform, and 1.18771 geometric. The old profile, four-signature, and
affine routes cost 15.47, 51.74, and 43.04 times the previous portfolio;
the 319-key old multilevel case costs 8.35 times it. All regressions remain.

The host is Apple M4, Python 3.9.6, macOS 26.5 arm64. Load averages were
12.42/11.62/11.38 initially and 12.53/11.69/11.41 finally. Four observations
per case, same-process cycling, and visible variability limit the precision
and portability of the timing ratios. Logical counts include rejected
certificates and full fallback. Proofs establish the arithmetic bounds;
bit costs are additional. This route is retained separately, with no claim
that it should replace the earlier portfolio or optimized prior solvers.
