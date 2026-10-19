# Exact mixed-weight ruler slots and a capacity-deficit dynamic program

Let h be a prescribed height, c=2^h-1 its perfect-tree capacity, and
r=c-n>=0. An exact full mixed-weight optimum among trees of height at most h
can be constructed in **O(n(r+1)) arithmetic operations and words**, including
reconstruction. No restriction on weight amplitudes is used. This is a
height-limited component of the full research program; selecting a height
alone does not certify unrestricted optimality.

## Exact representation, including every gap

Use one-based keys p_1,...,p_n in this note, gaps q_0,...,q_n, and
v(t)=nu_2(t) for perfect-tree slots t=1,...,c. Slot t has comparison length
ell(t)=h-v(t). For any increasing slot sequence t_1<...<t_n, define

    F(t) = sum_i p_i ell(t_i)
         + q_0 ell(t_1) + q_n ell(t_n)
         + sum_{i=1}^{n-1} q_i max(ell(t_i),ell(t_(i+1))).

Then the height-limited optimum equals min_t F(t), with no ancestor-closure
constraint on the chosen slots. Equivalently it equals hW minus the maximum
of

    sum_i p_i v(t_i) + q_0 v(t_1) + q_n v(t_n)
      + sum_{i=1}^{n-1} q_i min(v(t_i),v(t_(i+1))).

The adjacent-gap depth identity is Becker's Lemma 1 in
[Optimal Binary Search Trees with Near Minimal Height](https://arxiv.org/html/1011.1337v1).
The endpoint gap depths equal the comparison lengths of the first and last
keys. Becker also gives a quadratic algorithm for a height bound within a
fixed additive constant of the minimum height. The representation here makes
the unused-slot parameter explicit; when r=Theta(n), its bound is quadratic.

Proof of exactness: any height-at-most-h tree embeds as an ancestor-closed
subset of the perfect tree, so it occurs among the slot candidates with its
exact mixed cost. Conversely start with any selected slots and delete every
unselected key from the perfect BST by ordinary successor deletion. A surviving
key's depth never increases. Since a gap's depth is the maximum comparison
length of its surviving neighboring keys (with the endpoint convention), its
cost also cannot increase. The resulting n-key BST has height at most h and
cost at most F(t). Nonnegativity gives both inequalities between the minima.
This extends the earlier key-only slot argument by retaining the pairwise gap
terms; dropping those terms is not a valid mixed-weight representation.

## Unused-slot states

Every increasing selection can uniquely be written t_i=i+y_i, where

    0<=y_1<=...<=y_n<=r.

Let D_i(y) be the maximum prefix reward ending at y_i=y, including gaps
q_0,...,q_(i-1). Then

    D_1(y)=(p_1+q_0)v(1+y),
    D_i(y)=p_i v(i+y)+max_{0<=z<=y}
               [D_(i-1)(z)+q_(i-1) min(v(i-1+z),v(i+y))].

The final score is max_y [D_n(y)+q_n v(n+y)]. There are exactly n(r+1)
states. Direct transitions would square the slack; the ruler structure
removes that additional factor.

## Linear work per state, amortized over the whole table

In row i, sweep y increasingly, inserting predecessor z=y. Maintain

    B_d=max{D_(i-1)(z): z<=y, v(i-1+z)=d},
    S_e=max_{d>=e} B_d.

Keep an attaining predecessor with each maximum. Inserting a predecessor
of valuation d updates B_d and S_0,...,S_d. For e=v(i+y), the transition is

    max( max_{d<e}(B_d+q_(i-1)d), S_e+q_(i-1)e ).

Scan the e lower levels and query S_e once. The cost at this state is
O(1+v(i-1+y)+v(i+y)). Generation tags clear the level arrays logically
between rows, avoiding an O(h) initialization per row.

Each slot index occurs at most min(n,r+1) times among all i+y. Also

    sum_{t=1}^c v(t)=c-h<c,
    min(n,r+1)c <=2n(r+1).

The latter follows by splitting r+1<=n and r+1>n. Hence all level scans
and suffix updates total O(n(r+1)). Tabulating v, allocating level arrays,
initializing the first row, and choosing the last state fit the same bound,
because c=n+r<=n(r+1). This proves the arithmetic operation count without
assuming uniform work per row or omitting array resets.

## Full reconstruction

Store one predecessor per state and trace back the selected slots. Build the
perfect c-key tree with parent/child pointers, predecessor/successor threads,
and a location array for each original slot label. Delete unselected labels
in increasing order. For a node with two children, its threaded successor
is available in constant time: copy that successor's label into the node,
update the location array, and splice out the successor. Other deletions
splice out the node directly. Every deletion changes only a constant number
of pointers. Thus construction, c-n deletions, and output take O(c+n),
within O(n(r+1)). The concrete implementation uses arrays throughout this
step, including selected-slot membership, rather than a hashing assumption.

The coordinatewise depth argument above applies to this exact procedure.
When the slot sequence minimizes F, the repaired tree must attain the same
cost: any strict decrease would contradict equality of the two minima.

## The complementary terminal-penalty regime

For an interval with n>=c and penalty M>hW, the maximum-exposure argument
forces exactly c exposed keys. Their skeleton is perfect, and every gap
reaches a terminal at depth h. Therefore

    A_h(0,n)=M(n-c)+hW
             -max_{1<=t_1<...<t_c<=n} sum_{j=1}^c p_(t_j) v(j).

At n=c both slot formulas agree: neighboring ruler valuations have minimum
zero, and the endpoint valuations are zero. Above capacity, all gap weights
occur solely in the additive hW term. Consequently a density cell strictly
above j-i=c, whose four intervals all have at least c keys, is independent
of gap weights. A change in the global penalty also cancels there because
its length term is affine. This isolates the mixed interaction below the
capacity boundary without deleting the gaps from the problem.

## Independent audit and scope

`check_mixed_slots.py` compares the constructor against an independent
all-root height recurrence and literal slot/tree enumeration. It tests the
repair map on every nonempty slot subset through h=4 (32902 subsets).
All costs, reconstructed heights, and coordinatewise depth bounds are checked.
Additional tests compare the above-capacity formula and its gap-independent
densities with independently generated full mixed penalty layers.

Scale rows use arbitrary positive mixed weights with large integer baselines
through capacity 4095 and count every DP state, level scan, suffix update,
traceback step, and reconstruction node. Larger rows check the recovered tree
and slot objective; only rows explicitly marked as independent controls also
run the all-root interval recurrence. Exact source hashes and counts are in
`results/mixed_slots.json`. No wall-clock timing is used.

The implementation entry point is `solve(p, q, h)` in `code/mixed_slots.py`,
using the repository's zero-based key array. It returns the cost, complete
tree, selected slots, height limit, and capacity deficit. `None` means the
height has insufficient capacity.
