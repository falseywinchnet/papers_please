# What an endpoint response does, and does not, preserve

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. These results concern a proposed representation, not a
general lower bound for optimal-BST construction. Priority is unestablished.

For fixed ordered key weights p and gap weights q, define

    F(x,y) = OPT(p, q + x e_0 + y e_n),  x,y >= 0.

For a fixed tree this is C(T)+x*d_0(T)+y*d_n(T). Hence F is the concave
lower envelope of finitely many affine planes. A tempting interval summary
would store this response together with the interval length, total mass, and
endpoint gap weights, and defer the interior until adjacent intervals are
joined. Two distinct obstacles need to be separated: sufficiency of the
summary and the size of an explicit envelope.

## The value response is not a sufficient composition summary

Take the same four key weights in two intervals:

    p  = (1,1,2,3),
    qA = (1,4,2,1,1),
    qB = (1,4,1,2,1).

Both have mass 16, endpoint gap weights one, identical key weights, and even
the same multiset of gap weights. Their response functions are exactly equal
on the entire nonnegative quadrant:

    F(x,y) = min(45+x+2y, 42+x+3y, 43+2x+y,
                 36+2x+2y, 39+3x+y).

This equality has a small finite certificate. Enumerating the 14 four-key
shapes and minimizing the base cost at each endpoint-depth pair gives:

| Endpoint depths | A intercept | B intercept |
|---|---:|---:|
| (1,2) | 45 | 45 |
| (1,3) | 42 | 42 |
| (1,4) | 44 | 45 |
| (2,1) | 43 | 43 |
| (2,2) | 36 | 36 |
| (2,3) | 36 | 37 |
| (3,1) | 39 | 39 |
| (3,2) | 36 | 36 |
| (4,1) | 43 | 42 |

Every plane omitted from the displayed common response is pointwise dominated
by a retained plane whose two slopes and intercept are no larger. Thus this
argument uses no floating-point hull computation or sampled equality test.

Now prepend keys of weights (7,1), append keys of weights (1,7), and give all
four newly introduced gaps weight one. The two full inputs have identical keys

    P = (7,1,1,1,2,3,1,7),

and gap weights

    QA = (1,1,1,4,2,1,1,1,1),
    QB = (1,1,1,4,1,2,1,1,1).

Their full optima are **101 and 100**. Minimum costs conditional on the root
being key 0 through 7 are, respectively,

    A: (108,108,103,101,101,101,111,110),
    B: (108,108,103,101,100,101,111,110).

Independent cubic DP, Knuth DP, and direct enumeration of all 1,430 eight-key
trees agree. Therefore no exact rule can recover all contextual optima from
this value response and the listed metadata alone. In particular, exact
prepend/append updates closed on that summary cannot exist: identical initial
summaries and identical updates would remain indistinguishable, contradicting
the final unequal optima.

The response has discarded a relevant internal alternative. Both intervals
have minimum cost 36 at endpoint depths (2,2). The shape with root key 2,
left child key 0 (whose right child is key 1), and right child key 3 has
those same endpoint depths, but costs 37 in A and 36 in B. Recording only
the least intercept erases that distinction; the surrounding tree can make
the additional alternative valuable.

This does not rule out retaining additional shape information, non-exposed
depth states, signed-parameter responses, or a richer interface. It also does
not claim a barrier specific to mixed weights versus alphabetic algorithms.
It rules out one proposed summary even on small strictly positive mixed inputs.

## Explicit envelopes can require quadratically many pieces

There is a second, independent barrier. A response on n keys has at most
n(n+1)/2 affine pieces: each plane's slopes are the endpoint depths (a,b),
their path union has a+b-1<=n keys, and only a least intercept for each pair
can be needed. This quadratic order is attainable.

Let m>=1, K=4m, and P_i=K*8^i for i=0,...,m-1. A one-sided instance has
these m keys, all m+1 gaps of weight one, and an added left-gap weight x.
Write S_j=sum_{i=0}^j P_i and choose probes x_j=2S_j+2m.

At x_j every optimal tree first uses keys m-1,m-2,...,j+1 as successive
roots, then key 0. To justify this, an endpoint key and its adjoining outer
gap are forced to the root when their combined weight exceeds every other
weight in the interval. Rotating that key toward the root saves one comparison
on both outcomes at each step and adds at most one to each other outcome.
The strict inequality makes every such rotation improve the tree.

For k>j,

    P_k+1 > S_(k-1)+x_j+k+1,

and in the remaining prefix,

    P_0+1+x_j > (S_j-P_0)+(j+1).

The geometric weights and K=4m imply both inequalities. Thus the left endpoint
gap has depth exactly m-j in every optimum. All m possible slopes 1,...,m
occur on open intervals of x: strict inequalities persist under small changes.

For a two-sided instance, put a mirrored copy on the right of a central key:

    p = (P_0,...,P_(m-1), R, P_(m-1),...,P_0),
    q = (1,...,1),  n=2m+1.

Let X=x_(m-1), S=S_(m-1), B=2S+2m+2+2X, and R=(2m+2)B.
For 0<=x,y<=X the outside mass is at most B. A center-root tree costs at
most R+nB<2R, whereas any tree with another root costs at least 2R from
the central key alone. Therefore the center root is forced throughout the box.
At every (x_j,x_k), the endpoint-depth pair is

    (m-j+1, m-k+1).

These are m^2 different gradients. All optima at each probe share its gradient,
so finiteness of the set of trees gives an open affine region around the probe.
Distinct gradients require distinct affine pieces. Consequently an explicit
list of all pieces can require Omega(n^2) entries for a **single interval**.

All weights are positive integers, but their bit lengths grow as O(n).
This is an arithmetic/output-size obstruction to explicit facet enumeration,
not a word-RAM lower bound with O(log n)-bit weights and not a lower bound
for arbitrary exact representations or for a single OPT query.

## The same quadratic envelope has a linear-size factorization

The preceding example deliberately demonstrates why facet count alone is not
enough to exclude implicit representations. Let H_m(x) denote its one-sided
response. With

    C0 = sum_i (m-i) P_i + m + m(m+1)/2,

the exact response for all x>=0 is

    H_m(x) = C0 + m*x - sum_(i=1)^(m-1) max(0, x-(P_i-P_0)).

At x_j the forced optimal tree is the high-key root chain above key 0, whose
right subtree is the remaining decreasing-key chain. Passing from j to j+1
rotates key 0 above key j+1. At base weights the intercept increases by
P_(j+1)-P_0 and the endpoint slope decreases by one. Every possible endpoint
depth occurs among these m trees; because each is optimal at a probe, its
intercept is minimal for that depth. Their lower envelope gives the formula.

The two-sided response within the forced-center box is

    R + 2S + 2m + 2 + x+y + H_m(x)+H_m(y).

In fact the entire quadrant has a linear-size factorization. Write

    W = R+2S+2m+2,  V = W-P_0-1,
    L = C0-m*P_0-m-1,
    J = R+2(S-P_0)+2m+2L.

Here L is the fixed cost of keys 1,...,m-1 with unit gaps; J is the fixed
cost of the inner interval after removing both outer keys and outer gaps.
For all x,y>=0, the exact full response is

    W+x+y + min(H_m(x)+H_m(y),
                V+y+L+H_m(y), V+y+J,
                V+x+L+H_m(x), V+x+J).

To prove it, any root other than 0,m,2m gives both added endpoint weights
depth at least two and gives the central key comparison length at least two.
A center-root candidate with the two outer keys as its children also gives
both endpoints depth two, but its base cost is at most R+n(W-R)<2R.
Thus such a root is strictly worse for every x,y>=0. If root 0 is used,
the remaining one-sided problem similarly has only the center and the other
outer key as possible roots; symmetrically for root 2m. Expanding these five
possibilities gives the formula. The choices also give an exact reconstructed
tree, using the one-sided chains specified above.

The full quadrant has exactly **m^2+2m+2** affine pieces. The center-root term
has m^2 candidate slopes, all already exposed by the original probes. Each
outer-root term has m+1 slopes: the m one-sided pieces and a final piece after
the opposite outer key becomes the next root. All are exposed by choosing
the first outer endpoint's added weight sufficiently large. These slopes have
one coordinate equal to one and are distinct from the center-root slopes.
The displayed five-term minimum supplies the matching upper bound.

The representation retains only 2(m-1) hinge terms and five outer alternatives.
Sorted thresholds and prefix sums support O(log m) value queries after O(m)
arithmetic preprocessing; outputting the complete tree takes O(m). The
`FactoredFamily` implementation counts threshold comparisons, four outer-minimum
comparisons, and exactly n constructed keys per solve. The quadratic facet
theorem therefore cannot be promoted to a quadratic expression-size theorem.
This factorization does not repair the composition counterexample: even a
lossless representation of the value function discards information that a
larger surrounding tree may need. The geometric family is already easy for
endpoint-dominance shortcuts; it demonstrates a cost of explicitly listing
responses, not hard single queries.

## Positive endpoint weights bound the response complexity

There is also a favorable parameter regime. Let W be the original total mass,
with q_0,q_n>0. In any optimum after adding arbitrary x,y>=0, if the left
endpoint depth is a>=2, its last internal ancestor lies at depth a-2 within
the root's left subtree. That subtree is optimal and excludes the opposite
endpoint and its added y. Its mass is at most W+x, while the last ancestor's
subtree has mass at least q_0+x. The proved mixed Fibonacci mass bound gives

    F_(a-1) <= (W+x)/(q_0+x) <= W/q_0,  F_1=F_2=1.

Similarly, F_(b-1)<=W/q_n. Therefore the entire unbounded-parameter response
has at most

    O(log(2+W/q_0) * log(2+W/q_n))

affine pieces, also bounded by O(n^2). In particular, polynomial endpoint
mass ratios give O(log^2 n) pieces. The arbitrary x,y additions do not appear
in this bound. The geometric lower-bound example has exponential base mass
ratio, so the two results are consistent.

This bounds the number of pieces, not the work to find them. More importantly,
the small counterexample already has only five pieces: small response size
does not imply that the response is sufficient for exact interval composition.

## Verification and next step

The standard-library exact-arithmetic harness is `code/boundary_response.py`;
raw results and its source hash are in `results/boundary_response.json`.
It passes 875 response queries against cubic DP on 175 small inputs, with
rational half-plane clipping to check the exposed envelopes; 725 retained
planes satisfy the endpoint Fibonacci bounds. On the geometric family it
checks 408 hinge queries including exact thresholds and neighboring integers,
1,496 two-parameter probes through 33 keys, 204 full cubic comparisons,
30 all-shape checks that every optimum has the prescribed depth pair, and
680 strict endpoint inequalities. The product checks execute 887,808 Knuth
root candidates. Another 304 queries expose every outer-root piece, and
384 arbitrary/global-threshold queries test the complete factorization.
All 2,184 factored complete constructions match Knuth and direct tree cost,
and construct exactly n keys. Exact full-quadrant envelopes through nine
keys have 5, 10, 17, and 26 pieces, agreeing with the proved formula.
Across all factored solves there are 14,492 threshold comparisons, 8,736
outer-minimum comparisons, and 52,232 constructed keys, excluding reference
solver work.

The collision search found the original context with outer weights 16; reducing
them to seven preserves a one-unit optimum difference. The published reduced
certificate checks domination algebraically and enumerates both eight-key
instances independently, without relying on clipping or sampled parameters.

The next representation must retain something about the sequence of decisions
along the boundary paths, or about internal alternatives that the isolated
endpoint response discards. These obstructions prevent two tempting shortcuts
from being mistaken for a general solution. They neither resolve nor replace
the full mixed-weight subquadratic objective.
