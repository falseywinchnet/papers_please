# Charging outcome weights across all terminal-penalty layers

For full mixed nonnegative integer weights with total mass W=O(n), the exact
Monge construction takes **O(n^(3/2) log^(3/2)(n+1)) arithmetic operations**,
including conversion and full tree reconstruction. This saves one logarithmic
factor over multiplying the maximum intermediate core size by the height.
The proof does not change the algorithm or infer a bound from measurements.

Let L=ceil(log2(n+1)), H=min(n,f(W)+L), and K_h=delta(E_h), using the notation
of [the terminal-penalty construction](MONGE_PENALTY.md). Then

    S = sum_{h=0}^H K_h
      = O(n H + n sqrt(W L) + W L^3 + H W L).

The construction takes O(S log(n+1)) operations. Retaining the published
succinct witness structures takes O(S) words; arbitrary range-query backends
can have different auxiliary storage. The earlier H times maximum-core bound
remains available, so use the smaller of the two bounds.

## Per-position overlap lemma

For analysis only, pad to N=2^ceil(log2 n), retaining q_n at its original
position and appending zero weights. Thus n<=N<2n. Original interval entries
are unchanged. Keep the original M and H: the proof needs only M>hW for each
layer under consideration, not an optimal-height bound for the padded input.

At early layer h<L put c=2^h-1. Partition the padded upper-triangular density
grid into maximal dyadic squares avoiding j-i=0 and j-i=c. The exceptional
original line has at most n cells. There are no cuts at the original boundary
n; entire padded tiles may be used to bound their original portions.

An accepted side-s tile with anchor (a,b) has a rejected side-2s parent (A,B)
meeting a diagonal j-i=d, d in {0,c}. Consequently

    |B-A-d| < 2s,      |b-a-d| < 3s.

For each row anchor and each d there are at most six column anchors. There
are N/s row anchors, hence at most 12N/s <=24n/s tiles per scale.
The tile's inclusive outcome span is J=[a,b+s]. If a fixed position x belongs
to J, then a<=x<a+d+4s. The possible row anchors are at most d/s+5, and there
are at most six column choices for each. Summing over the two diagonals gives
at most 60+6c/s <=60(1+c/s) covering spans. Inclusive endpoints handle gap
weights; key incidences are a subset of these same incidences.

## Local mass instead of total mass on each tile

Write A_h(i,j)=M(j-i-c)_+ + R_h(i,j), where
0<=R_h(i,j)<=h W(i,j). On an accepted tile the penalty has zero density.
Its density sum telescopes to two positive and two negative residual corners.
Both positive-corner intervals are contained in J, so its nonnegative integer
density sum is at most 2h W(J). Its support is also at most s^2.

Charge each individual key and gap weight to the spans containing it:

    sum_{side-s tiles T} W(J_T) <=60 W(1+c/s).

Thus the support K_{h,s} in original cells covered by side-s tiles satisfies

    K_{h,s} <= min(24ns, 120hW(1+c/s)).

There are at most L scales. Since min(x,y+z)<=min(x,y)+min(x,z),

    K_h = O(n + hW L + sqrt(n hW c)).

The first term includes the exceptional and completion diagonals. For the
last term use the geometric bound
sum_{dyadic s} min(ns,hWc/s)<=4 sqrt(n hWc). If hWc<n, the bound follows
from sum_s hWc/s<=2hWc; otherwise split at sqrt(hWc/n). Zero mass is immediate.

## Summing the growing boundaries

Because c_h<2^h and 2^L<=4n,

    sum_{h=1}^{L-1} sqrt(h c_h) = O(sqrt(L n)).

The early layers sum to O(nL+W L^3+n sqrt(WL)). At h>=L, the balanced-tree
cost bound gives K_h<=n+LW. The initial core has n entries, and H>=L. Adding
them proves the displayed bound on S.

Every product, conversion, and witness construction costs
O((n+K_{h-1}) log(n+1)). Every completed core has its n completion entries,
so the full sum including n reconstruction queries is O(S log(n+1)).
The published witness storage sums to O(S).

When W=O(n), H=O(L), hence

    S = O(n^(3/2) sqrt(L) + n L^3) = O(n^(3/2) sqrt(L)),

using L^(5/2)=O(sqrt n). Multiplication by the product/query logarithm gives
O(n^(3/2) log^(3/2)(n+1)). The expression with both summands is also valid
and avoids suppressing the logarithmic summand at finite n.

The [odd-ramp lower bound](RAMP_CORE_TIGHTNESS.md) still forces
Omega(n^(3/2)) entries in one layer. This proof reduces the cost of summing
layers; it does not close the remaining sqrt(log n) per-layer size gap.

## Independent audit

`code/aggregate_core_audit.py` implements its own all-root recurrence and
padded quadtree. It checks 766 partitions, 4508 geometry scales, 998378 tiles,
and 1891752 position/scale incidences. Weighted checks cover 290 inputs,
including exhaustive mixed binary weights through three keys, zero mass,
uniform/random/geometric inputs, and either endpoint gap carrying all mass.

The record has 1977 original/padded layer comparisons, 452644 residual-bound
checks, 28013 weighted tiles, 1367 weighted scales, 548 early-layer checks,
and 1139 late-layer checks. The diagnostic uses 685551 dense states and
8636426 candidate roots. These are verification operations, not the sparse
constructor's complexity. The source-hashed result is
`results/aggregate_core_audit.json`.
