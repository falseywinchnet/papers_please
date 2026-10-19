# Penalized partial trees and a core-sparse Monge reduction

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. This is a mathematical reduction using an existing sparse
matrix multiplication theorem. The accompanying implementation is a **dense
reference audit**, not an implementation or benchmark of the fast backend.
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

arithmetic operations. Retaining the witnesses uses at most
O(H [n + min(n^2,n sqrt(W L))]) words. In particular **W=O(n) gives
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

The next required implementation step is the actual compact Monge product and
witness path, followed by full-construction operation counts and adversarial
comparisons. Broad practical performance and priority are unresolved. This
reduction advances the full mixed-weight objective without asserting that the
unrestricted question is settled.

Primary source:
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.74
