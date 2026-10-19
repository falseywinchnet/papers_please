# The missing ordering constraint and an arbitrary-window obstruction

This continues the full mixed-weight investigation. It excludes a proposed
repair to the depth-price relaxation; it is **not** a lower bound on the
complexity of general OBST construction. The next exact approach must retain
nonlocal ordering information. Novelty of the results below is unestablished.

## Exact characterization

Use the lengths, gap formula, and level-flow equations in DEPTH_DUAL.md.
Call a length sequence ranked when every nonempty contiguous interval has
a unique minimum. This is the standard vertex-ranking condition on a path
with label order reversed: equal labels must have a smaller label between
them. Vertex ranking and its bounded-path variants are existing notions;
see McDonald (2015), https://arxiv.org/abs/1401.2669, and Bose et al. (2022),
https://arxiv.org/abs/2007.06455. We do not claim to introduce that condition.

**Proposition.** A sequence l in {1,...,n}^n is the inorder
key-comparison-length sequence of a BST if and only if it is ranked and
satisfies K_1=1 and every level-flow equality.

Necessity follows from the unique shallowest key in each inorder interval
and the two children of every internal node. For sufficiency, after deleting
all labels at most d, let U_d be the number of nonempty remaining runs, and
let A_d be the number of deleted labels. Let G_(<=d) count gap lengths at
most d, using g_i=max(l_(i-1),l_i), with the endpoint convention.

Counting adjacent deleted pairs and deleted endpoints gives

    G_(<=d) = A_d + 1 - U_d.

For example, if deleted labels form R runs and e endpoints are deleted,
the two sides are A_d-R+e and A_d+1-(R+1-e), respectively. Summing the
level-flow equations from 1 through d gives

    G_(<=d) = A_d + 1 - K_(d+1).

Thus U_d=K_(d+1). Ranking permits at most one label d+1 in each remaining
run, so equality forces exactly one. At d=0, K_1=1 supplies the root;
inductively every nonempty surviving interval receives its root at the
next level. This constructs the required BST with exactly the supplied
lengths. The empty-input case is handled separately.

Ranking itself has a linear recognizer. Scan left to right with a strictly
increasing stack: pop larger labels, reject an equal top, and otherwise
push the new label. An equal top witnesses equal endpoints with no smaller
label between them. Conversely, any such pair survives on the stack until
its second endpoint. Each label is pushed once and popped at most once.
The flow counts can also be checked in linear time when labels lie in 1..n.
Cheap recognition does not establish cheap minimization over all sequences.

## A positive-weight obstruction for every window width

Fix any integer w>=2. Enforce ranking on **every interval containing at
most w keys**, as well as exact global level flow and a unique length1
root. These requirements are still insufficient, even with a constant
relative cost gap on strictly positive weights.
Equivalently, at every n>=5 the construction passes all intervals of up to
n-3 keys; the limitation is not restricted to very small constant windows.

Take n=w+3 keys and the inadmissible sequence

    l = (3, 1, 2, 3, 4, ..., w+1, 2).

The middle ascending part contains w-1 entries. The two length2 entries
enclose w+1 keys, and this is the only interval with a repeated minimum.
Every window of at most w keys therefore passes. Direct substitution into
the gap formula verifies every level-flow equation and K_1=1. The sequence
cannot describe a BST: the unique root is key1, its singleton left subtree
has length3, and two keys on its right both claim length2.

Give every gap weight1. Give keys 1, 2, and n-1 weights 3B, B, and B,
respectively, and every other key weight1. Let

    E = sum of the unit-weight contributions in this sequence
      = w^2 + 4w + 10.

Its claimed cost is C_false=7B+E. Every actual BST costs at least 8B:

- If key1 is the root, the two B-weight keys both lie in its right subtree.
  At most one has comparison length2; their lengths sum to at least5.
  The three heavy keys alone therefore cost at least 3B+5B=8B.
- If another key is the root, key1 has length at least2. Each B-weight
  key has length at least1, giving at least 6B+2B=8B.

Choose B=tE for any integer t>=2. The inadmissible sequence costs less than
every actual tree, satisfies all the enforced constraints, and has zero
penalty for every choice of level-flow prices. Thus any such priced bound L
satisfies

    L <= 7B+E <= (7/8 + 1/(8t)) OPT.

In particular t=16 gives L <= (113/128) OPT, for **every** w. Taking larger
t makes the ratio approach 7/8 from above. Increasing a fixed window or
spending more time optimizing prices cannot make this family a universally
exact certificate. This result concerns the stated window-minimum and
level-flow relaxation; it does not exclude other local constraints,
adaptive nonlocal cuts, or a faster exact algorithm using a different state.

## Fixing finitely many top levels does not remove the obstruction

The same strict gap can be buried under an arbitrarily long, genuinely
optimal prefix. Suppose the current instance has mass W and a feasible
tree of cost U. Prepend a new key of weight A=W+U+2 and a new leftmost gap
of weight1. A tree with the new key as root and the feasible old tree on
its right costs A+1+W+U=2A-1. Every tree with another root costs at least
2A from the new key alone. Thus every optimum has the new root, and

    OPT_new = A+1+W+OPT_old.

Transform the invalid sequence to (1,l_0+1,...,l_(n-1)+1). Its cost changes
by the same additive amount A+1+W; its flow remains zero and its local
window property is preserved. Repeat D times. The first D keys now form
the unique optimal top-D right-chain prefix, with an empty left child at
every level. The invalid sequence agrees with that prefix and still has
the original strict cost gap below it.

Therefore even supplying the true first D levels, for any fixed D, does
not turn the window/flow relaxation of the remaining part into an exact
bound. The constant relative gap above is **not** claimed after this
embedding: the forcing weights add a potentially large common cost.
This also does not contradict algorithms that solve the remaining pieces
exactly rather than using this relaxation on them.

## Exact verification

`code/depth_order.py` compares the characterization against independently
generated binary-tree shapes on every sequence in {1,...,n}^n for n=1..7:
873,612 sequences in total. It separately compares the linear stack
recognizer against a direct all-interval scan. The accepted sets have
1, 2, 5, 14, 42, 132, and 429 members, exactly the tree-shape sets.

Width3 plus flow already permits four invalid sequences at n=6 and 34 at
n=7. The family above is checked for all 127 widths w=2..128 at t=16,
including the exact cost identity, zero violations, window validity,
nonvalidity globally, and the universal lower bound. Knuth and a direct
tree evaluator check every witness; the independent cubic DP also checks
w<=24. Full integer results are in `results/depth_order.json`.
An additional 120 instances combine widths2..16 with forced prefix depths
1..8. The forcing weights are computed from a feasible right-chain cost,
not an optimum. Cubic DP, Knuth, direct cost evaluation, and inspection of
the optimal prefix verify the exact additive identity and preserved gap.

The proof identifies why the proposed bounded-window extension cannot close
the structural gap. We therefore do not invest in its larger DP before
addressing nonlocal constraints. The full mixed-weight subquadratic objective
remains open in this investigation.
