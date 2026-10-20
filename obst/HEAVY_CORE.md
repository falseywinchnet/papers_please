# Joint heavy-outcome cores for full optimal BSTs

The single-gap separator fails on two comparable heavy gaps. This extension
selects several heavy outcomes together, keeps the keys required to distinguish
them as an ancestor-closed core, and solves the intervening intervals exactly.
All original key and gap weights remain in the objective. The sufficient
condition is conservative; its priority has not been established. The general
worst case is still quadratic.

## Selected outcomes and their necessary keys

For n>=1, choose a nonempty set H of positive-weight key or gap outcomes. Include in A
each selected key and the adjacent key(s) of each selected gap. An endpoint gap
has one adjacent key; an internal gap has two. Write m=|A|, theta=min weight(H),
and W_light for the total weight of every outcome outside H. Each key in A lies
on the search path to a selected outcome (possibly itself) in every BST: both keys bordering
an internal gap lie on that gap's search path.

Call a tree core-closed if no key outside A is an ancestor of a key in A.
Then A forms a top BST, with every intervening original interval attached to
one of its external gaps. Protected gaps remain singleton gaps because their
neighboring keys are in A. No selected outcome is inside a nonempty payload.

## A projection lemma that preserves all selected depths

Every tree can be reduced to a BST on A without increasing the depth of any
selected outcome. If the original tree is not core-closed, at least one
selected outcome becomes strictly shallower.

This is not simple deletion of comparisons at arbitrary nonretained keys:
a nonretained key can separate retained outcomes on both sides. The following
exchange supplies the missing argument.

Consider a subtree rooted at r outside A which contains some key in A. If
only one child contains A-keys, replace the root by that child. The other
branch contains no selected outcome: a nonempty subtree containing a selected
gap must contain at least one of its adjacent keys, and a selected empty child
gap would make r itself a member of A. Every selected outcome in the retained
child becomes shallower.

If both children contain A-keys, let a be the largest A-key in the left
subtree. Replace r by a, restrict the old left subtree to keys below a and
its endpoint gaps, and leave the old right subtree in place. There is no
selected outcome strictly between a and r: a selected key would be in A,
and a selected gap there would put another adjacent key in A before or at r.
All A-keys are retained. Selected left outcomes lose zero or more comparisons
under the contiguous restriction; right outcomes keep their depths. If a is
selected, it moves strictly upward. Otherwise a must border a selected gap
on its left: its right gap could not be selected because that would put a+1
in A, contradicting either maximality of a or r outside A. That selected left
gap loses the comparison at the old a. Thus at least one selected depth falls.
The exchanged tree can omit light keys; they will be reinserted later.

Repeat until no outside key has an A-key descendant, then discard the remaining
anchor-free branches. Each exchange reduces the number of outside keys and
retains A, so the process terminates. Selected gaps are preserved throughout.
The resulting A-tree proves the componentwise nonincrease and strict-saving
claim. The proof uses contiguous restriction only within the explicit exchange.

## Dominance certificate and exact composition

First consider a deliberately conservative bound. Reinsert each missing interval
as a balanced BST beneath the projected core. With L=ceil(log2(n+1)), every
light outcome costs at most m+L comparisons. Thus theta>=(m+L)*W_light suffices.
The implementation retains this option as `height_bound=False`, but its default
uses the following stronger argument.

Let W_H be the total selected weight and F_1=F_2=1. Define

    H = max { j in 1..m : F_j*theta <= W_H }.

Make a protected-only core instance: selected weights retain their values and
all other weights become zero. Every internal subtree in any core tree has
mass at least theta, because it contains an A-key and that key is an ancestor
of some selected outcome. The previously proved mixed-weight Fibonacci bound
says that a depth-d internal subtree in an optimum has mass at most
W_H/F_(d+1). Consequently every protected-only optimal core has height at most
H, including its external leaves.

If

    theta >= (H+L)*W_light,

there exists a core-closed optimum. Project any non-core-closed optimum: its
selected weighted cost decreases by at least theta. Replace the projected
core by an optimal protected-only core; this cannot increase its selected
weighted cost, although individual selected depths may change. Reinsert balanced
payloads, giving total light cost at most (H+L)*W_light. Since the old light
cost was nonnegative, the new full tree costs no more. Equality is allowed.

H bounds this protected-only witness, not the final full-weight core. The
constructor optimizes the latter without any height restriction. For k equal
selected weights, H is O(log(k+1)) rather than potentially 2k. The useful
improvement is in the sufficient certificate, not a deletion of light weights
from the final optimization problem.

Let the original intervals between A-keys (including the two end intervals)
have masses W_t and exact relative optimum costs C_t. Collapse each to one gap
of weight W_t, keeping each A-key's original weight. Then

    OPT(original) = OPT(core keys, collapsed gaps) + sum_t C_t.

At core-gap depth d, an attached payload contributes d*W_t+C_t. The two terms
in this formula are optimized independently, and reinsertion recovers every
original key. Empty intervals have C_t=0 and retain their original gap weight.

## Selecting a threshold without quadratic rescanning

The implementation chooses H as all outcomes of weight at least theta, with
theta drawn from the distinct positive input weights. A key i is in A exactly
when max(p_i,q_i,q_(i+1))>=theta. Call that maximum its activation weight.

Sort all outcome weights and all activation pairs. Sweep theta upward. Before
evaluating theta, mark as unanchored every key with activation weight strictly
below theta. The active unanchored runs are the payload intervals. A disjoint-set
structure merges neighboring runs, maintaining their total triangular state
count. Joining runs of sizes a,b increases this total by a*b; a new singleton
adds one. Union by size bounds each find by O(log(n+1)) even without relying on
an inverse-Ackermann analysis. The selected-outcome threshold and light mass
are handled in groups, so equal weights are never partly selected.

For every certified threshold, minimize

    tau(m) + sum_t tau(k_t),  tau(k)=k(k+1)/2.

This chooses the best full-Knuth state proxy among the checked thresholds,
not the minimum actual frontier runtime. Sorting and the whole sweep take
O(n log(n+1)) work and O(n) arithmetic storage. Fibonacci values through index n take O(n)
additions. During the upward threshold sweep, W_H/theta is nonincreasing;
a single decreasing index finds the largest feasible Fibonacci index in O(n)
total index decrements. Cap it by m for each threshold. Accept only a strict proxy improvement
on tau(n); otherwise use the previous separator constructor. A failed test
therefore adds O(n log n) screening work, not a failed quadratic solve.

## Exact kernels and bounds

Each payload and the core are solved exactly. The `kernel='frontier'` variant
uses the variable mass-frontier constructor; `kernel='knuth'` uses Knuth.
Both first check for uniform key weights and uniform gap weights. For constants
p,q, the cost is (p+q)*IPL+n*p+2n*q, so a balanced tree minimizing unweighted
internal path length is optimal and can be built in O(n) work. This familiar
uniform-weight fact is not claimed as a new algorithm.

If K(s) denotes the selected kernel work for an s-key component, a successful
core plan costs O(n log(n+1)+K(m)+sum_t K(k_t)), with sum_t k_t=n-m. The
frontier term includes its own parameter selection. Both variants retain
O(n^2) general worst-case work and O(n^2) worst-case storage. Payload scratch
can be reused sequentially, retaining only output trees between calls.

For k selected outcomes, m<=2k. With a uniform residual background, the work
is O(n log(n+1)+k^2): all payloads are uniform and the core can use its full
table. With all residual weights in [a,Ca] for fixed a>0 and fixed C, each
payload's local frontier costs O(s^alpha), alpha=1+log_(2*phi)(2)<1.59024.
This gives O(n log(n+1)+k^2+sum_t k_t^alpha). If payload sizes are at most B,
it is O(n log(n+1)+k^2+n*B^(alpha-1)). These bounds describe the certified
plan; a proxy-minimizing selector need not minimize this sharper expression.

For the preceding two-heavy-gap obstruction, all background weights are one
and q_1=q_(n-1)=n^3. At n>=5, m=4, W_light=2n-1, and
n^3 >= (3+bit_length(n))*(2n-1). Here the two equal selected gaps
give H=3 even though m=4. The four-key core and uniform payloads give
O(n log n), whereas the previous separator/frontier constructor selects all
n(n+1)/2 cells. For n<5 this particular placement has no nonempty intervening payload. Replacing
the background by bounded positive mixed weights and choosing sufficiently
large equal gap weights gives a certified O(n^1.59024) plan. These are scoped
improvements on full mixed-weight families, not a general subquadratic theorem.

## Verification

The projection checker enumerates every nonempty selected-outcome subset and
every tree shape through four keys. For all 1,937 non-core-closed cases it finds
a core-closed tree whose selected depths are componentwise no greater and
strictly smaller in at least one coordinate. The weighted harness checks
22,140 inputs with weights in {0,1,100} through four keys. All 17,054 qualifying
nontrivial threshold certificates match the minimum over all tree shapes and
the exact core/payload composition identity.

Another 2,640 full solves on 1,320 inputs through 32 keys use both kernels and
match independent cubic DP and reconstructed costs. On 520 small inputs, the
union-find selector matches a direct scan of every possible threshold and
its complete payload partition. A 30-fixture sweep through 2,048 keys compares
both kernels with Knuth and the previous separator constructor. It includes
ordinary random, near-uniform, geometric, single-key and single-gap spikes,
two heavy gaps, many heavy gaps, moderate heavy gaps at certificate equality, and mixed heavy
keys/gaps. The moderate fixture uses the protected-height bound and is designed
to fail the older size-based certificate. All weights are
retained; key-only and gap-only cases appear only as harness controls.

## Matched construction timings

Ninety matched trials use ten balanced orders per fixture: five cyclic rotations
and their reversals, not all 120 permutations. All 450 timed complete solves
include preprocessing and reconstruction; all costs agree and every output tree
is directly evaluated. The platform is Apple M4, Python 3.9.6. Each entry is a
median paired runtime ratio to Knuth; smaller is better. S is the previous
separator, CF/CK the new core with frontier/Knuth kernels, and RC the earlier
recursive contraction solver.

| n / Fixture | S | CF | CK | RC |
|---|---:|---:|---:|---:|
| 2,048 / random | 0.85643 | 0.86589 | 1.00373 | 1.02785 |
| 2,048 / near-uniform | 0.90215 | 0.85239 | 1.02368 | 1.04692 |
| 2,048 / two gaps, unit background | 0.97393 | 0.00700 | 0.00551 | 0.98506 |
| 2,048 / two gaps, random background | 1.01846 | 0.70676 | 0.79129 | 0.99945 |
| 2,048 / 45 heavy gaps | 0.84243 | 0.08905 | 0.03125 | 0.99792 |
| 2,048 / 45 moderate gaps | 0.81550 | 0.08573 | 0.03229 | 0.98979 |
| 2,048 / 45 mixed heavy outcomes | 0.87777 | 0.08823 | 0.03204 | 1.00118 |
| 512 / random | 1.68034 | 1.76764 | 1.03732 | 1.02439 |
| 1,024 / geometric | 0.00648 | 0.02255 | 0.02378 | 0.03135 |

The core improves cases where both previous solvers remain near Knuth. Knuth
kernels win on small payloads; frontiers help the large random payload. The
unit-background two-gap paths share uniform shortcuts and a tiny core, so their
timing difference is not an asymptotic distinction. At 512 random keys the
frontier path is slower than Knuth. On geometric input, threshold screening
adds cost before the same endpoint fallback. Sub-unit ratios on failed-core
controls do not demonstrate an algorithmic benefit. These are instrumented
Python measurements, not broad or production-language superiority claims.
The incomplete initial size-certificate timing batch was stopped after the
height refinement and is not used for these claims. All final observations
are in `results/heavy_core_matched.json`.

## Large full constructions

Full trees at 512, 2,048, 8,192, 32,768 and 65,536 keys on the unit-background
two-heavy-gap family match an independent four-key cubic optimum with
p=[1,1,1,1],q=[1,n^3,2n-7,n^3,1], plus the uniform payload cost
2*I_min(n-4)+3*(n-4). Every full tree is directly evaluated. The uniform formula
also matches independent cubic DP at n=0..16.

At 65,536 keys the exact cost is 1,407,374,885,846,941. The new full solve took
0.59933 seconds in one exploratory run. It used ten core cells, fifteen core
root candidates, 196,799 sorting comparisons, 65,535 Fibonacci additions,
65,535 height checks, 65,532 activations, 65,531 unions, 65,529 find steps,
and 196,609 uniformity comparisons. All 65,532 payload keys and four core keys
were constructed. The previous constructor was counted only: it selected
2,147,516,416 cells. No timing ratio to an unexecuted old solve is claimed.
Raw results are in `results/heavy_core_scale.json`.

The arithmetic model does not make a bit-complexity claim. In particular, this
prototype precomputes Fibonacci values through n even when a much shorter
prefix would suffice; that can produce large intermediate integers. Limiting
this table by the maximum relevant selected-mass ratio is a practical follow-up.
Raw `kernel_actual_height` and selected-depth metadata sum over kernel calls;
`plan_core_height_bound` describes the protected-only witness, not the final
full-weight core's height.
