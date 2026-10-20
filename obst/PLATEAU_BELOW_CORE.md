# Exact below-capacity cores for one constant key block

Fix a valid terminal-penalty layer h>=1, c=2^h-1, and zero gap weights.
Keys z,...,e-1 have common weight alpha>0, where e=z+m; all other keys
have weight zero. The weight alpha may be real. The ordinary density is
D(i,j)=A(i,j+1)+A(i+1,j)-A(i,j)-A(i+1,j+1).

**Theorem.** Every positive density strictly below capacity equals alpha.
The entire below-capacity core can be enumerated in

    O(n+U_h(m)) work and space,
    U_h(m)=sum_(r=1)^(h-1) max(0,m-2^r+1).

Its size is at most 2(n-m)+U_h(m). Every dyadically aligned side-s square
wholly in the ordinary region and strictly below capacity has at most 8s
positive entries. These bounds do not depend on the magnitude of alpha.
Together with the previous above-capacity plateau theorem, the local
boundary-plus-mass hypothesis holds for this entire key-only family, on
both sides of capacity, using the side term alone. Arbitrary gaps below
capacity and unequal or disconnected positive key blocks remain outside
this theorem.

## Slot reduction and a top-sum identity

For an interval [i,j) of length at most c that contains the complete block,
its positive keys can occupy any m slots of

    [z-i+1, c-j+e]

in the one-based ruler word v(t)=nu_2(t), 1<=t<=c. The zero keys before
and after the block fit precisely when the slots belong to this window.
The established slot-deletion repair proves that the optimum is
alpha times hm minus the sum of the m largest ruler values in the window.
This is an exact optimization: the order of m equal positive weights
imposes no additional restriction on which m slots are selected.

For any finite nonnegative integer word v and any m no larger than its
length, write Top_m(v) for the sum of its m largest values. Then

    Top_m(v)=sum_(r>=1) min(m, #{t: v(t)>=r}).               (1)

For an outer interval [U,V] whose interior has at least m positions,
its negative mixed difference is

    Top_m([U,V-1])+Top_m([U+1,V])
       -Top_m([U,V])-Top_m([U+1,V-1])
    = sum_(r>=1) 1[v(U)>=r, v(V)>=r,
                    #{U<t<V: v(t)>=r}=m-1].               (2)

This follows by applying the four-corner difference to each clipped count
in (1): a nonzero difference occurs exactly when the two endpoints compete
for the last available unit of rank capacity. Neither formula chooses
separate optimizing subsequences; (1) is an identity for the top-sum itself.

## Four disjoint endpoint cases

All formulas below concern 0<=i<j<n and j-i<c.

**Both changed endpoints are outside the block.** A nonzero density requires
i<z and j>=e, so all four intervals contain the complete block. Put

    U=z-i, V=c-j+e.

These are the two endpoints in (2). For ruler values, the threshold set at
level r is precisely the multiples of d=2^r. Formula (2) is one exactly if

    U and V are multiples of d, and V-U=m d,  r>=1.         (3)

Different r cannot satisfy the distance equation for the same cell, so the
density is alpha, not a sum of several copies. Equivalently the capacity
distance satisfies c-(j-i)=m(2^r-1). Explicit generation uses

    max(1,c+e-n+1-md)<=U<=min(z,c-md), U=0 mod d,
    i=z-U, j=c+e-U-md,                                    (4)

and retains ordinary below-capacity cells. The number of generated pairs is
at most sum_(r>=1) floor(z/2^r)<z when z>0. Reflection gives the analogous
bound by n-e. No ruler array of length c is constructed.

**A positive left endpoint and a zero right endpoint.** Here z<=i<e<=j.
Put k=e-i and b=c+e-j. The interval's positive keys have access to the
prefix [1,b], so its cost is alpha times hk-Top_k([1,b]). Four-corner
subtraction gives alpha times the increase of the kth largest prefix value
when b is appended. Using (1), this increase is one exactly when

    b=k 2^r for some 1<=r<=nu_2(b),                        (5)

and zero otherwise. Each r gives a distinct k. With t=j-e+1, b=2^h-t,
so nu_2(b)=nu_2(t) for 1<=t<2^h. Enumerate those r, set k=b/2^r and
i=e-k, and retain 1<=k<=m. The total candidates are at most
sum_(t=1)^(n-e) nu_2(t)<=n-e, with the range shortened if t>=2^h.
Thus this case has linear work even when c is much larger than n.

**A zero left endpoint and a positive right endpoint.** Reflect the preceding
case using the reflected block [n-e,n-z) and the cell map
(i,j)->(n-1-j,n-1-i). The ruler word is reflection-symmetric because
nu_2(2^h-t)=nu_2(t). This gives fewer than z candidates when z>0.

**Both changed endpoints are positive.** Every corner is a uniform-key
interval. Its optimum is the minimum-internal-path-length cost; the
increment for adding the kth key is bitlength(k). Therefore

    D(i,j)=alpha iff j-i=2^r-1 for 1<=r<h,

and it is zero otherwise. The exact number of these cells is U_h(m).
If an endpoint lies beyond the block on the wrong side, all affected positive
weights are absent or independent of that endpoint and the density is zero.
This exhausts the ordinary cells, including block-boundary cuts and empty
shortest intervals.

The first three cases contribute at most
z+(n-e)+min(z,n-e)<=2(n-m). Each divisor event and each uniform-cell output
is generated once. The recurrences nu_2(2t)=nu_2(t)+1 and nu_2(2t+1)=0
generate the needed short ruler prefixes in linear work. Powers with no
possible left endpoint are skipped before iteration. Thus the construction
cost is O(n+U_h(m)), including when c>n, in the arithmetic model. The
arithmetic operands retain the O(h+log(n+1))-bit capacity coordinates.

## Local side charge

In any interval of at most s consecutive positive integers, remove the
position of maximum 2-adic valuation. That maximum is unique: two equal
maxima would have a larger valuation between them. At every level r having
any multiple, removing it leaves at most floor((s-1)/2^r) multiples. Hence

    sum of the remaining valuations <= sum_(r>=1) floor((s-1)/2^r)
                                     <= s-1.               (6)

In the complete-block case, a row with ruler endpoint U has at most nu_2(U)
neighbors, one for each r in (3). Among a side-s square's row endpoints,
all but the maximum-valuation row therefore contribute at most s-1 cells;
the remaining row contributes at most s. The bound is 2s-1. Restricting to
the actual complete-block rows or columns only removes cells. In the
positive-left case the same argument applies to columns b via (5), and
reflection handles the positive-right case. Each has at most 2s-1 entries.

For the uniform case, write the dyadic square as
[a,a+s) x [b,b+s), with b-a=D s and D>=1. For s=1 the bound is immediate.
If D>=2, the possible powers (j-i)+1 lie in
[(D-1)s+2,(D+1)s]; all are at least 2s, and this interval of width 2s-2
contains at most one power of two. Its diagonal has at most s cells.
If D=1, powers d<=s contribute d-1 cells each and d=2s contributes one:
the total is 2s-1-log2(s)<=2s-1. Cropping at the block boundary reduces it.
Adding the four disjoint cases gives fewer than 8s cells. Padding for
non-power-of-two input sizes can only remove original cells and is covered.

## Relation to the size-bound search

The separate excess diagnostic maximizes K(T)-W(J_T) on fixed accepted tiles,
using variable integer mass and key-only, gap-only, and mixed mutations.
It evaluates 34692 inputs through 640 keys, on both sides of capacity, with
22971840 tile-density evaluations and 11439157710 optimized root candidates.
Twenty-seven small winners have independent all-root controls. The largest
observed normalized excess is 39/64: K=63, W=24, s=64. This does not prove
K<=s+W or any asymptotic upper bound. It complements the earlier ratio
searches; the plateau theorem above is proved independently of every search.

## Verification

The independent audit checks 1025 block inputs, including every block through
17 keys, selected cases through 64 keys, rational alpha, and layers through
twice the binary length of n. It compares 8812 entire below-capacity cores
against the original all-root recurrence, checking 1070212 densities and
88033 independent top-sum interval values. There are 222434 local tile
controls and 336 arbitrary-template top-sum identity controls with literal
subset enumeration. The original recurrences use 18032986 root candidates
and 1556996 states. Sixteen larger all-layer sparse constructions reach
65536 keys; their checks use the explicit coordinate identities, with no
large independent all-root reference. Source hashes, scopes, and counts
are retained in plateau_below_audit.json and tile_excess_probe.json.
