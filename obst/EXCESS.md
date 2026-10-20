# Exact bounded-excess construction by aligned dyadic intervals

This is a full mixed-weight optimizer over a certified candidate class.
Every key retains its fixed inorder position and weight. A separate lower
bound either certifies global optimality or the constructor falls back to
Knuth. The general subquadratic objective remains open.

## Why expand the shape class

The ordered-residual experiment tried 32 multiplier iterations at two
baselines, both with and without a forced unique root. All 480 small
exclusion-bound checks passed, but none of 24 near-uniform fixtures was
newly certified. At n=512 one chain call sequence used 261,120 key-depth
cells, or 522,240 for the two-pass root version, versus 131,328 Knuth states.
These count different operations and do not imply timing superiority.

An attempted obstruction then exposed a candidate-class limitation. Set
n=2^h-1, every gap weight to A, and every key weight to A except keys
8j+1, which have weight A+1. At n=255 and A=16 the perfect-tree cost is
61,680, whereas the full optimum is 61,656. Its internal path length is
only two units above the minimum. The intended assertion that the perfect
tree stayed optimal failed; the corrected harness preserves both costs.
Thus a better exclusion bound alone cannot solve this family using only
minimum-path-length candidates.

## Dyadic representation, with key costs retained

Write N=n+1, h=floor(log2 N), S=2^h, r=N-S, and s=min(r,S-r).
An ordered full binary tree is equivalently a tiling of [0,1] by consecutive
aligned dyadic intervals. Gap i at depth d_i occupies width 2^(-d_i).
Alignment is essential: a leaf starting at x must satisfy x/2^(-d_i)
integer. Tiling the entire unit interval by such disjoint intervals gives
a complete prefix code, hence a unique ordered full tree.

At grid height H, let Y be an interior boundary in units of 2^(-H).
The key at that boundary has comparison length H-v2(Y). Therefore a
left-to-right DP can charge q_i*d_i for each gap and p_(i-1)*(H-v2(Y))
at its starting boundary. It does not discard internal weights.

## A nonnegative potential bounds the state space

Use widths w_i=2^(h-d_i), so the total width is S. Define

    f(d)=d-h-2+2^(h+1-d)=d-h-2+2w.

For integral d, f>=0, with zeros exactly at h and h+1. Since the minimum
external path length is h*N+2r and external path length equals IPL+2n,

    sum f(d_i) = IPL-I_min.

Thus restricting excess to k bounds the accumulated nonnegative potential
by k. Every allowed depth is at most H=h+k+2. Only O(k+1) integer depths
have f(d)<=k: O(k+1) on the deep side and O(log(k+1)) on the shallow side.

For each allowed depth the inequalities

    1/2-f(d)/2 <= w <= 1+f(d)

hold. After i leaves, apply these inequalities to both the prefix and its
remaining suffix. The cumulative position y must lie in

    max(i/2-k/2, i-r-k) <= y
        <= min(i+k, (S-r+i+k)/2).

The interval has width O(s+k). This is a bound on all trees in the class,
not a heuristic beam or an assumption about the weighted optimum.

Set K=2^(k+2). DP states are (i,u,z), where u=K*(y-i) is integral drift
and z=K*sum f is spent potential. A gap of depth d has integer width
W=2^(H-d), requires alignment (i*K+u) mod W=0, and updates

    u' = u+W-K,
    z' = z+K*(d-h)+2*(W-K).

Keep 0<=z'<=K*k and the position band above. Start at (0,0,0), finish
after N leaves with u=-r*K, and minimize over all allowed z. For fixed u,
z is congruent to 2u modulo K, so there are at most k+1 possible z values.
The number of states per stage is therefore

    O((s+k+1)*(k+1)*2^k).

Each state tries O(k+1) depths. Exact optimization and reconstruction take

    O(n*(s+k+1)*(k+1)^2*2^k) arithmetic work,
    O(n*(s+k+1)*(k+1)*2^k) space with all backpointers.

For fixed excess and logarithmic s this is O(n log n). If s is proportional
to n it is quadratic even at zero excess. Increasing k without a fixed
budget is exponential; this is not a general subquadratic algorithm.

## Sharper perfect-size specialization

When N=S, use f_0(d)=d-h+(3/2)*(2^(h-d)-1). This is nonnegative on integer
depths, vanishes only at h, and also sums to excess. The inequalities
|2^(h-d)-1|<=2f_0(d), together with zero total drift, give |y-i|<=k.
Now H=h+k+1, K=2^(k+1), and z=2K*sum f_0. The updates and congruence become

    z' = z+2K*(d-h)+3*(W-K),  z congruent to 3u modulo 2K.

This reduces the implemented state count while keeping the same bound
above with s=0. Every tree in the excess class is still represented.

## Full-problem exclusion certificate and fallback

Let C_k be the optimum just computed. Set a=min p, b=min q, and let H'
be the order-free mixed-node Huffman bound for residual weights p-a,q-b.
Every tree outside the candidate class has cost at least

    B_k=(a+b)*(I_min+k+1)+(a+2b)*n+H'.

If C_k<=B_k, the returned tree is globally optimal. Otherwise use Knuth.
Sorting and the two-queue residual bound are fully counted. `excess.solve`
uses k=2 by default and only attempts the DP if s<=bit_length(n); other
sizes go directly to Knuth. With fixed k its attempted work is O(n log n)
and worst-case total work remains O(n^2). It does not assume success from
near-uniformity, and failure to certify does not return a restricted optimum.

## Verification and prior work

The generalized implementation passed 1,200 comparisons of restricted
optima against all tree shapes through eight keys, using budgets 0..4,
and 3,000 mixed-weight inputs through thirty keys checked against cubic
DP. The latter check the heap and counted two-queue bounds independently,
every successful certificate, and full construction with fallback.
Additional adversarial families include zeros, geometric weights, spikes,
and key-only/gap-only controls. Raw results are in `results/excess.json`.

The dyadic/prefix-code interpretation and sequential frontier DPs are
established ideas. Becker's 2010 paper explicitly gives a sequential
full mixed-weight DP for near-minimal height in O(n^2). The result here
uses excess *total unweighted path length* to bound the position band;
it does not claim to improve that different height-restricted problem.
The potential, band proof, and certificate were derived in this project;
priority has not been established by a comprehensive literature review.

Reference: https://arxiv.org/abs/1011.1337.

## Operation evidence

At n=1,023 on the periodic A=16 fixture, budgets 0 and 1 return the
suboptimal candidate 312,464. Budget 2 returns 312,154, equal to Knuth,
and certifies it with an exclusion bound 312,185. It uses 27,570 states,
137,835 transition checks, 6,052 sorting comparisons, and 1,022 two-queue
merge comparisons, versus 523,776 interval states and 1,046,532 root
candidates for Knuth. Reconstruction includes all 1,023 keys.

At n=1,024 with seeded amplitude-4 perturbations, budget 2 uses 48,003
states and 240,000 transition checks, plus 13,784 sorting and 1,264 merge
comparisons. It certifies cost 19,477,996. Knuth uses 524,800 states and
1,051,208 root candidates. These are separately reported operation types,
not a conversion of all work into a single unit. Larger perturbations
can still fail the exclusion bound even when the candidate is optimal.

The generalized sweep retains 65 fixtures at budgets 0..3; the correctness
run also retains all 104 adversarial-family checks. The mathematical state
band admits direct array indexing; the Python implementation uses sparse
dictionaries. Arithmetic bounds exclude arbitrary-precision bit costs.

## Matched timing with failure controls

Six trials per fixture use all six orderings of Knuth, the preceding
baseline-price hybrid, and the excess-two constructor, on identical
inputs within each trial. All preprocessing and reconstruction are timed;
every output is checked afterward. These are Apple M4/Python3.9.6 results.

| Fixture | Median excess-two/Knuth time | Certified trials |
| --- | ---: | ---: |
| n=1,023, amplitude4 | 0.23600 | 6/6 |
| n=1,024, amplitude4 | 0.44831 | 6/6 |
| n=1,023, periodic A=16 | 0.20790 | 6/6 |
| n=2,047, periodic A=16 | 0.17101 | 6/6 |
| n=1,023, ordinary random | 1.34949 | 0/6 |
| n=2,047, amplitude16 | 1.13631 | 0/6 |
| n=768, near-uniform width control | 0.93148 | 0/6 |

The skipped n=768 case runs the same Knuth routine after a constant-size
width check; its apparent gain is measurement variation, not an algorithmic
improvement. Periodic fixtures are identical repetitions, while random and
perturbation fixtures vary between trials. The large failure overhead on
ordinary random data is material. These are exploratory timings, not broad
speed guarantees. All 42 matched observations and operation counts are
retained in `results/excess_matched.json`.
