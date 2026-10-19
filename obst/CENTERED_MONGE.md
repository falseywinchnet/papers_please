# Centering the Monge core bound around constant key and gap baselines

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. This extends the terminal-penalty reduction to large
integer baselines with small total deviation. It does not settle unrestricted
weights or establish a practical speedup. The sparse product and witness
algorithms remain the prior work of Gawrychowski, Gorbachev, and Kociumaka.

## Statement

For n>=1, let p and q be nonnegative integer key and gap weights. Define

    a = min_i p_i,    b = min_j q_j,
    u_i = p_i-a,      v_j = q_j-b,
    R = sum u_i + sum v_j,       W = sum p_i + sum q_j,
    L = ceil(log2(n+1)).

For W>0 let s be the smallest positive singleton mass p_i+q_i+q_(i+1).
Let z=0 if all singleton masses are positive, and z=L otherwise. Use

    H = min(n, f(floor(W/s))+z),

where f(x) is the first Fibonacci index with F_f>x, F_0=0,F_1=1.
For W=0 use H=L. With the same M=(H+1)W+1 and finite completion as in
MONGE_PENALTY.md, every completed layer has core size

    K = O(n + min(n^2, n sqrt(W L), nL + n sqrt(H R L))).

Thus the published core-sparse product/witness algorithm constructs a full
optimum in O(H K log(n+1)) arithmetic operations. Published succinct witnesses
use O(H K) words; the ordinary maps implemented here can use O(H K log(n+1)).

In particular, **R=O(n) gives O(n^(3/2) log^3(n+1)) arithmetic construction,
independent of the sizes of a and b in the operation count.** Both kinds of
weights may vary arbitrarily subject to that total-deviation condition. For
example p_i=n^c+u_i and q_j=n^d+v_j, with fixed nonnegative integer c,d and
bounded nonnegative integer deviations, have O(log n)-bit arithmetic even
though total mass need not be O(n). Arbitrarily large integer baselines retain
a bit-cost dependence on their representation length. More generally, if
R=O(n^c) for fixed c, the bound is O(n(1+sqrt(R)) log^3(n+1)). Thus
R=O(n^(2-epsilon)) gives O(n^(2-epsilon/2) log^3(n+1)) for fixed 0<epsilon<=2,
regardless of baseline magnitudes in the arithmetic model. This is an extension
of this project's core-size guarantee, not a first subquadratic algorithm
for every family it covers; earlier restricted-weight algorithms remain
relevant, and priority of the present application is unestablished.

## The normalized height bound

Every positive-mass internal interval contains a positive-mass singleton
interval. If a positive key supplies the mass, choose that singleton. If a
gap supplies it, choose an adjacent key belonging to the interval. Thus every
positive internal subtree has mass at least s. The previously proved mixed
Fibonacci subtree inequality gives W>=F_(d+1) s for every such subtree at
depth d in an optimal tree. Its positive part therefore has bounded depth
using f(floor(W/s)). Zero-mass subtrees can be balanced without changing cost,
adding at most L levels. If every singleton is positive, no nonempty zero-mass
subtree exists and no extra L is needed. The trivial height n is also valid.
The same global H works for every subinterval. If W=0 a balanced optimum of
height L suffices. This is a rescaling of the actual-optimum height argument;
it is not a rotation claim about partially expanded trees.

## Exact baseline layer formula

Let I(k) be minimum unweighted internal path length for k keys, with I(0)=0.
For k>=1 and d=floor(log2 k),

    I(k)=d k - 2^(d+1) + d + 2.

A full k-key tree with constant key/gap weights a,b has cost
(a+b) I(T)+(a+2b)k. This familiar internal/external path-length identity is
already used by the earlier minimum-path-length certificate.

Write c_h=2^h-1. The optimal h-level partial-tree cost for those baseline
weights, using the *same* terminal penalty M, is

    F_h(k) = (a+b)I(k)+(a+2b)k                         if k<=c_h,
             M(k-c_h)+(a+b)h(k+1)-a c_h              if k>c_h.

Since M>HW, every minimizing partial tree exposes min(k,c_h) keys. If k<=c_h,
a full minimum-path-length tree fits in h levels. If k>c_h, exposing c_h
keys forces a complete first h levels. Its explicit keys contribute
sum_(t=0)^(h-1) a(t+1)2^t; unfinished keys contribute a h(k-c_h), and all
k+1 gaps contribute b h. This gives the displayed second branch.

Let A_h be the original full-weight layer. Comparing the best full-weight
partial tree to a baseline-optimal partial tree gives

    A_h(i,j) = F_h(j-i) + E_h(i,j),
    0 <= E_h(i,j) <= h R(i,j),
    R(i,j)=sum_(i<=r<j) u_r + sum_(i<=r<=j) v_r.

This does **not** replace the input weights by deviations in the solver.
The solver retains the original full costs. Centering is an analysis of their
representation; the residual is not asserted to be Monge.

The length-only baseline density at length k>=1 is exactly

    a+b       if k=2^t-1 for 1<=t<h,
    M-b       if k=2^h-1,
    0         otherwise.

Only lengths inside the matrix matter. Thus all baseline densities are on
at most L parallel diagonals, regardless of how large a and b are.

## Packing the residual tiles without multiplying the mass bound by L

Remove the density cells on every line j-i=2^t-1 inside the triangular
domain, and the main diagonal. They account for O(nL) cells. Partition the
remaining density-index domain into maximal aligned dyadic squares that do
not cross these lines or the domain boundary, using a power-of-two enclosing
square. For a side-s tile T=[x,x+s) x [y,y+s), let its spanning input interval
be J_T=[x,y+s], inclusive for gaps.

Two geometric facts hold at each scale s:

1. There are O(nL/s) tiles. Each parent meets a removed line or an outer
   boundary, and any one straight boundary meets O(n/s) aligned squares.
2. Every input position lies in J_T for only O(n/s) such tiles. This second
   bound has **no factor L**. To see it, charge each tile to a boundary
   intersecting its parent. Tiles charged to a diagonal of distance d>=s
   lie within O(s) of that diagonal. For a fixed input position x, their
   row starts occupy an interval of length O(d+s), with spacing s; at each
   row start only O(1) column starts lie near the diagonal. They contribute
   O(1+d/s) covering intervals. The distances d are geometric, so their sum
   is O(n) and the sum of these covering bounds is O(n/s). All diagonals
   with d<s lie in one O(s)-wide strip near the main diagonal and together
   contribute O(1) covers of a fixed input position. Outer-boundary tiles
   number O(n/s) in total. A constant number of charge choices only changes
   constants.

The second fact implies sum_T R(J_T)=O(nR/s), for every nonnegative residual
weight vector, by charging each weight to its covering intervals.

On an ordinary tile the baseline density is zero, so the true nonnegative
integer density telescopes to

    E_h(x,y+s)+E_h(x+s,y)-E_h(x,y)-E_h(x+s,y+s)
        <= 2h R(J_T).

The number of nonzero densities is at most both s^2 and this density mass.
Summed over side-s tiles, this is

    O(min(nLs, hnR/s)).

The sum over dyadic scales is O(n sqrt(hRL)); split the geometric sum at
s approximately sqrt(hR/L). If R=0 all ordinary densities vanish. Adding
the removed cells and finite-completion diagonal gives

    delta(E_h_completed) = O(nL + n sqrt(hRL)),

also capped by O(n^2). For h=0 the completed core is O(n). Combining this
with the previous bound O(n+n sqrt(WL)) proves the stated uniform K bound.
Every product, conversion, and witness reconstruction still uses the actual
condensed matrix, so the established reduction supplies the running time.

If R=O(n), H=O(log(n+1)). When a+b=0, W=R and s>=1 whenever W>0. Otherwise
s>=a+2b>=1 and W=n a+(n+1)b+R<=n(a+2b)+R; all singleton masses are positive.
In general H=O(log(n+R+1)); when R is polynomial in n this is O(log(n+1)).
For R=O(n), W/s=O(n) in either case (plus the possible L term). Substitution gives
O(n^(3/2) log^3(n+1)). The earlier O(n^(3/2) log^(5/2)(n+1)) bound remains
better when total mass itself is O(n).

## Independent evidence and implementation limits

`centered_layers.py` is a dense falsification harness, not a fast constructor.
It passed 1,100 complete solves, 824 independent cubic comparisons, 3,317
all-root cells, 1,538 baseline all-shape checks, 99,087 baseline-density
checks, 685,288 tiles, and 2,327 scale-packing checks. It explicitly computed
4,153,053 dense states and 8,223,340 root candidates and reconstructed 11,656
keys. The formulas are tested with independent key/gap offsets including
2^256 and 2^200, zeros, concentrated gap mass, and geometric weights.

At n=256, three large-baseline fixtures have total deviations 501, 505, and
504. The normalized height budgets are 14, 14, and 12, compared with the
old numerical-mass budgets of 256. Their maximum interior cores are 6,428,
6,386, and 6,351. These are budget and representation comparisons, not runtime
improvements: the previous constructor already uses exact early stopping.
The 64-key geometric control still needs H=64 and has every one of its 2,016
interior density cells nonzero.

`centered_obst.py` is a separate version of the actual condensed constructor,
using the normalized height bound and the same published compact product.
Keeping the earlier implementation unchanged preserves the previous
source-hashed benchmark controls. The new complete audit passed 999 solves,
790 cubic comparisons, 32 fixed-budget controls, 1,001 intermediate values
and leftmost witnesses, 12 comparisons against the original compact solver,
and 9,992 reconstructed keys. Large-baseline 256-key fixtures finish in ten
layers with completed cores of 6,624, 6,540, and 6,496. Both key and gap
weights remain in the exact objective. No new timing advantage is claimed.

`centered_geometry.py` independently checks the tile partition and maximum
spanning-interval overlap at every input position, rather than testing only
sampled residual weights. It passed 163 sizes through 4096 and 749 scale checks; its source-hashed
results accompany the two solver audits. Observed constants are diagnostics; the asymptotic statement uses
the geometric proof above. The previous compiled backend's severe losses
remain reported, and no unrestricted subquadratic result is claimed.
