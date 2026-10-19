# Necessary terms in a proposed off-capacity mass estimate

The full mixed research target is the unproved estimate

    T_(h,d)=O(W(L+c_h/d)),

where T is ordinary density mass over |j-i-c_h|>=d, d>=1, and
L=ceil(log2(n+1)). The capacity line itself is excluded. The results below
prove that both terms are necessary and determine a sharp lower constraint
on the constant. They do not prove the proposed mixed upper bound.

## One key: an exact tail and the limiting coefficient four

Take h>=2, n=2^(h+1), c=2^h-1, and one unit key at x=2^h+1, all other
weights zero. The proved single-key classification in LOCAL_TILE_OBSTRUCTION.md
places all ordinary densities at distances 2^r-1 from capacity, 1<=r<h.
At distance 2^r-1 there are 2^(h-r) below-capacity entries and
2^(h-r)-2 above-capacity entries, all of value one.

Put r_0=ceil(log2(d+1)). If r_0>=h the tail is zero. Otherwise summation gives

    T_(h,d)=2^(h-r_0+2)-2(h-r_0)-4.                         (1)

The count is also the tail support. For an arbitrary one-key input,
boundaries only remove entries from this classification. If the key has
weight w, therefore

    T_(h,d)<=4w(c+1)/(d+1).                                (2)

To see why the coefficient cannot be reduced in the candidate estimate,
take h=2r and d=2^r-1. Here L=2r+2 and c/d=2^r+1, so exactly

    T_(h,d)/(W(L+c/d))=(4*2^r-2r-4)/(2^r+2r+3) ->4.       (3)

Thus no uniform inequality T<=C W(L+c/d) with C<4 can hold. Scaling the
single key to weight n makes W=n without changing this ratio. Formula (3)
is an asymptotic proof, not an extrapolation from a finite search.

## Uniform positive mixed weights require the WL term

Use the same n,h,c, and put every key and gap weight equal to one. The
uniform layer has density two on j-i=2^t-1 for 1<=t<h, zero elsewhere
off capacity. At d=2^(h-1), all those diagonals lie outside the band. Hence

    T_(h,d)=2 sum_(t=1)^(h-1) (n-(2^t-1))
           =2((h-1)n+h-c).                                (4)

Now W=2n+1 and c/d<2, but T/(WL)->1. An O(Wc/d) bound alone is therefore
false even for strictly positive uniform mixed weights. Equations (3) and
(4) show separate regimes in which each term of the candidate is required.

## Targeted diagnostics

The expanded C++ search evaluates every integer d=1,...,n at every early
layer. Its 851 structured inputs include one/two-key cases, periodic combs
on keys, gaps, or both, clustered/spread ramps, geometric and ruler weights,
near-uniform weights, and positive alternating keys. It also runs 18
fixed-mass searches through n=512, with 11868 candidate evaluations.
All 133 small reference vectors are checked against an independent all-root
recurrence, including the complete list of best bands at every layer.
The largest observed ratio is 20/7 at n=1024, on a one-key input. This is
consistent with (3); it does not certify a universal bound.

Structured evaluation records 515067958 states, 991657809 root candidates,
513507096 densities, and 1560862 band evaluations. The searches record
1044782928 states, 2074271291 root candidates, 1037289648 densities, and
7493280 bands. Source hashes, exact weights, seeds, and winners are in
`results/core_tail_search.json`. The optimized diagnostic is dense and is
not the sparse construction algorithm.

The separate lower-family audit compares (1) and (4) against independent
all-root layers through n=128: 4803968 root candidates, 125056 states,
21576 density checks, and 496 tail-formula checks. Larger rows, through
h=128, evaluate only the proved formulas and are labeled accordingly in
`results/core_tail_extremes.json`.

A further diagnostic tests the stronger interaction allowance

    T_(h,d)(w)<=sum_x w_x T_(h,d)(e_x)+hW.

This inequality is unproved. It is checked on 3103 basis/input vectors,
including all mixed binary vectors at n=4,5 and random/structured inputs
through n=32, with 46370 interaction comparisons. The largest observed
positive excess divided by hW is 17/26. The all-root work is 4983120
candidate roots and 537572 states. This is a potential proof route, not a
consequence of the existing one-key theorem; the gap unit inputs and the
interaction term must both be controlled. Records are in
`results/core_tail_interaction.json`.

## Boundary computation

The band itself can now be evaluated exactly without a quadratic table:
CAPACITY_BANDS.md proves O(n(d+1)H) work for all intervals within width d
of every capacity c_h. That component is valid for arbitrary mixed weights
and does not depend on the unproved tail estimate. It provides a concrete
way to separate direct treatment of the boundary from analysis of the tail.
