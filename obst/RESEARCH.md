# Full optimal binary search trees: research record

Started 2026-10-18, America/Chicago. Research and exposition by OpenAI Codex
Sydney, with sponsorship and problem selection by the repository owner.

## Objective and status

Find a substantively useful improvement for the full optimal binary search tree
problem, or prove an appropriate barrier to subquadratic construction. The
general exact subquadratic problem remains unresolved by this project.
The current checkpoint combines exact certificates and frontiers with an
implemented core-sparse Monge construction. Its centered extension gives
O(n(1+sqrt(R)) log^3(n+1)) arithmetic work for polynomial integer deviation R
above constant key and gap baselines, independently of baseline magnitudes
in the operation count. Bit costs still depend on representation length.
The compiled compact backend loses to Knuth in all 90 published scaling
trials; representation bounds do not establish practical superiority. The
unrestricted objective and mathematical priority remain unresolved.
The latest audit proves that positive near-uniform ramp weights can have
quadratic Monge and fourth-difference support while still admitting a compact
exact interval formula and linear tree construction. An adjacent-exchange
condition also removes wide last-level shape DPs on certified inputs. These
are a representation barrier and a conditional exact shortcut, not a general
lower bound or unrestricted subquadratic construction.
The next constructor uses the affine structure to prune the minimum-IPL
shape grid by an exact regret lower bound. Near p_i=q_i=4(n+1)^3+i, arbitrary
signed perturbations of total magnitude at most n admit O(n log^2 n) full
construction, while independent unit perturbations on all keys and gaps
admit O(n log n). The global certificate is proved to pass for these
families, including nonmonotone inputs and changes of optimal tree shape.
Joint-signature blocks now give an O(nk)-time, O(n)-space class optimizer
and an explicit full certified family with arbitrary non-affine residuals.
The signature is (p_i,q_i+q_(i+1)); raw gaps may alternate within a block.
A measured block-count route combines this kernel with the affine solver,
while retaining the standalone kernel's adverse fragmented-input controls.
The general objective and priority remain unresolved.

Input: ordered keys 1..n, key weights p[1..n], gap weights q[0..n], all
nonnegative. No normalization is required. Use comparison cost with root key
cost one and gap cost equal to the number of internal ancestors. In half-open
key intervals [i,j),

    C(i,i) = 0
    W(i,j) = sum(p[i:j]) + sum(q[i:j+1])
    C(i,j) = W(i,j) + min_r(C(i,r) + C(r+1,j)), i <= r < j.

The common convention charging one additional unit at every gap differs by
sum(q), independent of tree shape.

## Prior-art map (initial)

- Knuth (1971), Optimum binary search trees: quadratic dynamic programming
  using monotone roots. DOI 10.1007/BF00264289. Need inspect original proof.
- Larmore (1987), A subquadratic algorithm for constructing approximately
  optimal binary search trees, Journal of Algorithms 8:579-591.
  DOI 10.1016/0196-6774(87)90052-6. Exact subquadratic under weight restrictions;
  also approximation. Author's 1986 report:
  https://escholarship.org/content/qt4v7249bv/qt4v7249bv.pdf
- Karpinski, Larmore, Rytter (1996), Sequential and Parallel Subquadratic Work
  Algorithms for Constructing Approximately Optimal Binary Search Trees.
  https://theory.cs.uni-bonn.de/marek/publications/seq_and_par_subquadr.pdf
- Nagaraj (1997), Optimal binary search trees, TCS 188:1-44.
  https://community.wvu.edu/~krsubramani/courses/fa16/Aaoa/lecnotes/obst.pdf
  Crucial: Section 2.3 corrects subtree-weight claims when gaps have weight.
  Section 5.1 asks about subquadratic construction and verification.
- Nipkow and Somogyi (2025), Isabelle/AFP formalization of Knuth/Yao/Mehlhorn:
  https://www.isa-afp.org/browser_info/current/AFP/Optimal_BST/document.pdf
- Becker (2010), Optimal Binary Search Trees with Near Minimal Height.
  https://arxiv.org/abs/1011.1337. Full mixed weights; O(n^2) for a fixed
  additive height excess. Sequential key placement uses a bit-vector state
  for the occupied right-fringe levels. Relevant to near-uniform inputs;
  this representation is existing work, not a novel proposal here.

## Research directions to discriminate

User steering: primary measurements are visited interval states, candidate
roots, and all preprocessing/bound work. Include geometric, reversed geometric,
folded geometric, near-uniform, random, zeros/ties, and mixed key/gap inputs.
An improvement must avoid most of the interval table in its claimed regime.

1. Sparse optimality certificates / demand-driven exact DP: can many interval
   states be excluded by certified lower bounds without losing exactness?
2. A representation of mixed key/gap cost that permits an efficient relaxation
   with a verifiable gap. Preserve key termination; do not silently convert to
   the alphabetic special case.
3. Rotation-based or stronger local certificates: find exact small
   counterexamples before investing in claims of sufficiency.
4. Compressed interval DP and structural parameterization: identify which
   parameters actually bound work, and compare with Larmore's existing method.

## Second checkpoint: depth prices and recursive decomposition

The previous goal turn was progress: it produced a committed, pushed,
compiled, visually checked manuscript and an exact contraction implementation.
The full research objective is still unresolved.

The new depth-chain relaxation retains fixed key and gap positions and prices
the necessary level-flow equations. An affine-tail projection lemma makes
each full-problem bound evaluation O(n log n), without assuming a bound on
the unknown optimal BST height. A unique-root version obtains all forced-root
marginals in two passes. See DEPTH_DUAL.md for the proof and exact checks.

Crucial negative evidence: a positive five-key input has an invalid depth
sequence satisfying all these constraints with cost 470, versus true OPT 472.
No multipliers can close this gap. At n=256 the root marginals also leave
254 roots on the ordinary random mixed instance. This lower bound has not
yet supplied an efficient exact construction method.

`recursive_contract.py` combines the existing exact single-key reductions,
whole-instance Huffman equality certificates, and block decomposition. A
decomposition is accepted only when its table-state estimate drops by at
least one quarter. This bounds recursion depth and avoids repeated scans
after tiny reductions. It passed 3,000 independent cubic checks and 20
nested 383-key checks against Knuth, exercising two decomposition levels.
Matched five-trial measurements at n=1024 gave median runtime ratio 0.134
on positive heavy-separator inputs, but essentially no gain on random or
near-uniform mixed weights. Several n=512 controls were slower. No broad
practical superiority is claimed.

## Third checkpoint: the nonlocal ordering obstruction

The JesseSort discussion did not advance this objective. The next research
turn revalidated the checkout and pursued the proposed bounded-window repair.

DEPTH_ORDER.md now characterizes exact BST depth sequences as reverse-ranked
paths satisfying level flow. Its proof equates the number of unfilled runs
after level d with the required number of keys at level d+1. A linear stack
recognizer checks the global ranking condition, but this is not an optimizer.
Ranking and bounded-path ranking are established notions; primary sources
are cited, and no priority claim is made for this reformulation.

More decisively, for every window width w>=2 there is a positive-weight
instance with w+3 keys whose invalid sequence passes all window-minimum and
global flow checks, but whose cost is at most (7/8+1/(8t)) OPT at weight
scale t. All multiplier penalties vanish on it. The harness uses t=16,
giving ratio 113/128, and checks every width through128. This eliminates
the hope that simply enlarging the window and optimizing prices perfectly
could turn this relaxation into a universal exact certificate. It does not
exclude different constraints or prove a general algorithmic lower bound.

The obstruction can also be buried under any fixed number of forced optimal
top levels using a new dominant root and a positive gap. This preserves the
strict additive gap, though not the constant relative one. An additional
120 cubic/Knuth/direct-tree checks exercise depths1..8 and widths2..16.

Exhaustive enumeration through seven keys (873,612 sequences) matches
independent tree shapes exactly and checks the stack recognizer separately.
The next representation must retain nonlocal subtree allocation. Adaptive
violated-interval constraints or compression of the global frontier remain
unresolved; the bounded-window DP is no longer the first experiment to build.

## Fourth checkpoint: a successful shape certificate

The preceding turn was progress: it committed and uploaded the global
ordering characterization and arbitrary-window obstruction. Inspection of
Becker's full frontier confirmed that the straightforward representation
is existing work and remains quadratic near minimum height. The new route
instead optimizes the minimum-unweighted-path-length shape class, then
uses a separate residual-weight bound to exclude all other shapes.

COMPLETE.md gives the proof and a DP over optional bottom-level expansions.
Its width is min(r,2^h-r)+1 rather than the number of intervals. A successful
attempt with logarithmic width uses O(n log n) work including sorting and
the lower bound. A necessary-condition test rejects impossible certificates
before merging, and sorted lists support the standard two-queue bound.
Both key and gap weights remain arbitrary nonnegative inputs; an explicit
certificate, not a near-uniformity assumption, determines success.

The constructor is validated against all tree shapes through eight keys,
and the Knuth-fallback and recursive-fallback variants both match cubic DP
on 3,000 mixed-weight inputs. Near-uniform sizes near powers of two benefit;
ordinary random data and wide shape spaces still require fallback.
The global subquadratic objective remains unresolved. A potential next
extension is a bounded excess in unweighted path length rather than only
the exact minimum; no such extension is currently claimed.

The final six-trial matched test at n=1,024 gave median hybrid/Knuth ratios
0.03934 on near-uniform, 0.10478 on heavy separators, and1.05454 on random.
At n=512 some failed attempts add material overhead relative to the prior
recursive solver. The additional size controls deliberately expose skipped
shape spaces. These are exploratory Python measurements; full counters and
all timing observations are retained. A cheaper next experiment before
excess-shape DP is the concave baseline-price search derived in COMPLETE.md.

## Fifth checkpoint: optimize the exclusion baseline

The previous turn was progress: the minimum-I shortcut, both fallback
variants, exact checks, matched timings, and manuscript were committed and
uploaded. This turn implements the proposed baseline-price extension.

BASELINE_PRICES.md proves that the exclusion bound is concave in a common
decrease of the key and gap baselines. A lexicographic Huffman oracle gives
both its value and a supergradient from internal path length. Binary
elimination finds the best integer price when uncapped; production permits
only bit_length(n) extra linear oracle calls, preserving O(n log n) work
for the attempted shortcut. Every sampled price remains a valid exclusion
bound whether or not the integer maximum was reached.

Exact checks cover 400 small shape-profile oracle comparisons, 1,200 full
integer-price sweeps, and 3,000 cubic-checked mixed-weight inputs for both
fallback versions. The new search recovers 87 previously unsuccessful
unrestricted certificates. The seeded perturbation sweep recovers n=1,024
with amplitude2 and n=2,048 with amplitude1, while larger perturbations
generally fail the fixed-profile ceiling and receive no extra oracle calls.

The remaining barrier is now sharper: baseline optimization cannot beat
the order-free minimum-I profile ceiling. The next representation needs
additional order information in its residual bound or an expanded shape
class. The full objective is still open; this checkpoint is not completion.
The next concrete experiment is to substitute the existing order-sensitive
depth-chain lower bound for the order-free residual bound in the exclusion
certificate. It need not be exact because the baseline supplies a positive
exclusion margin; all extra bound work must still be counted.

The matched six-trial experiment newly certified all n=1,024 amplitude2
and n=2,048 amplitude1 inputs, with median priced/Knuth ratios0.04953 and
0.06128. Larger perturbations and ordinary random controls still failed.
A zero-extra-call control showed noticeable timing variation, so only
large effects are interpretable; exact operation counts remain primary.

## Sixth checkpoint: expand shapes with a dyadic excess budget

The previous research checkpoint was progress and is now uploaded at
3c95fd2, including the baseline-price TeX/PDF. The intervening Jessesort
conversation did not advance the OBST goal. Current work revalidated the
repository and completed the proposed ordered-residual experiment.

The latter passed 480 exact checks but rescued none of 24 tested fixtures
at 32 iterations per oracle configuration. Four configurations per fixture
used two baselines and both ordinary and unique-root depth oracles. This
is evidence about that budget, not a proof that the best dual cannot help.
The attempted periodic obstruction unexpectedly falsified the assumption
that small nonuniformity preserves a perfect tree. The failed assertion
and corrected measurements led to an expansion of the candidate class.

EXCESS.md proves a dyadic tiling representation retaining both key and gap
costs. A nonnegative leaf potential sums exactly to excess unweighted IPL.
Its prefix/suffix inequalities bound cumulative-position drift, giving
O(n*(s+k+1)*(k+1)^2*2^k) exact class optimization, where k is excess budget
and s is the earlier bottom-level shape-width parameter. The implementation
uses a sharper potential at perfect sizes. Fixed k and logarithmic s give
O(n log n) attempted work including a global exclusion certificate. On
failure or skipped widths, the constructor runs Knuth; worst case is n².

The generalized DP passed 1,200 weighted comparisons against all shapes
through eight keys, 3,000 mixed-weight cubic checks including full fallback,
and 104 adversarial-family checks. Sixty-five larger fixtures retain all
budgets 0..3. At n=1,023 with periodically placed weights 17 among 16s,
budgets 0 and 1 give the suboptimal cost312,464; budget2 finds and certifies
312,154 using27,570 states and137,835 transition checks, plus sorting and
residual-bound work, versus Knuth's523,776 states and1,046,532 root checks.

Six matched timing trials per fixture newly certified all tested amplitude4
inputs at n=1,023 and1,024 and all periodic A=16 inputs at n=1,023 and2,047.
Median excess-two/Knuth ratios were0.23600,0.44831,0.20790,0.17101. Failed
random input added34.9% median overhead; failed n=2,047 amplitude16 added
13.6%. A skipped-width control shows timing noise. All42 trials are retained.

The next substantive barrier is broadening the useful class without paying
for an exponentially growing excess budget or a wide bottom-level band.
Potential next steps are tighter band pruning from feasible upper costs,
sharing the dyadic transition geometry across levels, and combining the
expanded certificate with the baseline-price search. These are next actions,
not established results. The general objective remains active and unresolved.

## Seventh checkpoint: split-height class without the width skip

The previous substantive research turn made progress by implementing and
checking split-height construction; its matched timing job was still live
when the conversation turned to JesseSort. That discussion did not advance
the OBST objective. This continuation inspected the actual checkout and
confirmed the benchmark process on the Mini before waiting for its result;
it was not restarted. Its output was copied before any later remote build.

SPLIT_HEIGHT.md gives the full dyadic construction, including boundary key
costs, exact lower-tree tables, SMAWK's finite band padding, reconstruction,
and operation accounting. The split-height/Monge mechanism is explicitly
prior Karpinski--Larmore--Rytter work in Section5 of their longer preprint,
not an invention of this project. For a fixed extra height the attempt is
O(n^(3/2)) at every input size, removing the old bottom-band width skip.
An exact greedy computation of minimum IPL among taller trees supplies a
separate sufficient certificate for unrestricted optimality. Failure invokes
Knuth, so the general worst case remains quadratic.

The final harness passed 450 exhaustive weighted height optima,44 exact
tall-tree minima,2,000 cubic-checked full inputs (917 certificates),520
independent height-DP/SMAWK/divide-search checks,261,482 short-table entries,
and104 adversarial-family inputs. A larger36-fixture sweep at three budgets
certified every near-uniform fixture, including384/768/1000/1536 keys.
Random,geometric,gap-spike controls failed certification. The initial large
geometric run exceeded Python's reconstruction recursion limit; the corrected
harness raises that limit and completed without changing algorithmic results.

The48 matched timing trials show a qualified practical gain. Minimum height
at n=1000/1536 near-uniform cost0.71530/0.65826 times Knuth. At n=3072 it
failed the certificate despite optimal candidates, while one extra level
certified all six trials at0.70837 times Knuth. One extra level also certifies
all n=1536 amplitude4 and n=1023 periodic16 fixtures, but costs1.18924 and
1.06171 times Knuth. Ordinary random inputs still fail and cost1.55378 or
1.93841 times Knuth. The two budgets certify small near-uniform inputs but
can be slower there. Exact counts, failures, and all timing data are retained.

The next step toward the full objective is to implement a proper width-limited
Larmore/KLR comparator using the same matrix infrastructure, with its proven
subtree-mass guarantees, then determine what additional order-sensitive
certificate could reduce its cost. Another cheap extension is to generalize
the already-tested baseline-price search from a minimum-IPL cutoff to the
exact taller-tree IPL cutoff. Neither extension is presently implemented.
The mixed-weight problem remains the objective; this is not completion.

## Eighth checkpoint: full exact construction on a variable mass frontier

The previous turn was progress: commit3ad277b uploaded the split-height
implementation, proof, exact checks, and18-page manuscript. This turn examined
the stated width-limited prior-work baseline and implemented both a uniform
envelope and a variable contour, preserving full mixed key/gap weights.

The first mass-bound transfer failed. Using2W/F_(d+3) at edge depth d produced
an empty admissible class on a gap-spike input. A smaller positive witness is
p=[1,1],q=[1,100,1]: both trees cost206, total mass104, and the depth-one
internal child has mass102>2*104/3. The sharper constant is therefore not used
in this model. MASS_FRONTIER.md proves a sufficient W/F_(d+1) internal-subtree
bound directly by single/double rotations and a Fibonacci recurrence, retaining
the broad known architecture and asymptotic regime. The rejected transfer and
exact counterexample are preserved; this is not a claim to refute KLR's method.

For depth d, only intervals with mass at most W/F_(d+1) are stored, with empty
intervals always allowed. Their right endpoints form a hereditary monotone
contour. A cancellation proof bounds all Knuth root searches by3S_d, where
S_d is the number of stored intervals. Bucketing only actual cells avoids
scanning nonexistent diagonals. Variable-band SMAWK handles holes in reachable
rows and output columns. All global optimal trees are represented, so this
constructor has no failed certificate followed by a second quadratic solve.
Selection takes O(n log n), and total work is
O(n log(n+1)+min_d[S_d+n*2^d]); worst case remains quadratic via depth zero.

The harness passed960 exhaustive weighted contour-class checks,914 independent
interval costs,90,193 brute matrix minima,2,400 full cubic-checked solves, and
24,600 internal-subtree mass inequalities. Both implementations also match
Knuth on56 larger mixed-weight fixtures through2,048 keys. At n=2048 random,
adaptive stores309,261 cells versus Knuth's2,098,176, with616,642 root checks
plus1,245,431 genuine top queries and separately retained padding/scanning work.
Geometric inputs choose the full table. The Fibonacci and top-skeleton ideas
are prior work; priority of this particular contour specialization is unproven.

A positive family with a central n^(3/4)-key light block proves a separation
within this architecture: adaptive work O(n^1.59024), whereas every global-width
plan has proxy Omega(n^1.75). This is not a lower bound on other algorithms;
the same family can also benefit from our existing certified contraction.
Both modes were exactly checked at n=16,81,256,625. Larger inputs only count
plans: at n=65536, depth9 proxies are119,041,540 adaptive and361,608,522
uniform. These are not completed large solves or runtime predictions.

The48 matched timing trials show adaptive/Knuth ratios1.61204,1.55650,0.91021
on random input at512/1024/2048 keys. On a2048-key localized light window,
adaptive costs0.77546 times Knuth and0.65523 times uniform width. On a single
heavy key it costs1.04249 times Knuth and0.70113 times uniform width. The
instrumented Python implementation still loses on several small cases and
does not establish broad superiority. All observations are retained.

The next substantive step is to combine the variable contour with the existing
certified contractions or use a multi-depth frontier so a heavy outcome does
not inflate the interval domain everywhere. A compiled implementation would
clarify the constant-factor question, but a faster language alone would not
remove the worst-case quadratic state count. The unrestricted mixed-weight
objective remains active and unresolved.

## Ninth checkpoint: dominant-gap separators and local frontiers

The preceding JesseSort discussion did not advance this active research goal.
On resumption, the pending correctness session handle was no longer present;
read-only Mini inspection found no running separator process and a completed
result file. The final endpoint-first results were copied before the next
mirror/build operation. All recorded checks had passed.

The new constructor separates at certified dominant endpoints, keys, and
interior gaps before running the mass frontier on each terminal component's
local mass. For an internal gap q with adjacent key weights p_a,p_b and
outside interval masses W_L,W_R, q+min(p_a,p_b)>=W_L+W_R guarantees an optimum
with that gap at depth two. Restriction/exchange arguments give the exact
identity OPT=C_L+C_R+W+q+min(p_a+W_L,p_b+W_R). Both orientations use the same
two outside solves, so they do not duplicate recursion. All key/gap weights
and offsets remain in the formula. Replacing min by max is false: the positive
p=[100, 1, 50],q=[1, 1, 1, 1] witness has optimum 212 but depth-two restricted cost 261.

The gap score 2q+p_a+p_b+min(p_a,p_b) is static on original intervals. Two
range-maximum indexes plus prefix sums find certificates without repeatedly
scanning long components. Endpoint tests run first; indexes are constructed
only when needed. Total arithmetic work is
O(n log(n+1)+sum_t min_d[S_(t,d)+m_t*2^d]), including local parameter selection.
If all terminal sizes are at most b, it is O(n log(n+1)+nb). The full mixed
geometric family p_i=q_i=2^i,q_n=2^n is exhausted by endpoint certificates in
O(n) arithmetic operations, with no index or terminal DP; this is not linear
bit complexity. Hierarchically dominant gaps with bounded terminal sizes give
an O(n log n) mixed-weight family. These are structured regimes, not a general
subquadratic theorem. Priority of the separator conditions remains unestablished.

The harness passed 22,140 exhaustive assignments through four keys, checking
3,211 qualifying gap certificates, 2,036 endpoint certificates and 380 key
certificates against all tree shapes. Both terminal strategies passed 3,280
full solves on 1,640 inputs through 40 keys against independent cubic DP and
direct tree evaluation. Both also matched Knuth and the direct frontier on
40 larger fixtures through 2,048 keys. At n=2048 the heavy-gap fixture uses
153,582 terminal cells versus 1,047,552 direct-frontier cells; hierarchical
gaps use 22,333 versus 522,242. The latter also uses 42,885 root candidates,
39,284 genuine top queries, 6,261 padding queries, 6,142 index-build comparisons,
1,476 range-query comparisons and 254 endpoint tests. Full counter categories
are retained. Terminal metadata sums are explicitly distinguished from the
global reconstructed tree's height.

A new positive obstruction makes the remaining failure concrete. Set all
weights to one except q_1=q_(n-1)=n^3 for n>=5. No separator can fire. Exact
contour counting proves every positive-depth work proxy exceeds the depth-zero
Knuth table, so this implementation stores all n(n+1)/2 cells on the family.
An independent contour check corrected an initial depth-two counting error:
intervals containing one heavy gap also face a length cutoff. The corrected
four sets of floor((n-1)/2) intervals are included in the proof and harness.
This is an obstruction to the present architecture, not an OBST lower bound.

### Matched timings

Ten balanced orders per fixture compare five solvers: five cyclic rotations
and their reversals, not all 120 permutations. The 70 trials contain 350
full timed solves, including preprocessing and reconstruction. Every tree's
cost is independently evaluated and all five answers agree. The platform is
Apple M4, Python 3.9.6. Inputs vary between trials except deterministic spike
and geometric families. Each entry is a median paired runtime ratio to Knuth;
smaller is better. SF uses frontier terminals, SK uses Knuth terminals, and
RC is the earlier recursive contraction solver.

| n / Fixture | Direct frontier | SF | SK | RC |
|---|---:|---:|---:|---:|
| 2,048 / Random | 0.87985 | 0.87172 | 1.03209 | 1.00381 |
| 2,048 / Near-uniform | 0.87747 | 0.90863 | 1.06833 | 1.06450 |
| 2,048 / Heavy key | 0.99362 | 0.74038 | 0.52307 | 0.01605 |
| 2,048 / Heavy gap | 0.99617 | 0.77197 | 0.51357 | 1.03871 |
| 2,048 / Random background, heavy gap | 0.90780 | 0.75211 | 0.49766 | 0.97692 |
| 2,048 / Hierarchical gaps | 1.06953 | 0.04608 | 0.01843 | 0.99421 |
| 1,024 / Geometric | 1.05318 | 0.00781 | 0.00548 | 0.04206 |

The gap certificate adds substantial coverage where RC does little, especially
hierarchical gaps. RC remains much faster on the heavy-key fixture. The local
frontier terminal implementation is slower than plain Knuth on these smaller
components despite reduced cell counts. SF and SK follow the same endpoint
path on geometric inputs, so their timing difference is not algorithmic.
Random and near-uniform controls do not split. These instrumented Python
measurements do not establish broad or production-language superiority.
Raw per-trial values and counters are in `results/gap_separator_matched.json`.

The obstruction harness passed eight full checks through 256 keys and four
plan-only checks through 65,536 keys. The largest plan selects 2,147,516,416
cells; this is not a completed large solve.

The next substantive target is joint treatment of several comparable heavy
outcomes, where no one outcome is dominant but its presence still inflates a
global frontier. The positive two-gap family gives a specific regression
control for that work. The unrestricted mixed-weight objective remains active.

## Tenth checkpoint: joint heavy-outcome cores

The previous goal turn was progress: commit 1ef72c3 uploaded the dominant-gap
separator, matched comparisons, and a positive two-heavy-gap family on which
that constructor selects the full quadratic table. This turn uses that family
as a concrete target while preserving the unrestricted mixed-weight objective.

Choose selected key/gap outcomes H and retain every selected key plus the
adjacent key(s) of every selected gap. An exchange lemma projects any tree
onto these necessary keys without deepening any selected outcome. A tree that
has an outside comparison above retained keys saves at least one selected
comparison. This is not arbitrary restriction to a noncontiguous key set:
when an outside root has retained keys on both sides, promote the largest
retained key on its left, restrict the left subtree below that key, and keep
the right subtree. The adjacent-key condition preserves selected gaps and
supplies a strict saving. This point was resolved before relying on the lemma.

The initial sufficient certificate was theta >= (m+L)*W_light, with m retained
keys and L=ceil(log 2(n+1)). It passed the full exact harness. Before publishing,
it was strengthened using the earlier Fibonacci mass lemma. A protected-only
core (all unselected weights zero) has every internal subtree mass at least
theta, because each retained key lies on a selected search path. Its optimal
height is at most H=max{j<=m:F_j*theta<=W_selected}. Replacing the projected
core by a protected-only optimum and reinserting balanced light payloads proves
that theta >= (H+L)*W_light suffices. The final core is then optimized with ALL
original and collapsed weights, without a height restriction. The protected-only
problem is a proof witness, not a replacement objective.

For threshold-selected outcomes, key activation is max(p_i,q_i,q_(i+1)). An
ascending threshold sweep activates unanchored keys, using union-find to
maintain payload runs and their triangular state totals. Grouping equal
weights prevents partial ties. The best certified tau(m)+sum tau(k_t) proxy
is selected in O(n log(n+1)) arithmetic work. A decreasing Fibonacci index
handles all protected-height bounds in O(n) index decrements. This chooses
a Knuth-state proxy, not a minimum wall time or a minimum frontier proxy.
Failure uses the previous separator constructor with screening overhead.

Both core and payloads are solved exactly, using frontier or Knuth kernels.
A known uniform-key/uniform-gap shortcut builds an optimal balanced tree in
linear work. Thus a certified plan costs O(n log n+K(m)+sum K(k_t)). With k
selected outcomes and uniform residual background the bound is O(n log n+k^2).
Bounded positive residual weights give O(n log n+k^2+sum k_t^alpha), with
alpha<1.59024. The former two-heavy-gap obstruction now takes O(n log n) with
unit background. This is a scoped improvement; the general worst case remains
quadratic and priority is unestablished.

The refined harness passed 1,937 componentwise projection cases, all selected
subsets and tree shapes through four keys; 17,054 qualifying certificates on
22,140 inputs in {0,1,100}; 2,640 full solves on 1,320 inputs through 32 keys;
and 520 threshold choices against direct enumeration. Both kernels matched
Knuth and the previous separator on 30 larger fixtures through 2,048 keys.
The moderate-gap fixture is set at exact certificate equality. At n=2048 it
has 90 retained keys but protected height bound 9; the older m-based condition
fails, while the new condition passes with theta=42,395,178. It uses 23,695
interval cells versus 304,486 for the prior constructor. Full counter categories
include sorting, Fibonacci additions/checks, activations, unions/finds, kernel
cells and candidates, matrix queries/padding/scans, and reconstruction.

While preparing the large-case independent oracle, an erroneous draft coefficient
on uniform internal path length was corrected using E=I+2n: the full uniform
cost is (p+q)*I+n*p+2n*q. The constructor always evaluates its tree directly,
so no constructor or benchmark result depended on the erroneous draft formula.

An initial size-certificate timing batch was explicitly terminated after the
height refinement changed the algorithm; its incomplete timings are not used
for final performance claims. The final comparison includes the revised
certificate, the equality fixture, previous separators and recursive contraction,
and both new kernel choices. No restart was triggered by an observation timeout.

The final 90 matched trials (450 complete solves) show CF/CK-to-Knuth ratios
0.00700/0.00551 for unit-background two-heavy-gap inputs, 0.70676/0.79129 for
random background, and 0.08573/0.03229 for the moderate-gap equality fixture
at n=2048. The mixed heavy-key/gap case gives 0.08823/0.03204. Small random
frontier solves remain slower than Knuth, and global screening loses to the
existing geometric endpoint shortcut. All failures and raw comparisons remain.

The new method also completed five large full constructions through 65,536
keys on the previous two-gap obstruction. Direct evaluation and an independent
four-key cubic core plus the uniform closed form agree. The largest exact cost
is 1,407,374,885,846,941; the single exploratory solve took 0.59933 seconds.
The previous algorithm was only planned there and selects 2,147,516,416 cells.
These facts are not a measured speedup against an executed old solve.

The broad objective remains open. Next implementation work should bound the
Fibonacci precomputation by the largest relevant mass ratio and avoid global
screening before cheap endpoint certificates. The mathematical target remains
several levels of concentration without an overwhelming threshold gap: the
current core certificate is sufficient, not a characterization of optimality.
Neither the new construction nor its structured-family bounds prove a general
subquadratic algorithm or an impossibility theorem.

## Publication audit of the tenth checkpoint

The intervening JesseSort discussion made no progress on the active OBST goal.
On resuming, the local uncommitted sources and results were re-inspected rather
than inferred from the conversation. The raw result audit verified all five
correctness counts, 30 larger fixtures, 90 matched trials with 450 equal-cost
solves, recomputed all paired median ratios, and checked all five scale records
including their explicit plan-only status for the previous constructor. The
29-page final PDF was reviewed in rendered contact sheets, with full-size
review of the new mathematical and measurement pages. Output copies were
verified byte-identical to the repository TeX and PDF. The checkpoint is being
published without a claim of general subquadratic complexity or established
priority; the broad research goal remains active.

## Eleventh checkpoint: residual-cost core exclusion

The preceding goal turn was progress: ab7187d uploaded the joint heavy-outcome
core theorem, implementation, exact results, and reviewed 29-page TeX/PDF. This
turn attacks the sufficient condition's excessive charge for light search cost.

For selected weights w_H and residual weights w_0, let P be the protected core
optimum and B_0 a valid lower bound for the full residual instance. The projection
lemma gives C_H(T)>=P+theta for every non-core-closed T. Independently
C_0(T)>=B_0. Thus every excluded tree costs at least P+theta+B_0. A closed witness
below that bound certifies the existence of a closed global optimum; an exact
closed candidate below it is globally optimal. This applies to arbitrary
selected subsets, not only thresholds, and equality is safe.

The default constructs a protected-optimal core with balanced payloads and tests
its residual cost U_0-B_0<=theta before any exact payload solve. The existing
mixed-node order-free relaxation supplies B_0; no new Huffman algorithm is
claimed. For a fixed selected set it is at least as strong as the old height
test, but candidate selection is not exhaustive. The optional refinement solves
one exact closed candidate after all witnesses fail. The one-refinement limit
prevents an extra logarithmic factor in failed exact solve work.

The first prototype chose a single minimum-proxy threshold. Its completed test
showed that smaller ordinary weights could enter the selected set and defeat
the certificate even while a heavier threshold worked. The final selector keeps
two representatives per dyadic core-size band: minimum triangular proxy and
highest threshold, capped at floor(sqrt(n*ceil(log2(n+1)))) core keys. There are
O(log n) representatives and the sum of their core-size squares is O(n log n).
Sorting the original key/gap profiles once permits each residual lower bound in
linear work by dropping selected entries and appending zeros. Total witness
screening is O(n log n). A successful plan retains the earlier exact component
bound. General worst-case work and storage remain quadratic.

The first full harness failed on Counter.update with list-valued fallback
metadata; direct field assignment fixed it. The entire final harness was rerun.
Final exact checks: 22,140 exhaustive inputs in {0,1,4}; 17,054 nontrivial
excluded-class inequalities; 13,669 witness certificates; 15,181 refined
certificates, including 1,512 rescues. Arbitrary selected subsets with weights
{1,3} through three keys yielded 14,912 excluded-tree checks. Both kernels and
both refinement settings passed 6,560 full solves on 1,640 inputs through 40
keys against independent cubic DP and direct tree costs. All 1,640 portfolios
matched direct enumeration. There are 48 larger fixtures plus nine independently
varying positive key/gap background fixtures through 2,048 keys. All final result
files carry the same solver source hash.

For n=2^h>=8, all original weights one except q_1=q_(n-1)=theta, the protected
four-key optimum is 5*theta. A specified core and balanced payload have light
cost U_0=(2h+3)n-6h-3. Using E=I+2n, the residual problem reduces, for its
order-free lower bound only, to leaf weights two ones and n-1 twos. Huffman
first merges the ones, then has n equal twos, giving B_0=2nh-n+2. Consequently
U_0-B_0=4n-6h-5. Linear theta=4n certifies closure although the old height test
requires (h+4)(2n-1). The full optimum at theta=4n is (2h+23)n-6h-3; the four
protected-optimal shapes and the cost of every higher protected level justify
the optimal full-weight core. The algorithm uses O(n log n) work and O(n) space
on this positive mixed family, with O(log n)-bit intermediate values. This is
not a lower bound on previous frontier methods, which can omit states here.

Fourteen full constructions, every power of two from eight through 65,536,
match the closed form, an independent four-key cubic oracle plus the uniform
payload formula, and direct evaluation of the complete output tree. At 65,536,
the exact cost is 3,604,381; the excluded-class lower bound is 3,604,482. The
proof and full-weight cores each have ten cells and fifteen root candidates.
The entire tree was constructed, in about 0.6574 seconds for one exploratory
run. The preceding method's 146,498,625 frontier cells were planned only.

The 80 matched trials (320 complete solves) use four cyclic orders and their
reversals. At n=1024, the new frontier/Knuth-kernel ratios to Knuth are
0.01539/0.01965 for two gaps of weight 4n, 0.03458/0.03469 for many unit-background
gaps, and 0.03594/0.03472 for mixed unit-background heavy outcomes. With ordinary
weights independently in [1,1000] and selected weights 4000n, ratios are
1.23537/0.87326 for two gaps, 0.15569/0.10279 for many gaps, and 0.14830/0.11509
for mixed selected outcomes. The random control remains slower than Knuth.
Geometric screening is about 4.91 times slower than the previous core/frontier
solver. Failed-certificate ratios below one are not algorithmic successes.
These are instrumented Python results; practical claims remain scoped.

A precise remaining gap is preserved. At n=2048, heavy gaps of weight 2n have
closed candidate cost 71,611, exactly the global optimum, but the bound is only
67,586. At weight n, the closed candidate is suboptimal: 61,371 versus 59,332.
Independent minima for protected and residual costs can be too optimistic to
certify a correct structure. A preliminary, unintegrated scalar-peeling probe
raised the 2n-case bound to 69,612 at peeled weight 3,073, still below 71,611;
it is not part of the final solver or a claimed resolution. The next research
target is a tighter coupling of residual costs to the excluded structure,
including multi-level concentration, not further reliance on overwhelming
weights. The general subquadratic or impossibility objective remains active.

The revised manuscript is 33 pages, with full proofs, scoped bounds, all timing
controls, operation-category distinctions, and a citation to Huffman's original
paper. Credit remains OpenAI Codex Sydney; problem selection and sponsorship
remain with the repository owner. Priority of the derived certificates remains
unestablished. Final publication follows rendered-page and remote-blob checks.

## Twelfth checkpoint: couple the first violating skeleton to its forests

The recovered complete harness confirms a stronger two-gap exclusion bound.
For A equal to the two gaps' neighboring keys, every nonclosed tree has
selected gap depth sum at least |A|+2. At equality, the selected paths share
only the root and their union has exactly A plus one outside bridge key.
This permits a constant-size shape enumeration. Ordinary residual intervals
receive unordered mixed-tree bounds; the bridge interval receives a two-root
forest bound after lowering both attachment depths to their minimum. Only
then is assigning a largest regional key weight to the bridge justified.
Higher depth sums receive a separate tail bound. The final certificate takes
the maximum of the earlier bound and the minimum of the two new classes.

The mixed-forest greedy rule is proved by a deepest-cherry exchange and
contraction, with empty trees allowed and equal-depth roots. It is checked
independently by forest shape enumeration and rearrangement of weights.
This is not a claim about arbitrary unequal-depth forest roots.

The new family takes n=2^h, h>=5, s=n/16-1 arbitrary middle key positions
of weight two, all other keys and ordinary gaps of weight one, and selected
q_1=q_(n-1)=3n. For every placement, the first and tail bounds exceed the
midpoint witness by at least 5n/8+h+9 and 25n/16+7h+8. For h>=6, even
the exact closed optimum exceeds the old fixed-pair bound by at least
n-6h-5. This is a strict certificate separation, without a claim about
every other core the old selector could try.

A scope correction matters: constant key weights absorb into gap weights
via C(T;c,q)=sum(q_g+c)d_g-cn, so unit-background examples alone reduce
to alphabetic trees. The new family has Theta(n) nonuniform keys in arbitrary
positions. Nevertheless, its total mass is still O(n) with minimum key weight
one. The established global frontier already has the same O(n^alpha),
alpha=1+log_(2phi)(2)<1.59024, guarantee. The new certificate improves
construction work inside that regime; it does not expand the asymptotic
subquadratic regime. An initial interpretation suggesting otherwise was
removed before publication.

Validation: 11,880 forest checks; 24,188 exhaustive weight inputs; 51,654
pair-exclusion checks with separate first and tail tests; 3,288 coupled-only
exact-candidate certificates; 6,560 complete cubic-checked solves; 36 larger
adversarial fixtures through n=2,048 in both kernels. All checks passed.
The family harness has 31 nonuniform placement/size cases, 28 independently
checked by Knuth and eight by cubic DP, plus 14 uniform formulas through
n=65,536. Its initial run stopped on a test-harness tuple-unpacking mistake
(cubic returns two values); that was fixed and the entire family run repeated.

At n=2,048, unit background and selected weight 2n, the new bound 71,619
certifies exact cost 71,611, resolving the previous 67,586 bound gap. At
selected weight n, the proposed closed class is still suboptimal and rejected.
At n=16,384 with 1,023 random doubled keys, full construction returns 767,240
and uses 11,681,397 DP states, versus 134,225,920 for a full Knuth table.
It also executes 42,351,013 top-matrix queries and 15,502,473 short-root
candidates. Every output key is constructed and directly evaluated. The
largest quadratic reference was not executed; exactness there uses the
proved certificate and exact payload constructor, not an independent table.

The 224 n=512 timed complete solves use balanced cyclic and reversed orders.
Spread/random nonuniform PF/Knuth ratios are 1.48227/1.39273, whereas
PF/previous ratios are 0.48126/0.47931. The Knuth payload kernel gives
0.93990/0.86098 against plain Knuth. Unit 2n-gap PF/PK ratios are
0.04285/0.03927. Random, near-uniform, geometric, and varying-background
controls fail the new certificate; their timings remain in the report.
Sixteen larger matched complete solves, alternating order on fresh random
placements, give PF/Knuth medians 0.65948 at n=2,048 and 0.56309 at
n=4,096. All costs match exact Knuth and direct evaluation. These are
instrumented Python observations, not optimized implementation comparisons.

The JesseSort discussion motivates keeping compact boundaries and postponing
interior construction. For optimal BSTs, an intact subtree's interaction with
its ancestors is C+dW; the difficult question is when that subtree can remain
intact. This checkpoint supplies one exact constant-size certificate for that
decision. It does not show that arbitrary input admits a small or cheaply
maintained boundary representation. That remains the substantive next target:
more general coupled path unions, or a rigorous obstruction to a proposed
representation, while retaining the full mixed-weight objective.

Code and raw source-hashed results are in `pair_skeleton*.py/json` and
`check_pair_skeleton.py`; the detailed proof is in `PAIR_SKELETON.md` and
the manuscript. Credit remains OpenAI Codex Sydney; sponsorship and problem
selection remain with the repository owner. General completion is not claimed.
The revised 37-page manuscript compiles without warnings. All pages were
rendered and visually checked, with the new proof and measurement pages also
inspected individually. Recorded test and implementation hashes match the
published sources.

## Thirteenth checkpoint: audit the endpoint-response representation

The previous turn published a stronger core certificate but did not enlarge
the asymptotic subquadratic regime. The next question was whether an interval
could instead be summarized by its response F(x,y) to added endpoint-gap
weights. This is a natural way to keep boundary decisions explicit while
postponing interior construction. Harness-first investigation now establishes
both an information obstruction and a separate explicit-representation bound.

Two four-key intervals have identical key vector p=(1,1,2,3), gap vectors
(1,4,2,1,1) and (1,4,1,2,1), equal mass 16, equal endpoint gap weights,
and the same gap multiset. Their complete nonnegative endpoint response is
the same minimum of five affine planes. Enumerating all 14 shapes proves
this exactly: every differing plane is pointwise dominated by a shared plane
whose slopes and intercept are no larger. Nevertheless, prepending keys
(7,1), appending (1,7), and giving all new gaps weight one yields optima
101 and 100. Independent enumeration of all 1,430 eight-key trees per
instance, cubic DP, and Knuth agree. Thus even an exactly represented value
response plus these metadata is not sufficient for contextual composition.
The result does not exclude extra witnesses, non-exposed states, signed
responses, or richer interfaces, and is not asserted to distinguish mixed
from alphabetic algorithms.

Separately, the response has at most n(n+1)/2 affine pieces because its
integer slopes are endpoint depths a,b with a+b-1<=n. A strictly positive
geometric family attains Omega(n^2). On m keys, set P_i=4m*8^i, all gaps
one, and probe added left weight x_j=2*sum_(i<=j)P_i+2m. Strict endpoint
dominance forces depth m-j. Mirror two copies about a sufficiently heavy
central key to obtain all m^2 depth pairs in a bounded parameter box.
Weights have O(n)-bit length; this is an output-size obstruction to explicit
facet listing, not a general computational or fixed-word-size lower bound.

The same family exposes the limit of that argument. Its one-sided response
is exactly C0+m*x-sum_i max(0,x-(P_i-P_0)); the two-sided response separates
into two such functions plus an affine term in the forced-center box.
For the entire quadrant, any optimal root must be the center or an outer
key. Any other root puts the center and both added endpoint weights at
comparison depths at least two, and is strictly beaten by a center-root
candidate with both outer keys as children. The analogous one-sided argument
after choosing an outer root reduces the full function to a minimum of five
expressions in the two hinge functions. It has exactly m^2+2m+2 affine pieces
but only O(n) hinge terms. Threshold prefix sums support O(log n) value
queries after O(n) arithmetic preprocessing over the entire quadrant.
The selected expression reconstructs exactly n keys in O(n) additional work.
The family is already easy for endpoint-dominance methods. No expression-size
lower bound, difficult-query result, or new general solver is claimed.

A favorable general bound also follows from the existing mixed Fibonacci
mass lemma. If original endpoint gaps are positive and original mass is W,
then any optimal endpoint depths a,b after arbitrary x,y>=0 satisfy
F_(a-1)<=W/q_0 and F_(b-1)<=W/q_n when the respective depth is at least two.
Take the root's left subtree to exclude added y (and symmetrically for x);
the last endpoint ancestor has mass at least q_0+x. Hence the entire response
has O(log(2+W/q_0)*log(2+W/q_n)) affine pieces, independent of the added
weights. Polynomial mass ratios give O(log^2 n) pieces. This does not bound
their discovery cost, and the five-piece composition counterexample still
applies. Compactness and sufficiency are distinct requirements.

The final exact harness passes 875 envelope queries on 175 inputs through
seven keys, 725 retained-plane Fibonacci checks, 408 hinge formula queries,
1,496 product-family queries through 33 keys, 204 full cubic comparisons,
30 all-shape checks of unique optimal depth pairs, and 680 strict endpoint
inequalities. Product queries execute 887,808 Knuth root candidates. Another
304 queries expose the outer-root pieces and 384 test arbitrary parameters
and the global transition threshold. All 2,184 factored full constructions
match exact Knuth and direct evaluation, with exactly n keys constructed.
The generator was changed from repeated prefix summation to a single pass
before the final run, so the actual preprocessing matches the linear bound.
The first collision search used outer weights 16; the reduced publication example
uses seven. Its envelope equality is checked by direct componentwise
domination, independently of rational polygon clipping. Both full tree sets
are enumerated directly. Code and source-hashed raw results are in
`boundary_response.py/json`; the proof is in `BOUNDARY_RESPONSE.md` and
the manuscript.

The next interface must retain more than the value response to two added
gap weights: some sequence of decisions along the boundary paths, or internal
alternatives suppressed by the isolated optimization. These are concrete
obstructions to candidate representations, not completion of the original
mixed-weight subquadratic or impossibility objective. Credit remains OpenAI
Codex Sydney; sponsorship and problem selection remain with the repository
owner. Novelty remains unestablished.

## Publication audit of the thirteenth checkpoint

The endpoint-response harness source hash matches its recorded results.
The 42-page manuscript compiles with Tectonic without warnings. All pages
were rendered and reviewed as contact sheets, and pages 37--41 containing
the new statements and proofs were inspected individually. The publication
preserves the distinction between a representation obstruction and a general
algorithmic lower bound. The unrestricted objective remains open.

## Fourteenth checkpoint: terminal penalties and sparse Monge products

The endpoint-response checkpoint was committed and its GitHub blobs verified
at 5eafeded369aed644fdf9ecfda0a33dabd24ae1f. The next investigation retains
the actual interval table in a condensed Monge representation.

A useful first identity is that the sum of the triangular Monge densities is
C(0,n) minus the sum of singleton interval costs. Nonnegative integer weights
therefore give only O(W log n) nonzero densities in the final table. This
alone does not construct the table and was not presented as an algorithm.

A proposed upward iteration from additive singleton costs had a flawed
convergence proof: rotations can lift unfinished intervals and force extra
refinement. The proposed proof was discarded despite small passing tests.
No convergence theorem for that lower iteration is claimed.

The retained construction starts instead from M times interval length, where
M=(H+1)W+1 and H is a safe actual-optimum height bound. Each layer expands one
level and retains M per unfinished key. It is a decreasing upper iteration.
Every optimum at layer h exposes min(length,2^h-1) keys, giving an explicit
penalty ramp plus a residual between zero and h times interval mass. Finite
Monge completion, including diagonal boundary cases, allows a published
core-sparse Monge product to compute the next layer.

The crucial intermediate bound removes the penalty ramp's one density line
and tiles the remaining triangular domain by dyadic squares. There are
O(n/s) tiles of side s, and each has at most min(s^2,2hW) nonzero integer
densities. Summation gives O(n sqrt(hW)), capped by n^2. After a balanced full
tree is feasible, telescoping gives the stronger O(W log n) bound. This
establishes O(H [n+min(n^2,n sqrt(W L))] log(n+1)) arithmetic work with
L=ceil(log2(n+1)), using the published Gawrychowski--Gorbachev--Kociumaka
product and witness algorithms. For W=O(n) this is
O(n^(3/2) log^(5/2)(n+1)), including full reconstruction and permitting zeros.
It improves the exponent of the prior frontier guarantee in that regime;
it does not resolve unrestricted numerical weights.

The dense reference harness passed 1,092 complete solves: 680 exhaustive
binary inputs, 384 random inputs, and 28 scaling/adversarial fixtures. All
values and reconstructed trees match Knuth and direct evaluation. It also
passed 7,972 cubic interval checks, 8,048 all-root cell checks, 792 explicit
padded products, 792 all-shape truncated-layer checks, and 139,992 tile checks.
Its actual costs were 6,318,862 dense states, 12,381,033 root candidates, and
11,912 constructed keys. At n=256 the largest interior core on mixed {1,2}
weights was 3,857 out of 32,640 positions; near-uniform weights gave 6,196.
The exponentially weighted 64-key geometric control needs all 64 layers,
consistent with dependence on W. Source-hashed data is retained.

This is a proved reduction to a published primitive, with a dense diagnostic
implementation. The actual compact product backend and its complete timing
and operation-count evaluation remain to be built. Novelty is unestablished.
The next action is implementing the condensed representation, finite-product
conversion, and witness reconstruction without silently materializing the
quadratic table. The full original goal remains active.

The final 45-page manuscript compiled without warnings. All pages were rendered
and reviewed in contact sheets; the new proof pages 42--45 were also inspected
individually. The final harness source hash matches its result file. Publication
includes the theoretical construction's implementation boundary explicitly.

## Fifteenth checkpoint: actual condensed constructors and measured costs

The previous reduction was published at 44b248161661a2dc07a5e791c6c1a49cdf54658f.
The next implementation replaces the dense layer tables with top/left
boundaries and nonzero Monge densities. Python and C++ versions implement the
published Gawrychowski--Gorbachev--Kociumaka compression, balanced core split,
staircase merge, decompression, and root witnesses. Product authors retain
credit; OBST reduction/implementation/exposition credit is OpenAI Codex Sydney.

The constructors detect equality of entire consecutive condensed tables and
stop exactly at a fixed point. Uniqueness follows by induction on interval
length. Root reconstruction is iterative and checks every original key.
Ordinary witness maps add a possible logarithmic storage factor relative to
the published succinct witness oracle. C++ uses bounded dense product leaves
of at most 64 cells; these preserve the asymptotic product time. The C++ driver
uses signed-128 arithmetic with an explicit conservative domain check and
n<=8192, while Python uses arbitrary-precision integers.

The final Python product audit passed 1,600 rectangular products, 251,779
cells/witnesses, and 1,600 arbitrary submatrix checks. Three seven-core distance
matrix products through dimension 2048 retain nonempty seven-entry outputs.
The complete Python audit passed 1,134 solves, 838 cubic checks, 32 fixed-budget
controls, 78 fully checked layers (3,367 cells/witnesses), and 15,544 keys.
The C++ sanitizer audit passed 1,278 solves and 18,248 keys with no reported
address or undefined-behavior error. The release run passed 1,362 solves and
88,904 keys, with 1,302 independent Python Knuth comparisons and 826 cubic
checks. Full costs also match the separate C++ Knuth implementation on every
case. Each binary explicitly rejected three invalid inputs.

The complete compiled comparison is negative: all 90 scaling trials lose to
Knuth. At n=2048, the six family median time ratios range from 44.3 to 185.1.
Their maximum completed cores are 17,894--116,104 entries versus 2,098,176
nonempty interval cells, but the product machinery traverses 55.7--306.9
million core entries, and retains 3.68--9.33 million witness integer slots.
These counts expose real costs that representation sizes omit. They are
separate counter categories, not equal-cost machine instructions or RSS.
Measurements use Apple Clang 21, C++20 -O3 -DNDEBUG, exact signed-128 arithmetic,
full preprocessing and reconstruction, and alternating execution order.
Sanitizer timings and independent Python audit costs are excluded from the
performance claims. Three trials per family/size are a scoped experiment,
not a universal performance estimate.

All four new result files have matching recorded source hashes. The actual
constructor now exists; no new asymptotic theorem or practical speedup is
claimed from these tests. The next research target is reducing repeated
core traversal and retained maps, while investigating a representation whose
work does not depend on small total integer mass. The original full mixed-
weight objective is still open and active. This checkpoint does not replace
it with an implementation-only objective.

## Completion requirements

- A fully stated, proved result or substantively validated algorithm for the
  requested mixed-weight problem, with honest scope and prior-art comparison.
- Reproducible correctness and adversarial evidence; practical claims require
  appropriate matched benchmarks against Knuth and relevant alternatives.
- TeX manuscript and compiled, visually checked PDF uploaded to papers_please.
- Continued pursuit of the full objective; intermediate notes are not completion.

## Publication audit of the fifteenth checkpoint

The final 47-page manuscript compiles with Tectonic without warnings. All pages
were rendered and reviewed in contact sheets; the updated theorem introduction
and new implementation/evidence pages 42 and 45--47 were inspected individually.
The rendered table agrees with the three-trial medians in the release JSON.
All four new result files' recorded source hashes match the committed sources.
The updated manuscript preserves the numerical-mass restriction and explicitly
reports all 90 compiled scaling losses. The original objective remains active.


## Sixteenth checkpoint: baseline-centered core bounds

The complete compact constructor and negative compiled measurements were
published at 542854f4d3037fed8bd435dc4de99b301635fe85. Those implementations and
source-hashed results remain unchanged. The next investigation centers the
representation analysis around a=min(p), b=min(q), with total nonnegative
integer deviation R. The solver retains the original mixed weights.

For the same large terminal penalty, the baseline-optimal h-level layer has
an explicit length-only formula. Its nonzero density is supported only at
lengths 2^t-1. The actual layer differs from it by a residual between zero
and h times local deviation mass. Remove those exceptional diagonals and
tile the remainder by maximal dyadic squares. At scale s, O(nL/s) tiles
exist, but each input position lies in only O(n/s) spanning intervals:
the diagonal distances are geometric. Therefore total residual mass over
all tiles is O(nR/s), without an additional factor L. Combining tile area
with integer density mass gives O(min(nLs,hnR/s)) nonzero cells per scale,
and O(nL+n sqrt(hRL)) over all scales including the removed lines.

A normalized height bound uses the minimum positive singleton mass. Every
positive internal interval contains such a singleton. The mixed Fibonacci
subtree inequality therefore bounds depth using W/s rather than W. Balanced
zero-mass subtrees add at most L. In general H=O(log(n+R+1)), independent
of baseline magnitudes. With polynomial R the resulting construction uses
O(n(1+sqrt(R)) log^3(n+1)) arithmetic operations. Thus R=O(n) gives
O(n^(3/2) log^3(n+1)), and R=O(n^(2-epsilon)) gives
O(n^(2-epsilon/2) log^3(n+1)) for fixed 0<epsilon<=2. This extends our
core-size theorem, not the scope of the original objective. Earlier
restricted-weight subquadratic algorithms are still prior work; the
small-total-mass theorem retains its better logarithmic factor.

The dense diagnostic passed 1,100 solves, 824 cubic comparisons, 3,317
all-root cells, 1,538 baseline all-shape checks, 99,087 baseline-density
checks, 685,288 tiles, and 2,327 scale checks. It recorded 4,153,053 dense
states and 8,223,340 candidate evaluations. An independent geometry audit
passed 163 sizes through 4096 and 749 scales, checking every input position's
maximum spanning-interval overlap. These observations audit the code; the
packing theorem is proved geometrically in CENTERED_MONGE.md and the paper.

The actual condensed Python variant passed 999 complete solves, 790 cubic
comparisons, 32 fixed-budget controls, 1,001 intermediate interval values and
leftmost witnesses, 12 original-compact comparisons, and 9,992 reconstructed
keys. Independent key/gap baselines include 2^256 and 2^200. At n=256 the
three large-baseline fixtures finish in ten layers and have completed cores
6,624, 6,540, and 6,496. Their allowed height budgets are 14, 14, and 12
instead of the old numerical-mass budgets of 256. This is not a measured
speedup: the earlier constructor already uses exact fixed-point stopping.
The geometric 64-key control still needs H=64 and has a dense interior core.

A targeted prior-work check also encountered Larmore's 1987 paper titled
Height Restricted Optimal Binary Trees. Its title alone does not establish
a competing full mixed-weight theorem: Larmore and Przytycka's own 1994
abstract identifies that older hybrid bound as length-limited Huffman coding.
Primary source: https://doi.org/10.1137/S0097539792231167 . The full mixed
Larmore/Karpinski-Larmore-Rytter work already cited remains relevant. No
priority claim is inferred from the absence of a search result.

All three new result files match their recorded source hashes. The unchanged
compiled benchmark losses remain prominent. The full mixed-weight objective
is still active; arbitrary nonuniform weights with large deviation and the
compact implementation's substantial overhead remain unresolved.

## Publication audit of the sixteenth checkpoint

The final 50-page manuscript compiles without warnings. All pages were rendered
and reviewed as contact sheets; the revised abstract and new proof/evidence
pages 47--50 were inspected individually. The normalized height, baseline
formula, weighted packing proof, arithmetic-model qualification, and unchanged
negative performance evidence are all explicit. New source hashes match the
three result files. The full original research objective remains active.

## Seventeenth checkpoint: ruler structure beyond sparse differences

The latest JesseSort discussion did not change the OBST research state.
This turn resumed from the clean published 8cf0273 checkpoint, tested the
next representation, and produced three source-hashed exact harnesses plus
a new full constructor. No earlier implementations or benchmark data changed.

When a penalized h-level interval contains at least 2^h-1 keys, maximizing
the exposed count forces a perfect skeleton. Its nonseparable cost is the
negative of a maximum weighted subsequence with ruler coefficients v_2(t).
All gap weights still contribute h times their mass. Independent subsequence,
all-root, and all-shape checks verify the identity. A three-level example
rejects greedy selection of the largest eligible root. Monotone key weights
make the saturated score depend on one endpoint, and hence give zero core
outside the short band even with arbitrary gap weights.

A second identity computes an adjacent swap of optional bottom-level slots:
(1+v_2(g+1))(p_i-p_(i+1))+q_i-q_(i+2). A sufficient linear-time inequality
makes every leftward swap nonincreasing, so the left-filled minimum-IPL tree
is class-optimal without a wide shape DP. Reflection handles the other side.
The existing mixed residual-Huffman gate, not the exchange condition alone,
certifies global optimality. ordered_complete.py implements this exact route
and Knuth fallback. Accepted instances cost O(n log n), or O(n) for monotone
weight lists whose bound requires no sorting. All reconstruction is included.

The positive family p_r=q_r=B+r, B=4(n+1)^3, has R=n^2 and polynomial-size
weights. The baseline forces minimum IPL, and the strict exchange inequality
forces a left-filled last level in every interval. An explicit dyadic-sum
formula answers interval values in O(log n); the full tree takes O(n).
Within each length band, its core equals 3+v_2(s). The next mixed difference
is v_2(s+1)+v_2(s-1)-2v_2(s), nonzero for every interior s. A band with
Theta(n) lengths and Theta(n) placements proves Omega(n^2) support in both
differences and rowwise changes. Explicit support enumeration is therefore
quadratic even for this family with a compact exact formula. This is not a
general computational lower bound, and it does not contradict the earlier
R=o(n^2) core-size regimes.

ruler_layers.py passed 921 layer solves, 70,100 ruler interval identities,
22,437 range-max checks, 20,432 all-root checks, and 2,168 all-shape layers.
It reports 5,708,220 dense layer states and 11,108,348 layer candidates;
the separate full controls use 1,422,592 states and 2,692,718 candidates.
ruler_barrier.py passed 221,284 formula checks across 68 sizes through 512,
202,127 core identities, 179,486 fourth-difference identities, 2,974 shape
enumerations, and 13 cubic checks. Formula/tree controls extend to 65,536.
At 512 all 130,816 core cells and 129,795 valid fourth-difference cells are
nonzero; the theorem only needs the explicitly proved quadratic subset.

ordered_complete.py passed 1,210 complete solves with 826 cubic comparisons,
658 shape-DP controls, and 386 independent minimum-IPL enumeration checks
over 950 shapes. There are 349 certificates, 512 exchange rejections, and
349 global-gate rejections. Sorted geometric controls correctly fall back.
Positive ramps, reflected ramps, and compensated nonmonotone keys certify
through 768 against Knuth. Full positive-ramp construction reaches 98,304
keys, with 98,303 exchange checks, 98,304 constructed keys, 196,607 order-scan
pairs, 98,304 residual contractions, and 121,509 queue comparisons. No
interval table or comparison sort is used in that accepted construction.

A targeted prior-work search did not establish priority. The existing
minimum-IPL shape characterization, residual mixed-node bound, and published
core-sparse product remain credited. Semi-local unit-Monge representations
cannot be imported unchanged for arbitrary weighted subsequence scores.
The new mathematical obstacle is product closure for symbolic dyadic baselines
with arbitrary residual weights; subtracting the baseline need not preserve
the Monge property. The general objective remains active, and the existing
compiled compact backend's negative performance evidence is unchanged.

## Publication audit of the seventeenth checkpoint

The 54-page manuscript compiles with Tectonic without warnings, undefined
references, or overfull/underfull boxes. Every page was rendered and reviewed
in contact sheets. The revised abstract and new pages 50--54 were inspected
individually; the exchange theorem was kept together across the page break.
All three new result files match their recorded source hashes. The manuscript
separates the conditional fast constructor from its exact fallback and the
representation barrier from a general computational lower bound. Existing
source-hashed implementations and measurements remain unchanged. The full
research objective remains active.

## Eighteenth checkpoint: affine-regret corridors

The exact ruler formula now supplies a pruning potential rather than an
explicit density support. A minimum-IPL shape is a binary word over the
bottom slots of a perfect skeleton. Under affine key/gap slopes lambda,mu,
the cost of an expansion moving right across boundary g is
lambda+2mu+lambda*v_2(g+1). Integrating gives
F(g)=(2lambda+2mu)g-lambda*popcount(g). For a prefix with a zeros already
used and b ones still needed, the exact least affine regret through that
state is a four-prefix-sum expression K(a,b). It is at least
(lambda+2mu)ab.

A signed residual rearrangement bound limits any class optimum's possible
gain over the reference to V. Every prefix of a class-optimal path therefore
has K(a,b)<=V. Retained transitions still charge the original weights;
unnecessary retained paths cannot invalidate the exact class optimum. With
D=floor(V/(lambda+2mu)), at most S+1+min(sz,D*bit_length(z)) states survive.
Zero slope, zero gain, and perfect-tree cases have explicit safe handling.
The global mixed residual-Huffman certificate remains separate, with exact
Knuth fallback and a pre-DP budget cap.

The full positive family p_i=B+i+u_i, q_i=B+i+v_i, B=4(n+1)^3, n>=32, now
has two complete construction guarantees. Arbitrary integer perturbations
with total absolute magnitude <=n give O(n log^2 n) time and space;
independent unit perturbations at every position give O(n log n). The
forward slopes are recovered by a median of disjoint half-separated secants.
All fits, sorts, certification, and reconstruction are included. The first
gain bound is V<=h E_p+E_q. The second uses total key depth deficits
2S-h-2 and gap cardinality min(2s,z), yielding V<6S. The large constant
baseline forces the global gate to pass even with zero residual lower bound.
Both weight types vary, may be nonmonotone, and use O(log n) bits. This is
a restricted-family result; no unrestricted or priority claim follows.

A positive n=24 witness costs 13,252,388 in the reference shape and
13,252,387 after moving one expansion by two slots. The old exchange-only
constructor rejects it; the new optimizer finds and certifies the better
tree. At n=98,304 the alternating perturbation similarly improves on the
reference by 13 units, using 410,752 states and 788,734 candidate transitions.
Independent unit perturbations of both lists use 411,924 states. Formula
counts for the unrestricted shape grid and Knuth table at this size are
1,073,807,360 and 4,831,887,360; these dense tables were not executed there.

The final harness passes 1,166 full solves, 802 cubic checks, 1,107 full
shape-DP checks, 782 independent shape enumerations, 819 affine cost checks,
579 minimum-prefix-regret checks, 819 signed-profile checks, 299 retained
optimum checks, 1,383 direct exchanges, 280 slope-recovery pairs, and 42
concentrated-perturbation solves. There are 535 certificates, one budget
rejection, and 630 gate rejections. Two n=1536 controls compare the scaling
families to both dense solvers. All new recorded source hashes match.

The initial matched run revealed wasted shape work before certificate
failure. A preflight compares the original-weight relaxed class-profile
lower bound with the gate ceiling. If the former is larger, no candidate
can pass this sufficient certificate, so the solver skips directly to Knuth.
This does not assert that class optimality fails. The final suite includes
391 preflight rejections and 802 unfiltered controls with equal exact cost
and certificate outcome. A large-baseline near-constant case separately
exercises budget rejection after preflight passes. The only earlier test
interruption was a missing zero counter in progress printing, corrected
before the full suite was rerun; no cost mismatch preceded it.

Final measurements use four solvers in four cyclic orders on ten groups:
40 matched trials, 160 complete constructions, exact Python integers,
M4 arm64, Python 3.9.6 and macOS 26.5. At n=1536 the median paired ratios
versus Knuth are 0.0284, 0.0364, 0.0320 on the three certified families;
ratios versus unrestricted shape DP are 0.0818, 0.1091, 0.0995. Random and
geometric controls fall back, with ratios versus Knuth 1.1247 and 1.0110
at n=768, and 0.9962 and 0.9777 at n=1536. Subunit fallback ratios are
timing variation, not saved Knuth work. At n=768 preflight eliminates
66,048 wasted shape states and 131,582 transitions; versus unfiltered
construction its ratios are 0.6017 and 0.5570. Timings include all
preprocessing and reconstruction. Prior negative C++ backend measurements
remain unchanged, and no optimized prior-library comparison is claimed.

The user's JesseSort suggestion was checked against its current primary
repository (https://github.com/lewj85/jessesort). It already describes
dual-direction Patience decomposition, compact assignment blueprints,
deferred reconstruction, and adaptive routes. These are useful examples
of representing discovered structure before materializing data, not an
unclaimed new sorting direction. Barbay and Navarro's earlier compressed
permutation work (https://arxiv.org/abs/1108.4408) also connects monotone
subsequence representations with adaptive sorting. For full OBST, preserving
inorder key/gap positions and certifying discarded candidates are essential;
sorting weights or importing a pile count alone does not give an exact
composition rule. The affine corridor is a concrete, separately proved
instance of the broader representation principle. No claimed theorem here
relies on JesseSort's reported speedups.

## Publication audit of the eighteenth checkpoint

The final 58-page manuscript compiles with Tectonic without warnings,
undefined references, or overfull/underfull boxes. All pages were rendered
and reviewed in contact sheets; the abstract and pages 53--58 were also
inspected individually. A final page-break adjustment keeps the status
section together and the affected pages were rendered and inspected again.
Both new result manifests match their recorded source hashes. The final
TeX/PDF output copies are byte-identical to the repository artifacts. Exact
family bounds, formula-only dense comparison counts, fallback timing noise,
unestablished priority, and the unrestricted remaining objective are explicit.

## Nineteenth checkpoint: joint-signature block transfers

This turn starts from published afd8e80 and extends the representation beyond
small perturbations of affine slopes. A minimum-IPL shape is encoded by an
inorder key word with S-1 ones and no adjacent zeros: ones are perfect-skeleton
keys, zeros are optional cherries. For c_i=q_i+q_(i+1), its full cost is a
tree-independent constant minus the selected rewards
(1+v_2(r_i))p_i+c_i. The internal and external weights remain present.

For each constant run of (p_i,c_i)=(a,c), the reward from skeleton ranks
r0 to r1 telescopes as U(r1)-U(r0), where
U(r)=(2a+c)r-a*popcount(r). Four boundary-bit pairs determine intervals of
feasible rank increments. Their exact transfers are sliding maxima, computed
with standard monotone deques. No affine fit or residual-gain approximation
is needed. The shape kernel takes O(nk) arithmetic operations for k runs.
Hirschberg-style forward/backward recomputation reconstructs in O(n) space:
split the block list, restrict rank intervals to selected endpoints, and
release profiles before recursion. At level d the total rank width is at
most m+2^d and each subproblem has at most ceil(k/2^d) blocks, giving
O(km+k log k) total sweep work plus linear output. The established traceback
principle is credited to Hirschberg's 1975 primary paper.

The global certificate also compresses. Constant c forces gap weights to
alternate, so at most k key and 2k+1 gap multiplicity records suffice for
sorting and the mixed residual-Huffman bound. For arbitrary nonnegative
u_i,v_i<=M, M>=1, adding B=4(n+1)^2M to every weight forces the gate to
pass. The full standalone constructor is O(nk) time and O(n) auxiliary
space on this family, including input scans, bound construction, and output.
This allows arbitrary block values and gaps changing at every position.
Polynomial M gives O(log n)-bit words. Without the baseline, few blocks do
not ensure certification: p=(100,1,1,1), q=(1,1,1,1,1) has two signatures,
class optimum 218 and full optimum 121. All fourteen four-key trees, cubic
DP, and Knuth independently confirm those values; the gate rejects.

The identity harness was written before the production module. It checks
40 boundary count intervals, 1,365 independent shape/word costs, 228 block
path-independence identities, 120 block reconstructions, and 1,000 forward
and backward transfer vectors by exhaustive word enumeration. The final
M4 run passes 1,023 standalone full solves, 778 cubic controls, 1,023 full
shape-DP controls, 762 independent shape enumerations, and 1,023 compressed
sorting checks. There are 366 certificates, 657 gate rejections (411 in
preflight), and no cost mismatches. Another 1,023 portfolio solves match:
912 route to signatures and 111 to affine. Eight large portfolio controls
also agree; the two 1536-key scaling cases match both dense solvers.

The full standalone constructor reaches 98,304 keys with four and sixteen
signatures. Including traceback, it uses 2,621,448 and 12,058,760 window
queries respectively. Both maximum profile widths are 65,536 ranks; this
is not a peak-memory byte measurement. The four-block case sorts thirteen
records using 26 comparisons, expands 196,609 weights, performs 98,304
residual contractions, and reconstructs every key. Full vectors retain all
source scans, deque operations, potentials, bound work, and output costs.

An initial matched experiment revealed roughly tenfold standalone regressions
on one-key blocks. The final portfolio scans k and calls the signature
kernel only when k<=max(16,floor(n/32)); otherwise it uses the existing
affine solver and its exact fallback. The threshold is empirical, not a
correctness premise. On the explicit positive family, O(nk) work is preserved
even if routed away, since then k>n/32 and O(n^2) is O(nk). The portfolio
does not preserve the standalone kernel's linear-space guarantee on all
such inputs, because the alternate route may use more space. Both APIs
and the negative standalone control remain available.

The final benchmark uses five solvers in five cyclic orders across twelve
groups: sixty matched trials, three hundred complete constructions, exact
Python integers, M4 arm64, Python 3.9.6/macOS 26.5. Preprocessing, routing,
certification, and reconstruction are timed. At n=1536, portfolio/Knuth
ratios are 0.0259 (four signatures) and 0.0961 (sixteen); portfolio/full-shape
ratios are 0.0893 and 0.3958, and portfolio/affine ratios 0.0247 and 0.0981.
The standalone kernel's irregular and affine ratios versus Knuth are
10.4922 and 10.8220. Routing changes these to 1.0612 and 0.0292. Ordinary
random and geometric portfolio ratios are 1.0687 and 1.0216 with fallback.
The old full shape DP is still better on irregular large-baseline inputs:
portfolio/full-shape ratios are 1.9778 at 768 and 3.1576 at 1536. The route
is not claimed optimal. Subunit timing ratios between identical selected
kernels or fallback paths are variation, not saved algorithmic work. Earlier
source-hashed implementations and negative compiled measurements are unchanged.

Targeted searches did not establish priority. Standard deque maxima,
minimum-IPL structure, mixed-node bounds, and Hirschberg traceback are
credited. The full objective still requires a representation covering much
more irregular signatures and taller optimal shapes.

A separate, unpublished probe identifies a possible next step: alternating
two-level key weights with alternating gaps have k=n but their shape optimum
appears directly constructible. Eighty small cases through n=40 matched
the unrestricted shape DP. These are exploratory observations, not a claimed
full theorem or a replacement for the original objective. The next test is
whether a profile-attainment construction extends beyond strict alternation.

## Publication audit of nineteenth checkpoint

The pending work was revalidated from the authoritative checkout after an
intervening JesseSort discussion that made no OBST research progress. Both
new result manifests match all nine recorded source hashes. All sixty
matched trials contain five full constructions, and all paired portfolio
summary ratios recompute from the raw times. The exact harness, independent
transfer oracle, and production reconstruction were inspected against the
proof. No source changes invalidate the stored experiments.

The 63-page manuscript was compiled again with Tectonic without warnings.
All pages have been rendered and visually reviewed, including full-size
inspection of the abstract and new proof, count, timing, and status pages.
The final TeX/PDF are copied byte-for-byte to the user-facing output paths.
The unrestricted mixed-weight objective remains open; the new theorem's
large-baseline condition and the portfolio's space qualification are explicit.
The next research step is profile attainment with fragmented signatures,
starting with independent enumeration before a production implementation.

## Continuation: exact parity intervals for two-level profile attainment

After publishing the nineteenth checkpoint at 8190391, a new independent
probe addressed fragmented signatures. A high key must remain in the
skeleton; a low key may remain only at an odd skeleton rank; removed keys
cannot be adjacent. Exact bit-set states agree with literal enumeration
on all 1,023 binary input patterns through length nine. Merging identical
exact prefix states, while preserving multiplicities including dead states,
covers every pattern through length forty. The final layer represents
2^40 patterns using 658 distinct states (657 live). The M4 run checks
16,972 transitions, 67,888 parity-interval properties, and 5,630 interlaced
endpoint properties. Its source hash matches the authoritative checkout.

An additional direct-tree check covers all 865 eligible binary patterns
through nine keys. With key levels 17 and 2 and alternating gaps 3 and 11,
independent enumeration of minimum-IPL trees matches the recognizer:
359 attain the sorted-profile bound and 506 do not. The final source
manifest includes the probe and its independent tree-enumeration/cost modules.

The resulting invariant now has an inductive proof in PROFILE_INTERVALS.md.
At retained-high boundaries, encode even ranks as 2A and odd ranks as 2B+1.
A and B are integer intervals; when both are nonempty, their lower and
upper endpoint differences are each zero or one. Zero, one, two/three,
or four-plus intervening low keys have four explicit exact transformations.
They preserve the invariant and support linear recognition and witness
reconstruction. This is a reachability lemma, not a completed full solver.

A tempting stronger compression fails: high pattern 010100 reaches ranks
{3,5}, so an ordinary unpartitioned interval invents rank four. The probe
retains that counterexample. The positive relevance is limited but concrete:
for high-count H between S/2-1 and S-1, successful recognition attains the
sorted key-depth profile; constant adjacent-gap sums make the class gap
cost constant. Arbitrary nonperiodic patterns may therefore bypass the
k=n bottleneck. A production constructor, full global gate, independent
BST cost oracles, and operation measurements are still required. This
continuation is separate from the published 63-page manuscript and does
not change that manuscript's claims. The unrestricted goal remains active.

## Twentieth checkpoint: a global alternating-gap bound removes the baseline

The preceding goal turn made progress: 440d6ea published the joint-signature
constructor and the parity-interval reachability lemma. This turn began with
an independent full-constructor harness; its identity-only mode passed 865
profile/tree checks before implementation. The first implementation used the
existing mixed-Huffman gate, passed 2,134 full solves, and reached 393,216
keys. Its initial benchmark is preserved outside the repository as exploratory
evidence, not as the final measurement.

A search for profile-attained candidates that were globally suboptimal led
to a stronger bound. Give one parity of external leaves weight one and the
other parity zero. Deleting a zero leaf and contracting its parent decreases
the selected depth sum by at least one: remaining zeros are separated by
selected leaves, so the sibling cannot contain only zeros. After Z deletions,
H selected leaves remain, with external path length at least E_min(H).
Since S/2<=H<=S, E_min(H)+Z=hH+s. Every minimum-IPL shape attains this
simultaneously for both parities. Arbitrary alternating nonnegative gap
weights therefore have global lower bound G=h*sum(q)+s*(q0+q1), attained
by every class shape. The bound covers all taller trees and needs no baseline.

The level-capacity/rearrangement key bound K=sum sorted(p)_r*bitlength(r)
is also global. Any legal class tree attaining K attains K+G and is fully
optimal. The two-level interval constructor attains K when its high count
is in [S/2-1,S-1] and its profile word is feasible. Its accepted path now
takes O(n) work and space without residual-Huffman work or a large baseline.
For nonperfect sizes, strictly alternating keys always admit an explicit
low-position deletion witness in either orientation. This gives a full
linear family with k=n and arbitrary relative key/gap magnitudes. Nonperiodic
witness-generated patterns also qualify. One key level is direct. Perfect
shapes that miss K retain the old mixed gate or fallback. The exception is
real: p=(100,1,100), q=0 has balanced cost 401 and full optimum 303. An
initial handwritten expected value of 302 in the regression assertion was
corrected after the independent recurrence exposed that arithmetic error;
no algorithmic inequality failed. Cubic DP and Knuth both return 303.

The separate gap oracle checks every tree through nine keys: 13,834 parity/tree
and 69,170 mixed-weight/tree inequalities, including equality of each size/parity
minimum with the formula. The final M4 full suite passes 3,157 standalone
solves and 3,157 portfolio solves, including 2,847 cubic controls and 1,325
shape-DP candidate checks. Recognition matches literal words on 1,022 nonempty
binary patterns. Of 1,201 accepted full solves, 1,083 use global profile
equality, 116 use the old mixed gate, and two are empty. Rejections comprise
86 unsupported key alphabets, 600 unsupported gaps, 241 high-count exclusions,
905 unattained profiles, and 124 failed perfect-shape gates. Rejected full
solves remain exact. Zeros, ties, huge integers, geometric, random, near-uniform,
binary patterns with and without baselines, and earlier affine inputs occur.

Scaling now adds no baseline. At n=393,216, the nonperiodic family has
262,111 signatures, 196,305 interval transitions, and 212,793 membership
queries; strict alternation has 393,216 signatures, 196,608 transitions,
and 262,144 queries. Each reconstructs every key, orders two multiplicity
records, and expands n key weights. Neither uses residual-Huffman contractions
or a dense shape table. Traceback steps equal stored high boundaries.
Ten scaling portfolio controls agree; both n=1536 cases also match Knuth
and the unrestricted shape DP. Larger cases use the proved global bound and
direct tree-cost checks. These are logical work counts, not instruction totals
or measured peak bytes.

The final benchmark uses five solvers in five cyclic orders across sixteen
groups: 80 matched trials and 400 full constructions, exact Python integers,
M4/Python 3.9.6/macOS 26.5 arm64. At n=1536, no-baseline nonperiodic and
alternating portfolio/Knuth ratios are 0.0022 and 0.0033; ratios to the
previous portfolio are 0.0021 and 0.0031, and to full shape DP 0.0018 and
0.0027. The large-baseline control also certifies. Rejected inputs preserve
the previous portfolio, with visible costs: at 768 keys, unattained-profile
and four-signature ratios to the old portfolio are 1.1857 and 1.1662;
at 1536 keys four-signature and affine ratios are 1.0293 and 1.0590.
Ordinary random and geometric portfolio/Knuth ratios are 1.0690 and 1.0375.
Identical kernels and fallback paths vary noticeably; subunit ratios are
not saved algorithmic work. Five short observations per row do not support
precise universal speedup claims. Linear bounds and counts are the primary
evidence. The raw source-hashed vectors retain all results.

GAP_PARITY.md contains the global proof, PROFILE_INTERVALS.md now documents
the completed constructor, and both are integrated into the manuscript.
Targeted searches did not establish priority. The unrestricted mixed-weight
objective remains open. The next extension is arbitrary key profiles and gap
sequences: the gap bound already applies to arbitrary key weights, but finding
an attaining legal tree is separate, and not every instance attains the bound.

### Publication audit of twentieth checkpoint

The three new manifests match all recorded sources (2, 11, and 11 hashes).
All eighty five-constructor trials and every paired summary were revalidated
from the local JSON. The 67-page manuscript compiles with no warnings or
undefined references. All pages were rendered: pages 2--61 are pixel-identical
to the previously reviewed PDF; the new abstract and pages 62--67 were reviewed
at full size. A split final sentence was removed and the affected pages were
recompiled, rendered, and reviewed again. The final TeX/PDF were copied
byte-for-byte to the stable user-facing outputs. The repository-root compile
log accidentally created by an initially mistargeted command was removed;
the unrelated root manuscript source was not modified.

Candidate next directions, not claims in this checkpoint: for arbitrary
key values, a max-Cartesian tree with minimum path length and weight-ordered
depth layers would attain K(p), suggesting a broader linear certificate.
For arbitrary gap values, thresholding the weights suggests replacing the
number of zero leaves by the number of contiguous zero runs in the deletion
bound. A proposed indicator bound is E_min(H)+number_of_zero_runs for H>0.
It must be checked independently and proved before use. Layering such bounds
could extend the global certificate beyond alternating gaps. Both directions
remain future work; no new solver or performance claim is attached to them.
