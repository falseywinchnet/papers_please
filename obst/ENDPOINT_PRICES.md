# Exact endpoint prices and the limit of additive weight transfers

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. This extends the full mixed-weight investigation. The
unrestricted subquadratic problem and mathematical priority remain open.

## All cost-preserving additive transfers, not just one normalization

For n>=3, consider an additive change of the key/gap weights whose effect on
cost is independent of the chosen tree. Every such change has three degrees
of freedom: a common interior transfer, and transfers between either endpoint
key and its adjacent outer gap. In particular, define

    L=p_0+q_0, R=p_(n-1)+q_n,
    p'=(x, p_1-a, ..., p_(n-2)-a, y),
    q'=(L-x, q_1+a, ..., q_(n-1)+a, R-y).

Then C(T;p',q')=C(T;p,q)+an for every tree. These are exactly all such
additive transformations. Nonnegativity is equivalent to the box

    -min(q_1,...,q_(n-1)) <= a <= min(p_1,...,p_(n-2)),
    0<=x<=L, 0<=y<=R.

Sufficiency follows from the usual internal/external depth identity and
the endpoint equalities l_0=d_0 and l_(n-1)=d_n. To prove necessity, write
U_i=delta p_i+delta q_i and V_i=delta p_i+delta q_(i+1).
Rotating the two-key subtree on i,i+1 gives U_i=V_(i+1).
Comparing the same rotation with and without one additional key in the
outer left subtree gives U_i=0 for 0<=i<=n-3. The symmetric comparison
gives V_i=0 for 2<=i<=n-1. The first relations supply V_1=0 and U_(n-2)=0.
Thus all interior delta q values equal one a, every interior delta p=-a,
and the endpoint key/gap sums are unchanged. The constant cost difference
is an. All rotations used can occur inside a full tree on the original keys.

This characterizes additive transfers on the given outcome coordinates.
It does not characterize arbitrary data structures, nonlinear encodings,
or all possible lower bounds for OBSTs.

## The three-variable bound reduces to two endpoint prices

Let K be the key-capacity bound and A the exact alphabetic gap optimum.
Every admissible triple gives a valid bound

    F(a,x,y)=K(p')+A(q')-an <= OPT(p,q).

Set a*=min(p_1,...,p_(n-2)). A global maximum over the entire box is
attained on the face a=a*. This remains true even when an endpoint key
is much smaller than every interior key.

Proof: start at any feasible (a,x,y), increase a by delta, and replace
x,y by max(0,x-delta), max(0,y-delta). Consider a segment on which e of
the endpoint residual keys are clamped at zero, e in {0,1,2}. Before
reaching a*, all interior residual keys are positive. The remaining
n-e positive keys decrease uniformly, so K has slope -M(n-e), where
M(k) is the minimum sum of k unit key comparison lengths. Every gap
except those e endpoints increases at unit rate. The minimum sum of
their depths is E(n+1-e)+e, by the binary-indicator/zero-run lemma.
Since E(n+1-e)+e=M(n-e)+n, every affine tree term in F has nonnegative
slope on this segment. Their minimum is nondecreasing, and continuity
joins the segments. Thus moving to a* cannot reduce F.

At a=a*, maximize the concave piecewise-affine function F(x,y) over
[0,L] x [0,R]. This maximum is at least the previous shifted bound,
although a limited search need not reach it and deterministic alphabetic
tie-breaking can still miss a feasible equality witness.

## Exact separation, bounded work, and integer-cost certification

At a price (x,y), construct an alphabetic optimum for q' and assign the
residual key multiset to the capacity lengths in decreasing weight order.
Let lambda_i be those assigned lengths and d_j the alphabetic gap depths.
This supplies F(x,y) and the globally valid supporting plane

    F(X,Y) <= c + (lambda_0-d_0) X + (lambda_(n-1)-d_n) Y,

where c is evaluated exactly from the fixed interior weights and depths.
This plane is an upper bound on the concave *bound function*. F(x,y)
itself is a lower bound on the full optimum. These directions must not
be interchanged. The original ordered cost of the constructed alphabetic
tree supplies a feasible upper bound on OPT.

The implementation maximizes the minimum of the planes seen so far.
It enumerates vertices of their three-dimensional hypograph intersected
with the endpoint box, using integer determinants and Cramer's rule.
All feasibility and objective comparisons are exact integer cross-products;
only the returned price and value are represented as Fractions. There is
no floating-point optimizer or tolerance-based optimality decision.

The best sampled lower bound and the best original tree cost are retained
across calls. For integer original weights, if ceil(best lower)=best tree
cost, the tree is fully optimal. If the LP upper bound on max F equals
the best sampled F, the price maximum has been proved. Otherwise the
search may be stopped at its declared call budget; that does not imply
price optimality. Early full-tree certification also need not complete
the price search. Result metadata distinguishes these conditions.

With b oracle calls, complete preprocessing, pricing, and candidate
construction take O(b n log(n+1)+b^5) arithmetic operations and O(n+b)
space. Each alphabetic call is O(n log n), and the elementary exact LP
checks O(b^3) triples against O(b) constraints per call. The default
b=max(2,bit_length(n)) gives O(n log^2(n+1)+log^5(n+1)) work, asymptotically
O(n log^2 n), for the attempted certificate. On rejection, solve uses
exact Knuth and remains quadratic in the unrestricted worst case.
The tiny n<3 case is solved directly. The earlier portfolio is unchanged.

Every supporting slope is an integer of magnitude O(n), and each intercept
is an integer of magnitude O(nW), for total original mass W. Thus LP
vertex denominators are O(n^2), and the scaled alphabetic calls use weights
with only O(log n) additional bits. These are arithmetic-operation bounds;
bit costs remain additional. The finite uncapped search has no proved
small iteration bound here, so it is used only as a diagnostic oracle.

## A four-key obstruction for the entire transfer class

Take

    p=(1,1,2,1), q=(1,2,1,1,1).

The full optimum is 24. With every original weight set to one, the cost
is at least 20. The two extra units add l_2+d_1. If key 2 is the root,
gap 1 has depth at least 3, so this sum is at least 4. Otherwise l_2>=2
and the internal gap has depth at least 2, again giving at least 4.
Root 1, left child 0, and right child 2 with right child 3 attains 24.

The maximal interior shift is a*=1, L=R=2. At any prices the transformed
vectors are

    p'=(x,0,1,y), q'=(2-x,3,2,2,2-y).

The key-capacity assignment (2,3,1,2) gives K(p')<=2x+1+2y.
The feasible alphabetic gap depths (2,2,2,3,3) give
A(q')<=26-2x-3y. Hence

    F(x,y) <= 23-y <= 23.

At x=y=0, K=1 and A=26. For the latter, five gaps of weight two cost
at least 2E(5)=24, and the extra unit on the internal gap costs at least
two; the displayed depths attain 26. Therefore max F=23 exactly.

The maximal-shift theorem and exhaustive characterization of transfers
show that **no nonnegative additive reweighting preserving relative tree
costs can make this K+A certificate exact on this instance**. Integer
rounding cannot close the gap. The obstruction already has only one
positive residual interior key after normalization. It is not a lower
bound against a different algorithm or richer joint representation.

The obstruction is robust, not a tie artifact. Perturb each of its nine
weights by at most epsilon=1/100. The interior minimum remains p_1. The
same key assignment and gap tree give max F at most

    2p_0+2p_1+p_2+3p_3+2q_0+2q_1+2q_2+3q_3+3q_4.

The coefficients sum to 20, so this is at most 23+20 epsilon. Every
four-key tree has unit-weight full cost at most 24, so its perturbed
original cost is at least 24-24 epsilon. The entire box therefore has
OPT-max F >= 1-44 epsilon > 0. All 512 integer corners of 100(p,q)+/-1
are independently checked; the observed minimum gap is 94, above the
proved lower bound 56. An all-distinct integer example is
p=(996,997,1998,999), q=(1000,2001,1002,1003,1004): full OPT=23999 and
max F=23004, a gap of 995. Its constant supporting plane certifies the
price maximum in one call.

## Positive family with nearly all weights distinct

Let h>=3, B=2^h, n=B-1. Use the perfect tree, whose key comparison lengths
are l_i=h-v_2(i+1). Set

    p_i=B+(h+1-l_i)B+i,

then replace p_0=p_(n-1)=1 and p_2=B. Set q_0=B, q_n=B+n, and q_j=j+1
for 1<=j<n. There are n-1 distinct key weights and n+1 distinct gap
weights; every weight is positive and has O(log n) bits.

At a*=B, x=y=0, exactly three bottom residual keys are zero. The other
n-3 residual keys attain the capacity profile and decrease by depth.
Every transformed gap equals B+j+1, in the interval [B+1,2B]. With B
a power of two, an unrestricted Huffman construction pairs nodes level
by level: each generated mass exceeds every unmerged mass at the same
level because max weight < 2 min weight. All B gap depths are h. The
perfect alphabetic tree attains this unrestricted optimum, so it is
alphabetic-optimal as well. It attains both transformed bounds and is
therefore a full mixed optimum. The first pricing call certifies it;
no LP vertex enumeration or interval-DP cells are needed.

Its exact cost is

    ((8h-11) B^2 + (13-7h) B)/2 - 1.

This follows by summing the perfect capacity lengths and squared lengths,
using symmetry for sum i*l_i, and applying the three bottom-key corrections.
The independent explicit tree evaluator checks the same closed form.

The preceding uniform shift is only min(p)=1. Its lower bound cannot
equal the full optimum: in the last four shifted gaps, the two
left weights sum to 2B-3 while the rightmost weight is 2B. Replacing their
balanced four-leaf subtree by the right-heavy alternative saves three.
The perfect tree already attains the old residual key-capacity bound.
Thus the balanced full optimum exceeds the old K+A shifted bound by at
least three, for every h>=3. The new endpoint treatment strictly extends
that certificate on a family with linearly many distinct keys and gaps.

Twelve full constructions reach n=262143, with 262142 distinct keys,
262144 distinct gaps, and full cost 4569830391807. The old bound is
4561240391642, a deficit of 8590000165. The largest new run uses one
alphabetic call, 262143 merges, 7111153 priority comparisons, 8924411
heap-item comparisons, and 1482369 key-sort comparisons. All fixed scans,
heap events, depth recovery, and full output visits are recorded. Seven
sizes through 511 keys match Knuth, and three also match cubic.

## Independent evidence and limitations

The independent harness was written before the price search. It enumerates
every tree-cost vector through eight keys, checking 2052 transfer identities
and exact ranks: the difference span has rank 2n-2, leaving nullity three.
The necessity proof above is not inferred from those finite ranks.
For 60 instances with three or four keys, it independently builds the
arrangement of every alphabetic-tree and key-rank breakpoint, evaluating
5111 exact candidate points. All maxima agree with the cutting-plane search.

On 600 mixed instances through 64 keys, 1712 individual alphabetic oracle
values match independent cubic values; small cases also match literal
trees. All 600 bounded full solves match cubic, Knuth, and direct tree cost.
The bounded search certifies 220, including 152 previous rejections, and
falls back on 380. The uncapped diagnostic certifies 228, rescues 160,
and completes every price maximum within ten calls in this suite. No
small iteration bound follows. There are 358 strict bound gaps, and 600
independent clamped-transfer monotonicity checks pass.

Coordinate reduction takes 19 exact controls to obtain the four-key
obstruction. Another 6000 seeded positive cases search for nonintegral
maxima; none is found. This finite observation is not an integrality
theorem. Intermediate prices can be fractional: the obstruction search
queries y=1/3 and obtains F=68/3. Correctness uses exact rational arithmetic
and does not assume integral maxima.

All scripts, witnesses, counters, source hashes, and M4 commands are
retained. The benchmark includes random, near-uniform, geometric, and
old-shortcut controls, including full pricing and fallback overhead.
There are 80 matched trials and 320 complete constructions in four cyclic
orders, on Apple M4 / Python 3.9.6 / macOS 26.5 arm64. At 511 keys, median
paired priced/Knuth ratios are 0.12608 for the new family, 1.30491 random,
1.15055 near-uniform, and 1.08209 geometric. Old profile, four-signature,
and affine routes are 14.64, 42.65, and 37.44 times the previous portfolio;
the 319-key old multilevel route is 8.54 times that portfolio. Those
regressions remain explicit and the old portfolio is not replaced.
Initial load averages were 10.97/11.34/11.74, ending at 11.44/11.44/11.77.
Four observations per row and same-process cycling under load do not
establish precise isolated-machine speedups. Arithmetic proofs and full
logical counters establish scaling, with bit costs additional.
The unrestricted objective remains active: the four-key obstruction
shows exactly why maximizing this separable bound cannot finish it.
