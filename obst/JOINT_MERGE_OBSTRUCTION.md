# Joint key/gap coupling and a strict compatible-merge obstruction

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. This is a rejected algorithm with a proved obstruction,
not an unrestricted complexity lower bound or a new production solver.

## The relaxation being tested

Keep the gap weights in their original order, but allow the key weights to
permute among internal nodes. Let J(p,q) be the resulting minimum. If p_[r]
are the key weights sorted decreasingly and l_(r)(T) are the key comparison
lengths sorted increasingly, then

    J(p,q) = min_T [sum_r p_[r] l_(r)(T) + sum_i q_i d_i(T)].

This is a lower bound for the full ordered optimum. It is at least the sum
K(p)+A(q), where K is the independent key-capacity bound and A is the exact
alphabetic gap optimum. In particular it dominates K(p)+G(q), using the
previous threshold bound G. An exact inexpensive J could certify candidates
that the separate bounds miss; this probe does not supply such an algorithm.

There is an exact profile representation. Write P=sum p, S_j for the sum of
the j largest key weights, and A_t(T) for the number of keys whose comparison
length is at most t. Then the optimally permuted key contribution is

    P + sum_{t>=1} (P - S_{A_t(T)}).

Every key of comparison length l is counted once in P and l-1 more times.
The sum is finite, ending when all keys have appeared. The function
f(j)=P-S_j is decreasing and discretely convex: its successive differences
are -p_[j+1], which are nondecreasing. This is an exact expression for the
global profile coupling, not a proof that its tree minimization is easy.
Rearrangement and the tail-sum identity are standard; priority for this
application is not established.

## Precisely the rejected rule

Start with the ordered gap leaves. Two active items are compatible if no
unmerged original leaf lies strictly between them. Repeatedly select the
compatible pair of smallest total mass, add the smallest unused key weight,
replace the left item with the resulting internal item, and remove the right
item. Recover original-leaf depths, then reconstruct an alphabetic tree with
those depths. Finally assign the key multiset optimally to the reconstructed
internal depths. This last reassignment gives the proposed rule its best
cost on its chosen profile; the rule still fails.

For equal primary scores the probe uses the sum of distinct powers of two
assigned to the original leaves as a symbolic secondary weight. This is a
fully specified deterministic tie convention, not bounded-word arithmetic.
The decisive counterexample has no primary-score ties, so it is independent
of that convention. Hu and Tucker's classical alphabetic construction is
credited separately; adding different internal-node weights is the proposed
extension being rejected, not a counterexample to their algorithm.

## Positive six-key counterexample

Use the full ordered vectors

    p = (7, 1, 5, 8, 6, 4),
    q = (18, 2, 13, 3, 17, 1, 2).

The key multiset is (1,4,5,6,7,8). The greedy trace is:

| Next key | Pair masses | New mass | Margin over next pair |
|---:|---:|---:|---:|
| 1 | 1, 2 | 4 | 12 |
| 4 | 2, 13 | 19 | 1 |
| 5 | 3, 17 | 25 | 1 |
| 6 | 18, 4 | 28 | 1 |
| 7 | 19, 25 | 51 | 3 |
| 8 | 28, 51 | 87 | only pair |

The sum of charges is 214. Reconstruction is valid and its optimally
reassigned key cost is also 214. The comparison is:

| Quantity | Greedy reconstructed profile | Better feasible tree |
|---|---|---|
| Sorted key comparison lengths | 1,2,2,3,3,3 | 1,2,2,3,3,4 |
| Ordered gap depths | 2,3,3,3,3,3,3 | 2,4,4,3,2,3,3 |
| Optimally assigned key cost | 64 | 65 |
| Gap cost | 150 | 148 |
| Total | 214 | 213 |

The better tree is root key 3, with left root 0 whose right child is 2
and whose grandchild is key 1 as the left child of 2; the right subtree is
root 4 with right child 5. Its inorder key comparison lengths are
(2,4,3,1,2,3), so the displayed ordered p attains the relaxed assignment.

The exhaustive relaxed oracle checks all 132 six-key shapes and obtains
J=213. Independent cubic and Knuth recurrences obtain full OPT=213. The
separate quantities are K=64, G=144, A=148. Thus K+G=208, K+A=212, and
J=OPT=213. Even replacing the threshold gap bound by the exact gap optimum
does not eliminate the coupling deficit.

The value 214 is a *relaxed* candidate value. The reconstructed tree with
the original ordered p has cost 220. It would be incorrect to report 214
as the full cost of that tree. The counterexample is stronger: even freeing
all key positions fails to make this merge extension optimal. It is also
unsafe as a lower bound, since its returned value exceeds the full optimum.

## Robustness and arbitrarily many keys

Scale every weight by M>0. The same strict trace returns 214M and the
optimum is 213M. This proves unbounded additive error as magnitudes grow,
not an unbounded approximation ratio.

There is also a full-dimensional positive box of failures. Perturb each of
the thirteen original weights independently by at most epsilon=1/1000.
All key ranks remain unchanged. For the fixed trace, each active mass is
a sum of disjoint original outcomes, so each competing pair-score difference
changes by at most 26 epsilon. Its original strict margin is at least 1.
Induction therefore preserves the trace. The candidate minus the displayed
witness cost is exactly

    q_4 - q_1 - q_2 - min(p),

which remains at least 1-4 epsilon>0. The proof covers the entire real box;
the harness additionally checks all 8192 integer corners of 1000(p,q)+/-1,
where the smallest gap is exactly 996. This uses a feasible witness and
does not assume that the witness stays globally optimal after perturbation.

To extend the failure, let a full ordered instance have total mass W and a
known optimal tree of cost U. Put A=W+U+1 and P=2A. Prepend a new key of
weight P and a new gap of weight A, leaving the old vectors in order.
The tree whose root is the new key, with an empty left child and the old
tree on the right, costs

    P + A + W + U = 4A-1 = 2P-1.

Any different root puts the new key at comparison length at least two and
therefore costs at least 2P. Thus the new root is forced and
OPT'=P+A+W+OPT. Every old compatible pair has total mass at most W, whereas
every pair involving the new original leaf costs more than A>W. P is the
largest key. Consequently all old merges occur first and the last charge
is P+A+W. Reconstruction adds one to every old depth, with the new largest
key at the root; the optimally reassigned candidate cost gains the same
amount. Starting with the six-key example preserves candidate-OPT=1 for
every n>=6, with positive weights, distinct key weights, and strict pair
choices. This statement does not require J=OPT for the padded instances.

The recurrence satisfies W'=W+3A, U'=4A-1, and A'=W+7A, between 7A and 8A.
Thus the maximum weight has O(n) bits. The harness checks full Knuth/tree
cost equality at n=6,7,8,16,32,64,128,256, with cubic checks through 16.
At n=256 the largest weight has 732 bits and the literal candidate evaluates
32904 pairs. These counters describe a rejected diagnostic implementation,
not a subquadratic production algorithm.

## Uniform transfer cannot repair the deficit

For -min(q)<=a<=min(p), set p'=p-a and q'=q+a componentwise. All weights
remain nonnegative. Every extended binary tree with n internal nodes obeys

    sum_i d_i(gap) - sum_i l_i(key) = n.

This follows from external path length = internal path length + 2n and
l_i=internal_depth_i+1. Therefore every fixed tree cost increases by an,
as do OPT and J. The sorted orders are unchanged. If M(n) is the minimum
unit key comparison-length sum and E(n+1) the minimum unit gap depth sum,
then E(n+1)-M(n)=n. The independent key bound changes by -a M(n); the
threshold gap bound changes by a E(n+1), because its variation part is
translation invariant and its rank coefficients sum to E(n+1). Hence

    K(p') + G(q') - an = K(p) + G(q).

The entire K+G deficit is invariant. No invariance of K+A is claimed:
unlike G, the exact alphabetic optimum A need not shift by a E(n+1).
The uniform transfer proof applies to the full mixed cost, J, and the
explicit K+G expression only.

For the proposed merge rule every active cluster contains one more original
gap than consumed key. Its mass therefore increases by exactly a. All
compatible pair scores increase by 2a, leaving the schedule and margins
unchanged, and every merge charge increases by a. This transformation
cannot fix the counterexample. When all keys have the same weight a,
transferring that a makes the keys zero and reduces to classical alphabetic
merging; the existing uniform-key reduction is not new.

## Evidence, reproduction, and scope

The oracle was written before the candidate was treated as a potential
bound. `joint_merge_probe.py` checks 1092 pure-alphabetic controls, 2400
seeded mixed controls, 616500 literal tree evaluations, and 42563 candidate
pair evaluations. There are 2385 exact and 15 suboptimal candidates.
No invalid reconstructed depth sequence occurs in that suite; that finite
observation is not a general reconstruction theorem.

`joint_coupling_audit.py` exhausts key multisets and ordered gap vectors
over {0,1} and {1,2} through seven keys: 7172 cases. The binary alphabet
has 3 failures at six keys and 11 at seven. All 3586 {1,2} cases pass;
no general two-positive-level theorem follows. It also checks 2036
constant-key reductions, 6918 profile/depth identities, and 1421 full
cost, bound, trace, margin, and reconstruction transfer controls.

The root AGENTS.md gives the M4 commands for all three scripts. The three
JSON result manifests record seeds, witnesses, counters, and source hashes.
There is no wall-time benchmark because the proposed algorithm fails exact
correctness. Existing certified constructors remain unchanged.

Prior work: T. C. Hu and A. C. Tucker, *Optimal Computer Search Trees and
Variable-Length Alphabetical Codes*, SIAM J. Applied Mathematics 21(4),
514-532 (1971), https://doi.org/10.1137/0121057. This note rejects only the
specified mixed extension. A fast exact joint-profile optimizer, a broader
full ordered algorithm, and any unrestricted complexity lower bound remain
open here. Targeted prior-work searches do not establish mathematical novelty.

The companion SHIFTED_ALPHABETIC.md develops a valid O(n log(n+1)) full
certificate from the exact alphabetic bound after uniform transfer. It
certifies the six-key obstruction at 213 and a positive nonuniform family.
It does not rehabilitate the mixed greedy rule or compute J in general.
