# Exact coarse-regret screening for arbitrary mixed weights

A coarse cost table can screen roots for every arbitrary nonnegative original
input, including inputs that fail the earlier small-error certificate. The
new allowance preserves at least one full original optimum. A hierarchy of
compressed root-range products enumerates qualifying roots without scanning
all positions between their extremes. Its preparation has a proved bound;
the number of surviving intervals and roots remains input-dependent.

The manuscript gives the self-contained statements and proofs under
“Screening roots by coarse cost and height.” The main bounded-mass Monge
result remains the lead theorem. The general arbitrary-weight subquadratic
objective remains open.

## Signed regret bound

Let a be any nonnegative integer coarse key/gap weights, x any nonnegative
original weights, and delta>0. On interval I=[i,j), let m=j-i and include all
its keys and both endpoint gaps. Define

    Eplus(I)  = sum max(x-delta*a, 0)
    Eminus(I) = sum max(delta*a-x, 0)
    eta(I) = (min(m,Hc)-1)*Eplus(I) + (min(m,Hf)-1)*Eminus(I).

Hf bounds the height of some full original optimum. Hc bounds an attaining
coarse optimum on every interval, as supplied by the completed coarse layers.
Retain every valid root r satisfying

    Cbar(i,r)+Cbar(r+1,j)+Wbar(i,j) <= Cbar(i,j)+eta(I)/delta.

Choose an original optimum of height at most Hf and compare each of its
subtrees with a coarse-optimal tree of height at most min(m,Hc). Every
outcome comparison length in a nonempty interval is at least one. Positive
errors can increase the latter tree's error cost by at most Hc-1 per unit;
negative errors can increase the difference by at most Hf-1 per unit, with
both heights capped by m. Original optimality bounds coarse regret by eta.
The least coarse cost with the original subtree's root is smaller still.
Thus that root survives at every subtree of the chosen full optimum.

No closeness condition is needed. The screen can exclude tall tied original
optima; existence of one surviving full optimum suffices. Every reached
interval also retains a coarse-optimal root, so the grammar is feasible.
Evaluate the original recurrence over retained roots and reconstruct a full
tree. Its original cost is exactly optimal.

## Root-range index and complete work bound

For a finite square Monge matrix C of order n+1 and core size K, build a
balanced binary hierarchy of root ranges I. Each node stores

    D_I(i,j) = min over r in I of C(i,r)+C(r+1,j).

In the first factor keep only outer row changes touched by densities whose
column is internal to I; in the second keep outer column changes touched by
densities whose row is internal to I+1. All other rows/columns differ by
root-independent offsets, recovered from the original matrix. This avoids
an n-entry outer boundary at each node.

At a fixed hierarchy depth, each density occurs in at most one first-factor
range and one second-factor range. Total inner dimensions are at most n,
and total assigned core entries at most 2K. Splitting drops crossing inner
densities instead of copying them. The published condensed-Monge product
core bound and persistent entry indexes give O((n+K)L^2) preparation and
space, where L=ceil(log2(n+1)). Each range-minimum query takes O(L).

Pruning by a threshold enumerates a qualifying roots in any valid contiguous
root range in O((a+1)L^2). Visited nodes charge to the emitted leaves'
ancestors, pruned siblings and two boundary paths. Interrupted prefixes have
the same bound with emitted roots plus one.

If the coarse construction has aggregate parameter Sbar, total preparation is

    O(Sbar*L + (n+K)*L^2).

For V reached nonempty intervals and A retained root choices, a complete
original query, including height selection, error prefixes, expansion,
original recurrence and full traceback, takes

    O(n*L + (V+A)*L^2).

Retained index and query space is O((n+K)L^2+V+A). Ordinary coarse witness
maps add O(Sbar*L) during preparation. The same prepared index supports
unrelated fine inputs and any positive delta. Balanced dictionaries support
the deterministic comparison bound; the Python implementation counts
explicit dictionary-access events. Arithmetic bounds exclude operand bit
costs and instrumentation events are not machine instructions.

## Automatic route and its remaining boundary

Set b=L^3, delta=max(x)/b, and round each outcome to the nearest multiple of
delta. Coarse total mass is at most (2n+1)L^3. The final completed core has
K <= n+L*Wbar by telescoping positive integral density mass. This bound is
for the final core; the earlier odd-ramp obstruction for intermediate layers
is unaffected. Together with the aggregate theorem and H=O(L), preparation
costs O(n^(3/2)*L^3+n*L^7)=o(n^2).

Check a budget of 4*n*L before each reached-state and retained-root charge.
A successful or interrupted screening attempt costs O(n*L^3). On exhaustion,
run ordinary Knuth on the original input and include all failed work in the
counts. The constructor is exact for every input, has subquadratic complete
work when screening finishes within budget, and O(n^2) global worst-case
work. Uniform key and gap sequences have a direct linear construction.

The surviving grammar can still be dense: zero-regret coarse-optimal roots
always survive. The earlier uniform coarse family supplies quadratic states
and cubic rules if expansion is unbounded. A universal sparse-screen theorem
has not been established.

## Independent checks and measured limits

The harness establishes the signed subtree inclusion before importing the
constructor. Sixty generic finite Monge matrices with signed boundaries
support 130,020 dense range-minimum comparisons and 17,940 threshold-set
checks, including partial valid ranges and non-power-of-two orders. It checks
per-depth charges, product-core sizes, index allocation and inner dimensions.

The main audit includes 540 subtree inclusions, 108 complete original solves,
1,980 exact root sets and independent direct threshold formulas, 72 literal
controls evaluating 2,352 tree costs, and 108 zero-budget fallbacks. Ninety-six
supplied coarse-base/scale pairs fail the older certificate but refine
exactly. Fifteen random, near-uniform and geometric cases through n=256,
four dense uniform-face controls, five rational cases, three unrelated reused
queries and twenty uniform/empty cases retain complete original optima.

A separate matched experiment uses four unstructured positive inputs with
256-bit weights at n=32,64,128,256, each run at b=1,16,L^2,L^3 against the
same independent Knuth optimum. Default b=L^3 finishes screening at every
size; b=L^2 finishes only at n=32, while b=1,16 always exhaust the budget.
At n=256 the default has V=1,029 and A=1,311, but preparation alone records
17,521,921 core visits and screening 14,244 range-minimum calls. The reference
Knuth solve tests 66,070 roots. These different event categories do not
establish a practical speedup; the preparation cost is substantial.

The records retain exact inputs, scales, costs, complete counters and seventeen
source-hash entries. Reproduce with the root AGENTS.md commands. Sources are
`code/root_ranges.py`, `code/coarse_screen.py`, `code/coarse_screen_audit.py`
and `code/coarse_screen_scale.py`; both audit JSON files are in `results/`.
The index uses the already cited published core-sparse product primitive.
No priority claim is made for generic coarse rounding or root pruning.
