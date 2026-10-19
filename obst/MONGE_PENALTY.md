# Penalized partial trees and a core-sparse Monge reduction

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. This is a mathematical reduction using an existing sparse
matrix multiplication theorem. Dense reference audits and actual condensed
Python and C++ constructors now accompany the reduction. The implementation
details, operation counts, and measured limitations are recorded below.
Priority is unestablished; the unrestricted subquadratic objective remains open.

## Result and computational model

Let n>=1 and let all key and gap weights be nonnegative integers of total mass
W. Put L=ceil(log2(n+1)). For W>0 let f(W) be the first index with Fibonacci
number F_f>W (F_0=0,F_1=1), and use the same definition for W=0. Choose

    H = min(n, f(W)+L),
    M = (H+1)W+1.

When every key weight is positive the +L in H can be omitted. The construction
below, together with Gawrychowski--Gorbachev--Kociumaka's published core-sparse
Monge product and witness oracle, gives full exact BST construction in

    O(H [n + min(n^2, n sqrt(W L))] log(n+1))

arithmetic operations. Using the published succinct witness representation, retaining the witnesses
uses at most O(H [n + min(n^2,n sqrt(W L))]) words. The implementations here
use ordinary index arrays and can incur an extra logarithmic factor in space. In particular **W=O(n) gives
O(n^(3/2) log^(5/2)(n+1)) exact construction**, with arbitrary ordered mixed
integer weights, including zeros. The bit lengths of the intermediate numbers
are O(log(n+1)+log(W+1)). The claim for linear mass therefore also fits the
usual O(log n)-bit arithmetic model. Knuth remains the fallback when this bound
is not favorable. Neither a general strongly subquadratic bound independent
of numerical weights nor a practical speedup has been established.

The earlier mass-frontier exponent below 1.59024 applies to positive bounded
backgrounds; the present reduction gives a smaller exponent, up to logarithms,
for linear total integer mass and does not require a positive minimum weight.
It does not invoke alphabetic-only optimization or make all key weights equal.

## The iteration

Let C be the true interval-cost table with C(i,i)=0, and W(i,j) the usual mixed
interval mass. Start from a large **upper** bound:

    A_0(i,j)=M(j-i),
    A_h(i,i)=0,
    A_h(i,j)=W(i,j)+min_{i<=r<j}[A_(h-1)(i,r)+A_(h-1)(r+1,j)].

A_h is the minimum cost of a tree expanded for h levels, charging M for each
key still in an unfinished terminal interval. An empty interval costs zero.
An explicit decision charges the ordinary interval mass. For any such partial
tree with t explicit keys the cost is

    M[(j-i)-t] + D,  0<=D<=h W(i,j).

A partial tree can expose at most min(j-i,2^h-1) keys, and this number is
attainable with inorder labels. Since M>H W, every minimizer for h<=H exposes
that maximum number. Consequently, with c_h=2^h-1,

    A_h(i,j)=M max(0,j-i-c_h)+R_h(i,j),
    0<=R_h(i,j)<=h W(i,j).

The residual R_h need not itself be Monge. That distinction matters below.

A_0>=C, and the monotone recurrence preserves this inequality. Also
A_1<=A_0 because W(i,j)<=M, so all layers decrease. If h is large enough for
an optimal full tree, the full tree is feasible in the h-level computation
without a terminal penalty, proving A_h=C on that interval.

The mixed Fibonacci subtree bound ensures that every positive-mass internal
node of any optimal tree has depth d with F_(d+1)<=W. Zero-mass subtrees can
be replaced by balanced trees of height at most L without changing cost.
Thus some optimal full tree has height at most f(W)+L. The trivial n bound
also holds, proving A_H=C for every interval. When all key weights are
positive every internal subtree has mass at least one and the extra L is
unnecessary. This is a height argument for an actual optimal tree, not an
unjustified rotation argument for unfinished trees.

## Monge preservation and finite completion

For 0<=i<j<n define the interior density

    Delta_A(i,j)=A(i,j+1)+A(i+1,j)-A(i,j)-A(i+1,j+1).

Every layer has nonnegative integer density. Here is a direct reduction
that also explains how to compute it with finite Monge matrices. Let

    P=4nM+4W+1,
    E_h(i,j)=A_h(i,j) if i<=j, and P(i-j) otherwise.

E_0 is Monge. Assuming E_(h-1) is Monge, multiply its first n columns by its
last n rows in the min-plus sense:

    B_h(i,j)=min_(0<=r<n) [E_(h-1)(i,r)+E_(h-1)(r+1,j)].

For i<j, every invalid r has a term at least P, while a valid pair has value
at most nM. Therefore B_h gives precisely the restricted recurrence.
The product is Monge. Adding W(i,j), a row term plus a column term, preserves
density in all squares strictly above the diagonal. The only interior
squares involving a reset diagonal entry have j=i+1; their new density is

    min(A_(h-1)(i,i+1),A_(h-1)(i+1,i+2)) - q_(i+1) >= 0.

At h=1 both old singleton entries equal M; afterward each is its singleton
interval mass. Thus the inequality always holds. The finite completion adds
only n diagonal core entries P+A_h(i,i+1); all densities below that diagonal
are zero. This proves the induction, including the diagonal boundary cases.

## Why the intermediate cores are subquadratic

A core is the list of nonzero densities. Counting only the final core is not
enough: early layers include large terminal penalties.

First, for any triangular A with A(i,i)=0, telescoping gives

    sum_(i<j) Delta_A(i,j)=A(0,n)-sum_i A(i,i+1).

For h>=L a balanced full tree is available and A_h(0,n)<=LW. Hence the
interior core has at most LW entries, by nonnegative integrality.

For 1<=h<L, the penalty term M max(0,j-i-c_h) has density only on the line
j-i=c_h. Remove that line and the main diagonal, accounting for O(n) cells.
Tile the remaining density-index triangle into maximal dyadic squares that
do not cross either line. Using a power-of-two enclosing square and also
splitting at the outer boundary handles arbitrary n. At side length s there
are O(n/s) tiles: their parents intersect one of a constant number of straight
boundaries, each of which meets O(n/s) grid squares at that scale.

On a tile with density indices [a,b) x [c,d), all penalty densities vanish.
Its density sum telescopes to

    R_h(a,d)+R_h(b,c)-R_h(a,c)-R_h(b,d) <= 2hW.

All densities on this tile are nonnegative integers, even though residual
densities on the removed line may be negative. The tile therefore contains
at most min(s^2,2hW) nonzero entries. Summing over dyadic scales gives

    O(sum_s (n/s) min(s^2,2hW)) = O(n sqrt(hW)),

capped by n^2. The geometric sum introduces no extra logarithm. For W=0
only the removed-line entries can remain. Combining early and late layers,
and the n completion entries, yields the uniform bound

    delta(E_h)=O(n+min(n^2,n sqrt(W L))).

This is a bound on intermediate **representation size**, not a density-mass
bound polluted by the arbitrarily large penalty M.

## Computing and reconstructing without a dense table

Gawrychowski, Gorbachev, and Kociumaka (ESA 2025), Theorem 1.2, multiply finite
Monge matrices in time linear in their dimensions plus input core size times
its logarithm. Theorem 4.7 supplies compact witnesses in the same time.
Fact 4.1 supplies logarithmic-time entry queries after core-based preprocessing.

Use those algorithms on the two contiguous submatrices of E_(h-1). For the
next completed matrix, retain the product core strictly above the first
superdiagonal, where the added interval mass has zero density. Recompute
O(n) diagonal and first-superdiagonal entries, discard lower entries, and
recover the top row and left column. Filtering the core and O(n) logarithmic
entry queries take O((n+delta)log(n+1)) work. All steps use compact inputs;
none first enumerates the n^2 entries. Sorting core coordinates if needed is
included in the same bound. The published product also bounds its output
core linearly in the two input cores, so the temporary product is covered.

Keep each layer's witness oracle. From interval (0,n) at layer H, retrieve
its root and recurse on both children at layer H-1. There are n nonempty
calls. An unfinished nonempty interval at layer zero would cost at least M,
but the optimal complete answer is at most LW<M when H>=L. Therefore no
such terminal survives. (The n-step case is complete by depth alone.) This
recovers every original key, with O(n log(n+1)) additional witness work.
The dimensions, representation conversion, and reconstruction are all included
in the stated total bound.

## Evidence and limitations

`code/penalty_layers.py` checks the layer recurrence using dense tables and
counts every state and root candidate. It checks padded min-plus products,
all-root minima, all-shape truncated costs on small cases, exact reconstruction,
the residual bounds, the telescoping identity, and the dyadic tile accounting.
The reference solver is intentionally not presented as a fast implementation.
Source-hashed data is in `results/penalty_layers.json`. The final run passed
1,092 complete solves, 7,972 cubic interval checks, 8,048 all-root cell checks,
792 padded products, 792 all-shape truncated-layer checks, and 139,992 dyadic
tiles. It computed 6,318,862 dense states and 12,381,033 root candidates;
these are diagnostic costs, not the theoretical compact algorithm's costs.

The initial idea of starting from the additive singleton lower bound was
not used for the theorem. A proposed logarithmic convergence proof there
failed: rotations can move an unfinished interval upward and require costly
refinement to restore the specified number of levels. Small passing tests
were not a proof. The large upper penalty avoids that argument entirely.

## Implemented condensed product and exact stopping rule

`core_monge.py` stores a top row, left column, and positive density triples.
Two linear bucket passes order and combine those triples. Selecting submatrices
aggregates their cores and recovers only the required boundary rows/columns.
The product follows the published compression, balanced core split, staircase
merge, and decompression algorithm. Adjacent-entry recomputation scans each
relevant core row or column only a constant number of times per merge.
Leftmost root witnesses are retained through ordinary coordinate maps.
No production operation expands the full matrix into its entries.

`compact_obst.py` implements the penalty layers, finite completion, conversion,
and iterative full-tree reconstruction on those representations. It stops at
H or at an exact fixed point of the **whole condensed table**. The left column
is fixed; equality of the top row and canonical core triples is equality of
the matrix. A fixed point satisfies the original interval recurrence, whose
solution is unique by induction on interval length. Equality of the full cost
alone is not used. The stored finite-layer witnesses still reconstruct a full
tree: any nonempty unfinished terminal would cost M, exceeding the cost of an
optimal tree of height at most H. All charges are nonnegative.

The ordinary witness maps occupy at most O((n+K) log(n+1)) words per product,
where K bounds the input cores. This is one logarithmic factor more than the
published succinct witness bound. Each recursive level takes O(n+K) work,
with dimensions bounded by core size after compression; the core count halves
along a branch. Thus the time bound of the reduction is preserved. These are
algorithmic bounds; a Python dictionary operation is not a machine-instruction
count, and the C++ implementation uses vector buckets for the core.

`compact_obst.cpp` independently implements the same construction using
signed 128-bit integers. It uses constant-size dense product leaves of at
most 64 output cells. Each such leaf costs O(64 times the compressed inner
dimension), plus bounded-many boundary sweeps; this preserves the asymptotic
bound. It does not allocate the full OBST interval table. The benchmark
executable separately runs Knuth, which does allocate that table.
The driver accepts n<=8192 and rejects weights outside a conservative safe
arithmetic domain before running either algorithm:

    W <= (2^120-1)/(16 n^2 (H+2)+16).

These are prototype driver restrictions, not assumptions of the mathematical
reduction. Python uses arbitrary-precision integers.

The matrix harness passed 1,600 random rectangular products, checking 251,779
values and exact leftmost witnesses against dense enumeration, plus 1,600
arbitrary submatrix selections. Three sparse distance-matrix products at
sizes 128, 512, and 2048 each have seven nonzero input and output core entries.
Their nontrivial products are checked by exact queried minima; core visits
stay at 673 while dimension scans grow. This tests real sparse output rather
than only products with an empty core.

The complete Python constructor passed 1,134 solves, including 682 exhaustive
binary-weight inputs (with the two zero-key cases), 838 independent cubic
solves, and 32 controls with fixed-point stopping disabled. The latter include
78 layers checked on every interval, totaling 3,367 exact values and leftmost
root witnesses. Complete reconstructed trees contain 15,544 checked keys.

The C++ sanitizer run passed 1,278 complete solves and 18,248 reconstructed
keys, including 826 cubic comparisons, 12 Python compact comparisons, all
binary weights through n=4, random weights through n=48, geometric and folded
weights through n=64, and zero/one-active-gap controls. Its independent parent
array audit checks inorder validity, unique key coverage, and direct mixed
weighted cost. Three invalid-input tests confirm explicit rejection. No
address- or undefined-behavior sanitizer error was reported.

Release measurements are recorded in `results/compact_cpp_release.json`.
Both algorithms include preprocessing and full-tree reconstruction, use the
same signed-128 arithmetic, and alternate execution order. Instrumented
categories count core traversal, boundary and map slots, candidate evaluation,
and witness work; they are not interchangeable machine instructions or an
exhaustive count of every arithmetic operation. Independent Python audits
are outside the timed regions. Sanitizer timings are not performance evidence.

The release run passed 1,362 full solves and checked 88,904 reconstructed
keys; 1,302 also matched the independent Python Knuth oracle. Every case
matched the separate C++ Knuth implementation. The scaling portion consists
of 90 paired trials (six families, five sizes 128..2048, three trials each).
The compact backend lost **all 90**. At n=2048, medians are:

| Input | Maximum core | Core visits | Compact seconds | Knuth milliseconds | Paired time ratio |
|---|---:|---:|---:|---:|---:|
| Uniform | 20,493 | 69,545,038 | 1.455 | 34.98 | 44.3 |
| Mixed 1--2 | 54,860 | 164,643,682 | 3.236 | 34.41 | 92.4 |
| Mixed 100--102 | 116,104 | 306,935,485 | 5.142 | 27.79 | 185.1 |
| Mixed 1--16 | 78,225 | 260,374,190 | 4.694 | 32.96 | 145.2 |
| Sparse 0--1 | 17,894 | 55,747,535 | 1.417 | 21.88 | 64.8 |
| Alternating | 30,229 | 102,416,246 | 1.959 | 34.35 | 56.2 |

The time-ratio column is the median of paired ratios, not the ratio of medians.
Knuth uses about 4.19 million root candidates and 2,098,176 interval cells
per trial at this size. A core visit is not the same unit as a root-candidate
evaluation. The full counter vectors, including the remaining categories,
are retained. Ordinary witness maps retain 3.68--9.33 million integer slots
across these median fixtures; these are not peak-RSS measurements. Maximum
core counts alone substantially understate implementation work. No crossover
or practical improvement has been demonstrated. The known next costs are
repeated core traversal, allocation, and retained witness maps.

Broad practical performance and priority remain unresolved. This reduction
advances the full mixed-weight objective without asserting that the
unrestricted question is settled.

Primary source:
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.74
