# Exact arbitrary-key transfers and dense local cores

The two-block finite-product idea extends to arbitrary nonnegative key weights
as a **rank-transfer representation**. This preserves the weighted subsequence
optimization that determines the above-capacity part of a BST layer. The
resulting transfer matrices can nevertheless have quadratic local cores.
Their coordinates are starting and ending ruler ranks, not interval endpoints.
Consequently the dense family below is a barrier to a sparse-transfer shortcut;
it is not a counterexample to the original local interval-core hypothesis.

## A finite representation for arbitrary key weights

For integer capacity c>=1 define

    F(t)=sum_(j=1)^t nu_2(j),  0<=t<=c.

Partition an input key sequence into r constant runs (w_l,m_l), where w_l>=0
and m_l>=1. A transfer from rank u to rank v selects v-u input keys, in their
original order, and assigns them consecutive ruler ranks u+1,...,v. Let the
transfer cost be the negative maximum reward. Its feasible domain is

    0<=u<=v<=c,  v-u<=sum_l m_l.

Use one global finite penalty

    K=1+F(c) sum_l w_l

and the run matrix, for 0<=u,v<=c,

    Q_l(u,v)=K[max(u-v,0)+max(v-u-m_l,0)]
               +w_l F(u)-w_l F(v).                       (1)

Every Q_l is finite and Monge. Its only densities are K on v-u=0 and
v-u=m_l, omitting diagonals outside the matrix. Thus delta(Q_l)<=2c,
and its condensed representation is directly available in O(c) work.
The row/column potential accounts for the entire ruler reward of the
selected part of this constant run.

The min-plus product T=Q_1...Q_r equals the desired transfer on its feasible
domain. A feasible path chooses t_l in [0,m_l] and has reward
sum_l w_l(F(u_l+t_l)-F(u_l)). It represents exactly a subsequence with those
counts per run. Conversely every subsequence has such a path and the same
reward. An infeasible path incurs at least K in penalties. The negative
part of all its potentials has magnitude at most F(c) sum_l w_l, so its
cost is at least one. A feasible path has cost at most zero. Thus an
infeasible path cannot replace a feasible optimum.

For c=2^h-1 and any interval [i,j) of length at least c, its original
terminal-penalty layer value is

    A_h(i,j)=M(j-i-c)+h W(i,j)+T_(p[i:j])(0,c).             (2)

This applies to arbitrary nonnegative key weights and arbitrary nonnegative
gap weights. Gap contributions are in W; they cancel from ordinary densities
strictly above capacity. Equation (2) does not compute the below-capacity
mixed region or by itself provide a fast all-interval constructor.

**Balanced construction bound.** By the published inequality

    delta(XY)<=2(delta(X)+delta(Y)),

a balanced product tree of height ceil(log2 r) gives

    delta(T)<=2 r 2^ceil(log2 r) c <=4r^2 c.               (3)

A leaf's core is multiplied by at most 2^height in this charging argument.
The sum of core sizes throughout the tree is O(r^2 c). The published
condensed-product algorithm therefore gives O(n+r^2 c log(c+1)) arithmetic
work, including extraction of the runs from n keys. No dense conversion
is required. The implementation retains ordinary witness maps during each
product, so O(r^2 c log(c+1)) is a conservative auxiliary-space bound.
This is polynomial rather than exponential in the number of runs; it is
not a weight-independent subquadratic full-BST bound.

The multiplication primitive is prior work: Gawrychowski, Gorbachev, and
Kociumaka, ESA 2025, Theorems 1.1 and 1.2:
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.74.

## An exact dense-core family using actual key weights

Take r input keys with weights p_j=j, for j=1,...,r. If t=v-u keys are
selected, their k-th selected index is at most r-t+k. Every ruler reward
is nonnegative. The last t input keys therefore maximize every summand
simultaneously. Define G(t)=sum_(j=1)^t j nu_2(j). On the feasible domain,

    T(u,v)=-[(r-v)(F(v)-F(u))+G(v)-G(u)].                 (4)

For an ordinary cell whose four corners are feasible, namely
1<=v-u<=r-1 and 0<=u,v<c, direct differencing gives

    D_T(u,v)=nu_2(u+1).                                  (5)

In particular, choose r=2s and c>=2s. In the square

    0<=u<s,  s<=v<2s,

all four-corner transfers are feasible. Every odd u has positive density
in every column, and every even u has zero density. The square has exactly

    s floor(s/2)                                        (6)

positive entries. This is quadratic, although the input has only 2s keys.
For c=2r-1 and even r, the entire strict feasible strip has exactly

    sum_(odd u, 0<=u<=c-2) min(r-1,c-1-u)
      =3r^2/4-3r/2+1                                    (7)

positive entries. In particular its core is Omega(rc). These lower bounds
hold for every completion agreeing on feasible entries; they are not artifacts
of the particular finite penalty in (1).

The input's total integer key weight is r(r+1)/2. Thus (6) does not contradict
a mass-dependent bound. Nor do transfer coordinates identify with the original
interval coordinates. What fails is an O(s) local bound for these transfers
uniformly over the number and sizes of the key weights, and any O(c+r) bound
for their total feasible core. The original O(s+W(J)) tile hypothesis remains
open.

## A chain of narrow bands can also make a dense square

The equal-block interior representation has another exact extension. For
r>=2 functions f_l on {0,...,N-1}, maximize sum_l f_l(u_l) subject to

    u_1<=A, u_r>=B, 0<=u_(l+1)-u_l<=g_l.                 (8)

Use K=1+sum_l(max f_l-min f_l), the two finite prefix/suffix selectors,
and r-1 band matrices, charging f_l once in its outgoing band and f_r in
the final band. Their total input core size is at most 2r(N-1). The same
penalty argument and a balanced product give a finite completion of the
negative optimum with at most

    2r 2^ceil(log2(r+1)) (N-1)                           (9)

core entries and O(r^2 N log(N+1)) work. The feasible domain is exactly
B<=A+sum_l g_l.

For unit-weight positive key blocks of lengths m_1,...,m_r with total P<=c,
let N=c-P+1 and P_l=sum_(t<l) m_t. Their complete-block interior uses

    f_l(u)=F(P_l+u+m_l)-F(P_l+u).

If the first block begins at z and total intervening zero length is G,
then A=z-i and B=c+z+G-j. After clipping frozen endpoints, a product
core cell (a,b) maps to i=z-a-1, j=c+z+G-b-1. This constructs the portion
whose four intervals contain every complete block; endpoint cuts are
outside this extension.

**Why (9) alone supplies no uniform local bound.** Set every g_l=1,
f_1(u)=...=f_(r-1)(u)=u and f_r(u)=-(r-1)u. Writing
u_(l+1)-u_l=e_l in {0,1}, the reward is -sum_(l=1)^(r-1) l e_l.
If B>A, at least d=B-A increments are necessary; choosing the first d
increments is optimal. If B<=A, a constant path has zero cost. Hence

    H(A,B)=-d(d+1)/2,  d=max(B-A,0),                      (10)

throughout the feasible domain. With r=N=2s+1 every output is feasible,
and the square 0<=A<s, s<=B<2s has density one in all s^2 cells.
All transition bands have width one. This counterfamily concerns arbitrary
unary functions, not the special ruler block rewards above. A uniform
boundary charge for many binary blocks must use that additional structure.

## Verification

`rank_transfer_audit.py` uses independent literal subsequences, feasible-state
DP, dense finite matrix products, and original all-root mixed BST layers.
Its two dense families are checked with exact arithmetic. Larger formula
and product checks are labeled separately from the smaller independent DP
controls. Operation counts and executed-source hashes are retained in
`results/rank_transfer_audit.json`; no timings are used for any bound.

The final audit exhausts 363 inputs over key weights {0,1,3} through five
keys. Its 23232 finite product entries, including infeasible completions,
match independent dense products with 459456 candidate additions. All
11385 feasible entries also match a separate subsequence DP and 52245
literal subsequences. Another 32 rational-weight inputs supply 1048 exact
entry controls. On 70 mixed inputs through 32 keys, 1172 original-layer
scores match (2). The combined original all-root controls, including the
many-block tests below, use 987840 root candidates and 104460 states.

One hundred signed-function chain inputs supply 3850 independent feasible
scores. The explicit width-one family has 1493 formula entries checked
against both the feasible-state DP and the condensed product, and 341
density-one square cells. Six weighted-ramp constructions through c=255
check 33138 formula entries and 32136 density formulas. The four smaller
rows, through c=63, also have 2130 independent subsequence-DP entries.
At c=255 and r=128 the strict feasible core has exactly 12097 entries;
the side-64 square has 2048. Thirty-two many-block inputs, with varied
block lengths and nonzero gap weights, have 128 original-layer support-set
comparisons and 3544 independent interior densities.
