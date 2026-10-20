# Exact binary-block dilation above capacity

Replicating sparse keys into aligned binary blocks does not amplify interior
core support. The precise reason is an exact reduction to the original ruler
problem. The identity applies to arbitrary binary key patterns on intervals
that retain complete positive blocks, with at most coarse-capacity many such
blocks. Arbitrary nonnegative gap weights do not affect the above-capacity
densities. This is a representation identity and an amplification barrier;
the general mixed-weight size bound remains open.

## Saturating the positive keys

Let a binary word have P ones, and let v_1,...,v_c be any nonnegative rank
rewards. Some maximizing c-subsequence contains min(P,c) ones.

If P>=c, selecting c ones attains sum v_r, the largest possible score.
If P<c and a selected subsequence omits a one, it selects a zero. Choose
a selected zero nearest to the omitted one in physical order, so all
selected entries between them are ones. Insert the omitted one and remove
that zero. Shifting the intervening ones changes the selected binary word
only by replacing one zero with one. The score cannot decrease. Repeating
retains all P positive keys. The same argument includes zero rank rewards
and ties; it makes no uniqueness assumption.

## The dilation identity

Fix h>=1, C=2^h, and c=C-1. For a binary input p_1,...,p_n, let S_h(a,b)
be the maximum ruler reward sum p_k nu_2(r) over c selected keys in
[a,b), whenever b-a>=c. Here interval coordinates are zero-based and
key positions are one-based, so [a,b) contains keys a+1,...,b.

Take d=2^ell, replace every input key by d consecutive copies, and use
fine height h+ell, capacity c_d=dC-1. Let S_d be its ruler score. Consider
a fine interval [a,b) with b-a>=c_d that cuts no positive block: each
replicated positive block is either wholly contained or wholly excluded.
Put

    A=ceil(a/d), B=floor(b/d), m=sum_(k=A+1)^B p_k.

Assume m<=c. Then B-A>=c, and the exact identity is

    S_d(a,b) = m(d-1) + S_h(A,B).                         (1)

The rounding of both endpoints is part of the statement. In particular,
the fine interval need not have aligned endpoints when it cuts only zeros.

**Block reward.** A block of d consecutive selected ones starting after
rank r has reward

    sum_(t=r+1)^(r+d) nu_2(t)
       = d-1 + nu_2(floor(r/d)+1).                        (2)

Every residue modulo d occurs once. The sum of valuations capped at ell
is sum_(j=1)^ell d/2^j=d-1. Only the unique multiple of d has an uncapped
remainder, equal to the last term in (2). For legal block starts
0<=r<=c_d-d, the coarse rank floor(r/d)+1 lies in [1,c].

**Feasible coarse ranks.** If m=0 both scores vanish; assume m>=1.
Let X_1<...<X_m be the positive coarse key
positions inside the interval. Saturation permits all md positive fine
keys to be selected, because md<=dc<c_d+1. Each positive block therefore
occupies d consecutive selected ranks. Write its start as

    r_j=d(u_j-1)+rho_j,    0<=rho_j<d.

Feasibility of the fine starts is exactly

    r_1 <= R=d(X_1-1)-a,
    r_m >= Q=d(X_m+C-1)-b-1,
    d <= r_(j+1)-r_j <= d(X_(j+1)-X_j),
    0<=r_j<=c_d-d.                                       (3)

The first and last bounds count available zero keys before and after the
positive blocks; the intervening bounds count zeros between blocks.
Taking floors shows that the coarse ranks satisfy

    1<=u_1<...<u_m<=c,
    u_1<=X_1-A, u_m>=X_m+c-B,
    u_(j+1)-u_j<=X_(j+1)-X_j.                            (4)

These are precisely the constraints for retaining all m positive coarse
keys in a c-subsequence of [A,B). It remains to show that every such
coarse choice admits phases rho_j satisfying (3).

If the first coarse bound is tight, it imposes rho_1<=R mod d; otherwise
there is no phase restriction there. If the last is tight, it imposes
rho_m>=Q mod d; otherwise there is no restriction there. Use upper d-1
and lower 0 at unrestricted endpoints. If the allowed endpoint ranges
intersect, one common phase satisfies all constraints.

Otherwise the final phase must exceed the initial phase. Write
D_j=X_(j+1)-X_j and e_j=u_(j+1)-u_j. If some e_j<D_j, the phases can
increase once across that edge and stay constant elsewhere. Its upper
gap bound has at least d units of slack, while the phase increase is
at most d-1; its lower gap bound is also satisfied, including e_j=1.
All other edges keep a common phase. If every e_j=D_j, then both tight
endpoint bounds imply

    (Q mod d)-(R mod d)
      =Q-R-d(u_m-u_1)
      =c_d-(b-a) <= 0,

contradicting the need to increase. Hence every coarse choice lifts.
For m=1 the same equation settles the two endpoint bounds directly.

Applying (2) to all m blocks proves (1). Conversely, coarse saturation
ensures that optimizing (4) is exactly S_h(A,B), even when a coarse
subsequence that omits positives is also optimal.

## Exact transport of density support

Consider a square T=[a0,a0+s) x [b0,b0+s) whose four-corner intervals
all contain the same m positive coarse keys, with m<=c. Thus both endpoint
fringes have zero key weights. Assume b0-a0-s>=C, so both T and its
dilated square dT are strictly above their capacity lines. Gap weights
may be arbitrary and need not be replicated.

On every relevant fine interval, (1) holds with the same m. Above capacity
the cost is an affine terminal-penalty term plus height times interval
weight minus the ruler score. Those first two terms have zero ordinary
density. The rounded left coordinate changes from i to i+1 only when
i is divisible by d; the right coordinate changes from j to j+1 only
when j is congruent to d-1 modulo d. Consequently

    D_fine(di, d(j+1)-1) = D_coarse(i,j),                 (5)

and every other cell of dT has zero density. Thus dilation preserves
both the number of positive densities and their total mass exactly.
For zero gap weights, local input mass and tile side both increase by d,
so the ratio K(T)/(s+W(J_T)) decreases by exactly a factor d.

For d>=2, every transported positive cell is outside the universal
unit-outcome envelope. Its fine capacity distance is d(j-i-c)>0;
adding one gives an odd integer greater than one, never a power of two.
Thus the support can become entirely an interaction contribution without
increasing its cardinality.

For the prior two-key family, start with s=2^t, n=8s, C=4s, unit keys
at 3s+3 and 4s+2, and T=[0,s) x [5s,6s). Every dyadic replication has
exactly the same tile support and density mass as the base instance.
The fine tile is still accepted and maximal: it is strictly above
capacity, and its parent meets capacity. In particular the known t-2
explicit witness cells transport by (5), but copying each key d times
creates no additional positive cell in this tile.

## Why the restrictions are needed

Cutting a positive block can invalidate (1). Start from coarse input
(1,0,0), h=1, d=4. The fine interval [1,9) has binary word
(1,1,1,0,0,0,0,0), fine capacity seven, and maximum ruler score one.
Its rounded coarse interval [1,2) has no positive key, so the expression
on the right of (1) would be zero.

The condition m<=c is also necessary. For coarse input (1,1), h=1,
d=2, and fine interval [0,4), the fine capacity is three and its score
is one. The right side of (1) would be 2(2-1)+0=2. Neither example
affects the stated identity; they delimit the required hypotheses.

## Verification appendix

The independent audit checks saturation on 1536 cases using 21588 literal
subsequences, with arbitrary nonnegative rank rewards. Two scope
counterexamples use twelve further literal subsequences. Forty dilation
instances give 6142 score controls and 4392 density controls from separate
generic subsequence recurrences, using 416654 transitions and 8958 score
entries. Original all-root layers with arbitrary nonzero gap weights check
2286 entries and 1434 densities, using 398656 root candidates and 38304
states. All 42 positive controlled fine densities lie outside the unit
envelope. These checks include rounded endpoints inside zero blocks.

The separate fixed-tile amplification search evaluates 2470 inputs through
1024 keys. It uses 1858339360 states, 3315818765 root candidates, and
6790720 density evaluations. Six retained tiles have independent all-root
controls using 7126080 candidates and 179808 states. Its largest observed
ratio K/(s+W) is 12/25; no upper bound follows from this finite maximum.
The search explores translated pairs, shared endpoints, unequal weights,
and local integer-weight mutations, so it also includes inputs beyond the
binary dilation theorem.

The larger original-layer audit checks 27 replicated pair, alternating,
and three-block patterns through 1024 keys. Each preserves the base tile's
core and density mass; every positive fine density for d>1 is off-envelope.
The run uses 22874208 states, 40616815 root candidates, and 84672 densities,
recorded in `binary_dilation_family.json`. Reproduction sources and hashes
are also in `binary_dilation_audit.json` and `pair_amplification_probe.json`.
