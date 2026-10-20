# Implicit mixed prefix functions with additive decision diagrams

The full mixed slot recurrence can be evaluated on shared binary functions
without enumerating either slots or strict prefix records. This changes the
representation of the general problem: all key and gap weights remain
arbitrary nonnegative exact numbers. The construction returns a complete
optimal tree at the prescribed height. Height n always suffices for an
unrestricted optimum; the existing sufficient-height certificate can select
a smaller height.

Additive edge-valued decision diagrams are established prior work, introduced
by Lai and Sastry and developed subsequently. This implementation uses the
sharing principle described in [Bryant's 1995 paper, Section 7.2](https://www.cs.cmu.edu/~bryant/pubdir/iccad95.pdf).
The OBST-specific work is the exact mixed transition and complete traceback.
The prefix bound and the explicit minimum obstruction below identify what
this representation does and does not provide. No novelty claim is made for
the underlying decision-diagram data structure.

## Representation and exact operations

Addresses have h bits, in most-significant-bit-first order. A reference is
an additive offset and a normalized node. The offset is the minimum finite
value of the represented function. The node stores its level and its two
child references; identical normalized triples are shared. Infinity has a
separate sentinel, while the only finite leaf is zero. Levels are retained
when both children coincide. Induction on the level proves canonicality.

The minimum is the root offset. Each node also stores its exact maximum,
including infinity if any address is infeasible. Pointwise addition factors
out the sum of incoming offsets. Pointwise minimum factors out their common
minimum, while retaining the relative offset in its memoization key. The
relative offset cannot be discarded: the same node pair with different
relative offsets represents different comparisons.

## A proved prefix operation bound

Define PF(b)=min_{a<b} F(a), with PF(0)=infinity. For the two halves L,R,

    P(L || R) = P(L) || min(min(L), P(R)).

Also P(F+c)=P(F)+c, so the normalized version of each input node needs to
be processed only once. Every prefix-minimum function is nonincreasing.
Capping a nonincreasing function by a constant follows at most one boundary
per binary level: a block wholly above the constant becomes constant, and
a block wholly below it is retained. Stored extrema certify both cases.
Thus a cap uses O(h) work, and prefix minima of a D-node diagram use O(hD)
arithmetic operations, node constructions, and dictionary operations.

This is an operation-count theorem. It does not use observed diagram sizes.
Dictionary lookup costs and exact operand bit costs must be included in an
implementation-level complexity model.

## The arbitrary mixed transition and traceback

Normalize the original mixed weights to keys w and residual gaps g by the
existing exact common-gap identity. Put v(b)=nu_2(b) for b>0 and v(0)=0.
Initialize f_0 at zero only. Let M_d be zero on valuation class d and infinite
elsewhere, with slot zero included in class zero. Then

    P_d = P(f_k + M_d),
    f_(k+1)(b) = min_d [P_d(b)-g_k min(d,v(b))-w_k v(b)].

The masks partition exactly the feasible predecessors a<b. This is the
original mixed recurrence, evaluated symbolically. With g_k=0 it simplifies
to P(f_k)-w_k v. Functions of valuation and their masks have small recursive
binary representations.

The work can be bounded before the final minimum merge. A mask has O(h)
nodes and a function of valuation has O(h^2). Addition uses at most the
product of its operands' node counts, because both offsets factor out.
For an incoming D-node function, a zero-gap update therefore costs O(h^3 D).
For a general gap, masking, prefix minima, and reward addition cost
O(h^4 D) per valuation class. The whole update costs O(h^5 D + X), where
X counts the expanded normalized minimum contexts merging the h candidates.
X retains relative offsets and is not bounded by the product of graph sizes.
These are arithmetic and dictionary-operation bounds; the displayed powers
are conservative bounds, not claimed tight exponents.

Store each prefix root. A prefix range [0,b) has at most h complete dyadic
blocks. Read their minima, descend into an attaining block, and compare the
valuation-class gap penalties to recover a predecessor. Repeat for all keys,
then use the previously proved sparse ancestor repair. No perfect-tree
expansion is performed. All output order, depths, gaps, and costs are checked
independently in the audit.

## Why generic monotone minimum is insufficient

There is no polynomial bound for general minimum in terms of the sizes of
its operand diagrams, even when both functions are strictly decreasing.
This statement is for the fixed address order, not all variable orders.

Let h=2m, N=2^m, and b=NX+Y with 0<=X,Y<N. Set

    F(b)=-2b+X,  G(b)=-2b+Y.

Each is a weighted sum of individual bits and has exactly 2m+1 nodes in
this representation. F decreases by either 2 or 1 on the next address.
G decreases by 1 inside a low-bit block and by N+1 across its boundary.
Their minimum is H(b)=-2b+min(X,Y).

After fixing the high bits X=x and removing the minimum of the residual,
the low-bit function becomes

    H_x(Y)=2(N-1)-2Y+min(x,Y)-x.

Its consecutive differences are -1 before Y=x and -2 thereafter. All N
normalized residual functions are distinct, so the result needs 2^m
nodes at level m. In fact its complete size is exactly 3*2^m-2. At a
remaining low-bit level d, the only shape parameter is the clipped kink
position, giving exactly 2^d nodes. These lower levels total 2^(m+1)-2.
Each upper prefix stays distinct after setting the remaining high bits to
zero, giving 2^m-1 upper nodes. One terminal completes the count. Small operands and monotonicity therefore do not
control a generic minimum. These particular functions have not been
realized as OBST prefix transitions; the structural question for the actual
mixed recurrence remains open.

## Verification and next obligation

The audit compares every small prefix value with a direct all-predecessor
recurrence, and each optimum with the original all-root height recurrence.
Complete geometric controls compare with the proved unique-chain formula
and independent ordinary Knuth. A separate probe checks arbitrary prefix
functions, the explicit monotone minimum obstruction, and complete mixed
instances at certified sufficient heights.

The implementation reports every intermediate node, every recursive operation,
and final and history sizes separately. The initial version passed its small
correctness audit but explored many redundant minimum contexts on larger
geometric inputs; that run was deliberately interrupted. Exact range pruning
implements the proved prefix bound. All final counters belong to the pruned
version, and source hashes identify the executed code. Timings are not used.

A compact final diagram alone is not a construction-time bound. The next
necessary result is control of the particular normalized minimum contexts
created by mixed OBST, or a representation that avoids those contexts. The
new theorem rules out relying on monotonicity alone for that step.

## Endpoint dominance and one-path predecessor queries

Actual mixed prefix functions satisfy a stronger endpoint relation: if
1 <= a <= c and v(a) <= v(c), then f_k(c) <= f_k(a). Move only the last
selected key to c. Its key reward and preceding-gap reward cannot decrease.
This argument uses nonnegative weights on both kinds of outcomes.

Write b-1 as a sum of powers of two in descending order. Its successive
partial sums are a skyline S(b), together with slot zero. Every positive
a<b lies between two successive partial sums and is dominated by the right
endpoint: that endpoint is later and has greater or equal valuation. Thus,
for every nonnegative prospective gap g,

    min_(a<b) [f_k(a)-g min(v(a),v(b))]
      = min_(a in S(b)) [f_k(a)-g min(v(a),v(b))].

Store the value at local address zero in each normalized diagram node.
It is the left child's first-address value plus its edge offset, with
infinity propagated. This costs one value and constant work per created node.
Walk the bits of b-1 from most to least significant. Each 1-bit enters a
right child whose first address is the next skyline point; its valuation
is the bit position. The cached first-address value supplies its candidate
cost in constant work. The entire query takes O(h) arithmetic/address
operations and creates no nodes. The sentinel b=2^h with g=0 also finds
a global optimum. Ties choose an attaining skyline point, which need not
be the globally earliest minimizer.

The complete constructor in `code/slot_dag_skyline.py` uses this query for
all n slot choices, giving O(nh) slot traceback with exactly nh path steps
in the implementation and no new diagrams. It retains the previous forward
recurrence and subsequent sparse tree repair. Intermediate diagram sizes
and forward minimum contexts are still the unresolved general bound.

## Directed size searches

`slot_dag_size_search.py` evaluates actual mixed prefix functions at h=n,
independently normalizes every dyadic block, and maximizes the largest
reachable diagram across all stages. It explores shuffled geometric key
weights, geometric gaps, and local weight/swap mutations. Each candidate's
full optimum has an independent Knuth check; each size winner has every
prefix value checked against the implicit constructor. Height n is always
sufficient but need not be necessary on these unrestricted search inputs.

`slot_dag_chain_search.py` separately enforces necessary height n. With
A=8(n+1)^2, choose arbitrary integer coefficients alpha_i,beta_j in [1,n]
and set p_i=alpha_i A^(n-i), q_j=beta_j A^max(0,n-j-1), using zero-based
indices. For every suffix i, p_i exceeds n times all its other outcome
weights. Indeed, with r=n-i, the latter mass R is below
2n A^r/(A-1)+n, so nR/p_i < 3n^2/(A-1) < 1. A tree with another root
costs at least 2p_i, whereas the right chain costs at most p_i+nR.
Recursing forces the unique full right chain. This supplies a proved
height certificate for every coefficient mutation, independently of search.

The finite search results and verification counts are recorded in the
manuscript appendix and source-hashed JSON. They do not establish a size
exponent. In particular, neither search proves a general upper bound or
realizes the earlier exponential generic-minimum example as an OBST update.
