# One weight unit defeats constant local tile charging

The factor h in the local bound `density_mass(T) <= 2h W(J_T)` cannot be
replaced by a universal constant. The same is true if density mass is replaced
by the number of nonzero densities. This obstruction occurs with total mass
W=1, although the entire layer core remains linear in n.

## Explicit family and theorem

Let h>=4, s=2^(h-2), n=8s=2^(h+1), c=2^h-1=4s-1, and x=4s+1.
Give key x weight one and every other key and gap weight zero. Use any terminal
penalty M>h at layer h (in particular the manuscript's prescribed penalty).

The maximal dyadic tile

    T = [2s,3s) x [7s,8s)

has exactly h-3 nonzero densities, each equal to one, while its inclusive
span has mass one. The complete finite Monge matrix has exactly

    delta(E_h) = 2n + 2^h - 2h - 1

core entries. Multiplying the single positive weight and a valid penalty
accordingly scales the ordinary densities, without changing their support.

## Exact one-key interval formula

Put C=2^h=c+1. For any interval [i,j) containing x, write k=j-i and

    U=x-i+1,       V=c+x+1-j,
    v(r)=nu_2(r),  1<=r<=c.

Its value is

    A_h(i,j) = M(k-c)_+ + h - max v(r),

where r ranges over `[min(U,V),max(U,V)] intersect [1,c]`.
An interval not containing x has value M(k-c)_+.

For k<=c, every key is exposed. The perfect-slot representation places the
positive key in any slot from U to V: there must be enough slots for the
preceding and following zero keys. Slot r has comparison length h-v(r).

For k>=c, exactly c keys are exposed and their skeleton is the perfect
height-h tree. If x is exposed at slot r, selecting the preceding r-1 and
following c-r keys is possible precisely when V<=r<=U, with clipping at
1 and c. If x is unexposed its comparison contribution is h. The feasible
slot interval is nonempty, and its maximum valuation is nonnegative, so
allowing an unexposed x does not improve the formula.

Both exposure statements follow from M>hW: losing one exposed key raises
the terminal penalty more than the largest possible ordinary-cost saving.

## Ruler endpoint pairs describe every ordinary density

Extend v to two virtual endpoints by v(0)=v(C)=h. For a<b, let t be the
maximum valuation strictly between a and b, with t=0 for an empty interior.
Taking the four-window difference of a range maximum gives the nonnegative
quantity

    max(0, min(v(a),v(b))-t).

It is positive precisely when a and b are consecutive multiples of 2^d
for some 1<=d<h, and is then exactly one. Indeed, if the smaller endpoint
valuation is d, a greater separation contains an interior multiple of 2^d;
at separation 2^d the interior maximum is d-1. Endpoint valuation zero
cannot give a positive difference. The pair (0,C) would have d=h but maps
to i=j and is outside the interior density grid.

For cells below the penalty line, `j-i<c`, the endpoint pair maps to

    i=x-a,       j=c+x+1-b,       0<=a<b<=C.

Virtual endpoint 0 or C covers the case where x enters or leaves the
interval in the four-corner difference: the corresponding savings h cancel
the formal h contribution and give zero cost for the missing key.

For cells above the penalty line, `j-i>c`, the mapping is

    i=x+1-b,     j=c+x-a,         1<=a<b<=c.

When clipping prevents an endpoint from moving, the density is zero.
Cells with x outside all contributing intervals also have zero ordinary
density. At either key boundary above the penalty line, its exposed or
unexposed comparison length is h in both relevant intervals, giving zero.

In the stated n,x family every listed pair maps inside the input. The number
below the line is

    sum_{d=1}^{h-1} 2^(h-d) = 2^h-2.

The number above it is

    sum_{d=1}^{h-1} (2^(h-d)-2) = 2^h-2h.

The last summand is zero. All these densities equal one. The n-c cells on
the penalty line are positive: their residual density is zero or the negative
absolute difference of adjacent (possibly virtual) valuations, with magnitude
at most h, while the penalty contributes M>h. Finally the completion diagonal
has n entries. Adding these four counts proves the exact completed core size.

## The maximal tile

Every cell of T lies strictly above j-i=c. Its side-2s parent has anchor
(2s,6s) and intersects that line, so T is an accepted maximal tile of the
same quadtree used in the upper bound.

The four corner slot windows, in telescoping order, are

    [1,2s+2], [s+1,s+2], [s+1,2s+2], [1,s+2].

Their maximum valuations are h-1, 1, h-1, h-2. Their ordinary costs are
1, h-1, 1, 2, respectively; the affine penalty cancels. The tile's density
mass is therefore h-3.

More explicitly, its nonzero density cells are exactly

    (i,j)=(3s+2-2^d, 7s),       d=2,...,h-2.

These are the consecutive-power pairs (a,b)=(s,s+2^d). Thus there are h-3
entries of size one. The growing density mass is not confined to one large
coefficient; the support itself grows with h.

## A global contrast: one weighted key has linear cores

For any input length n and any position of a single positive key, with all
other weights zero, every completed layer core has at most 3n entries.
The same endpoint-pair classification applies; input boundaries only remove
pairs. If c<n, the two ordinary regions have at most c-1 and c+1-2h entries;
together with n-c penalty-line cells and n completion entries this is below
3n. If n<=c<2n-1, only the below-capacity region can occur and it has at most
c-1 entries, again giving less than 3n after completion. If c>=2n-1, every
interval containing the positive key can put it at the root and balance the
zero keys on either side within height h. Its cost equals the key weight,
so all interior densities vanish. Layer zero has only its n completion entries.

Consequently a stronger general upper bound needs a charge across tiles or
another structural restriction. A constant charge independently to each tile
is false even for one weight unit. This result leaves the n sqrt(W) core
conjecture and the sqrt(log n) gap in the current bound unresolved.

## Verification

`dyadic_mass_probe.py` first searches mixed-weight patterns and fixed-mass
local mutations for large tile-mass ratios. `single_key_tile.py` then checks
the derived formulas against the original penalty recurrence, including
literal all-root controls on smaller cases. Its larger closed-form-only rows
are labeled separately. Counts and executed-source hashes are retained in
`results/dyadic_mass_probe.json` and `results/single_key_tile.json`.

The formula audit records 700024 interval checks, 697992 density checks,
1023 penalty-line checks, and 1316 general one-key cases with 88170 additional
density checks. Its totals are 6387678 dense diagnostic states and 12975174
root candidates. The probe records 1199 evaluations and 123 all-root controls.

## Side length resolves the one-key local growth

[The square-support lemma](BOUNDARY_TILE_TARGET.md) proves that every side-s
ordinary square off capacity has at most 1+floor(log2 s) one-key densities.
The family above has log2 s-1, so the leading logarithmic dependence is sharp.
An additional boundary term proportional to s therefore accommodates this
obstruction. The general boundary-plus-mass local bound remains open.
