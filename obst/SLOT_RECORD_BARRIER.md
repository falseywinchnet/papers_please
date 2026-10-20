# Exact exponential prefix-record support at necessary height

The magnitude restrictions in the prefix-record theorem cannot be removed
by proving a polynomial upper bound for all of its explicit record lists.
There is a strictly positive mixed-weight family whose unique optimum needs
height n, and whose final prefix has exactly 2^n-n records. Every intermediate
record count has a closed binomial formula. The same inputs are handled in
linear arithmetic work by the existing affine-period constructor, so this
is a limitation of the explicit representation.

## A universal binary envelope for arbitrary mixed weights

At any prescribed height h, a k-key prefix record can occur only at

    b>=k with pc(b)<=k,

so B_k <= E_h(k) := sum_(r=0)^min(k,h) binomial(h,r)-k.
This bound needs neither integrality nor a restriction on gaps.

Given an attaining slot tuple, move each slot successively to the earliest
position after its moved predecessor with the same valuation. Each new
position is no greater than the original one. All key and adjacent-gap
rewards are unchanged because the complete valuation vector is unchanged.

Such a step raises popcount by at most one. Write the predecessor as
Q*2^(d+1)+r, 0<=r<2^(d+1), for the next required valuation d. If r<2^d,
the next position is Q*2^(d+1)+2^d. Otherwise it is (Q+1)*2^(d+1)+2^d;
adding one to Q raises its popcount by at most one, and the old remainder
already contained a one bit. In either case the new popcount is at most
the old popcount plus one. After k steps it is at most k.

An optimal ending position b with more than k one bits would therefore
compact to an earlier position of the same valuation and equal reward.
Monotonicity forces equal prefix values, excluding a record at b. Counting
the allowed positive h-bit positions and removing 1,...,k-1 gives E_h(k).
The geometric family below attains this bound; it is an exact envelope,
not a heuristic candidate set.

## A strictly positive mixed family with a unique chain

For n>=2 put A=n+1 and set

    p_i = A^(n-i)-1,  0<=i<n;
    q_j = 1,         0<=j<=n.

All key and gap weights are strictly positive integers. Common-gap
normalization gives w_i=A^(n-i), all residual gaps zero, and adds n to every
normalized tree cost. For every suffix starting at i,

    n sum_(j>i) w_j = w_i-A < w_i.

A right chain on that suffix costs less than 2w_i. Any tree whose first
key is not its root costs at least 2w_i from that key alone. Thus the first
key must be the root, and induction forces the unique right chain. Its
height is n, so no smaller height budget can preserve the optimum.

The original optimum is

    n + sum_(i=0)^(n-1) (i+1) A^(n-i)
      = n + A[A^(n+1)-(n+1)A+n]/(A-1)^2.

The largest input integer has O(n log(n+1)) bits; the family has a finite
polynomial-size binary encoding. This is not an artifact of treating a
single input weight as an infinitely precise object.

## Lexicographic ruler optimization

Use the necessary height h=n and capacity c=2^h-1. Each slot valuation is
between zero and h-1. For any two valuation vectors, the first differing
coordinate determines the weighted reward: its change has magnitude at
least w_i, while all later coordinates can change the reward by at most

    (h-1) sum_(j>i) w_j < w_i.

Thus maximizing the weighted reward is exactly lexicographically maximizing
the valuation vector in key order. With r slots left to choose in an interval
ending at U, choose the slot of highest valuation in

    [previous+1, U-r+1].

This maximum occurs at a unique position: two positions with the same
maximal valuation would enclose a position of larger valuation. Greedy choice
is therefore exact and gives a unique maximizing slot sequence.

Write pc(x) for the number of one bits of x. Let G_m(U) be the maximum
reward of the first m keys placed anywhere in [1,U], with m>=1 and U>=m.
The greedy sequence ends at U if and only if

    pc(U) <= m.                                                (1)

To prove this, write U=P+s, where P is its largest power of two and 0<=s<P.
If m<=s+1, the first greedy slot is P. For x in [1,s], nu_2(P+x)=nu_2(x),
so the rest is the same greedy problem with m-1 slots on [1,s]. Induction,
including the empty suffix case, gives (1) because pc(U)=1+pc(s).
If m>s+1, every choice made while more than s+1 slots remain lies below P:
its feasibility upper endpoint is below P. When exactly s+1 slots remain,
P becomes feasible and is selected; every following slot through U must
then be used. Here pc(U)=1+pc(s)<=s+1<m, so (1) holds in this case too.

Uniqueness now gives the exact strict-increase locations of G_m: the value
rises at U precisely when pc(U)<=m. If the optimum ends before U, it was
already feasible at U-1. If it ends at U, no equally good sequence was
feasible earlier. Treat the first feasible U=m as an initial record.
For m=0, G_0 is constantly zero.

## Exact record set of every prefix

For a k-key prefix whose last slot is b, with m=k-1,

    f_k(b) = -G_m(b-1) - w_m nu_2(b).

Fix valuation d and write b=(2j+1)2^d. Consecutive positions in this
valuation class differ by 2^(d+1). When both are feasible, the G_m argument
advances over the integer interval

    [b-2^(d+1), b-1].

The minimum popcount in this interval is pc(j). Its right half contains
j*2^(d+1), of popcount pc(j). Its left half has minimum pc(j-1)+1, and
pc(j)<=pc(j-1)+1. By (1), the prefix cost strictly decreases within its
valuation class exactly when pc(j)<=m. Since pc(b)=pc(j)+1, this is

    b is a record  <=>  b>=k and pc(b)<=k.                      (2)

The first feasible position in each class also obeys (2). Indeed, its
j-index is max(0,ceil((k-2^d)/2^(d+1)))<=k-1, so pc(b)<=k. For k=1,
only j=0 is retained in each class, as required by the constant G_0 case.

Consequently the exact number of records after k keys is

    B_k = sum_(r=0)^k binomial(n,r) - k,       1<=k<=n.         (3)

There are sum_(r=0)^k binomial(n,r)-1 positive n-bit integers with at most
k one bits; all k-1 positive integers below k are among them and are removed.
In particular,

    B_n = 2^n-n,
    sum_(k=1)^n B_k = (n+2)2^(n-1)-1-n(n+1)/2.                (4)

For arbitrary prescribed height h, choosing base A=h+1 gives the same
lexicographic dominance. The support calculation applies for any prefix
k<=2^h-1 and attains E_h(k), including k>h. Thus the universal binary
envelope is sharp.

The final record list is already exponential. Retaining every stage's
predecessors as in the current constructor uses Theta(n 2^n) records on
this family. Even the middle stage has a constant fraction of all 2^n
possible slots, by the central binomial sum in (3).

A direct subfamily of strict records is useful for independent checking:
choose any k-1 distinct bit positions d_1>...>d_(k-1)>=1 and set
b=1+sum_i 2^d_i. The attaining first k-1 slots are the partial sums of
these powers, with valuations d_1,...,d_(k-1). Their score is
sum_i w_(i-1)d_i. Every earlier odd ending slot has strictly smaller score
when feasible. This yields binomial(n-1,k-1) separately enumerated witnesses,
although (3) is the stronger exact count.

## Scope and the next representation question

The unrestricted-height theorem is exact here: any sufficient height capped
at n is n. The record explosion cannot be removed by improving that height
certificate. It also occurs with strictly positive weights on both outcome
types. It invalidates any weight-independent polynomial bound for the
explicit prefix records, and any general algorithm that must enumerate them.

The support itself is succinct: membership is the binary popcount test (2),
and its size is the binomial expression (3). A large explicit list therefore
does not imply a large implicit description or a hard full-OBST instance.
In fact these original mixed weights satisfy the already proved affine
translation with period one,

    lambda = 1/A,  alpha = 1/A-1.

The existing affine constructor returns the complete optimum with exactly
2n-1 root candidates. No new full solver is claimed for this family. The
integer-mass and fixed-exception record theorems remain valid. General
arbitrary-weight construction needs additional structure beyond a universal
small-record claim, while the original interval-core support question remains
independent.

## Verification

The harness uses a dense, zero-residual-gap subsequence recurrence, with every
ending slot retained, independently of the record kernel. It checks all
prefix values, attaining compressed predecessors, exact record sets, binary
support membership, and prefix-maximum jump locations. Small instances also
use literal slot subsets and literal BST shapes. Larger binomial values are
explicitly labeled formula-only; no exponential enumeration is claimed there.
The existing affine solver supplies complete large trees, compared with the
closed unique-chain optimum, with ordinary Knuth references at smaller sizes.
All arithmetic is exact, source hashes are retained, and no timings are used.

The universal envelope is separately checked on every nonempty slot subset
through height four (32,902 subsets and 246,221 selected positions), 72 mixed
rational inputs (12,424 retained records and 18,088 dense prefix values),
and every feasible key count through height six (2,667 exact stage sets).
These finite controls audit the proof; the earliest-embedding argument
establishes the universal bound.
