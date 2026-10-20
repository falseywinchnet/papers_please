# An exact mixed-weight solver with a variable interval frontier

The input retains every ordered key and gap weight. Unlike the preceding
height certificate, this constructor chooses a class guaranteed to contain
an unrestricted optimum before solving it. It compares a uniform short-width
implementation of the Larmore/Karpinski--Larmore--Rytter architecture with
an implementation that stores only an admissible variable interval contour.
Worst-case work remains quadratic. Novelty of the contour specialization is
not established; it is not a claim to invent subquadratic restricted OBST.

## A bound-transfer failure caught by the harness

The first implementation used the literal bound 2W/F_(d+3) for an internal
subtree at edge depth d. It failed on p=[1,1,1,1,1], q=[1,1,1000000,1,1,1]:
the resulting depth-one contour contained no feasible tree. The exact smaller
counterexample is p=[1,1], q=[1,100,1]. Both possible trees cost206. Their
internal child has mass102, while the whole tree has mass104, so102>2*104/3.
Every weight is positive. Gap costs shifted by a tree-independent constant
cannot repair that violation.

The Fibonacci approach and the sharper quoted formula occur in
Hirschberg--Larmore--Molodowitch, *Subtree Weight Ratios for Optimal Binary
Search Trees*, TR86-02, Theorem2; Section5 discusses mixed weights. KLR also
quotes a Fibonacci bound with a level convention. We do not rely on transferring
that sharper formula into our model. The elementary counterexample and a
separate sufficient bound below specify exactly what the implementation uses.
This does not refute the KLR construction or its asymptotic bounds.

Primary sources:
- https://ics.uci.edu/~dhirschb/pubs/TR86-02.pdf
- https://theory.cs.uni-bonn.de/marek/publications/seq_and_par_subquadr.pdf

## A sufficient Fibonacci bound proved in the full model

Let S be an INTERNAL subtree at edge depth d in an optimal tree of total
outcome mass W. With F_1=F_2=1,

    mass(S) <= W/F_(d+1).

The distinction between internal subtrees and arbitrary external leaves is
necessary. A heavy interior gap can itself occupy depth two with almost all
of the input mass; the construction always permits zero-key subtrees.

Proof: consider an internal grandchild X of a node v, and let its parent be y.
Let O be the mass outside y but within v's subtree, including key v. For a
straight two-edge path, promoting y changes cost by

    O - p_y - mass(X).

Optimality implies O>=mass(X). For a bent path, write X=x(B,C) and the local tree as v(y(A,x(B,C)),D).
The double rotation gives x(y(A,B),v(C,D)). Key x rises two levels; B and C
rise one level; key v and D fall one level; y and A keep their depths.
Thus, with O=p_v+mass(D), promoting X changes cost by

    O - p_X - mass(X),

and gives the same implication. These formulas include every gap weight.
Along the path upward from S, write T_0=S,T_1,...,T_d=T. Nonnegativity gives
mass(T_1)>=mass(T_0), and the grandchild inequalities give

    mass(T_i)>=mass(T_(i-1))+mass(T_(i-2))  for i>=2.

Induction yields mass(T_d)>=F_(d+1)*mass(S). All inequalities are weak, so
ties and zero weights are covered. This is a conservative bound, not a
claim of a sharp constant or a new Fibonacci method.

## The interval contour

For a fixed d, let W(i,j) be the total mass of keys [i,j) and gaps [i,j].
Define E_d(i) as the largest j>i satisfying

    F_(d+1)*W(i,j) <= W,

or i if no nonempty interval qualifies. Empty intervals are always stored
with cost zero. Nonnegative weights imply E_d(i) is nondecreasing in i,
and the admissible interval domain is hereditary under taking subintervals.
A two-pointer scan computes the contour with O(n) mass comparisons. Set

    S_d = sum_i (E_d(i)-i).

Every internal subtree rooted at depth d in every optimal tree is in this
domain by the mass lemma. The top grid has 2^d blocks; coarse external gaps
may span several blocks. Thus composing exact costs from this domain with
an unrestricted top skeleton recovers the full optimum.

For comparison, the uniform implementation takes ell_d=max_i(E_d(i)-i)
and stores EVERY interval of length at most ell_d. Its cell count is

    U_d = ell_d*(n+1)-ell_d*(ell_d+1)/2 >= S_d.

Both implementations use the same safe mass bound and top construction.
This controls the effect of replacing a global width by a local contour.
It is an implementation of the established architecture, not a benchmark
against every optimization in historical implementations.

## O(S_d) Knuth work on a nonrectangular domain

Simply scanning all starts for every possible length would cost
O(n*max_width), losing the proposed saving. Instead bucket only admissible
intervals by length, using O(n+S_d) construction work and space.
For each nonempty interval, use the ordinary unrestricted Knuth recurrence.
All child costs and adjacent shorter roots exist by heredity.

There is also a root-search accounting issue: diagonal gaps prevent direct
application of the usual full-diagonal telescoping explanation. Let r(i,j)
be the leftmost minimizing root and t(i,j)=r(i,j)-i>=0. For length>=2 the
number of tested roots is

    2+t(i+1,j)-t(i,j-1).

Sum over the contour. A positive t(a,b) term cancels its negative occurrence
whenever (a,b+1) is present. An unmatched positive term can occur only at
b=E_d(a), with E_d(a-1)=E_d(a). There is at most one per row, of size at
most E_d(a)-a. All unmatched negative terms can be discarded in an upper
bound. Including the length-one cells gives at most3*S_d root candidates.
Therefore the stored interval recurrence costs O(n+S_d), even if its
length diagonals have many holes. The harness asserts this bound.

## Top construction and variable-band matrix search

Use the preceding split-height tiling recurrence with upper depth d, but
replace height-limited lower costs by these unrestricted interval costs.
A block starting after i gaps may finish after j gaps exactly when

    i < j <= E_d(i)+1.

Its added cost is C(i,j-1)+d*W(i,j-1), plus the starting boundary key cost
p_(i-1)*(d-v2(b)) at nonzero grid boundary b. Shallower gaps retain their
aligned power-of-two skip transitions. Reconstruction uses ordinary lower
subtree roots, so lower trees may be arbitrarily tall within their sizes.

For output column j let L(j) be the smallest i with E_d(i)+1>=j. It is
nondecreasing and L(j)<=j-1. Reachable rows need not be contiguous; nor
must their feasible output columns form one interval. Scan once per grid
boundary to retain exactly columns covered by some reachable row. SMAWK
then runs on those rows and columns, not on a guessed contiguous region.

Let Z=(n+d+1)*W+1, greater than every finite prefix cost. In the transposed
matrix use Z+L(j)-i for i<L(j), Z+i-j+1 for i>=j, and the true entry inside
the band. The matrix is totally monotone. Inside the band, exact interval
costs are Monge and row/separable additions preserve the inequality. The
band moves right with j; finite entries beat padding and same-side distance
preferences are monotone. For candidates on opposite invalid sides, their
cost difference is i1+i2+1-j-L(j), nonincreasing with j. Removing arbitrary
rows/columns preserves total monotonicity. All searched columns contain a
finite entry, so every returned minimum is feasible.

Total top work, including row/column scans, padding queries, and all coarse
transitions, is O(n*2^d). Full backpointer storage has the same bound.

## Selection and full-problem complexity

The selector starts with d=0, the entire Knuth table, and evaluates increasing
d while n*2^d is below the best work proxy already found. At each depth it
computes S_d in O(n), then scores S_d+n*2^d (or U_d+n*2^d for uniform width).
No omitted depth can improve this proxy because its top term alone is too
large. At d=0 the direct Knuth solver is used without a redundant top pass.
Its proxy is S_0 rather than S_0+n; this changes only a lower-order term.
Selection requires O(n log(n+1)) arithmetic work and O(n) extra space.

For the adaptive contour, the full exact constructor has work

    O(n log(n+1) + min_d [S_d+n*2^d]),

and O(n+S_d+n*2^d) space at the selected depth. There is no posterior failure
certificate and no repeated full fallback after a failed restricted solve.
Choosing d=0 guarantees quadratic worst-case work. Python dictionaries
implement the finite top states; direct indexed arrays support the same
arithmetic bound. Bit complexity for unbounded integer weights is separate.

When every key has weight at least a>0 and W=O(n*a), admissible widths are
O(n/F_(d+1)), so S_d=O(n^2/phi^d), phi=(1+sqrt(5))/2. Balancing this with
n*2^d gives O(n^(1+log_(2phi)(2))) = O(n^1.59024). This recovers the familiar
restricted subquadratic regime of prior work; it is not a new worst-case
bound for arbitrary weights. The contour can be smaller when a long
low-mass interval is localized rather than representative of the whole input.

## Verification

The final correctness harness passed960 weighted comparisons against all
shapes through eight keys on arbitrary nondecreasing contours, including
infeasible classes. It independently checked914 short interval costs and
90,193 top minima against brute search. Another2,400 full solves (both
modes on1,200 inputs through40 keys) matched independent cubic DP and direct
reconstruction. All24,600 internal subtrees in those cubic-optimal trees
satisfied the conservative Fibonacci inequality. Input families include
zeros, ties, geometric and reversed/folded geometric, spikes, and key-only
and gap-only controls. The earlier unsafe mass normalization is preserved
as a two-key positive counterexample in the result file.

## A scoped asymptotic separation from a global width

Let n grow through fourth powers, L=n^(3/4), and A=n^2. Give every key and
gap weight A except one central block of L keys and its L+1 gaps, which
have weight1. All weights are positive integers. Total mass is Theta(nA).
Write beta=log_(2*phi)(2), approximately0.59023.

At a fixed depth d, any admissible interval contains at most
m=O(n/F_(d+1)) heavy keys. Intervals contained in the light block number
O(L^2). For starts outside the block, ordinary endpoints contribute O(n*m);
only O(m) starts can reach across a boundary and gain O(L) extra endpoints.
Starts inside the block add O(L*m) heavy endpoints. Hence

    S_d=O(n^2/F_(d+1)+L^2).

Taking d=floor(log_(2*phi)(n)) gives adaptive total work
O(n^(1+beta)+n^(3/2))=O(n^1.59024).

In contrast, every uniform-width plan in this implementation has work proxy
Omega(nL)=Omega(n^1.75). If 2^d>=L its top term already has that size.
Otherwise F_(d+1)=O(phi^d)=O(L^(log_2(phi))), and W/F_(d+1) is much larger
than the O(L) mass of the entire light block. Consequently ell_d>=L, so the
uniform table contains at least nL/2 cells. This argument covers every d,
including plans outside the implemented selector's stopping range.

This proves an asymptotic advantage over the specified uniform-envelope
construction, not over all earlier OBST algorithms, nor over combinations
of our contraction rules with other solvers. In particular this light block
also presents an opportunity for certified contraction. The role of the
example is to show that variable contour storage can improve an exponent,
rather than merely a constant, within the same top-skeleton architecture.

## Operation counts and matched timing

The larger exact sweep checks56 fixtures through2,048 keys in both modes.
At n=2048 on ordinary random mixed weights, adaptive chooses d=6 and returns
the full optimum21,053,524. It stores309,261 intervals and checks616,642
roots, compared with Knuth's2,098,176 intervals and4,215,527 roots. Additional
work is24,035 contour mass checks across7 parameter levels,1,245,431 genuine
matrix queries,149,319 padding queries,131,136 scans of each row/column type,
107,859 coarse transitions, and reconstruction of all2,048 keys. Selection
also makes linear endpoint passes per parameter level; those levels and all
major operation categories are retained, not equated to unit CPU instructions.

At that size, uniform width stores337,550 intervals on random input versus
adaptive's309,261. For log-uniform input the counts are431,951 versus308,487;
for a single heavy key,1,573,376 versus1,048,576. Geometric inputs choose the
full table in both modes; the contour alone does not solve that regime cheaply.

The matched benchmark uses all six orders of Knuth, uniform width, and the
adaptive contour on each fixture, for48 trials. Preprocessing and reconstruction
are timed, and every output is compared with Knuth and directly evaluated.
Inputs vary between trials except deterministic geometric and spike fixtures.
The light-window timing fixture uses weights near1000 outside a contiguous
floor(n^(3/4))-key block and weights1 inside; its position varies. This finite
benchmark is separate from the A=n^2 asymptotic family above.

| Fixture | Uniform / Knuth | Adaptive / Knuth | Adaptive / uniform |
| --- | ---: | ---: | ---: |
| n=512, random | 1.59908 | 1.61204 | 0.96602 |
| n=1024, random | 1.56592 | 1.55650 | 1.00412 |
| n=2048, random | 0.90002 | 0.91021 | 1.00096 |
| n=2048, light window | 1.13693 | 0.77546 | 0.65523 |
| n=2048, near-uniform | 0.87926 | 0.91295 | 1.02587 |
| n=1024, log-uniform | 1.67408 | 1.47983 | 0.88390 |
| n=512, geometric | 0.98060 | 1.04487 | 1.01772 |
| n=2048, heavy key | 1.50542 | 1.04249 | 0.70113 |

Each entry is the median of paired per-trial ratios, not a quotient of table
medians. These are instrumented Python3.9.6 measurements on the sponsor's M4.
The implementations are slower on several smaller fixtures; the adaptive
contour's saving over uniform width is clearest on localized light/heavy
structure, not on ordinary random inputs. Both geometric controls execute
the same Knuth kernel after selection; a ratio below one there is timing
variation, not an algorithmic saving. All raw data are in
results/mass_frontier.json and results/mass_frontier_matched.json.

## Separation-plan evidence

The positive A=n^2 family was solved exactly in both modes at n=16,81,256,625;
Knuth checked all four and cubic DP additionally checked the first two. Larger
instances below were used only to count selected plans, not to run full solves.

| n | Light keys | Adaptive depth / proxy | Uniform depth / proxy |
| ---: | ---: | ---: | ---: |
| 256 | 64 | 5 / 17,395 | 4 / 25,057 |
| 1,024 | 181 | 6 / 157,111 | 5 / 284,877 |
| 4,096 | 512 | 7 / 1,424,611 | 7 / 3,085,539 |
| 16,384 | 1,448 | 8 / 12,961,429 | 8 / 33,331,471 |
| 65,536 | 4,096 | 9 / 119,041,540 | 9 / 361,608,522 |

The proxy is S_d+n*2^d or U_d+n*2^d, not a sum of measured machine
instructions or an elapsed-time prediction. Parameter-selection work is
additional and retained as contour checks and levels. Data: results/frontier_separation.json.
