# Unit-outcome support and the interactions that survive it

This note isolates the support caused by individual outcomes. It proves a
uniform geometric bound for that support and an explicit obstruction to
charging the remaining support a constant amount per weight unit. The open
bound K(T)=O(s+W(J_T)) in [BOUNDARY_TILE_TARGET.md](BOUNDARY_TILE_TARGET.md)
remains unchanged.

Fix layer h>=1, C=2^h, and c=C-1. An ordinary density cell has 0<=i<j<n,
and density D(i,j)=A(i,j+1)+A(i+1,j)-A(i,j)-A(i+1,j+1). Exclude j-i=c.
The terminal penalty has the established valid size; its affine part cancels
on either side of capacity. Keys in this note are one-based; gaps are indexed
0,...,n.

## Exact density for one unit gap

Put a unit weight at gap x and zero at every other outcome. Above capacity
all ordinary densities vanish. Below capacity put g=c-(j-i)>0. Then D is
one exactly in either of the following cases, and zero otherwise:

1. x=i or x=j+1, and g+1 is a power of two.
2. i<x<=j, g+2=2^r, and x-i-1 is congruent to 2^(r-1) modulo 2^r.

To prove this, consider an interval [i,j) containing gap x, with k=j-i<=c.
Write u=x-i and v=u+c-k=x+c-j. The gap's maximal reward F(u,v) is the
largest a such that the integer interval [u,v] contains an aligned block
[z,z+2^a-1], where z is a multiple of 2^a. Its cost is h-F(u,v).

Indeed, such a block represents the 2^a consecutive external slots of a
perfect subtree collapsed into that gap. Its 2^a-1 internal key slots must
be omitted. The u preceding keys fit before the block exactly when z>=u;
the k-u following keys fit after it exactly when z+2^a-1<=u+c-k=v.
The mixed-slot deletion repair then gives a tree of no greater outcome
depths. Conversely, a gap at depth h-a in an embedded height-h tree
occupies precisely such an aligned block. This includes empty intervals:
[u,v]=[0,c] gives reward h and gap cost zero.

Write F=sum_(a=1)^h I_a, where I_a records the existence of such a block
of length d=2^a. For an interior gap, its cost density is

    F(u,v)+F(u-1,v-1)-F(u,v-1)-F(u-1,v).

For I_a, this is -1 when the outer interval [u-1,v] is exactly one
aligned d-block, +1 when it is exactly two consecutive d-blocks, and
zero otherwise. Here is the full endpoint accounting. Removing the right
endpoint changes I_a only when that endpoint finishes an aligned block
and there is no earlier complete block in the interval. Comparing the
intervals starting at u and u-1 changes that event only when the removed
left endpoint starts either that same block or its immediate predecessor.
These are exactly the one-block and two-block cases.

The outer interval has length g+2. A positive contribution at length 2^r
from level r-1 cancels a negative contribution at level r if the left
endpoint is a multiple of 2^r. Otherwise it survives precisely when
u-1 is congruent to 2^(r-1) modulo 2^r. For x=i or x=j+1 the endpoint
cost is h-floor(log2(g+1)); taking the two contributing costs gives
floor(log2(g+1))-floor(log2 g), which proves the first case. If the gap
is outside all four intervals there is no contribution. Above capacity
every gap has comparison length h, whose interval sums have zero density.

## A universal envelope with at most twice the tile side

Define E_h as follows, always excluding the capacity line:

    below capacity: g=c-(j-i)>0; g+1 or g+2 is a power of two;
    above capacity: g=(j-i)-c>0; g+1 is a power of two.

The support of every possible single positive key or gap is contained in
E_h. For gaps this follows from the preceding formula. For keys it follows
from the consecutive-ruler-pair classification in
[LOCAL_TILE_OBSTRUCTION.md](LOCAL_TILE_OBSTRUCTION.md): their distance
from capacity is 2^r-1. Scaling a single outcome preserves support.
E_h may include cells that no single outcome realizes on a particular grid.

**Theorem.** A dyadically aligned square of side s, lying wholly in the
ordinary region and wholly on one side of capacity, contains at most 2s
cells of E_h. Below capacity the bound is 2s-1. Maximality is unnecessary.
The coefficient two cannot be lowered for the union over all unit outcomes.

For s=1 the conclusion is immediate. Otherwise write the tile as
[a,a+s) x [b,b+s), with a,b multiples of s. The multiplicities of its
successive interval lengths are 1,2,...,s,...,2,1.

Below capacity the minimum distance is
g0=C-(b-a+s). Since b-a>=s and the tile avoids capacity, C>=4s; hence
g0 is a positive multiple of s. Distances range from g0 to g0+2s-2.
A contributing power d with g=d-1 or d-2 exceeds s and is a multiple
of s. The only candidates are d=g0+s and d=g0+2s. They cannot both
be powers of two: the first is at least 2s and their difference is s.
The first contributes diagonals of lengths s and s-1; the second can
contribute only the last corner. Thus the total is at most 2s-1.

Above capacity the minimum distance is g0=b-a-s-C+2 and only g=d-1
contributes. If C>=s, write g0=ms+2; positivity forces m>=0. For m>=1,
the contributing powers are at least 2s, so an interval of width 2s-2
contains at most two, each contributing at most s cells. For m=0, the
powers d<=s contribute d-2 cells each and d=2s contributes two. The
sum is 2s-2log2(s)<=2s. If C<s, write g0=ms-C+2. Now C<=s/2 and
C>=2, so m>=1. Contributing powers are at least s; again at most two
fit in the distance window, proving the bound. Restricting the grid to
non-power-of-two n can only remove cells, so the padded tiling is covered.

For sharpness take s>=2, n=C=4s, and T=[0,s) x [2s,3s). The two envelope
diagonals have j-i=2s and 2s+1, contributing s and s-1 cells. Every
cell on the first is realized by a unit key at one-based i+1; every
cell on the second is realized by a unit gap at x=i+s+1. The tile's
parent meets capacity, so this is an accepted maximal tile. This is
sharpness for the union over different inputs, not simultaneous attainment
of 2s-1 cells by one input.

For an arbitrary integer-aligned square, the weaker 8s bound follows without
dyadic alignment. Write g0 for its minimum positive capacity distance. If
g0>=2s, the eligible powers lie in an interval of multiplicative ratio
less than two, so at most one contributes, on at most two diagonals. If
g0<2s, every eligible power d is below 4s. Each of its at most two
diagonals has at most min(s,d) cells: counted from the nearest corner,
the multiplicity at distance g=d-1 or d-2 is at most g-g0+1<=d.
The powers d<s sum to less than 2s, contributing fewer than 4s cells.
There are at most two powers in [s,4s), contributing at most another
4s cells. Thus the finite arbitrary-square controls below also have an
independent geometric bound.

Across early layers h<L the envelope occupies O(nL) cells per layer and
O(nL^2) altogether, since it uses O(L) diagonals. It is therefore a
lower-order part of the known linear-mass core bound.

## Two keys create logarithmically many cells outside the entire envelope

**Theorem.** Let s=2^t with t>=3, n=8s, C=4s, c=C-1, and h=t+2.
Put unit keys at one-based positions X=3s+3 and Y=4s+2, with all other
weights zero. The accepted maximal tile T=[0,s) x [5s,6s) has local
mass two and at least log2(s)-2 positive densities outside E_h.

For each r=2,...,t-1 an explicit density-one cell is

    i=s+3-2^r,    j=5s+2^(r-1).

All lie in T. The tile is strictly above capacity, while its parent
[0,2s) x [4s,6s) meets capacity. At a witness the distance from capacity
is g=3*2^(r-1)-2, so g+1 is not a power of two. Thus no single outcome
of any position has positive density at this cell.

It remains to compute the joint density. For an above-capacity interval
[a,b) containing both keys, their exposed ranks u<v obey

    1<=u<v<=c,   u<=X-a,   v>=Y+c-b,   v-u<=s-1.

These conditions are sufficient: they give enough zero keys before,
between, and after the positive keys to fill the other selected ranks.
At every witness corner both can be exposed with positive total reward;
omitting one gives at most h-1=t+1 and cannot improve the formula below.

Write X-a=2s+x and Y+c-b=3s-y. At the four witness corners,
3<=x<=s/2 and 1<=y<=s/4. If v<3s, replacing u by 2s is feasible and
does not lower its valuation. Indeed v>2s, v-2s<=s-1, and 2s<=X-a.
If v>=3s, replacing v by 3s is feasible and does not lower its valuation:
the original separation forces u>=2s+1, while u<3s. These two cases give
the exact maximum ruler reward

    S(a,b) = t + max(floor(log2 x), 1+floor(log2 y)).

For v<3s, choose u=2s and maximize valuation on [3s-y,3s-1]; its value
is floor(log2 y). For v>=3s, choose v=3s and maximize on [2s+1,2s+x];
its value is floor(log2 x). The valuations of 2s and 3s are t+1 and t.
Both maxima are feasible. A score omitting both keys is zero, so allowing
omission leaves the formula unchanged.

At the stated cell x=2^r and y=2^(r-1)-1. With
F(x,y)=max(floor(log2 x),1+floor(log2 y)), its cost density is

    F(x,y)+F(x-1,y+1)-F(x,y+1)-F(x-1,y) = 1.

This proves the lower bound without asserting an exact total core count.
Consequently no constant A bounds the off-envelope support by A W(J_T).
Removing the supports of all unit inputs does not restore an additive
constant-per-weight charge. The original O(s+W(J_T)) target survives.

## Verification appendix

The unit-gap formula is checked against 274066 ordinary densities from
independent all-root layers, using 3079878 root candidates and 307625
states. Geometry checks cover 78240 maximal dyadic tiles, 688 literal
envelope counts, 248 single-key support comparisons, and 1222 arbitrary
square controls for the weaker 8s envelope bound. The largest observed
envelope-to-side ratio is 511/256, consistent with the proved 2s-1 family.

A directed two-outcome search examines 819 inputs through 2048 keys,
scanning 22696956 tiles. It uses 3760248528 states, 7001021069 root
candidates, and 3755113776 density evaluations. Six retained small winner
tiles agree with independent all-root layers, using 718432 candidates and
35984 states. The search excludes every envelope cell from its objective;
its outcomes motivated the explicit two-key theorem, but do not prove it.

The final family audit checks s=8,...,1024 (n=64,...,8192), with 36
explicit density witnesses and 144 four-corner score formulas. Independent
rank enumeration uses 23808 single-rank and 2090940 pair-rank candidates.
At n<=128, 12 scores also agree with the generic subsequence recurrence,
using 302446 transitions and 2806 score entries; three densities agree
with original all-root layers, using 2375360 root candidates and 59936
states. Large cases use rank enumeration, not a dense all-root computation.
All records include executed-source SHA-256 manifests:
`unit_support_envelope.json`, `interaction_support_probe.json`, and
`unit_envelope_obstruction.json`.
