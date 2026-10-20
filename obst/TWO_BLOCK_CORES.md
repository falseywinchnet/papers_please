# Linear above-capacity support for two equal positive blocks

**Theorem.** Suppose two disjoint consecutive blocks of keys have the same
positive weight alpha, and all other keys have weight zero. Gap weights
may be arbitrary nonnegative reals. In a terminal-penalty layer with valid
penalty and capacity c=2^h-1, the entire ordinary core strictly above
capacity has at most 28n entries. Any s-by-s square strictly above capacity
has at most 40s entries. All above-capacity entries, including their exact
values, can be constructed in O(n log(n+1)) arithmetic work and space.

The constants are conservative. The result includes endpoints inside either
positive block. It proves the proposed local boundary charge for this family
using the side term alone. Unequal block weights, more positive blocks, and
the below-capacity mixed region remain outside this theorem.

Write the zero-based blocks as [z,z+m) and [z+m+g,z+m+g+k), with m,k>=1
and g>=0. The case g=0 is allowed. Normalize alpha to one. Every interval
of length at least c has layer value

    M(length-c)+h W(interval)-S(interval),

where S is the optimum c-subsequence ruler reward. The first two terms
have zero ordinary density, so all gap weights cancel. Binary saturation
retains min(P,c) positive keys, where P is their number in the interval.
If P>=c, the score is the constant F(c), with

    F(t)=sum_(r=1)^t nu_2(r),
    R_l(r)=F(r+l)-F(r).

## A finite band-dominance factorization

For real sequences f_1,f_2 of common length N and an integer d>=0, define

    H(A,B)=max { f_1(u)+f_2(v): u<=A, v>=B, 0<=v-u<=d },        (1)

with A,B,u,v in {0,...,N-1}. The feasible domain is B<=A+d.
Let K=1+max f_1-min f_1+max f_2-min f_2, and define finite matrices

    L(A,u)=K max(u-A,0),
    Q(u,v)=K[max(u-v,0)+max(v-u-d,0)]-f_1(u)-f_2(v),
    R(v,B)=K max(B-v,0).                                  (2)

All three are Monge. With density convention
D_X(i,j)=X(i,j+1)+X(i+1,j)-X(i,j)-X(i+1,j+1), L and R have only
the main-diagonal densities K. Q has density K on v-u=0 and v-u=d,
with the two contributions added when d=0. The row/column additions
-f_1(u),-f_2(v) do not change its core. Hence

    delta(L),delta(R)<=N-1,   delta(Q)<=2(N-1).

For T=L min-plus Q min-plus R, every inadmissible choice incurs penalty
at least K. Its cost exceeds -min f_1-min f_2, while some feasible choice
has cost at most that number. Therefore T(A,B)=-H(A,B) throughout the
feasible domain. Every entry of every operand remains finite.

The published core-product inequality delta(AB)<=2(delta(A)+delta(B))
now gives

    delta(T)<=14(N-1).                                    (3)

All operand boundaries and cores are explicitly available in O(N) work.
The published condensed product algorithm constructs T in O(N log(N+1))
work. This uses the same finite-entry interface as the main OBST reduction;
no dense matrix conversion is needed.

**Local form.** Any s-by-s square of density cells with feasible corners
has at most 22s positive entries. To prove this, let A range over
[a,a'] and B over [b,b'], with each range containing at most s+1 indices.
Discard u>a' and v<b. Aggregate u=0,...,a into the first row and keep
a+1,...,a' as singleton rows. Keep b,...,b'-1 as singleton columns and
aggregate v=b',...,N-1 into the last column. A grouped entry Q' is the
minimum of Q on its row-group/column-group rectangle.

Blockwise minima on ordered disjoint groups preserve Monge: take minimizers
in the two off-diagonal group rectangles, uncross their coordinates, and
apply the original Monge inequality. Away from the first row and last
column, Q' is a consecutive submatrix of Q and has at most two density
diagonals. The first row and last column contribute at most s densities
each. Thus delta(Q')<=4s. Finite prefix/suffix selectors on the group
indices each have at most s core entries. Their product equals -H on the
requested feasible rectangle: the groups describe exactly its allowable
prefixes and suffixes, and the same K excludes invalid choices. Applying
the product inequality twice gives 2[2(s+4s)+s]=22s.

## Two complete positive blocks

Assume m+k<=c and put N=c-m-k+1. When an interval [i,j) contains both
whole blocks, all positive keys can be retained. Let u be the number of
selected zeros before the first block, and v the number of selected zeros
before the second block, excluding the m positive keys in the first block.
Then precisely

    0<=u,v<N,  0<=v-u<=g,
    u<=A=z-i,  v>=B=c+z+g-j.                              (4)

Their score is R_m(u)+R_k(m+v). Apply (1) with f_1(u)=R_m(u), f_2(v)=R_k(m+v),
and d=g. Clip A from above at N-1 and B from below at zero; clipping freezes
an endpoint and creates no additional density. A product-core cell (a,b)
maps to the original density cell

    i=z-a-1,   j=c+z+g-b-1.                               (5)

Thus the region retaining both complete blocks has at most 14(N-1)<=14c
entries globally and at most 22s in a side-s square. If m+k>c, saturation
makes this entire region constant and its ordinary densities vanish.

## All positive-endpoint cuts

Reserve the at most eight grid lines i=t-1 or j=t-1 for

    t in {z,z+m,z+m+g,z+m+g+k},                            (6)

and the two diagonals

    j-i=c+g-1 or c+g.                                     (7)

They contain at most 10n cells globally and 10s in a side-s square.
All remaining four-corner intervals have their endpoints inside fixed
pieces of the five-piece input (zero, positive, zero, positive, zero).
Intervals encountering at most one positive block agree with the one-block
input. The two one-block cores contribute at most 2c globally and 4s locally.
The region containing both complete blocks was handled above.

Consider a left endpoint inside the first positive block and a right
endpoint after the second. Let a=z+m-i be the remaining first-block length
and B=c+z+m+g-j. If a+k>=c, the score saturates. Otherwise all a+k positive
keys are retained. The first a selected ranks are positive, while the
second block starts after a rank offset t satisfying

    max(a,B)<=t<=min(a+g,c-k).

The exact score is therefore

    F(a)+max_(max(a,B)<=t<=min(a+g,c-k)) R_k(t).             (8)

The formula also agrees with saturation at a+k=c. A cell crossing from
a+k>c to a-1+k=c has all four scores saturated, hence zero density.
For the remaining cells, B-a=c+g-(j-i). Outside (7), either B<=a in all
four corners, making the score independent of j, or B>a in all four.
In the latter case (8), after removing the row term F(a), is the range
maximum over [B,min(a+g,c-k)]. Frozen upper endpoints contribute zero;
otherwise its density is a nonadjacent visibility pair of R_k. There are
at most c such pairs globally and 2s locally. Reflection proves the same
bounds for a right endpoint cutting the second block. The reflection
identity nu_2(2^h-r)=nu_2(r) includes the endpoint rewards.

Finally, when both endpoints cut positive blocks, let a and b be the
remaining positive prefix/suffix lengths. If a+b>=c, the score is F(c).
If a+b<c, the interval length ensures there are enough intervening zeros,
and the score is F(a)+F(b): the first a and last b selected ranks are
positive. The four scores separate except when a+b is c-1 or c, precisely
the two diagonals (7). All other densities in this region vanish.

Adding the contributions proves

    K_above <=14c+2c+2c+10n <=28n,
    K_square<=22s+4s+4s+10s=40s,                           (9)

where c<n whenever the above-capacity region is nonempty. Multiplying all
positive keys by alpha multiplies density values and preserves support.

## Constructing the whole above-capacity core

The proof specifies O(n) candidate cells: the complete-block product core,
the two one-block visibility cores, the two one-cut visibility cores, and
(6)--(7). Construct their union, discard cells outside the input or not
strictly above capacity, and evaluate the four interval scores at each
candidate. There is no scan over all n squared interval pairs.

Precompute F and the two block-reward sequences R_m,R_k in O(c) work using
the even/odd recurrence for ruler valuations. Segment trees give their
range maxima in O(log(n+1)) time. Saturated intervals use F(c); one-block
partial intervals use F(P); both-cut intervals use F(a)+F(b); and (8) or
its reflection gives a single-cut score. Whole one-block intervals use the
one-block range formula. Whole two-block intervals query T from (2).

For the O(n) queries to T, the condensed representation gives

    T(A,B)=T(A,0)+T(0,B)-T(0,0)
             -sum_(x<A,y<B) D_T(x,y).

Sort queries by A and sweep the O(c) core entries in row order, maintaining
column prefix sums in a Fenwick tree. This evaluates every query in total
O(n log(n+1)) work and O(n) additional space. Subtract the four scores
with the correct density sign and retain precisely the positive results.

The reused sparse-product implementation builds ordinary witness maps,
so the stated implemented space bound is O(n log(n+1)). The theorem does
not assume its arrays are succinct. Its output core has O(n) entries.
The full mixed OBST constructor and its main complexity theorem are unchanged.

## Verification appendix

The generic band audit checks 1332 inputs, including exhaustive binary f,g
through N=4 and signed integer arrays through N=16. It compares 28024 finite
product entries against 2098072 literal pair choices, including infeasible
completion entries, and checks 23821 feasible rewards. It also checks 3996
coarsened cores and 11808 coarsened-product entries. These controls directly
test the finite penalties and local aggregation, rather than only the loose
support constants.

The interior audit checks 576 support sets against original mixed all-root
layers on 168 inputs through 32 keys, with 5690 densities and 672 literal
subsequence intervals from 20517 choices. Its original recurrence uses
1345248 root candidates and 146592 states. Twenty-four larger condensed
constructions reach 16384 keys; those rows are explicitly constructor
checks, with 661 additional square controls, not original all-root runs.

The complete audit checks 952 mixed inputs through 64 keys, including all
792 binary words with exactly two positive runs through ten keys and 160
seeded larger inputs with common positive key weight three. Nonzero gap
weights are included. All 2953 complete above-capacity support sets and
334032 densities agree with the independent all-root recurrence, which
uses 12507215 root candidates and 784506 states.

Fourteen larger full constructions reach 8192 keys and include 864 local
square controls. For two unit keys at that size, the constructor considers
31017 distinct density candidates and outputs 3219 positive densities.
It performs 26527 range queries and 15631 condensed-matrix value queries;
its record includes the separate sparse-product operation counts. No timing
or fitted exponent supports (9) or the construction bound.

Sources and hashes are recorded in `results/band_dominance_audit.json` and
`results/two_block_core_audit.json`. The constructor is `code/band_dominance.py`;
its audits are `code/band_dominance_audit.py` and `code/two_block_core_audit.py`.
