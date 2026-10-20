# An order-free mixed-weight relaxation

This is an elementary extension of Huffman's contraction proof. Novelty is not
claimed. It is a candidate lower-bound component for exact full OBST search.

## Lemma

Given n nonnegative internal weights P and n+1 nonnegative external weights Q,
allow arbitrary assignments within each node type and arbitrary full binary
tree shape. Charge internal weights at depth+1 and external weights at depth.
An optimum is obtained by repeatedly combining the two smallest current
external weights a,b beneath the smallest remaining internal weight p,
replacing them with external weight a+b+p, and adding a+b+p to the cost.

## Proof

Choose a deepest internal node v of an optimal tree. Its children are leaves.
Among internal nodes, moving a minimum internal weight to v by swapping labels
cannot increase cost. Independently, the two minimum external weights can be
swapped into v's children without increasing cost. This uses only maximal depth
and nonnegative differences; ties do not matter. These swaps preserve the full
tree shape and the internal/external types.

Contract this cherry into a leaf of weight s=a+b+p. If v was at depth d, the
three removed contributions were p(d+1)+a(d+1)+b(d+1)=s*d+s.
The new leaf contributes s*d, so contraction subtracts exactly s. All other
contributions are unchanged. The contracted tree must be optimal for the
reduced multisets, otherwise an improved reduced tree could be expanded to
improve the original. Induction proves the algorithm. The zero-internal-node
base case has one leaf at depth zero and cost zero.

Sorting P and maintaining Q in a heap costs O(n log n) comparisons and O(n)
space. A sorted two-queue implementation may reduce constants because generated
weights are nondecreasing (to be checked and stated separately).

## Relation to full OBST

Every admissible BST is feasible in this relaxation, hence its optimum is a
valid lower bound for the ordered problem with the same p and q. Equality
between this bound and the directly evaluated cost of a feasible BST certifies
global optimality in O(n log n) time. Equality is not guaranteed, and failure to
match the bound does not disprove optimality.

Applying this bound separately to the two sides of a candidate root gives a
valid pruning rule in a demand-driven exact interval solver. The cost of
constructing all lower bounds must be included; reducing the number of exact
DP states alone does not prove a faster algorithm.

## Initial evidence

`research.py` independently enumerates all tree depth profiles and uses the
rearrangement inequality to optimize each shape's labels. The relaxation agrees
with this oracle on 22,143 exhaustive small ternary-weight instances and 2,700
seeded random instances up to n=9. It is also bounded above by cubic/Knuth OBST
costs. See `results/initial.json` for reproducible counts and the bound survey.

## Two rejected local certificates

All weights in these counterexamples are positive. Keys are zero-based.

1. Single-rotation local optimality is insufficient: p=(3,5,18),
   q=(13,14,4,8). Tree 2(0(nil,1),nil) costs 127, every one-rotation neighbor
   costs at least 134, but the balanced tree 1(0,2) costs 125.
2. Promoting any descendant to the root of any existing subtree is also
   insufficient: p=(18,8,18), q=(17,11,1,13). Tree 1(0,2) costs 164,
   every distinct promotion neighbor costs at least 169, but
   0(nil,2(1,nil)) costs 157.

These are barriers to those specific local certificates, not complexity lower
bounds for the full problem.

## Sparse solver failure and quadrangle counterexample

The exact solver in `code/sparse.py` was correct on 900 independent cubic
checks and 104 benchmark cases, but its general performance was poor. At
n=128 random inputs, it visited roughly 4,300--4,600 exact intervals versus
Knuth's 8,256, yet spent about 3.9--4.1 million comparisons constructing
bounds and examined over 100,000 candidate roots. Counting only exact
intervals would have hidden this failure. Uniform and monotone geometric
instances were certified immediately. Folded geometric and gap-spike
instances still required quadratic contraction work for their bounds.

The lower-bound interval matrix H does not satisfy the quadrangle inequality.
For p=(9,1,12), q=(5,1,18,10), half-open intervals give

    H(1,2)+H(2,3)=60 > 54=H(1,3)+H(2,2).

Thus Knuth/Yao-style matrix optimization cannot simply be transferred to H.
