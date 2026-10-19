# A boundary term in the local core-size bound

The remaining linear-mass core gap is a factor sqrt(log n). The proved bound
sums integer density mass 2h W(J) on each maximal dyadic tile. A different
local statement would remove that factor:

**Open local hypothesis.** There is an absolute constant A such that, for
all nonnegative integer key and gap weights and every accepted early-layer
tile T of side s with inclusive outcome span J,

    K(T) <= A (s+W(J)).                                      (1)

Here K counts positive ordinary densities, not their sum. The layer uses a
valid terminal penalty, the tile avoids the main and capacity diagonals,
and padding and inclusive gap endpoints are as in AGGREGATE_CORES.md.
This hypothesis is unproved. It is compatible with the existing one-key
obstruction, which has logarithmic support inside a large tile.

## A proved logarithmic-side bound for one key

**Lemma.** If exactly one key has positive weight and all gaps have weight
zero, any s-by-s square of ordinary density cells wholly on one side of
the capacity line has at most

    1+floor(log2 s) <= s                                    (2)

nonzero entries. The square need not be maximal or dyadically aligned.
The logarithmic dependence is asymptotically sharp.

**Proof.** Use the one-key ruler-pair classification. Every positive density
corresponds to a pair (u,v) of consecutive multiples of 2^r, for some
1<=r<h. Its density is the key weight. Below capacity, the mapping is

    i=x-u,       j=c+x+1-v,      0<=u<v<=c+1;

above capacity it is

    i=x+1-v,     j=c+x-u,        1<=u<v<=c.

For a square wholly off capacity, the possible u and v values lie in two
ordered disjoint integer intervals I and J, each with at most s values.
Their gap g=min(J)-max(I) is at least two. Clipping only shortens them.
Every contributing pair spans a common point between I and J. At a fixed
scale, consecutive-multiple intervals have disjoint interiors; hence at
most one pair at that scale can contribute.

Every pair length lies between g and g+2s-2. Their ratio is at most s,
because g>=2. There are at most 1+floor(log2 s) powers of two in that range.
This proves (2), including s=1. The known family with s=2^(h-2) has exactly
h-3=log2 s-1 nonzero entries in one maximal tile, establishing the leading
logarithmic scale. Multiplying the key weight does not change support.

## What the open local hypothesis would prove

**Conditional theorem.** If (1) holds, the sum S of all completed layer
cores obeys

    S = O_A(nH + (n+W)L^2 + n sqrt(W) + HWL),
    L=ceil(log2(n+1)).                                     (3)

At W=O(n), the existing height bound gives H=O(L), so S=O(n^(3/2)).
The existing Monge product and witness construction would then take
O(n^(3/2) log(n+1)) arithmetic operations, with full reconstruction.
This is a conditional consequence, not a revised main complexity theorem.

**Proof.** At layer h<L with c=2^h-1, there are at most 24n/s accepted
tiles of side s. The established inclusive-position overlap lemma gives

    sum_T W(J_T) <= 60 W (1+c/s).

Thus (1) and the area bound imply

    K_(h,s) <= min(24ns, A[24n+60W(1+c/s)]).

Separate the constant-per-scale part from Wc/s. Summing over dyadic s,
using the geometric minimum bound, gives

    K_h = O_A((n+W)L + sqrt(nWc)).

The exceptional and completion diagonals add O(n). Since
sum_(h<L) sqrt(c_h)=O(sqrt n), the early layers contribute
O_A((n+W)L^2+n sqrt W). Late layers retain their proved bound n+LW,
which gives (3). Product, conversion, and succinct reconstruction costs
are O(S log(n+1)). The odd-ramp lower family already has Omega(n^(3/2))
entries in one layer at W=n, so the conditional core scale would match it.

## Verification appendix and search limitations

A broad diagnostic evaluates 21436 inputs, including structured inputs through
1024 keys, non-power-of-two sizes, sparse unit outcomes, and fixed-mass
mutations over keys, gaps, and mixed outcomes. It scans 87706185 accepted
tiles. The maximum observed ratio K(T)/(s+W(J)) is 121/136, on a gap-only
input. All 93 small independent all-root controls agree with the layerwise
maxima, covering 15301 independently enumerated tiles.

The maximum-over-all-tiles objective often settles on a small tile. A second
search therefore restricts the objective to capacity-adjacent tiles with
s>=4 and c>=4s, while preserving fixed total mass n/4 or n. It evaluates
37224 inputs through 512 keys, with 212592240 tile visits. Its maximum
eligible ratio is 11/14. Six retained small winner tiles are checked against
independent all-root layers. These are finite falsification searches, not
proofs of (1).

The one-key lemma has 1038774 maximal-square checks over all key positions
at selected power-of-two and non-power-of-two sizes through 128 keys. It
also has 1300 arbitrary-square checks, including non-dyadic sides, and
155 independent all-root support-set comparisons. The proof of (2) uses
only the ruler-pair classification and interval geometry.

Records and executed-source hashes are in `tile_boundary_probe.json`,
`tile_capacity_support.json`, and `one_key_square.json`.
