# Which endpoint responses retain the original interval?

Two exact results separate information loss from the cost of constructing
or composing a representation. Reassigning the two endpoint gap weights
to arbitrary nonnegative values is still insufficient for composition.
Allowing signed endpoint prices, however, determines all original gap
weights when the key vector, total mass, and left endpoint gap are retained.
For nonnegative integer input, at most n exact value queries recover them.
This is an oracle-recovery theorem, not a new general OBST construction.

## The entire legal endpoint domain can lose information

Fix keys p=(2,1,2,4) and internal gaps (4,2,1) or (4,1,2). Let R(u,v)
be the exact optimum with the endpoint gaps set to u,v>=0. Both responses
are identically

    min(45+u+2v,42+u+3v,43+2u+v,36+2u+2v,39+3u+v).       (1)

This follows from the existing four-key certificate: move each old outer
gap's unit weight to its adjacent endpoint key. Their depths are equal in
every isolated tree, so every shape's base cost is preserved. The same
nine endpoint-depth intercepts and coordinatewise domination proof apply.
Thus (1) is equality on the entire legal endpoint domain, including zero,
not merely equality under nonnegative additions to fixed positive gaps.

Choose actual endpoint gaps one. Both original inputs are strictly positive,
have mass 18, the same keys, and the same gap multiset. Prepend keys (1,6),
append keys (4,3), and give all four new gaps weight one. The full key vector
is (1,6,2,1,2,4,4,3); its gap vectors are

    A=(1,1,1,4,2,1,1,1,1), B=(1,1,1,4,1,2,1,1,1).

The root-conditioned cost vectors are

    A=(128,106,103,101,101,101,109,120),
    B=(128,106,103,101,100,101,109,120).

The full optima differ, 101 versus 100. Direct ordered-tree enumeration
and the original all-root recurrence independently verify these finite
certificates. Therefore the complete legal endpoint-response function and
those metadata cannot determine every contextual optimum.

## Extreme boundary-depth states recover the gap vector

A tree whose endpoint depths are a,b uses a+b-1 distinct keys on the two
boundary paths. Thus a+b<=n+1. Equality forces all keys onto those paths:
for each root r=0,...,n-1 there is exactly one such tree, with a=r+1,b=n-r.
Its left subtree is a decreasing left chain, and its right subtree an
increasing right chain. Let its original cost be C_r.

For a fixed outcome, its depth in neighboring chain trees changes by at
most one, so |C_r-C_(r-1)|<=W. Direct second differencing gives

    C_(r-1)-2C_r+C_(r+1)=2p_r+q_r+q_(r+1) >= 0.          (2)

The sequence C is convex. At the left boundary,

    C_1-C_0=2(p_0+q_0)+q_1-W.                            (3)

Consequently, given p, W, q_0 and the n chain costs, recover

    q_1=W+C_1-C_0-2(p_0+q_0),
    q_(r+1)=C_(r-1)-2C_r+C_(r+1)-2p_r-q_r,
    q_n=W-sum p-sum_(j=0..n-1)q_j.                       (4)

These are O(n) arithmetic operations. For n=1, the mass identity alone
recovers q_1. Thus the complete endpoint-depth profile, including its
non-exposed states, is sufficient with these metadata: the n states on
a+b=n+1 already determine the entire original input. In particular, no
collision preserving this profile and the stated metadata can exist.

The chain costs themselves can be constructed in O(n) from the input.
Start with C_0=sum_i(i+1)p_i+q_0+n q_n+sum_(j=1..n-1)(j+1)q_j,
use (3) for the first difference, and then (2) for successive differences.
This is a lossless change of coordinates, not a shortcut for computing the
full optimum of a joined input.

## A bounded signed line exposes every chain cost

Define the signed response

    F(x,y)=min_T [cost(T)+x*d_0(T)+y*d_n(T)],   x,y real.

It remains a finite minimum over ordinary ordered tree shapes even when
the two resulting endpoint weights are negative. Set

    M=n+1, T=4(n+1)(W+2), x=-T+t, y=-T, |t|<=W+2.

Every non-chain tree has a+b<=n and value at least -Tn-n|t|. Every chain
has value at most nW-T(n+1)+n|t|. The latter is strictly smaller because
T>nW+2n|t| throughout the stated range. Therefore

    G(t):=F(-T+t,-T)+T(n+1)=min_r[C_r+(r+1)t].             (5)

Convexity (2) and the bound on first differences expose every C_r on this
line, with ties allowed. Explicitly,

    C_r=sup_(|t|<=W+1) [G(t)-(r+1)t].                    (6)

Equations (4)--(6) prove information sufficiency for arbitrary nonnegative
real input weights. The signed domain is essential to this argument. For
the collision (1), already the absolute endpoint assignment (u,v)=(0,-1)
gives different values, 33 and 34; it is outside the legal nonnegative domain.

## Integer input: at most n value queries, without witnesses

Assume original weights are nonnegative integers and n>=2. A query must
return only its exact value, not a tree or slope. At a rational t_0=A/B
in lowest terms, B>0, query at

    t=t_0+1/(B M).

The unperturbed scores are multiples of 1/B. The perturbation changes any
pairwise difference by less than 1/B, so the minimizing chain is the one
with smallest index among the minimizers at t_0. Write its endpoint depth
a=r+1. From the returned G(t), the integer

    z=B M G(t)=B M C_r+a(A M+1)

satisfies z mod M=a, with 1<=a<=n<M. This recovers r and then
C_r=G(t)-a*t exactly from the scalar response.

Queries at t_0=W+1 and -W-1 recover C_0 and C_(n-1). For known endpoints
l<r with r-l>=2, query at t_0=(C_l-C_r)/(r-l). If the recovered minimizer
lies on the chord, convexity forces every intervening C_j onto that chord;
fill them by interpolation. Otherwise its index k lies strictly inside
(l,r), and recurse on (l,k) and (k,r). A minimizer outside the interval can
occur in the collinear case and is harmless: the algorithm tests equality
of the unperturbed score, not membership of the decoded index.

Every nonterminal query either discovers a new interior coefficient or
fills at least one previously unknown coefficient. Interior sets of the
recursive subproblems are disjoint. Thus the total, including the two
endpoint queries, is at most n. Interpolation and recursion use O(n)
additional arithmetic work and O(n) space; (4) completes recovery.
For interior queries B<=n-1, so all queried rational coordinates have
denominator at most n^2-1 and bit length O(log(n(W+2))). All prices have
magnitude O(n(W+2)). There is no numerical limit or infinitesimal oracle.

The known chain sequence supports (5) by binary search on its monotone first
differences, in O(log(n+1)) comparisons after O(n) preprocessing. That
restricted oracle is implemented separately. No faster general signed-OBST
oracle or fast composition rule is inferred. In particular, ordinary
nonnegative-weight Knuth monotonicity is not invoked on signed instances.

## Audit

The harness checks all binary mixed inputs through four keys and seeded
integer inputs through 24 keys, including geometric, uniform, gap-only,
key-only, and all-zero cases. Small queries use a fresh all-root recurrence
with signed endpoint weights; literal shapes provide another independent
reference through seven keys. The legal-domain equality is verified by
complete intercept tables and exact domination, and both eight-key contexts
are checked by full shape enumeration. Larger rows use only the proved
chain restriction and are labeled accordingly. Counts, seed, collision
certificates, and executed-source hashes are in signed_boundary_audit.json.
