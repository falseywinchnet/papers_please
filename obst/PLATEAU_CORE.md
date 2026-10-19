# A linear above-capacity core for one constant key block

**Theorem.** Fix a terminal-penalty layer h>=1 with capacity c=2^h-1
and a valid penalty. Suppose exactly the consecutive keys z,...,z+m-1
have common positive weight alpha, and every other key has weight zero.
Gap weights may be arbitrary nonnegative reals. The ordinary core strictly
above capacity has at most max(0,c-m-1) entries. Their coordinates and
values can be constructed in O(n) arithmetic work and space. The leading
coefficient one in the support bound is asymptotically sharp.

This constructs the above-capacity part of a layer. The below-capacity
mixed problem and the general boundary-plus-mass hypothesis remain open.

## Removing partial-block endpoints

Above capacity, the layer cost on [i,j) is an affine terminal-penalty term
plus h times interval weight minus the optimal c-subsequence ruler reward.
The first two terms have zero ordinary density, including all gap weights.
Thus we may divide by alpha and consider a binary key input.

For arbitrary nonnegative rank rewards, an optimal binary c-subsequence
can retain min(P,c) of its P positive input keys. If P>=c, selecting c ones
attains the sum of all rewards. Otherwise, replace a selected zero nearest
to an omitted one by that one. All selected intervening entries are ones,
so the resulting binary selected word changes only one zero to one.
Repeated exchanges retain every positive key without reducing reward.

Consider an ordinary density cell (i,j), j-i>c. Its four intervals have
length at least c. If the removed left key i is positive and the added
right key j lies inside the block, all four intervals are positive and
their scores saturate. If j is outside the block, the selected positive
keys form a prefix of length min(P,c), where P depends only on i. Their
score is F(min(P,c)), with F(t)=sum_(r=1)^t nu_2(r), independently of j.
In both cases the density is zero. The reflected argument applies when
the added right key is positive: nu_2(2^h-r)=nu_2(r), so a positive suffix
has the same reward as the corresponding prefix.

Every remaining positive density therefore has all four intervals
containing the whole block. If m>c, every such score saturates and the
entire above-capacity core is empty.

## A one-dimensional sequence of binary carries

Assume m<=c. For an interval containing the block, all m positive keys can
be retained, and they occupy consecutive selected ranks r+1,...,r+m.
The available zeros before and after the block give exactly

    max(0,c+z-j) <= r <= min(c-m,z-i).

Consequently its normalized score is the range maximum of

    R_m(r) = sum_(t=r+1)^(r+m) nu_2(t)
           = m+s_2(r)-s_2(r+m),       0<=r<=c-m,          (1)

where s_2 is the number of one bits. To prove (1), count each multiple
of 2^a once for each a>=1 to get F(t)=sum_a floor(t/2^a)=t-s_2(t).
Equivalently, R_m(r)=m-s_2(m)+kappa(r,m), where kappa counts the carries
in binary addition of r and m, one per column with an outgoing carry.

Put l=c+z-j and u=z-i. Where clipping freezes either endpoint, the
four-corner difference is zero. Otherwise set a=l-1 and b=u. The
nonempty interior has b-a=j-i-c+1>=2. If Q=max_(a<r<b) R_m(r), the
normalized density is exactly

    max(Q,R_m(b))+max(R_m(a),Q)
      -max(R_m(a),Q,R_m(b))-Q
      = max(0,min(R_m(a),R_m(b))-Q).                     (2)

Thus positive densities correspond to strict visibility pairs of this
single sequence. Each pair maps to exactly one cell:

    i=z-b,       j=c+z-1-a.                             (3)

Keep the pair if 0<=i<j<n. Its density is alpha times the positive gap
in (2). This is an exact representation, not a sum of separate optimizers
for the binary digits.

## Noncrossing support and a linear constructor

For any sequence of N values, a nonadjacent visibility pair (a,b) has
both endpoints strictly larger than every interior value. Two pairs
(a,c) and (b,d) with a<b<c<d cannot coexist: the first requires R(c)>R(b),
and the second requires R(b)>R(c). Place the vertices on a polygon in
index order. The noncrossing proper diagonals number at most N-3, and
the closing edge (0,N-1) contributes at most one. For N<=2 there are no
nonadjacent pairs. With N=c-m+1, this proves max(0,c-m-1).

This is the established horizontal visibility graph geometry; see
[Luque et al. (2009)](https://arxiv.org/abs/1002.4526) and the
[outerplanar characterization of Gutin, Mansour, and Severini (2011)](https://arxiv.org/abs/1010.1850).
The argument above supplies the precise nonadjacent count needed here.
The OBST step is the exact block-reward/range-maximum reduction (1)--(3).

Compute nu_2(1),...,nu_2(c) from nu_2(2r)=nu_2(r)+1 and zero on odd
arguments; sliding length-m sums compute R in O(c) arithmetic operations.
To enumerate visibility pairs, scan R with a stack of indices whose
heights strictly decrease. On reading x, pop each smaller height and
emit its pair with the new index; also emit the pair with the remaining
top, if any. Replace an equal-height top by the new index, since that
equal intervening height blocks any later strict visibility of the old
index. Discard adjacent pairs. The first popped index is the preceding
position; for each later pair the last popped height is exactly the
interior maximum. It therefore supplies the density value as well as
the edge. Every index is pushed once and popped at most once, and there
are at most twice N candidate pairs. Cropping by (3) is linear.

When c>=n the region is empty. Otherwise O(c) work and space are O(n).
The implementation uses the arithmetic recurrence, not a unit-cost
population-count assumption.

## A local boundary charge

**Corollary.** Every s-by-s square strictly above capacity contains at
most 2s-1 positive densities, independently of m and alpha.

Under (3), its possible left and right visibility endpoints lie in
ordered disjoint intervals of at most s indices each. For a<a', every
neighbor b of a is at least every neighbor b' of a': otherwise a<a'<b<b'
would be a crossing. Thus the nonempty neighbor sets have decreasing
spans with disjoint interiors, sharing at most one endpoint between
successive sets. For k participating left endpoints and t right endpoints,
the number of pairs is at most t+k-1<=2s-1. Empty support is immediate.
This proves the proposed boundary-plus-mass local charge for this
above-capacity family using the boundary term alone.

## Sharp leading coefficient

Take h>=3, m=1, C=2^h, n=2C, and z=C+1. All nonadjacent visibility pairs
of nu_2(1),...,nu_2(C-1) map inside the input. They are the consecutive
multiples of 2^r, for 1<=r<h: every interior valuation is smaller than r,
whereas any nonconsecutive pair has an intervening value at least the
smaller endpoint. Their count is

    sum_(r=1)^(h-1) (2^(h-r)-2) = C-2h.

The upper bound is C-3, and their ratio tends to one.

## Verification appendix

The independent original all-root recurrence checks 5561 complete
above-capacity support sets on constant blocks through 64 keys, including
nonzero gap weights. It checks 1143360 densities and 635883 positive-endpoint
zero identities, using 33319148 root candidates and 2723869 states.
Independent literal visibility enumeration checks 193533 pairs; 23375
block rewards agree with both direct ruler sums and (1). Each constructed
support set, including values, equals the original recurrence's result. The local corollary has
50032 square-support controls, exhaustive through twelve keys and sampled
at the larger sizes.

Twelve sharp-family constructions reach 32768 keys; these larger rows
use the linear constructor, not the original all-root recurrence. At that
size it computes 16383 ruler values, performs 16382 sliding updates,
pushes 16383 and pops 16369 stack indices, checks 32738 candidate pairs,
and outputs 16356 densities. Proofs, rather than these finite checks,
give the asymptotic bounds. Sources and executed-source hashes are in
`code/plateau_core.py`, `code/plateau_core_audit.py`, and
`results/plateau_core_audit.json`.
