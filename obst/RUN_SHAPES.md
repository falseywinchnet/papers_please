# Exact transfers for joint key/gap signatures

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. The full unrestricted mixed-weight objective remains
open. This note proves an exact O(nk) shape optimizer with linear auxiliary
space and a full-optimality certificate. It does not assert mathematical
priority or replace the general problem by the gap-only case.

## 1. A key word replaces a bottom-slot word

For n>=1, write h=floor(log2(n+1)), S=2^h, m=S-1, and s=n-m.
A minimum-internal-path-length shape contains the perfect m-key skeleton
and expands s of its S bottom slots into one-key cherries. Encode keys in
inorder: x_i=1 for a skeleton key and x_i=0 for a cherry. The exact feasible
words have m ones and no adjacent zeros. An initial or terminal zero is
allowed. Conversely every such word gives a feasible minimum-IPL shape.
Indeed, its zero positions select distinct slots of the perfect skeleton;
the count is binomial(S,s), agreeing with slot enumeration.

If a skeleton key has rank r among the ones, its comparison length is
h-v_2(r). A cherry has length h+1. A gap has length h+1 precisely when
one of its neighboring keys is a cherry, and otherwise has length h.
Because cherries are not adjacent, each deep gap is counted once by

    c_i = q_i+q_(i+1).

Consequently the full mixed cost is exactly

    C(x) = A - sum_(i:x_i=1) [(1+v_2(r_i))p_i+c_i],
    A = (h+1)sum p + h sum q + sum_i c_i.                         (1)

Every original gap remains in A and in c. The transformation is valid only
inside this shape class; arbitrary taller shapes require the separate gate.

## 2. Constant signatures have path-independent block rewards

Partition the sequence of pairs (p_i,c_i) into its k maximal constant runs.
On a run with p_i=a, c_i=c and L keys, define

    U(r) = (2a+c)r - a popcount(r),     U(0)=0.                    (2)

Since sum_(t=1)^r v_2(t)=r-popcount(r), a block increasing the skeleton
count from r0 to r1 always earns reward U(r1)-U(r0). Its internal zero/one
arrangement does not affect that reward. It matters only for feasibility.
This is an exact boundary transfer, with no affine fitting or residual
approximation. The values of a and c can change arbitrarily between runs.

Let t be the previous key's bit and u the final bit of the nonempty block.
The allowed number d=r1-r0 of skeleton keys is every integer in [ell,b]:

| Previous t | Final u | ell | b |
| --- | --- | --- | --- |
| 1 | 1 | ceil(L/2) | L |
| 0 | 1 | floor(L/2)+1 | L |
| 1 | 0 | floor(L/2) | L-1 |
| 0 | 0 | ceil(L/2) | L-1 |

An empty range is infeasible. These bounds follow by placing nonadjacent
zeros, with a first zero forbidden when t=0 and a last zero required when
u=0. Every intermediate count is achievable. The virtual initial bit is
t=1; the final bit may be either value.

If D_t(r0) is the maximum prefix reward at the preceding boundary, then

    D'_u(r) = U(r) + max_t max_(r-b <= r0 <= r-ell)
                                  [D_t(r0)-U(r0)].               (3)

Out-of-range and unreachable entries are excluded. Each inner maximum is a
sliding window. A standard monotone deque evaluates all r in linear time;
each candidate is pushed and removed at most once. There are only four
boundary-bit pairs. Backward profiles similarly use

    B_t(r) = -U(r) + max_u max_(r+ell <= r1 <= r+b)
                                   [B'_u(r1)+U(r1)].             (4)

Popcounts through m are tabulated in O(n) time. Thus each block sweep is
O(n), regardless of L, the weight amplitudes, or the number of raw gap
weight changes within the block. A single block or a perfect shape can
be constructed directly.

## 3. Complete reconstruction in O(n) space

An initial sweep chooses the best final bit at rank m. For traceback, split
the block list in half. Compute the forward profile of the left half and
the backward profile of the right half between the fixed endpoint ranks.
Their sum chooses an optimal middle rank and bit. Release both profiles
before recursing. For one block, explicitly place its required number of
nonadjacent zeros using the boundary rules above. The n-bit word then gives
all comparison lengths, and the existing linear Cartesian reconstruction
returns the full tree.

This is the established forward/backward recomputation principle of
[Hirschberg (1975)](https://ics.uci.edu/~dhirschb/pubs/p341-hirschberg.pdf),
applied to the exact block transfers (3)--(4), not a claim to have invented
linear-space DP traceback.

At recursion level d, each active problem has at most ceil(k/2^d) blocks.
Its rank interval is restricted to its chosen endpoints; the sum of active
rank-interval widths is at most m+2^d. The total sweep work over all levels
is therefore O(km+k log(k+1)), plus O(n) leaf output and preprocessing.
Because m=Theta(n) and k<=n, this is O(nk) for n>=1. At any instant only
a constant number of profiles over at most m+1 ranks are retained. Profiles
are released before recursion, so the stack does not accumulate them.
Including input summaries, the word, and the output tree, auxiliary space
is O(n). The theorem counts arithmetic/comparison operations; arbitrary
large integers retain their bit costs.

## 4. The full certificate also uses the compressed signatures

The existing full-tree certificate uses a0=min p, b0=min q and an unordered
mixed residual-Huffman lower bound H. A class optimum V is globally optimal
if

    V <= (a0+b0)(I_min(n)+1)+(a0+2b0)n+H.                        (5)

The original-weight fixed-profile lower bound supplies the same safe
preflight rejection used by the affine constructor. A failed gate or
preflight invokes exact Knuth. The general worst case remains quadratic.

Building the bound need not sort n arbitrary values. Every signature run
has one key weight. Within it, q_(i+1)=c-q_i, so the gap weights alternate
between at most two values. For a run of length L, record its L key weights
as one (value,multiplicity) pair and its L left gaps as at most two such
pairs. Finally record q_n once. There are at most k key records and 2k+1
gap records. Sorting these O(k) records and expanding their multiplicities
costs O(k log(k+1)+n). The two-queue mixed bound then takes O(n). All gaps
at block boundaries occur exactly once.

Thus an accepted full solve takes O(nk) arithmetic work and O(n) auxiliary
space, including signature discovery, certification, and reconstruction.
The O(n) space claim applies to the shape optimizer and accepted path;
the current Knuth fallback retains its quadratic table.

## 5. An explicit full mixed-weight family with unrestricted block values

Let 0<=u_i,v_i<=M, where M>=1, and put

    B=4(n+1)^2 M,    p_i=B+u_i,    q_i=B+v_i.                     (6)

Let k be the number of runs of (u_i,v_i+v_(i+1)). Both kinds of weights
can vary, the key weights need not be constant across blocks, and the
gaps can alternate at every position. There is no affine-closeness or
small perturbation budget on these residuals. Construction of a full
optimal tree takes O(nk) arithmetic operations and O(n) auxiliary space.
In particular k=O(1) gives linear construction, and k=o(n) is subquadratic.

Proof of the global step: the residual mass above a0,b0 satisfies
R<= (2n+1)M. Every class candidate has residual cost at most (h+1)R,
which is strictly less than 2B<=a0+b0. Every tree outside the class pays
at least one extra unit of internal path length, with baseline penalty
a0+b0. Therefore (5) passes even if H is replaced by zero, and preflight
cannot reject. The class optimizer is an unrestricted optimum for these
inputs. All weights are positive. When M is polynomial in n, the inputs
and intermediate costs have O(log n) bits and the word-RAM bound follows.

The large baseline is a genuine limitation. This does not give O(nk) full
OBST construction for arbitrary weights merely because their signatures
have few runs. Inputs without that baseline may fail the gate and fall
back. Nor does small k imply that the affine corridor is narrow; the two
representations exploit different structures.

For an explicit warning against omitting the gate, p=(100,1,1,1),
q=(1,1,1,1,1) has only two signatures. Its best minimum-IPL shape costs
218, whereas its full optimum is 121. The gate correctly rejects. These
values agree with direct enumeration of all 14 four-key trees, cubic DP,
and Knuth; the signature compression alone does not fix the shape restriction.

## 6. A bounded routing policy preserves both representations

The initial matched experiment exposed roughly tenfold regressions against
Knuth when k=n: linear-space recomputation and generic window handling
have substantial constants. The final experiment retains this standalone
kernel as an explicit negative control. `portfolio_solve` first scans the
signatures. For k<=max(16,floor(n/32)), it uses the signature constructor;
otherwise it calls the existing affine constructor and its exact fallback.
This empirical threshold is not a correctness premise or an optimal policy.
All routes remain exact and their preprocessing is counted.

On family (6), the portfolio still has O(nk) arithmetic work: the signature
route certifies, while a rejected block count has k>n/32, so even quadratic
fallback is O(nk). However the portfolio does not retain the standalone
kernel's unconditional linear-space guarantee on that family; its affine
or Knuth route may use more space. The standalone `solve` remains available
for the full O(nk)-time, O(n)-space family theorem. On arbitrary weights,
either full solver has a quadratic worst-case fallback. The route avoids
using the signature kernel to solve the earlier affine family inefficiently.

## 7. Independent validation and measurement scope

The harness was written first. Its initial identity-only run checked 40
boundary count intervals, 1,365 direct tree/word costs using independently
enumerated slot expansions, and 228 block path-independence identities.
It subsequently checked all 120 feasible boundary/count reconstructions
in those short blocks and 1,000 forward/backward transfer vectors against
explicit word enumeration, including arbitrary negative profile values and
unreachable entries. These checks do not reuse the production sliding window.

The final M4 exact suite passes 1,023 complete standalone solves, 778 cubic
comparisons, 1,023 unrestricted shape-DP controls, 762 independent shape
enumerations, and 1,023 checks that multiplicity sorting equals ordinary
sorting. There are 366 certificates and 657 global-gate rejections, 411 in
preflight. Another 1,023 portfolio solves return the same exact costs;
912 select the signature route and 111 select the affine route. Eight
large portfolio controls also agree with their standalone counterparts.
Zeros, ties, large integers, geometric weights, non-affine block signatures,
and irregular one-key blocks are included. Both scaling families at n=1536
also match independent Knuth and the unrestricted shape DP.

The certified full constructor reaches 98,304 keys with four or sixteen
joint-signature blocks. It performs 2,621,448 or 12,058,760 window queries,
respectively, including all traceback recomputation. Both maximum profile
widths are 65,536. These widths are logical ranks, not measured peak bytes.
Full operation vectors are retained in `results/run_complete.json`; the
matched full-construction experiment is `results/run_complete_matched.json`.
Previous implementations and their source-hashed measurements are unchanged.

The final M4 benchmark uses Python 3.9.6, macOS 26.5 arm64 and exact
integers for every solver. Five cyclic execution orders cover portfolio,
standalone signatures, affine, full shape DP, and Knuth. Sixty matched
trials yield 300 complete constructions, with all preprocessing and output
reconstruction timed. At n=1536, median paired portfolio/Knuth ratios are
0.0259 for four blocks and 0.0961 for sixteen; portfolio/full-shape ratios
are 0.0893 and 0.3958, and portfolio/affine ratios are 0.0247 and 0.0981.
Each summary has five paired observations, not a ratio of median seconds.

The standalone fragmented-input regression remains visible: at n=1536,
kernel/Knuth ratios are 10.4922 on irregular large-baseline weights and
10.8220 on the alternating affine fixture. The portfolio ratios on these
inputs are 1.0612 and 0.0292. Ordinary random and geometric portfolio ratios
are 1.0687 and 1.0216, with exact fallback. The old full shape DP is still
better on the irregular large-baseline family: portfolio/full-shape ratios
are 1.9778 at n=768 and 3.1576 at n=1536. Routing is therefore useful but
not optimal on every input. On selected signature paths the portfolio runs
the same kernel plus an extra scan; subunit portfolio/kernel ratios are
timing variation, not algorithmic savings. The same qualification applies
to subunit fallback ratios against Knuth. These small Python experiments
do not establish optimized-library superiority; all trial vectors and
source hashes are retained.

A targeted prior-work search did not establish priority. Standard deque
maxima, fixed-shape depth structure, mixed lower bounds, and Hirschberg
traceback remain credited. The unrestricted objective still requires a
representation that supports varying signatures and taller optimal shapes
without paying for most of the interval table.
