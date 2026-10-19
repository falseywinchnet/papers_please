# Exact capacity densities and a sharp interaction allowance

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. All identities concern arbitrary nonnegative weights on both
keys and gaps in fixed key order.

## Capacity density as two prefix maxima

Fix h>=1, c=2^h-1<=n, M>hW, P=sum p, Q=sum q, W=P+Q. Use zero-based keys
and gaps and v(t)=nu_2(t). For 0<=i<n-c and 0<=r<=(c-1)/2 set

    Z_(i,r)=sum_(l=1)^r v(2l)(p_(i+2l)-p_(i+2l-1)),
    F_i=max_r (-Z_(i,r)),
    G_i=max_r (Z_(i,r)+q_(i+2r+1)).

Then the ordinary density on the capacity line is exactly

    D_h(i,i+c)=M-F_i-G_i.                                  (1)

Proof: let B_i=sum_(t=1)^c p_(i+t-1)v(t). A perfect c-key interval has cost
hW(i,i+c)-B_i. The c-1 inner keys have cost
hW(i+1,i+c)-B_i-G_i by the one-missing-slot identity already proved in
MIXED_BOUNDARY_MASS.md. For the c+1 outer keys, maximal exposure selects
exactly c keys, and all gaps have comparison depth h. Omitting the first
key gives reward B_(i+1). If instead key i+t is omitted, its reward changes by

    sum_(k=1)^t v(k)(p_(i+k-1)-p_(i+k)).

Only even k contribute, so this is -Z_(i,floor(t/2)). Thus the long interval
has cost M+hW(i,i+c+1)-B_(i+1)-F_i. The two perfect rewards and interval
masses cancel in the four-corner difference, proving (1). At h=1 the inner
interval is empty, F_i=0 and G_i=q_(i+1); the same calculation holds.

## A proved width-one interaction bound

Let T_1(w) be the sum of all ordinary densities strictly off the capacity
line. Let e_x denote one unit on outcome x, whether a key or a gap. Let

    R_h(w)=A_h(0,n)-M(n-c)

be the full interval's ordinary comparison cost after removing its terminal
penalty. This depends only on w, provided the penalty is large enough.
For every nonnegative weight vector w,

    T_1(w)-sum_x w_x T_1(e_x)
       <= R_h(w)-sum_x w_x R_h(e_x)
       <= (h-1)P.                                        (2)

The middle term is nonnegative. The bound includes real weights; integrality
is not required. Each unit instance may use its own sufficiently large
penalty because every quantity in (2) is penalty-independent.

Proof: the sum of every ordinary density telescopes to the full interval
cost minus the sum of singleton costs. Summing (1) along the capacity line
cancels all M(n-c) penalty, giving the exact identity

    T_1(w)=R_h(w)-P-2Q+q_0+q_n+sum_i(F_i(w)+G_i(w)).       (3)

Each F_i and G_i is a maximum of linear forms, hence positively homogeneous
and subadditive. Substituting w=sum_x w_x e_x into (3) proves the first
inequality in (2). This is a global sum; it does not assert pointwise density
subadditivity.

For the second inequality, maximal exposure makes the full interval a
perfect c-key skeleton. Its ordinary cost is

    R_h(w)=hW-S_h(p),
    S_h(p)=max_(1<=t_1<...<t_c<=n) sum_(j=1)^c p_(t_j-1)v(j).

In particular every gap has depth h, so all gap terms cancel from the middle
expression in (2). S_h is a maximum of linear forms. It follows that

    R_h(w)-sum_x w_x R_h(e_x)
      =sum_(x=0)^(n-1) p_x S_h(e_x)-S_h(p)

lies between zero and (h-1)P: individual rewards are at most h-1, and S_h(p)
is nonnegative. This proves (2), including c=n when the skeleton is unique.

## The key-mass allowance is asymptotically sharp

Take h>=2, C=2^h, n=2C, c=C-1, p_x=1 for even x and zero for odd x, and
all gaps zero. Then P=C. Every prefix walk Z_(i,r) is monotone in r: increasing
for even i, decreasing for odd i. The maximizing endpoints for F_i and G_i
are therefore common to every positive unit key. Their sums are exactly
additive on this weight vector, so equality holds in the first inequality
of (2).

The skeleton reward is c-h. No reward can exceed sum_(j=1)^c v(j)=c-h since
p_x<=1. The contiguous subsequence starting at key index one attains it:
every even skeleton rank receives a unit key. Hence

    R_h(w)=(h-1)C+h+1.

For a unit key at one-based position X, its feasible skeleton ranks are
[max(1,X-C-1), min(C-1,X)]. At odd positions X, summing the best achievable
comparison lengths gives

    sum_(x even) R_h(e_x)
      =(C/2+1)+h+2 sum_(t=1)^(h-2) (h-t)2^(t-1)
      =2C-h-1.

The first term counts the keys that can occupy the root. The leftmost key
has depth h. The remaining left and right positions occur in pairs with
floor(log2 distance)=t, giving the last sum. Consequently

    T_1(w)-sum_(x even) T_1(e_x)=(h-3)C+2h+2,             (4)

and the ratio to (h-1)P tends to one. Thus a uniform multiplicative improvement
of (2)'s last bound is impossible. In particular, an O(P) allowance independent
of h is false. Multiplying all key weights by two gives W=n with the same
ratio. The total tail itself equals C(C-2), as follows from the earlier
alternating-key density formulas; the interaction is a smaller, but necessary,
Theta(P h) part of that total.

## A wider band destroys the boundary subadditivity argument

It is false that (2)'s first inequality holds after replacing T_1 by T_d for
every d. A four-key counterexample uses p=0 and q_2=q_4=1, all other gaps
zero. Put h=2, c=3, d=2. The only eligible length is one. Its only positive
density is

    D_h(2,3)=A_h(2,4)-A_h(2,3)-A_h(3,4)=3-1-1=1.

For either gap alone this density is zero, and every other eligible density
is zero. Hence T_2(w)=1 while sum_x w_x T_2(e_x)=0. Every full-interval gap
has depth two, so R_h(w)=4 and the unit full costs sum to four. The proposed
right-hand side is zero. This also disproves every all-width allowance
expressed only in key mass: here P=0.

The example leaves the separate candidate

    T_d(w)<=sum_x w_x T_d(e_x)+hW

open. The sharp width-one proof cannot establish that candidate by merely
including extra diagonals in the boundary sum. Uniform unit keys show that,
if the candidate is true, its hW coefficient cannot be reduced uniformly:
with n=2^(h+1), d=2^(h-1), every unit-key tail is zero by the consecutive-power
classification, whereas the uniform-key tail is (h-1)n+h-c. Its ratio to hW
tends to one. The full mixed tail upper bound and the main construction bound
remain unchanged.

## Independent audits and directed falsification

The all-root identity audit checks exhaustive mixed binary vectors through
five keys and seeded mixed inputs through 32 keys. It verifies every capacity
identity, the telescoping total, the subadditivity inequality, and (2).
The separate sharp-family audit compares (4) against all-root tables, with
unit-input controls at smaller sizes and clearly labeled formula evaluations
at large sizes. Exact counters and source hashes are retained in
results/capacity_interaction.json and results/capacity_interaction_sharp.json.

The compiled search maximizes the excess over weighted unit-input tails,
divided by hW, over every band width and early layer. It uses 15 fixed-mass
searches with 1200 mutations each, three starting patterns per size through
n=256, plus structured mixed, gap, key, alternating, ramp, and random inputs.
Unit profiles are recomputed by the same optimized recurrence, and small
vectors are independently checked against an all-root recurrence. The
largest observed ratio is 1223/1536, attained by uniform keys. This is evidence
for choosing the next proof target, not an upper-bound proof. The complete
weights, seeds, counters, and executed-source hashes are retained in
results/core_interaction_search.json.
