# A depth-sequence lower bound with an exact affine tail

Research checkpoint, 2026-10-18. The depth identity below is existing work
(for example Becker 2010, Lemma 1). The multiplier construction and tail
argument were derived in this investigation; novelty has not been established.
This is a certified lower bound, not an exact solver for arbitrary inputs.

## Exact representation on feasible trees

Let l_i be one plus the depth of key i. Adjacent keys cannot have equal
depth: one is an ancestor of the other, since their LCA would otherwise
be a key strictly between them. Their intervening gap is a child of the
deeper key. Consequently

    g_0=l_0, g_n=l_(n-1), g_i=max(l_(i-1),l_i) for 0<i<n,
    cost = sum p_i*l_i + sum q_i*g_i.

Let K_d count keys with comparison length d, and G_d count gaps at depth d.
The tree has exactly one root and every internal node has two children:

    K_1=1,
    G_d+K_(d+1)-2*K_d=0, 1<=d<=n, with K_(n+1)=0.

These necessary conditions are not sufficient for a valid ordered tree.

## Lagrangian relaxation

Permit any length sequence in {1,...,n} with unequal adjacent lengths.
For arbitrary real multipliers lambda_0,...,lambda_n, define

    L(lambda) = min_l [ cost(l) + lambda_0*(K_1-1)
                       + sum_(d=1)^n lambda_d*(G_d+K_(d+1)-2*K_d) ].

Every actual BST is a feasible length sequence and has zero penalty, hence
L(lambda)<=OPT for every multiplier vector, regardless of how it was chosen.
Rewrite the expression as a chain with unary key terms

    U_i(b)=p_i*b+lambda_(b-1)-2*lambda_b

and gap terms

    V_i(b)=q_i*b+lambda_b.

The constant is -lambda_0, and an interior gap contributes
V_i(max(a,b)). Its DP transition into b is the minimum of

    min_(a<b) F(a) + V_i(b),
    min_(a>b) [F(a)+V_i(a)].

Prefix and suffix minima evaluate every transition in O(H) per key for
a height domain 1,...,H. Backpointers reconstruct the minimizing sequence
and its constraint violations. A full n-height oracle costs O(n^2).

## Affine-tail lemma (no assumption about the optimal BST height)

Choose a cutoff h>=1. Permit arbitrary lambda_0,...,lambda_h, then extend

    lambda_d=lambda_h+s*(d-h), d>h,
    0<=s<=min_i p_i.

For b>=h+1, the unary key energy is affine with slope p_i-s>=0, and
the gap energy is affine with slope q_i+s>=0. Thus both are nondecreasing
through this tail.

Take any allowed length sequence containing l_i>h+3. Choose a replacement
from {h+1,h+2,h+3} unequal to both current neighboring lengths; there are
at most two forbidden values. This decreases l_i without increasing its
unary term. Either adjacent maximum is unchanged or decreases within the
affine tail, so neither gap term increases. Endpoint gaps obey the same
argument. The new sequence remains allowed. Repeat for every large length.

Therefore the full oracle over lengths 1,...,n has EXACTLY the same minimum
as the oracle over 1,...,min(n,h+3). This does not impose a height bound on
actual BSTs; it compresses the minimization in the relaxed lower bound.
Choosing h=ceil(log2(n+1))+2 gives O(n log n) work per oracle evaluation.

When optimizing the head prices, lambda_h controls the entire tail. Its
subgradient is the sum of the violations for d>=h, not just the violation
at h. The implementation folds these components before updating prices.
The affine slope is held fixed.

## Exact arithmetic and optimizer scope

`code/depth_dual.py` scales costs by 1024 and uses integer multipliers.
Every returned value divided by 1024 is a rigorous lower bound; no floating
point is used in the oracle or multiplier updates. Floating point is used
only to print normalized experimental gaps.

The ascent procedure is heuristic. It evaluates a balanced-weight and a
zero-head initialization, then uses an upper-bound-based subgradient step
with a decreasing step factor. There is no claim that 300 iterations find
the best multiplier vector. Any number of iterations retains validity.
The upper bound is the directly feasible bisection tree, not the optimum
from the oracle used to check the experiments.

The head initialization is informed by uniform weights: if all key weights
are P and all gap weights are Q, the family

    lambda_d=P*(d-1)+A*2^(-d)

makes the unary key terms constant and the gap terms a discrete convex
function of depth. Taking A=(P+Q)*2^ceil(log2(n+1)) supports the appropriate
two neighboring leaf levels. The implementation uses integer rounding and
an affine continuation; arbitrary prices still yield valid bounds.

## A definite limitation

Even exact global level counts do not characterize a BST. For n=5, take

    l=(3,1,2,3,2), g=(3,3,2,3,3,2).

Adjacent lengths differ, K_1=1, and every level-flow equality holds. Yet the
sequence is not a BST depth sequence: the single key to the left of the
root has length 3 rather than 2, while both length2 nodes lie on the right.
For positive weights

    p=(3,27,21,16,12), q=(18,22,27,22,12,22),

this inadmissible sequence costs 470, whereas the true optimum costs 472.
It has zero penalty for EVERY multiplier vector. Hence this entire dual
family is bounded above by470 on that instance, even with unlimited
optimization time and no truncation. It cannot be a universal exact
certificate without further ordering constraints.

## Verification and next discriminator

The harness compares the prefix/suffix oracle with exhaustive length-sequence
minimization through n=5, tests arbitrary signed multipliers against the
independent full-OBST cubic oracle, and compares the full and shortened
oracles directly on random affine-tail prices. These checks distinguish
oracle correctness, lower-bound validity, and the tail-compression claim.

The completed checks comprise 50 exhaustive-sequence oracle comparisons,
5,000 arbitrary-multiplier bound checks, and 1,050 direct full-versus-shortened
oracle comparisons. The latter include arbitrary signed head prices and
positive affine slopes. The unique-root version described below passed the
same checks; every forced-root marginal was also checked against an exact
root-constrained cubic cost.

## Unique-root strengthening and root marginals

The stronger oracle requires exactly one length1 label and all other labels
at least2. For each candidate root r, the left and right sequences decouple:
the gap joining a nonroot label b to root length1 has energy V(b). One forward
chain pass gives every left-prefix closing cost; a mirrored pass gives every
right-suffix closing cost. Add the root unary energy and subtract lambda_0.
This evaluates the lower bound for every forced root in O(nH) total time.
The affine-tail projection never changes a length1 label and never creates
one, so the truncation lemma holds for each forced-root marginal separately.

For each root retain its maximum bound over evaluated multiplier vectors.
The minimum of these maxima is a valid whole-instance lower bound, even
though different roots may use different vectors. A root with bound at least
the cost of an existing feasible tree cannot improve that tree. Eliminating
every improving root certifies the feasible tree as optimal.

This strengthens the relaxation at fixed multipliers, but the heuristic
optimizers follow different paths; their best bounds after a fixed iteration
budget need not preserve the same ordering.

## Preliminary results and a negative performance finding

All gaps below are (OPT-LB)/total_weight on the same seeded n=256 inputs:

| Family | Order-free Huffman | Chain dual | Unique-root dual |
| --- | ---: | ---: | ---: |
| Random mixed | 0.22080 | 0.15003 | 0.15223 |
| Log-uniform | 0.69807 | 0.33324 | 0.35872 |
| Alternating | 0.49294 | 0.00873 | 0.01488 |
| Gap spike | 0.99923 | 0.00120 | 0.00080 |

At 300 ascent iterations the chain version evaluates 1,082,368 key-depth
cells including initialization, versus 32,896 nonempty interval states in
Knuth's DP. The unique-root version uses two passes, or twice that cell
count. These cells have different constant costs; neither count supports
a speedup claim at this size.

The unique-root marginal bounds leave 254 of 256 roots capable of improving
the bisection upper bound on the random instance, and 255 on the alternating
instance. Only two survive on the gap-spike instance. A tighter cost bound
is therefore not automatically an effective root-pruning bound. This is an
experimental lower-bound component, not a competitive exact solver.

The proposed short-window repair has now been checked: DEPTH_ORDER.md gives
an exact characterization using all intervals, and a positive-weight
obstruction for every window width. At a chosen weight scale the latter
limits the repaired bound to at most 113/128 of OPT, for any multipliers.
This does not preclude pruning benefits on particular inputs, but rules out
universal exactness for that repair. Additional top-level subtree structure
or adaptive nonlocal constraints remain possible directions.

Primary reference for the depth identity:
Peter Becker, *Optimal Binary Search Trees with Near Minimal Height* (2010),
Lemma 1, https://arxiv.org/abs/1011.1337.
