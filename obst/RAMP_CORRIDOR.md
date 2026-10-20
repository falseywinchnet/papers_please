# Certified pruning around affine weight profiles

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. This is an exact full mixed-weight constructor on the
certified families below, and an exact fallback algorithm on other inputs.
The unrestricted subquadratic question and mathematical priority remain open.

The preceding ruler example showed that a quadratic Monge core can hide a
compact formula. Here the affine structure instead bounds which states of the
minimum-internal-path-length shape DP can participate in an optimum. It does
not require a sparse cost matrix, and it does not assume that perturbing the
weights preserves the reference tree.

## 1. Affine cost becomes an additive potential on bottom slots

Write h=floor(log2(n+1)), S=2^h, s=n-(S-1), z=S-s. A minimum-IPL shape
expands exactly s of the S slots of a perfect skeleton. Its reference shape
expands slots 0,...,s-1. The earlier exchange identity says that moving an
expansion one position to the right across skeleton key g costs

    (1+v_2(g+1)) (p_(i+1)-p_i) + q_(i+2)-q_i.

Choose nonnegative slopes lambda, mu and the affine reference weights
pbar_i=lambda*i, qbar_i=mu*i. Constant intercepts can be omitted because
their contribution is the same for every shape in this class. Put

    gamma = lambda+2*mu,
    F(g) = (2*lambda+2*mu)g - lambda*popcount(g),   F(0)=0.

Since sum_(t=1)^g v_2(t)=g-popcount(g), F(g+1)-F(g) is exactly the
rightward exchange cost gamma+lambda*v_2(g+1). Thus, for a selected slot
set A of size s, its affine cost above the reference is

    G(A) = sum_(g in A) F(g) - sum_(g=0)^(s-1) F(g).                 (1)

For gamma>0, this is at least gamma times the inversion count: the number
of unexpanded slots preceding expanded slots.

## 2. A signed residual profile bounds all possible improvement

Let delta_p=p-pbar, delta_q=q-qbar. These analytical residuals may be negative;
the actual problem weights remain nonnegative. Every minimum-IPL shape has
the same multiset of key comparison lengths and gap comparison lengths.
Therefore the rearrangement inequality gives a lower bound L_delta by
assigning the largest residual weights to the shallowest positions, separately
for keys and gaps. This remains valid for signed residuals.

If delta_p^down and delta_q^down are sorted in descending order, then

    L_delta = sum_(i=0)^(n-1) delta_p^down_i * bit_length(i+1)
              + h sum_i delta_q_i
              + sum(the smallest 2s entries of delta_q).             (2)

The final term is zero when s=0. Let T0 be the left-filled reference and set

    V = cost_delta(T0) - L_delta >= 0.                               (3)

For a class-optimal shape T*, comparison with T0 gives

    G(T*) <= cost_delta(T0)-cost_delta(T*) <= V.                      (4)

Adding any constant to all key residuals or all gap residuals changes both
terms in (3) equally. Thus V is independent of the intercept choice.
It is computable in O(n log n) including sorting and reference construction.

## 3. An exact state lower bound leaves a hyperbolic corridor

After a prefix of the slot sequence, let a be the number of zeros already
used and b the number of ones still required. Its grid coordinates satisfy
0<=a<=z and 0<=b<=s. Among all completions through this state, increasing F
makes the earliest available slots optimal within each side of the prefix.
The exact minimum affine cost above the reference is therefore

    K(a,b) = sum_(t=s-b)^(s-1) [F(t+a)-F(t)].                         (5)

With prefix sums P(t)=sum_(g=0)^(t-1) F(g), evaluate it in constant time:

    K(a,b) = P(s+a)-P(s-b+a)-P(s)+P(s-b).

Every prefix of T* must satisfy K(a,b)<=V. Hence deleting all other states
preserves at least one class optimum. The retained DP still charges the
original full key and gap weights on its transitions. It is not optimizing
the affine approximation. Paths retained unnecessarily cannot invalidate the
answer: they are still feasible shapes in the original class.

For gamma>0, K(a,b)>=gamma*a*b. Put D=floor(V/gamma). The retained state
count is bounded by

    S+1 + sum_(a=1)^z min(s, floor(D/a))
      <= S+1 + min(s*z, D*bit_length(z)).                            (6)

The first term counts the two boundary segments. The last inequality follows
by grouping the harmonic sum into dyadic blocks. Prefix F and popcounts take
O(n) work. Each state has at most two transitions, and stored predecessors
reconstruct all n keys. Consequently exact class optimization takes

    O(n log(n+1) + min(n^2, D log(n+1))) time,
    O(n + min(n^2, D log(n+1))) auxiliary space.                     (7)

If gamma=0 and V>0, the safe bound is the full shape grid. If V=0, T0 is
already class-optimal and can be returned directly. A perfect skeleton
(s=0) has only one shape and bypasses fitting and DP.

The implementation tries the original and reflected orientations, and chooses
the smaller certified state bound. `solve` caps this bound at
n*bit_length(n)^2 before starting DP; otherwise it goes directly to Knuth.
This cap controls unsuccessful attempts. `optimize_shape` also exposes an
unbudgeted mode for the general bound (7). Neither mode discards a state
without a proved lower bound. A failed global certificate still uses Knuth.

There is also an exact preflight rejection. Let L_class be the order-free
minimum-IPL profile cost on the original weights, and let L_out be the
existing lower bound used by the global certificate. If L_class>L_out,
no class-optimal candidate can pass that certificate, since its cost is at
least L_class. The solver can go directly to Knuth before fitting or building
a shape DP. This does not assert that the optimum lies outside the class;
it proves only that this sufficient certificate cannot succeed. The sorted
lists and residual bound are reused if preflight passes. The optional
`preflight=False` mode retains the unfiltered algorithm as a matched control.

## 4. Robustly recover integer slopes without trusting endpoints

For a weight list of length N, let m=floor(N/2). Form the m disjoint secants
w_(i+m)-w_i, i=0,...,m-1, take their median, divide by m, round to the nearest
integer, and clip to zero if negative. This costs O(n log n) with the counted
comparison sort used in the implementation. An odd final item is unused in
this fit, but remains in every cost and certificate.

Suppose w_i=A+lambda*i+u_i with integer lambda>=0 and E=sum|u_i|. Disjoint
pairing makes the sum of secant errors at most E. Thus the median differs
from lambda*m by at most E/ceil(m/2). If E<=n and the original instance has
n>=32 keys, both the key and gap fits recover their unit slopes exactly.
For unit-amplitude errors, each secant error is at most two, which also
guarantees recovery at these sizes. This is a robust estimate used to obtain
a favorable bound, not a correctness assumption: arbitrary fitted slopes
still give valid potentials, residuals, and pruning inequalities.

## 5. Full mixed-weight guarantees with arbitrary signed perturbations

Let n>=32 and B=4(n+1)^3. Consider

    p_i=B+i+u_i,     q_i=B+i+v_i,                                   (8)

with integer perturbations. Both kinds of weights may vary at every position;
they need not remain monotone. The following are guarantees for a globally
optimal full tree, not merely a height-restricted tree.

### Total perturbation magnitude at most n

If E_p+E_q=sum|u_i|+sum|v_i|<=n, construction takes O(n log^2(n+1)) time
and space, including the input scans, inferred slopes, signed profile,
global certificate, and complete reconstruction.

Proof: the forward fit gives lambda=mu=1 and gamma=3; selecting the better
orientation cannot increase the certified state bound. All key comparison
lengths in the class lie between 1 and h+1, and all gap lengths between h
and h+1. Therefore V<=h*E_p+E_q<=hn, including the relaxed profile (2).
Equation (6) gives O(n log^2 n) states and is below the default state budget.

It remains to establish full optimality. Let a0=min(p), b0=min(q), and
R0=sum(p-a0)+sum(q-b0). Then

    a0+b0 >= 2B-n,
    R0 <= n^2+(n+1)E_p+(n+2)E_q <= 2n^2+2n.

The residual cost of any minimum-IPL candidate is at most (h+1)R0, which
is at most 2n(n+1)^2 and is strictly smaller than 2B-n. Thus the existing
global gate passes even if its residual-Huffman lower bound is replaced
by zero. Every tree outside the class pays at least one additional unit
of internal path length, with baseline penalty a0+b0. The computed
class optimum is therefore a global optimum. All weights are positive and
use O(log n) bits. The claimed arithmetic bound is a word-RAM bound for
this family; no unbounded-real arithmetic advantage is being hidden.

### Every perturbation has magnitude at most one

If instead |u_i|<=1 and |v_i|<=1 independently at all positions, construction
takes O(n log(n+1)) time and O(n log(n+1)) auxiliary space. The total
perturbation may now exceed n.

Proof: again the forward slopes are recovered. Let rho_p and rho_q be the ranges
of the key and gap residuals. For the key depth deficits from h+1,

    Q = sum_i (h+1-key_length_i) = 2S-h-2.

The profile's possible gain on keys is at most rho_p*Q. For gaps it is at
most rho_q*min(2s,z), using either the deeper set or its complement. Hence

    V <= rho_p*(2S-h-2) + rho_q*min(2s,z) < 6S,

because both ranges are at most two. Therefore D<2S and (6) gives O(n log n)
states, below the default budget for n>=32. Here a0+b0>=2B-2 and
R0<=n^2+4n+2<=2n^2+2n, so the same global-gate argument applies.

More generally, the range bound makes (7) O((1+A)n log n) when residual
ranges are O(A), slopes are recovered, gamma is bounded below, and the
state budget permits the computed corridor. This parameterized observation
does not assert global optimality without the separate certificate.

## 6. A positive witness that the tree must actually change

For n=24, B=62,500, p_i=B+i+(-1)^i and q_i=B+i, the left-filled tree costs
13,252,388. Moving its expansion at slot 7 to slot 9 uses two adjacent
exchanges and produces cost 13,252,387, which independent exact DP verifies
is optimal. The previous all-one-direction exchange condition rejects this
input. The new corridor DP finds the better tree and certifies it globally.
Thus the perturbed-family guarantee does not follow from keeping a fixed
reference tree or merely checking a few rotations.

## 7. Validation and scope

The harness independently enumerates slot expansions by constructing tree
shapes, not by reusing the production depth-sequence builder. It verifies
the affine cost formula, minimum cost through each prefix state, signed
profile lower bounds, and retention of optimal paths. Full solves are checked
against Knuth, cubic recurrence, direct tree costs, and the old unrestricted
shape DP. Concentrated endpoint errors, the unused odd fitting endpoint,
both orientations, negative analytical residuals, zeros, ties, geometric
weights, near-constant weights, and ordinary random weights are included.

The first run reached the geometric control and stopped because a progress
print indexed a missing zero-valued counter after converting Counter to dict.
The print was corrected to use a zero default; no cost mismatch preceded it.
The complete suite was rerun after adding the amplitude-bound theorem and
an explicit state-budget rejection control.

Initial matched measurements exposed wasted shape work on random/geometric
inputs whose global gate subsequently failed. This led to the preflight
test above. The final source-hashed experiment retains an unfiltered control
and uses four cyclic execution orders, one for each complete constructor.

Exact totals and matched full-construction observations are recorded in
`results/ramp_complete.json` and `results/ramp_complete_matched.json`.
The final suite passes 1,166 full solves (802 cubic controls), 1,107 unrestricted
shape-DP comparisons, 782 independent shape enumerations, 819 affine shape
cost checks, 579 minimum-prefix-regret checks, 819 signed-profile checks,
299 optimal-prefix retention checks, and 1,383 direct exchanges. It includes
280 robust-slope recovery pairs and 42 concentrated-perturbation solves.
There are 535 certificates, one budget rejection, and 630 global-gate
rejections, including 391 in preflight. The 802 unfiltered controls agree
in both exact cost and certificate outcome.

On alternating key perturbations, actual corridor states at n=1536, 6144,
24576, 98304 are 4,270, 19,947, 91,251, 410,752. The corresponding full
shape-grid counts are 263,168, 4,198,400, 67,125,248, 1,073,807,360; Knuth
table counts are 1,180,416, 18,877,440, 302,002,176, 4,831,887,360. The dense
counts are formulas, not executions at the largest sizes. Independent
Knuth and full-shape controls cover both scaling families at n=1536.
The larger solves use the exact certificate and direct tree-cost checks.
At 98,304 keys the alternating instance improves on the reference by 13
cost units; independent unit perturbations of both lists use 411,924 states.

The M4 matched run uses Python 3.9.6, macOS 26.5 arm64, exact integers,
40 matched trials and 160 full constructions. Four cyclic orders cover
every solver position once in each size/family group. At n=1536, the median
paired corridor/Knuth ratios are 0.0284 (alternating keys), 0.0364 (random
signed total-magnitude perturbation), and 0.0320 (independent unit errors
in both lists). Corresponding corridor/full-shape ratios are 0.0818, 0.1091,
and 0.0995. Each is a median of four paired ratios, not a ratio of medians.

Ordinary random and geometric controls reject in preflight and run Knuth.
At n=768, the corridor/Knuth ratios are 1.1247 and 1.0110; ratios versus
the unfiltered solver are 0.6017 and 0.5570. Preflight avoids 66,048 wasted
shape states and 131,582 transitions per such input. At n=1536 the two
corridor/Knuth ratios are 0.9962 and 0.9777. These subunit fallback ratios
reflect timing variation, not an algorithmic advantage over Knuth; the
unfiltered control already rejects the larger grid by its budget. Full
counter vectors, source hashes, and every timed trial remain in the JSON.
These small Python measurements are not comparisons against optimized
implementations of other published algorithms.

The old minimum-IPL shape characterization, residual-Huffman certificate,
and earlier algorithms remain credited. The prior core backend's negative
timings remain unchanged. This establishes new proved regimes within this
project, not priority over all earlier restricted-weight algorithms. The
full unrestricted objective remains active.
