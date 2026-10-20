# A sufficient height after setting aside heavy outcomes

The rotation inequalities give a height bound that depends on the mass left
after removing a chosen number of outcomes from the accounting. No weight is
removed from the optimization. Combining this bound with the mixed prefix
vectors gives an unrestricted exact constructor with a subquadratic guarantee
for bounded positive key backgrounds, few runs, and few exceptional weights.

## Height theorem, including zero weights

Consider arbitrary nonnegative key and gap weights on n>=1 keys, with total
mass W>0. Let

    mu = min {p_i+q_i+q_(i+1) : p_i+q_i+q_(i+1)>0},
    z  = longest consecutive run of indices with p_i=q_i=q_(i+1)=0,
    ell = ceil(log2(z+1)),
    tau(V) = min {j>=0 : F_(j+1)*mu>V},  F_1=F_2=1.

Every positive-mass internal subtree has mass at least mu. Indeed, any
positive outcome in a nonempty interval belongs to a positive singleton
interval contained in it: use that key for a key outcome and an adjacent
key inside the interval for a gap outcome. Conversely, a singleton attaining
mu is a possible internal subtree. An all-zero interval has at most z keys.

Mark any k outcomes, keeping their weights unchanged, and let V be the total
weight of the unmarked outcomes. Define

    P = tau(W)                    if k=0,
    P = tau(V)+k+1                if k>=1.

Every positive-mass internal subtree in EVERY optimal tree has root depth
less than P. There exists an optimal tree of height at most

    min(n, P+ell).                                                (1)

Here height counts internal vertices along a root-to-gap path. When W=0,
a minimum-height balanced tree is optimal directly.

### Proof by disjoint mass increments

Fix a positive internal subtree S at depth d. Ascend from S to the root,
calling the successive subtree masses A_0,...,A_d. The straight and bent
rotations already proved in the mixed mass lemma give

    A_j >= F_(j+1)*mu,
    B_i := A_i-A_(i-1) >= A_(i-2)  for 2<=i<=d.                  (2)

B_i consists of the new ancestor key and its off-path sibling subtree.
These outcome sets are pairwise disjoint, and disjoint from every earlier
A_j when i>j. External gaps are individual outcomes in this partition;
none is counted twice.

For k=0, A_d<=W gives d<tau(W). For k>=1, if d<tau(V), the asserted
bound already holds. Otherwise let j be the FIRST index with A_j>V.
It exists and j<=tau(V). The subtree A_j contains a marked outcome,
since all unmarked outcomes together weigh only V. For every i>=j+2,
(2) gives B_i>=A_(i-2)>=A_j>V. Each such disjoint B_i therefore contains
another marked outcome. If d>=j+1, counting them gives k>=d-j; if d=j,
the same inequality is automatic. Hence d<=j+k<=tau(V)+k, proving P.
The single increment B_(j+1) is deliberately uncharged: its lower bound
only involves A_(j-1), which may be at most V.

Replace each maximal zero-mass subtree by a balanced tree on its own keys.
This preserves cost and every positive outcome depth. Its height is at
most ell, and it attaches below a positive internal node. Thus (1) follows.
If z=0 there is no extra term. The proof applies to any marked set, with
no dominance, separation, strict positivity, or integer-weight assumption.

The Fibonacci rotation method itself is prior work; this argument uses the
explicit sufficient mixed-weight version in the paper. Its contribution is
the disjoint accounting after the first mass crossing, not a transferred
sharp Fibonacci constant.

The SAME global height bound works for every contiguous input interval.
Its marked set has size at most k, its unmarked mass at most V, its smallest
positive singleton mass at least mu, and its longest zero interval at most z.
If its marked set is empty, use the stronger k=0 case locally; all-zero
intervals are balanced directly. Thus the selected height may also replace
the sufficient global budget in the terminal-penalty iteration, with its
finite penalty recomputed for that budget. This applies on whichever fixed
nonnegative instance, original or normalized, the iteration is run.

## Select the best bound in O(n log n)

For a fixed k, the k largest outcome weights minimize V and hence tau(V).
Sort all positive outcome weights and scan their suffix masses V_k. Retain
the smallest bound (1), including k=0. Ties may be broken arbitrarily.
Compute mu and z in one scan. Precompute mu F_(j+1) only until it exceeds
W or j=n, whichever happens first. Its last entry is at most 2W, and its
length is O(n). The index tau(V_k), truncated at n, only decreases, so all
index decrements take O(n) work. Truncating at n cannot improve a bound
below n incorrectly: such a candidate was already no better than the trivial
height n. Sorting dominates at O(n log n) comparisons; storage is O(n).

The selector uses exact comparisons, not floating-point logarithms. It
does not construct Fibonacci integers with an irrelevant exponential tail.
For integer weights, these height-selection intermediates have O(log(W+1))
bits. The full arithmetic bound still does not assert bit complexity for
unbounded input integers or rational denominators.

## Full mixed construction

Apply the established common-internal-gap normalization first:
b=min(q_1,...,q_(n-1)), endpoint keys w_0=p_0+q_0 and
w_(n-1)=p_(n-1)+q_n, interior keys w_i=p_i+b, internal gaps g_i=q_i-b,
and zero endpoint gaps. Original cost equals transformed cost plus bn for
EVERY tree. Thus the height bound on (w,g) guarantees an original optimum
at that height. The n=1 case is direct.

Let h be the selected sufficient height, c=2^h-1, r the number of constant
runs in w, and e the number of positive internal g_i. The prefix-vector
constructor now returns an UNRESTRICTED optimum in

    O(n log(n+1) + (r+e)c log(c+1)) work,
    O(n+(r+e)c) words.                                          (3)

All original weights and all output keys are retained. There is no posterior
certificate failure. With R_2 long-run passes and S_1 singleton passes, the
more precise kernel work is n+c(1+h R_2+S_1). Compare that work proxy with
n^2 before allocating a slot array. Choosing Knuth when the proxy is larger
gives O(n log(n+1)+min(n^2,c(1+h R_2+S_1))) work and quadratic worst-case
space. The selected vector kernel retains its O(n+c(1+R_2+S_1)) space bound.
This is an asymptotic work selector, not a prediction of elapsed time.

## A magnitude-independent subquadratic family

Put phi=(1+sqrt(5))/2 and alpha=log_phi(2), approximately 1.44042.
For any marked set of k>=1 outcomes with unmarked mass V,

    tau(V) <= 2+ceil(log_phi(1+V/mu)),
    2^h = O(2^(k+ell) * (1+V/mu)^alpha).                       (4)

The corresponding estimate for k=0 is at least as good. This follows
directly from F_(j+1)>=phi^(j-1), not from empirical heights.

For a concrete full mixed family, suppose the normalized keys are all at
least a>0. Apart from s exceptional keys of unrestricted size, they lie
in [a,Ca] for a fixed C. Suppose there are r_0 constant runs before those
s keys are replaced, and only e positive residual gap weights, of arbitrary
size. Mark the s exceptional keys and those e gaps. Then mu>=a, z=0,
V<=Cna, r<=r_0+2s, and (3)--(4) give

    O(n log(n+1)
      +(r_0+s+e) 2^(s+e) n^alpha (log(n+1)+s+e)) work.          (5)

For fixed r_0,s,e this is O(n^1.44042... log n), with a complete globally
optimal tree. Exceptional weights need not pass the earlier dominant-core
certificate and may have mutually unrelated magnitudes. The earlier
dominant-core methods can be faster on their accepted families; (5) is
not a claim of superiority on every structured input. Its constants depend
on C and the indicated exceptional count, not their numerical magnitudes.
The bound is arithmetic: reading and operating on very large weights still
has its usual bit cost.

Arbitrary runs and arbitrarily many exceptional outcomes are allowed by
the exact solver, but do not satisfy this subquadratic family guarantee.
The general arbitrary-weight objective and the original interval-core size
question remain open.

## Independent audit

The audit enumerates every optimal tree shape on small inputs, checks the
positive-subtree depth assertion for each sorted cut, and separately tests
arbitrary marked sets. It computes mu and z from all literal intervals,
independently of the singleton scan. Full mixed constructors are compared
with shape, all-root, and ordinary Knuth optima; rational, geometric,
zero, and large exceptional weights are included. Larger height-only plans
are explicitly distinguished from constructed trees. Operation counts and
executed-source hashes are in `results/trimmed_height_audit.json`.
The separate `trimmed_interval_audit.json` checks every interval against an
all-root recurrence retaining the minimum height among tied optimal costs.
