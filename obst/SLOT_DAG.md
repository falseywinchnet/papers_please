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
