# Cubic actual-prefix diagrams and quartic shared history

The missing all-stage size estimate has an explicit obstruction. There are
strictly positive mixed OBST instances at their necessary optimal height
whose final canonical punctured diagram has Omega(n^3) nodes. Even sharing
identical normalized nodes across every prefix, the retained history has
Omega(n^4) distinct nodes. These are lower bounds for the representation.
The same inputs have a directly certified unique right-chain optimum.

## Family and exact bounds

For n>=2, set A=4n+1 and

    w_i=A^(n-i), p_i=w_i-1 (0<=i<n), q_j=1 (0<=j<=n).

Common-gap normalization gives w, zero residual gaps, and additive cost n.
Since n sum_(j>i) w_j < w_i, the usual suffix dominance argument forces the
first key to be the root of every suffix. Thus the unique optimum is the
right chain, its height is n, and its original cost is

    n + sum_(i=0)^(n-1) (i+1) w_i.

Let f_k(b) be the k-key ending-slot cost at h=n. Write D_k for its canonical
punctured node count and H for the number of distinct nodes in the union of
all these diagrams, with full cross-prefix sharing. Put

    Q=2 ceil(n/2), d0=ceil(log2(Q+1))+2, N=max(0,n-d0).

Then

    D_k >= L_k := sum_(t=1)^N (N-t+1) min(t,max(0,k-3)),
    D_n >= binomial(N+2,3) = Omega(n^3),
    H   >= (n-2) binomial(N+2,3) - binomial(N+3,4) = Omega(n^4).

The last conclusion counts distinct shared nodes, not just a sum that might
count the same node again at different stages. It therefore applies to the
actual retained representation used for traceback. The final-stage bound
also applies if earlier roots are discarded.

## Integer coefficients survive additive normalization

A valuation vector has entries in [0,n-1]. Two differences of valuation
vectors cannot have the same weighted sum unless they are identical:
if their difference has first nonzero coefficient at i, its leading term
has magnitude at least w_i, while the remaining terms have magnitude at most

    2(n-1) sum_(j>i) w_j < 2(n-1) w_i/(A-1) < w_i.

This is why the convenient base here is 4n+1. It lets us recover each
coefficient vector from an exact scalar difference of two function values.
Additive normalization preserves those differences.

## Three entries identify a block and its prefix

For each depth d0<=d<n, choose s and r with

    d<=s<n, 1<=r<=min(n-s,k-3).

Choose a dyadic boundary B with exactly r high one bits, the lowest at s.
For example, use the top r-1 bit positions n-1,...,n-r+1 and bit s.
The punctured block is B+t, 1<=t<2^d; it lies inside [1,2^n-1].
Its three test addresses are

    t*=1, t-=2^(d-2)+Q, t+=2^(d-1)+Q.

They are interior because 2^(d-2)>Q>=n. All entries are finite. For an
ending slot b, lexicographic dominance makes its first k-1 selected slots
the greedy maxima of valuation in the successive feasible intervals; the
last slot is forced to be b. Let v(t) be the resulting k-coordinate
valuation vector. Then f_k(B+t)=-sum_i w_i v_i(t).

At t- and t+, the first r choices are the partial sums of the r high bits
of B. Each is feasible: at least n positions remain beyond the boundary,
and each earlier high bit has still more space. They are the unique
highest-valuation feasible positions. There remain m=k-1-r>=2 predecessor
slots to choose after B. Their first feasible upper endpoint, relative to B,
is t-m. Since 0<Q-m<2^(d-2), the next greedy choice has valuation d-2
at t- and d-1 at t+. Consequently,

    first nonzero coordinate of v(t+)-v(t-) is r,
    [v(t+)-v(t-)]_r=1.                              (1)

At t*=1, the first r-1 choices remain those high-bit partial sums. Write
P=B-2^s. There are j=k-r>=3 predecessor slots left in (P,B]. The first
two greedy choices are

    P+2^(s-1), P+3*2^(s-2),

of valuations s-1 and s-2. For the first choice, B itself is infeasible
because j>1, while the midpoint is feasible because 2^(s-1)>=j-1.
For the second choice, B is still infeasible because j>2, and the stated
quarter point is feasible because 2^(s-2)>=j-2. These follow from
2^(s-2)>=2^(d-2)>Q>=n. In particular,

    [v(t*)-v(t-)]_r=(s-2)-(d-2)=s-d.               (2)

Finally the forced ending key has valuation zero at t*, and valuation
nu_2(Q)>=1 at t-. Indeed 0<Q<2^(d-2), so adding 2^(d-2) does not change
its lowest one bit. Padding every vector to n coordinates gives

    last nonzero coordinate of v(t*)-v(t-) is k-1. (3)

Suppose two same-depth blocks had the same normalized punctured node.
Their scalar differences between these three addresses would agree.
Coefficient uniqueness then makes the vector differences agree.
Equation (3) recovers k, (1) recovers r, and (2) recovers s. Therefore
all witnesses indexed by (d,s,r,k) are distinct normalized nodes, even
across different prefix stages. Nodes at different depths are distinct
by the definition of this canonical representation.

## Counting the witnesses

Fix s and write t=n-s. There are N-t+1 eligible depths and
min(t,max(0,k-3)) eligible r values. This gives L_k. At k=n, all r<=t
are eligible, so the triangular sum is binomial(N+2,3).

For a fixed r, eligible stages are k=r+3,...,n, numbering n-r-2.
Thus the union of shared history nodes contains at least

    sum_(t=1)^N (N-t+1) sum_(r=1)^t (n-r-2)
      = (n-2) binomial(N+2,3) - binomial(N+3,4).

Since d0=O(log n), these formulas have leading terms n^3/6 and n^4/8,
respectively. The witnesses establish lower bounds; they do not claim to
exhaust all distinct nodes or give an asymptotically matching upper bound.

## Consequence and independent audit

The full construction theorem O(h(n+sum D_k)) remains valid. A universally
small D_k or shared history cannot make this representation subquadratic.
The obstruction occurs on actual OBST prefixes satisfying endpoint dominance,
with strictly positive original key/gap weights and necessary height h=n.
The unique right chain still has a linear-work construction and certificate;
this theorem imposes no lower bound on unrestricted OBST algorithms.

The independent audit checks greedy rewards against dense subsequence values
before running the compressed solver. Complete constructions verify the three
entries and actual canonical node identities at every witness and every
prefix, including cross-prefix sharing. They also check the closed chain cost,
ordinary Knuth, and original-weight tree structure. Larger rows evaluate only
the proved formulas. Exact finite counts belong in the manuscript appendix.
