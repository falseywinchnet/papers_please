# A width-sensitive upper bound for the alternating rank template

The clipped ruler at level one can be analyzed exactly as a fixed-cardinality
matching on a path. This settles its upper tail for arbitrary nonnegative
real key weights, including all interactions. Higher clipped levels and the
below-capacity mixed tail remain outstanding parts of the full OBST target.

## Statement

Let c=2m+1>=3, n>=c, p_0,...,p_(n-1)>=0, and P=sum p. Put v_r=1 for
even r and zero for odd r, 1<=r<=c. Define the subsequence score S(i,j) and
upper density tail U_d as in RANK_REWARD_STABILITY.md. For every integer d>=1,

U_d <= P min(m, 2+(c-3)/d).                                    (1)

In particular U_d=O(P(1+c/d)). No integer-weight assumption is needed.

## Matching representation

The m positively rewarded subsequence positions have at least one selected
zero-reward position before them, between consecutive ones, and after them.
Thus S(i,j) is the maximum total weight of exactly m indices in
[i+1,j-2], with consecutive indices at least two apart. Conversely any such
indices can be completed to a length-c subsequence by choosing one filler
in each intervening gap and at each end. Regard index x as edge (x,x+1)
of the path with vertices i+1,...,j-1. The problem is exactly maximum-weight
matching of cardinality m, with edge weight p_x.

The argument below uses the classical alternating-path augmentation operation
(see Berge, *Two Theorems in Graph Theory*, PNAS 43(9), 842-844, 1957,
https://doi.org/10.1073/pnas.43.9.842). The particular path packing and the
subsequent tail charge are proved here in full.

## Endpoint loss and d explicit repairs

Fix j-i=c+d, d>=1, and let delta=S(i,j)-S(i+1,j). Take an optimal matching
of size m on edges i+1,...,j-2. If edge i+1 is unused, the same matching is
feasible after removing the leftmost path vertex, so delta=0.

Otherwise remove that edge and the leftmost vertex. The remaining path has
j-i-2=2m+d-1 vertices and a matching M of size m-1. Exactly d+1 vertices
are unmatched. List them in path order as z_0<...<z_d. For each a=1,...,d,
the segment from z_(a-1) to z_a is an augmenting path: all interior vertices
are matched, and the path's edges alternate between unused and matched,
starting and ending unused. Flipping its edges gives a matching of size m
on the shortened interval.

The d paths can share unmatched endpoints, but their matched edges are
disjoint. Their removed matched weights therefore sum to at most weight(M).
At least one flip removes at most weight(M)/d; its added edges have
nonnegative weight. Since weight(M)=S(i,j)-p_(i+1),

d delta <= (d-1)p_(i+1)+S(i,j).                                (2)

This also holds in the unused-edge case because its right side is
nonnegative. The proof explicitly gives every repair and accounts for all
boundary vertices; no assumption about independent input contributions
appears.

## From local loss to the total tail

For k=c+d<n put b=n-k. Telescoping yields

U_d = sum_(i=0)^(b-1) [S(i,i+k)-S(i+1,i+k)] + S(b,n)-S(0,n).

The last difference is nonpositive, because any subsequence of [b,n) is
feasible in [0,n). Summing (2) gives

d U_d <= (d-1) sum_(i=0)^(b-1) p_(i+1)
          +sum_(i=0)^(b-1) S(i,i+k).

Each interval score is at most the sum of its eligible edge weights
p_(i+1)+...+p_(i+k-2). A fixed key appears in at most k-2 such intervals.
Consequently

d U_d <= (d-1)P+(k-2)P = (2d+c-3)P.

For k>=n the tail is empty. The other bound U_d<=mP follows by increasing
the m even-rank rewards from zero to one and applying rank-coordinate
stability. This proves (1).

## The capacity-over-width term is necessary with growing width

Let C=2^h, K>=3, C>=4K, c=C-1, n=2C, and put unit key weights at

x, x+3, ..., x+3(K-1)=C,       x=C-3(K-1).

At width d=K, the alternating template has exactly

U_K = ceil(x/2)-1 = ceil((C-3K+1)/2).                           (3)

Here P=K. Taking K=2^floor(h/2) gives d growing like sqrt(C), while
U_K/(Pc/d) tends to 1/2. Multiplying all weights by n/K gives integer
total mass W=n and preserves this ratio for those choices of K.

### Exact endpoint computation

Put k=c+K and b=n-k=C-K+1. For i<x, the length-k interval [i,i+k)
can reward all K keys. Its first positive local position is
r=x-i+1>=2. Omit u=0 positions before it if r is even, or u=1 if r is
odd, and one position between each consecutive pair of positive keys.
This uses K-1+u<=K omissions, and leaves the last rewarded rank at
C-K+2-i-u<=C-2. For the only delicate endpoint, K=3,i=0, r is odd and
u=1, so the inequality still holds. Any remaining omission follows the
last positive key. Thus all rewarded ranks are even and interior.

The shortened interval [i+1,i+k) has K-1 omissions. It rewards all K
keys exactly when x-i is even: their odd spacing requires one omission
between every pair, and their initial parity requires no additional
omission precisely in that case. If x-i is odd, K rewards are impossible;
dropping the first positive key from the rewarded set permits K-1 rewards.
Its new first local position is x-i+3, which is even, and only K-2
inter-key omissions are needed. The final rank fits; the potential
exception K=3,i=0 belongs to the even case already handled.
Hence, for i<x,

S(i,i+k)-S(i+1,i+k) = 1 if x-i is odd, and 0 otherwise.

For i>=x, fewer than K positive keys remain eligible, so both intervals
can reward every positive key strictly after their left endpoints.
The endpoint loss is one exactly when i+1 is a positive-key position.
The longer interval has at most K-1 eligible positives; the shorter has
at most K-1 as well, and their parity corrections fit their K and K-1
omissions. Their suffixes have ample space for the remaining omissions.

On [b,n), every positive key strictly after b is rewarded; on [0,n), all
K are rewarded. Substitution into the tail telescope cancels the losses
at positive-key boundaries, leaving exactly the odd-count ceil(x/2) minus
one. This proves (3) independently of the search.

## The additive P term is also necessary

Take c=3, so S(i,j)=max_(i+1<=x<=j-2) p_x. Put K>=2 unit keys at
1,1+s,...,1+(K-1)s, with s>=2 and n=(K-1)s+3. The only positive upper
densities connect consecutive unit keys: at (i,j)=(x-1,y+1), the outer
and two side scores are one and the inner score is zero. Each density
is one and has distance s-1 from capacity. Thus

U_(s-1)=K-1,       P=K.

Letting both K and s grow shows that an O(Pc/d) bound alone is impossible.
Together with (3), this establishes both scales in (1), up to constants.

## Scope and next obstruction

Level-one clipping has the required form O(P+Pc/d). For higher clipped
ruler rewards, a matching edge's reward also depends on its order among
the selected edges. An augmenting path can change those ranks. The proof
of (2) only prices the edges removed by a flip; it does not yet price
reward changes on retained edges. Extending this argument requires that
additional accounting, rather than reusing (2) unchanged.

The unchanged endpoint inequality already fails at the next level. Take
c=7, d=3, n=10, p_3=1 and all other weights zero, with template
(0,1,0,2,0,1,0). On [0,10), the positive key can have rank four and score
two; on [1,10), its feasible ranks are one through three and its best score
is one. Thus delta=1, p_1=0, and d delta=3>S(0,10)=2. A repair that merely
counts removed edge weights misses the changed reward on the retained key.

## Independent checks and search record

The audit compares generic rank-subsequence DP with an independently
implemented cardinality-matching DP on 2887 inputs. It checks 147191
endpoint bounds and explicitly constructs 41517 augmenting paths in 18703
packings, verifying cardinality, feasibility, removed weights, and all
repair inequalities. There are 58142 global bound checks. Exhaustive
binary inputs through nine keys include every admissible odd c; random
integer inputs extend through 128 keys.

Sixteen cluster-family instances through C=128 have both independent
recurrences, 1045 endpoint-formula checks, and 32 terminal-score checks.
Eleven spaced-maximum families check the additive term. Larger rows
through h=128 evaluate only the proved formula, with that distinction
recorded. An initial independent-matcher indexing error included the
left filler as a reward edge; the four-key input (0,1,0,0) exposed it before
any larger run. The corrected matcher begins its edge list at i+1.

The separate compiled clipped-ruler search evaluates 25683 vectors and
records 84957303 interval scores, 4737828651 candidate transitions, and
82044166 upper densities. It includes fixed-mass mutation searches, sparse
clusters, periodic combs, and small exhaustive binary controls. All 451
small control vectors agree with the generic Python subsequence recurrence.
It tests U_d/[P(t+(c+1)/d)]; its largest observed ratio is 321/292, on the
full height-seven template with two unit keys. This refutes coefficient
one for that displayed inequality, but gives no asymptotic upper bound.
Source hashes and exact inputs are retained in `alternating_tail_bound.json`
and `periodic_tail_probe.json`.

The subsequent [rank-repair analysis](RANK_REPAIR_BARRIER.md) writes the
retained-rank term exactly. Rightmost optima eliminate spurious zero-loss
repairs, but an explicit one-key family defeats even the best certificate
over all optimal starting witnesses. Its true tail is zero; the repair
certificate is quadratic in height. An optimal endpoint repair can require
linearly many alternating components in the capacity.
