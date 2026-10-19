# Rank-weighted matching repairs: canonical witnesses and exact barriers

This note studies the endpoint-repair route to the upper-tail estimate, after
[the alternating-template theorem](ALTERNATING_TAIL_BOUND.md). The representation
is exact at every ruler level. Its one-augmentation certificate, however, can
exceed the desired tail scale by an unbounded factor, even for one positive key.
The obstruction has a closed form and holds for every optimal starting witness.

## Exact representation and accounting

Use zero-based key positions and half-open intervals. Let c=2m+1 and let a
length-c reward template have v_(2r)=u_r>=0 and v_(2r-1)=0. Its subsequence
score S(i,j) is exactly

    max sum_(r=1)^m p_(a_r) u_r,
    i+1 <= a_1 < ... < a_m <= j-2,  a_(r+1)-a_r >= 2.

Index x denotes the edge (x,x+1) of a path. Fillers before, between, and after
the m edges give the original subsequence. For the ruler clipped at level t,
u_r=min(1+nu_2(r),t).

Fix j-i=c+d with d>=1, and an optimal matching A=(a_1,...,a_m). If A avoids
i+1, it remains feasible after deleting the left endpoint. Otherwise delete
edge i+1 and vertex i+1. The remaining matching M has m-1 edges and d+1
unmatched vertices. Between each consecutive pair lies an augmenting path.
Flipping one of these d paths produces a feasible m-edge matching B.

Writing R for the edges removed by that flip, N for the added edges, and E
for retained edges, the exact score loss is

    F(A)-F(B) = p_(i+1) u_1
      + sum_(x in R) p_x u_(rank_A(x))
      - sum_(x in N) p_x u_(rank_B(x))
      + sum_(x in E) p_x [u_(rank_A(x))-u_(rank_B(x))].

The last term is signed and need not vanish. Disjoint removed-edge sets
alone therefore do not provide the alternating-template argument.

Define delta(i,j)=S(i,j)-S(i+1,j). Define delta_hat(i,j) by choosing the best
of the prescribed repairs, and also minimizing the loss over **all optimal
starting matchings**. If an optimal start avoids i+1, allow it unchanged.
Thus delta_hat>=delta>=0. For k=c+d<n and b=n-k define

    U_hat_d = sum_(i=0)^(b-1) delta_hat(i,i+k) + S(b,n)-S(0,n).

The exact tail telescope gives U_hat_d>=U_d. This is the strongest certificate
available from independently choosing one such augmentation per endpoint.

## Rightmost optima recognize every zero endpoint loss

**Lemma.** For arbitrary rank rewards u, optimal matching tuples are closed
under componentwise minimum and maximum. They therefore have a unique
componentwise-rightmost optimum A^+. For nonnegative p,u and feasible shortened
intervals,

    S(i,j)=S(i+1,j)  if and only if  a^+_1>i+1.

**Proof.** If two tuples have gaps at least two, their componentwise minimum
and maximum do too. At each rank, the two chosen positions are merely exchanged,
so the sum of their two objective values is preserved. Optimality forces both
new tuples to be optimal. Taking maxima over the finite set gives A^+ (also
the lexicographically largest optimum). If the scores are equal, a shortened
optimum is an old optimum avoiding i+1; A^+ is at least that tuple coordinatewise.
The converse is feasibility. This lemma removes spurious repair losses at
zero-loss endpoints, but positive losses behave differently.

## Unique optimum: an unbounded local repair ratio

**Proposition.** For every integer B>=1, let c=7, n=10, u=(1,2,1), and

    p_2=p_3=2B, p_4=B, p_6=2B-1,

with other weights zero. On [1,10), the unique optimum is (2,4,6), with
score 6B-1. On [2,10), the optimum (3,6,8) has score 6B-2. Hence the actual
endpoint loss is one. The best one-augmentation repair loses B+1.

**Proof.** There are ten feasible old matchings. The score of (2,4,6) is
6B-1; all other scores are among 4B, 2B, and 6B-2 or 5B-2, each at most
6B-2. The four shortened matchings have scores 2B, 2B, 6B-2, 5B-2.
After removing edge 2, the unmatched vertices are 3,8,9. Flipping [3,8]
gives (3,5,7), score 2B; flipping [8,9] gives (4,6,8), score 5B-2.
Their best score is 5B-2. The old optimum is unique, so tie-breaking cannot
change this ratio.

## One key forces a quadratic-in-height certificate

**Theorem.** Let h>=3, C=2^h, c=C-1, m=C/2-1, n=4C, d=C, and put a single
unit key at x=C/2+1. Use the full ruler rewards u_r=1+nu_2(r), whose maximum
is t=h-1. Then

    U_C = 0,
    U_hat_C = (h-2)(h-3)/2.

The rightmost optimal starts attain the second equality. Since P=1 and
P(t+(c+1)/d)=h, the ratio of this best one-augmentation certificate to that
scale tends to infinity. Scaling the key weight by n makes W=n and preserves
the ratio.

**Proof.** Put k=2C-1 and b=2C+1. In a boundary interval [i,i+k), i<x, the
positive key can occupy precisely ranks 1 through

    R_i = min(m, floor((x-i+1)/2)).

There is enough room after x for every such rank, since k=2C-1. The unique
rank with maximum ruler reward is r=2^floor(log2 R_i). A rightmost optimum is

    a_s = x-2(r-s)                  for 1<=s<=r,
    a_s = i+k-2-2(m-s)              for r<s<=m.

The prefix packs against x and the suffix packs against the right boundary.
For i>=x, the rightmost optimum packs all m zero-weight edges against that
boundary. The first edge i+1 is used exactly at

    i=x-2r+1,  r=1,2,4,...,2^(h-2).

At all other starts the rightmost witness survives, so delta_hat=delta=0.
At a listed start, the positive key must have rank r in **every** optimum;
the available prefix has exactly enough vertices for r matching edges, so
that entire prefix is forced. For r=1, deleting the first edge deletes the
positive key, and both losses are one.

For r>=2, the shortened interval has maximum feasible rank r-1, whose
unique best ruler rank is r/2. The reward falls from 1+nu_2(r) to nu_2(r),
so the true loss is one. In the old remaining matching, the forced prefix
has only its leftmost vertex unmatched. Consequently no augmenting path
can lie entirely before the positive key. A path that reaches across that
key removes it, leaving score zero. Any other augmenting path lies after
it and retains it at rank r-1, which is odd, giving score one. Such an
after-key path exists: only one of the d+1 unmatched vertices lies before
the key, and d=C>=8. Therefore **every** optimal old matching has best
one-augmentation loss nu_2(r), independently of its suffix or tie choice.

The full score is h-1 and S(b,n)=0. The true endpoint losses sum to h-1,
proving U_C=0. The best repair losses sum to

    1 + sum_(a=1)^(h-2) a = 1+(h-2)(h-1)/2.

Subtracting the full score gives (h-2)(h-3)/2, as claimed.

## An optimal repair needs many alternating components

**Corollary.** In the preceding family, take the threshold i=2, where the
unit key's old rank is r=C/4. Delete the first matched edge. Relative to
that remaining matching, any shortened optimum has at least C/8-1
cardinality-decreasing alternating components and at least C/8
cardinality-increasing components. For the rightmost old optimum both
bounds are attained.

**Proof.** The positive edge is common to the remaining matching M and any
new optimum B, because it has positive optimal reward. Its new rank must
be r/2. Before this common edge, M has r-2 edges and B has r/2-1. Their
symmetric difference cannot cross the common edge. Each of its path
components changes cardinality by at most one, so at least r/2-1
components decrease cardinality before the key. Total cardinality rises
by one, requiring at least r/2 increasing components overall.

For attainment, write A for the rightmost old optimum given above. Keep
its edges a_(r/2+1),...,a_m, and insert the r/2 edges

    x+2, x+4, ..., x+r.

These fit in the large gap between the old prefix and suffix. The result
has m edges, with the positive key at rank r/2, hence is optimal. Relative
to M, the removed edges a_2,...,a_(r/2) and the added edges are pairwise
nonadjacent. They are exactly r/2-1 decreasing and r/2 increasing
single-edge components.

This is a barrier to bounding a prescribed local repair certificate. The
true tail of the family is zero. A compressed operation can move many
zero-weight edges together; the component count gives no lower bound on
running time for such an operation. A continuation of the matching route
must represent joint rank changes rather than bound one local augmentation.

## Verification appendix

The paired canonical diagnostics and the exact-family audit retain operation
counts, explicit witnesses, and executed-source hashes. The manuscript's
verification appendix reports their counts. The family proof above applies
at all heights; larger formula-only audit rows are explicitly labeled.
The records are `rank_matching_repair.json`, `rightmost_rank_repair.json`,
and `rank_repair_barrier.json` in `results/`.
