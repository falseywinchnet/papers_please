# Exact contractions retaining key order

Research checkpoint, 2026-10-18. These are independently derived sufficient
conditions; novelty has not been established. They do not establish a general
subquadratic worst-case bound.

## Single-key rule

Let key k have weight p and adjacent gap weights x,y. If both neighboring
keys exist, with weights a,b, the condition

    min(a,b) >= 2p+x+y

guarantees an optimum in which k has two external children. Hence replace
the three entries x,p,y by a gap of weight s=x+p+y and add s to the objective.
The optimum cost changes by exactly s. At the left endpoint it suffices that
the next key has weight at least p+x; at the right endpoint it suffices that
the preceding key has weight at least p+y. The last remaining key is always
contractible.

### Exchange proof

Consider any tree and key k at depth d. If its left subtree contains an
internal node, its greatest key is the immediate predecessor of k; let that
key have weight a and depth d+l, where l>=1. Likewise the successor, when
present in the right subtree, has weight b and depth d+r, r>=1. An absent
internal side corresponds to l=0 or r=0.

If l>=1, move the predecessor into k's position, replacing its original
position by its left child. Insert k as a cherry at the leftmost external
position of k's former right subtree. This preserves inorder order. Other
than k, the predecessor and the two adjacent gaps, no outcome moves deeper;
the predecessor's original left subtree moves up one level. Therefore the
cost change is at most

    -l*a + (r+1)*p + (r-l+1)*x + y.              (1)

The mirrored successor exchange has cost change at most

    -r*b + (l+1)*p + x + (l-r+1)*y.              (2)

If both sides are nonempty and l>=r, substitute a>=2p+x+y in (1). The bound
becomes (r+1-2l)*(p+x)+(1-l)*y <= 0. If r>=l, use (2) symmetrically.
If just one side is nonempty, (1) or (2) is nonpositive under the stated
condition; at an endpoint the weaker endpoint condition suffices.
If neither side is nonempty, k is already a cherry.

Thus an optimum can be changed into an equally good tree containing this
cherry. Contracting a cherry at depth d replaces contribution s*(d+1) by
s*d, subtracting exactly s. Conversely every tree for the contracted input
expands to a feasible tree for the original input at additional cost s.
These two inequalities prove equality of optimum values.

## Linear preprocessing

Maintain a doubly linked list of remaining keys and one current weight and
reconstruction payload for each gap. Initially queue each key. After a
contraction, only the predecessor and successor predicates can change;
queue these two keys. There are at most n initial queue entries and 2n
additional entries. Each predicate and splice takes constant arithmetic
operations. The pass therefore uses O(n) operations and O(n) space.

Solve the remaining m-key instance with Knuth's recurrence and substitute
the saved trees at its external positions. This is an exact O(n+m^2)-time,
O(n+m^2)-space algorithm in the arithmetic-operation model. The worst case
still has m=n. Large integer weights require separate bit-complexity
accounting; arithmetic-operation counts are not bit-operation counts.

The queue order is deterministic but no confluence or minimum-core theorem
is claimed. A failed predicate is not evidence that a key cannot be a leaf
in an optimum.

## Failed weaker condition

The apparently natural threshold min(a,b)>=p+x+y is false. For
p=(24,14,24), q=(1,0,9,0), contracting the middle key would yield cost142,
whereas the unrestricted optimum costs130. Its local mass is23 and both
neighboring key weights are24.

## Initial verification

`code/contract.py` compares full reconstructed trees and costs to an
independent cubic recurrence on 22,143 exhaustive instances with weights
in {0,1,2}, n<=4, and 6,000 seeded random instances through n=20, including
large dynamic ranges and small gap weights. All passed. The benchmark
includes the full contraction pass and records its predicate checks and
queue operations separately from the surviving quadratic table.

## Whole-block rule

For an interval B of k keys including its k+1 gaps, let W be its mass and
C its exact stand-alone optimum cost. If both boundary keys exist and have
weights at least W+C, some optimum contains B as one subtree. For a prefix
or suffix it suffices that the sole boundary key has weight at least C.
Contracting B to a gap of weight W subtracts exactly C from the optimum.

The complete exchange proof is in manuscript/main.tex (Theorem 2). At the
LCA of B's endpoint gaps, remove B's keys from the inward fringes of the
left and right children. Promote the deeper retained boundary key to that
LCA, then insert an optimum for B in the new boundary gap. All other outside
outcomes become no deeper. If the boundary depths relative to the LCA were
l>=r>=1, the boundary saves l*a while the block increase is at most C+r*W.
The condition a>=W+C suffices. With only one retained outside side the block
increase is at most C and promoting its boundary saves at least its weight.

A balanced-tree upper bound C<=W*ceil(log2(k+1)) tests admissibility without
first solving B. The independent block checker verified 19,486 qualifying
contractions across 4,500 random integer inputs through n=16.

## Adaptive selection

`block_contract.py` builds a maximum Cartesian tree on key weights, tests
its proper subtree intervals, and considers the maximal certified intervals
whose sizes are at most b. They are disjoint and separated by surviving keys.
An activation sweep chooses b minimizing the total number of subsequent DP
states, including both the surviving core and the independent block solves.
Integer sizes permit linear-time bucketing; a laminar-family traversal computes
all activation deltas. This is O(n) preprocessing, not an all-interval search.

The final exact bound is O(n+m^2+sum k_t^2). The state count cannot exceed
Knuth's full table, although preprocessing and reconstruction still count.
This minimizes only over size thresholds in the chosen hierarchy, not over
all possible partitions. Random correctness checks: 3,000 through n=20;
small instances additionally compare the sweep against every size threshold.

At n=512 the adaptive scan selected 22 surviving keys on the seeded positive
heavy-separator input, requiring 10,344 DP states including its blocks, versus
131,328 for the full table. Ordinary random mixed weights retained 511 keys.
These preliminary results neither establish a general subquadratic bound nor
a wall-clock speedup. See results/block_contraction_adaptive.json.

## Recursive prototype and bounded overhead

`recursive_contract.py` first performs the single-key pass. It then tries
equality between a directly feasible bisection tree and the order-free
Huffman lower bound. Only equality permits the shortcut. Otherwise it
selects certified blocks and accepts recursive decomposition only if its
total estimated state count is at most three quarters of the full table.
Components with at most eight keys fall back to exact DP after the equality
check. The depth-price relaxation is NOT used by this constructor.

For m>8, an accepted child size s satisfies s(s+1)<=3m(m+1)/4, hence
s<0.92m. The sum of child sizes is m. The recursion therefore has O(log n)
depth and O(n) key occurrences per level. Linear scans and reconstruction
cost O(n log n) in total; the heap-based equality checks cost O(n log^2 n).
If terminal DP sizes are r_t, total work is O(n log^2 n + sum r_t^2),
still O(n^2) in the worst case.

Checks: 3,000 random instances through n=30 against independent cubic DP,
plus 20 nested 383-key instances against Knuth and reconstructed-tree costs.
The nested fixtures reached two decomposition levels. A smaller preliminary
fixture reached only one because the selector flattened it immediately;
the fixture was enlarged to test actual recursive composition.

Matched five-trial Python timings alternate solver order and include complete
construction. At n=1024 the median recursive/Knuth ratio was 0.134 on the
positive heavy-separator family, with median 30,017 DP states versus 524,800.
Random mixed and near-uniform ratios were 0.986 and 1.001, respectively.
At n=512 their ratios were 1.131 and 1.093, showing preprocessing overhead.
These exploratory single-host measurements do not establish superiority
over compiled implementations or the existing Larmore algorithms. Full
counters and timings are in results/recursive_matched.json.
