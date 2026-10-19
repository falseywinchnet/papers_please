# Coupled upper-tail stability under rank-reward changes

This result controls joint optimization directly. It changes a reward attached
to a skeleton rank, while retaining all input weights and their interactions.
It does not decompose a mixed input into independently optimized unit inputs.

## General subsequence template

Let p_0,...,p_(n-1) be nonnegative real key weights, P their sum, and let
v=(v_1,...,v_c) be any real rank template, with 1<=c<=n. For j-i>=c set

S_v(i,j) = max_(i<=t_1<...<t_c<j) sum_r p_(t_r) v_r.

For integer d>=1 define

U_d(v) = sum_(0<=i<j<n, j-i>=c+d)
 [S_v(i,j)+S_v(i+1,j+1)-S_v(i,j+1)-S_v(i+1,j)].

An empty sum is zero. Each summand is nonnegative. Indeed, take optimizing
sequences for the outer interval [i,j+1) and inner interval [i+1,j).
Their componentwise minimum fits [i,j), and their componentwise maximum
fits [i+1,j+1). The sum of their rewards is unchanged. Taking maxima in the
two latter intervals proves the inequality.

For the ruler template v_r=nu_2(r), c=2^h-1, this is exactly the ordinary
above-capacity density mass of the terminal-penalty layer at distance at
least d. The proved mixed-slot representation gives, for every length >=c,
A_h(i,j)=M(j-i-c)+h W(i,j)-S_v(i,j). The first two terms have zero
four-corner difference. All gap weights therefore cancel on this side.

## Rank-coordinate stability theorem

Increasing any one rank reward by Delta>=0 gives

-2 P Delta <= U_d(v+Delta e_r)-U_d(v) <= P Delta.                 (1)

Consequently, for coordinatewise v' >= v,

U_d(v') <= U_d(v)+P sum_r(v'_r-v_r).                             (2)

For arbitrary v,v', absolute change is at most 2P ||v'-v||_1.
The input weights can be arbitrarily coupled by the maximizing subsequence.

### Canonical optimizers and endpoint monotonicity

For one interval, optimizing sequences are closed under componentwise
minimum and maximum: both resulting sequences remain strictly increasing,
and their total rewards sum to the original total. Each is feasible, so
both must remain optimal. Taking finitely many minima defines a unique
componentwise-leftmost optimum (also the lexicographically first optimum).

Suppose both endpoints of an interval move weakly to the right, while its
length remains at least c. Let a,b be the two leftmost optima. Their
componentwise minimum is feasible in the old interval and maximum in the
new interval. The total reward is unchanged; hence both are optimal in their
respective intervals. Leftmost minimality forces a=min(a,b), so a<=b
coordinatewise. This argument does not assume any ordering of the p's or v's.

### Telescoping and the interlacing derivative

Put k=c+d. For k>=n there are no eligible cells. Otherwise m=n-k>=1,
and telescoping the rows gives exactly

U_d(v) = sum_(i=0)^m S_v(i,i+k)
         -sum_(i=0)^(m-1) S_v(i+1,i+k)-S_v(0,n).                (3)

Vary v_r by a parameter lambda in [0,Delta]. Each score is the maximum
of finitely many affine functions of lambda. Outside finitely many
breakpoints its derivative is p at the rth selected position of its
canonical optimum. Ties persisting on an open interval have equal slopes.

Write a_i for that selected position in [i,i+k), and b_i for its position
in [i+1,i+k). Endpoint monotonicity gives the single interlacing chain

a_0 <= b_0 <= a_1 <= b_1 <= ... <= a_m.

The derivative of the first two sums in (3) is
sum_i p_(a_i)-sum_i p_(b_i). Occurrences of any one input position are a
contiguous block in this alternating chain. Cancelling equal positions
leaves a coefficient in {-1,0,1} at each position, so this derivative lies
between -P and P. The final term contributes -p_z in [-P,0]. Therefore the
whole derivative lies in [-2P,P] almost everywhere. Integrating proves (1).
Successive coordinate changes prove (2) and the two-sided L1 bound.

## Ruler clipping corollary

For h>=1, C=2^h, c=C-1>=1, and 0<=t<=h-1, set
v^(t)_r=min(nu_2(r),t). This is a template with period D=2^t (a constant
zero template when t=0). Its removed reward is exactly

sum_(r=1)^(C-1) [nu_2(r)-t]_+
 = sum_(s=t+1)^(h-1) (2^(h-s)-1)
 = 2^(h-t)-(h-t)-1.

Thus, for every d>=1,

U_d(v) <= U_d(v^(t))+P [2^(h-t)-(h-t)-1].                       (4)

Choose t=min(h-1,floor(log2 d)). The error is at most 2PC/d, and is zero
when t=h-1. The high-rank part is therefore controlled at the desired c/d
scale, with C=c+1. Bounding the remaining periodic template is a separate
mathematical problem. Equation (4) does not prove the full mixed tail
estimate, and does not apply directly to below-capacity slots.

## A periodic template still has a linear-capacity tail

The proposed shortcut U_d(v^(t))<=tP for d>=2^t is false by an unbounded
factor, even with two unit keys and t=1.

Take h>=3, C=2^h, c=C-1, n=2C, and put unit keys at x=C-5 and y=C.
Let v_r=1 for even r and zero for odd r. At d=2,

U_2(v)=C/2-4.                                                   (5)

Here P=2 and the claimed upper bound tP would be two. Scaling both key
weights by C makes total input mass W=n and preserves the ratio.

To prove (5), apply (3) with k=C+1. In its first boundary sum, starts
0<=i<=C-1 have length C+1, so there are two omitted positions. For
1<=i<=C-6 both unit keys can be assigned even ranks: with
r=x-i+1, omit u=0 positions before x if r is even and u=1 if r is odd,
and omit one further position between x and y. Their ranks are r-u and
r+4-u, both even and in [1,c]. The remaining omissions can follow y.
The reward is two. At i=0, y is the final position and can only be selected
at rank c, which is odd. At i=C-5, x is the first position and has rank one.
These two intervals have reward one. For C-4<=i<=C-1 only y remains, and
it can be placed at an even rank. Therefore the first boundary sum is 2C-6.

In the second sum, starts 1<=j<=C-1 have length C and one omission.
If both keys are present, their odd separation five forces that omission
to lie between them for both selected ranks to be even. Thus the reward is
two exactly when r=C-4-j is even and 2<=r<=C-6. There are C/2-3 such
starts. Every other interval has reward one. The second sum is consequently
(C-1)+(C/2-3)=3C/2-4. On the full interval both keys can occupy even ranks,
so S_v(0,n)=2. Substitution yields (5).

This is an obstruction for the auxiliary clipped template, not an additional
claim about the original ruler's tail. The clipping error and the remaining
periodic component can both need a capacity-dependent bound.

## Subsequent level-one upper bound

[ALTERNATING_TAIL_BOUND.md](ALTERNATING_TAIL_BOUND.md) now proves
U_d<=P min((c-1)/2,2+(c-3)/d) for the alternating template, with arbitrary
nonnegative real weights. Its path-matching repair argument supplies the
capacity-dependent control demanded by (5). Both scales are necessary,
including a family with growing d. Higher clipped levels remain open.

## Verification and search records

The proof above is independent of computation. `rank_reward_tail.py` audits
canonical optima against literal subsets, endpoint monotonicity, single-rank
perturbations, ruler clipping, and correspondence with independent all-root
mixed OBST layers. `periodic_tail_barrier.py` checks both boundary sums and
the exact periodic family against a generic subsequence DP through h=7;
for h=3 it independently enumerates all subsets. Larger listed heights are
closed-form evaluations only.

`sparse_tail_search.py` and `cluster_tail_search.py` instead attack the still
open total mixed target T_(h,d)=O(W(L+c_h/d)). They check all widths and early
layers, retain exact rational maxima and input weights, and independently
check small winners with an all-root recurrence. The first evaluates 23,183
inputs through n=1024; the second evaluates 462 repeated sparse clusters
through n=2048. Their largest respective ratios are 485/168 and 2828/1107.
These finite maxima provide no upper-bound proof. All four result records
include operation counts and hashes of the sources actually executed.
