# Full optimal binary search trees: research record

Started 2026-10-18, America/Chicago. Research and exposition by OpenAI Codex
Sydney, with sponsorship and problem selection by Joshuah Rainstar.

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
remain with Joshuah Rainstar. Priority of the derived certificates remains
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
selection remain with Joshuah Rainstar. General completion is not claimed.
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
Codex Sydney; sponsorship and problem selection remain with Joshuah Rainstar. Novelty remains unestablished.

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


## Twenty-first checkpoint: threshold runs and dyadic rank selection

The next-direction probe from checkpoint twenty is now independently checked,
proved, and implemented. Binary ordered gap indicators have exact optimum
E(H)+R, where H is the selected count and R is the number of zero runs.
Integrating thresholds gives a global arbitrary-gap lower bound G=F+D.
D is a downward-variation scan, and F is a rank-weighted sum with dyadic
coefficient blocks. Repeated deterministic median-of-five selection retains
nested top power-of-two sets, so their total size is less than 3N. Thus G
is evaluated in linear arithmetic work even when every gap weight differs.
The earlier extrema-multiplicity formula remains a cheaper checked scan route.

The key capacity lower bound K has a linear equality test: positive keys
must have exactly the minimum capacity-profile length sum, and weights
must decrease between depth layers. A standard max-Cartesian candidate
attaining K and G is globally optimal for the full mixed objective. The
constructor and all checks/output use linear work and space. With distinct
positive key weights it is an exact recognizer of K+G attainment. It does
not recognize all instances where the candidate happens to be optimal.
Ties and strict lower-bound gaps remain explicit negative controls.

A perfect skeleton with arbitrary odd-slot expansions gives a positive
family with Theta(n) key and gap levels and no large common baseline. Even
slots have maximal gap weight; odd slots have arbitrary intermediate values
or expand into minimum-weight cherries. Key weights decrease by depth.
Every threshold gap problem and the key profile are simultaneously attained.
Independent positive rescaling of p and q preserves this proof, so no
key-versus-gap mass dominance is needed. Joint signatures can all be distinct.

The independent probe checks 1022 binary patterns, 862118 indicator/tree
inequalities, 20560 weighted-tree inequalities and key-profile equivalences,
and 1200 cubic controls. The full harness checks 3000 standalone and 3000
portfolio solves against independent cubic/Knuth, with 2610 literal controls,
21844 gap-vector formulas, 36 positive multilevel Knuth fixtures, six scales
through n=327679, and an iterative 20000-key chain. Twenty dyadic-selection
controls through 100000 gaps cover random, ordered, duplicate, and organ-pipe
inputs. The largest positive family uses 655322 Cartesian comparisons and
constructs 327679 keys; full cost is 253331707448885247. Source-hashed results
retain all scans, selections, comparisons, reconstruction, and fallback work.

An initial five-way matched benchmark found that placing the new candidate
first nearly doubled the cost on uniform old-profile fast paths and added
roughly 50% on earlier nonperiodic profile fixtures. The portfolio was
reordered to try the old profile certificate first, then this certificate,
then the earlier signature/affine portfolio. This avoids the extra candidate
on those old profile successes; a targeted assertion checks that routing.
The whole correctness harness was rerun successfully before the final
matched benchmark. Initial source and timing artifacts are retained outside
the publication tree under work/threshold-first-route*.

During the final matched run, a read-only uptime observation reported
load averages 25.31, 16.11, 13.19 on the M4. Timings therefore are not an
isolated machine benchmark, and visible same-kernel variation must not be
interpreted as saved algorithmic work. Arithmetic bounds and operation
counts are the scaling evidence.

Standard Cartesian trees, rearrangement, threshold decomposition, and
deterministic linear selection remain credited. Prior alphabetic-code
upper bounds also contain variation terms (Bruno et al., arXiv:2407.16443).
Targeted searches do not establish novelty of the lower bound or certificate.
The unrestricted mixed-weight objective remains open. The next substantive
obstacle is nonattainment: separate key and gap optima can be incompatible.
A joint threshold bound or an efficient exact correction for that deficit
would broaden this representation beyond equality-certified families.

### Publication audit of twenty-first checkpoint

All three new result manifests match their recorded source hashes (2, 4,
and 13 files). All eighty final benchmark rows, their paired summaries,
and the old-profile route assertions were revalidated from local JSON.
The final 72-page manuscript compiles without warnings or undefined
references. All pages were rendered; pages 2--66 are pixel-identical to
the preceding reviewed checkpoint. Page 1 and pages 67--72 were reviewed
at full resolution. An almost-empty closing-paragraph page was removed
and the affected pages were compiled, rendered, and reviewed again.
The TeX/PDF were copied byte-for-byte to the stable user-facing outputs.
The final source-hashed timings retain high-load qualifications and all
negative controls. No unrestricted solver or complexity lower bound has
been proved; the full objective remains active.


## Twenty-second checkpoint: joint obstruction and shifted alphabetic certificates

The preceding turn's Jessesort discussion did not advance this goal. The
saved mixed-merge experiments were recovered from the M4, their completed
results copied locally, and all source hashes revalidated before use.

The free-key/fixed-gap relaxation J retains global internal-depth profile
coupling: with P=sum p and S_j the sum of the j largest keys, its key term
is P+sum_t(P-S_{a_t}), where a_t counts internal lengths at most t. The
function P-S_j is decreasing and discretely convex, but no fast minimizer
of this joint profile expression is established.

A proposed extension of compatible merging, adding the next smallest key
to each merged mass, fails on p=(7,1,5,8,6,4), q=(18,2,13,3,17,1,2).
All weights are positive, keys distinct, and all pair choices strict.
The relaxed candidate costs 214, while J=full OPT=213. The candidate's
original ordered-tree cost is 220, a distinction retained in the note.
The failure persists on an open positive perturbation box and extends to
all n>=6 with O(n)-bit weights. All 8192 integer box corners and padding
through 256 keys pass the independent controls. This is a rejection of
one algorithmic rule, not a general computational lower bound.

Uniform transfer p'=p-a, q'=q+a changes every mixed tree cost by an.
It leaves the K+G threshold-bound deficit and the rejected greedy schedule
invariant. Critically, it does NOT leave K+A invariant when A is the
exact alphabetic gap optimum. That distinction led to the constructive
result, rather than ending with only a negative result.

For m=min(p), L=K(p-m)+A(q+m)-mn is a valid full mixed lower bound.
It is the strongest member over the entire admissible scalar-transfer
interval: every affine term after subtracting a E(n+1) has nonnegative
slope. An alphabetic optimum for q+m whose original full cost equals L
is globally optimal. A leftist-heap/priority-queue implementation of the
established Hu--Tucker compatible-merging algorithm, followed by residual
key sorting, yields O(n log(n+1)) complete screening and construction,
with O(n) space. A maximum-original-leaf-index tie representation exactly
implements symbolic leaf weights 2^i without materializing those integers.
Rejection uses exact Knuth. The previous portfolio is unchanged.

The new positive family has n=7*2^h-1 keys and repeated seven-gap blocks.
A perfect skeleton of six-key gadgets is alphabetic-optimal after adding
one to the gaps; the compatible-merge phase proof is in SHIFTED_ALPHABETIC.md.
Residual-positive keys attain capacity, but original unit keys at the
bottom create a deficit (n+1)/7 in the original key bound. Thus the new
certificate strictly extends beyond the original capacity-equality family.
The concrete construction has 6*2^h distinct key weights, six gap values,
all outcomes positive, minimum key weight 1, and O(log n)-bit weights.
No mass-dominance hypothesis is used in the equality proof.

Harness first: the independent shifted-bound probe ran before the optimized
constructor. It checks 960 cubic controls, 3629 scalar shifts, and 37500
literal tree inequalities, with 138 certificates and 24 strictly stronger
than K+G. The implementation matches all 9840 ternary gap vectors through
seven keys, including literal candidate depth sequences. Its 960 full
mixed controls match cubic and Knuth, including 560 exhaustive controls;
336 certify and 624 fall back. All 279 constant-key controls certify.
Eight new-family sizes match Knuth, the four smallest also match cubic,
and a 1199-key skewed tree validates iterative reconstruction/traversal.

Five large constructions reach 229375 keys and 196608 distinct key weights,
with original capacity deficit 32768 and exact full cost 2029411090432.
The independent explicit family tree, output tree, and bound agree.
The largest run records 229375 compatible merges, 458749 priority pushes
and pops, 6885341 priority comparisons, 5136371 heap-item comparisons,
1473827 key-sort comparisons, and 5021690 meld calls; all fixed scans and
full reconstruction/cost visits are also retained. No interval cells occur.
These are logical arithmetic counts, not machine instructions or bit costs.

The matched experiment uses all six orders of standalone shifted,
previous portfolio, and Knuth on seven families at two sizes: 84 trials,
252 full constructions. At n=895, median paired shifted/Knuth ratios are
0.07629 new family, 1.02507 random, 1.14523 near-uniform, and 1.04554
geometric. The known constant-key reduction with arbitrary gaps gives
0.05598. The standalone constructor loses old routes: 213.67 times the
old portfolio on the old profile fixture, and 12.57 times it on the
639-key multilevel fixture. It is therefore not promoted over that
portfolio. All regressions remain in the raw source-hashed JSON.

The host was Apple M4, Python 3.9.6, macOS 26.5 arm64. Load averages were
11.57/11.66/13.47 at start and 13.56/12.13/13.54 at end. Same-process
order cycling, six observations, and this substantial load do not support
precise speedup claims. The mathematical bounds and counters establish
scaling. Hu--Tucker, uniform-key absorption, standard heaps, rearrangement,
and the depth identity remain credited. Targeted prior-work searches do
not establish novelty. The full unrestricted objective remains active.

### Publication audit of twenty-second checkpoint

All six new JSON manifests match their recorded source hashes. Every final
matched ratio was recomputed from the 84 raw rows. The 76-page manuscript
compiles without warnings, overfull boxes, or undefined references. All
pages were rendered; pages 2--70 are pixel-identical to the preceding
checkpoint, and page 1 plus pages 71--76 were reviewed at full resolution.
Stable user-facing TeX/PDF outputs match the manuscript byte-for-byte.
The full unrestricted objective remains active; no completion claim is made.


## Twenty-third checkpoint: all additive transfers and exact endpoint prices

The preceding turn made progress by publishing the shifted alphabetic
certificate. This continuation examined its failures while preserving the
full mixed-weight objective. The authoritative starting checkout was clean
at 15de 44a; the earlier production portfolio remains unchanged.

A rotation argument characterizes every additive reweighting whose cost
change is independent of tree shape, for n>=3. There are exactly three
parameters: a uniform interior transfer and the allocations x,y of the
fixed endpoint masses p_0+q_0 and p_(n-1)+q_n between keys and gaps.
Every such transformation changes all full costs by an. Its nonnegative
feasible region is an explicit box. This is a complete characterization
of additive transfers on these outcome coordinates, not all representations.

The largest separable bound K(p')+A(q')-an is attained at the largest
interior shift, a=min(p_1,...,p_(n-2)). Increasing a and clamping endpoint
residual keys at zero gives a nondecreasing path: with e clamped endpoints,
the relevant gap indicator has minimum E(n+1-e)+e=M(n-e)+n. This reduces
the entire three-parameter maximization to two endpoint prices.

The price oracle uses the existing exact alphabetic implementation and
sorted capacity assignment. It returns both a sampled lower bound on
OPT and an affine upper supporting plane for the concave price-bound
function. An exact determinant/Cramer's-rule hypograph LP selects the
next price. Integer cross-products verify every vertex, with rational
prices and no floating-point tolerances. Sampled lower bounds and original
full candidate costs are retained across calls. Integer-cost rounding can
certify a full tree. Price-maximum completion is recorded separately from
early tree certification and call-budget termination.

With b calls the attempt costs O(b n log(n+1)+b^5) arithmetic operations
and O(n+b) space. A logarithmic default budget is subquadratic; exact
Knuth fallback retains the unrestricted quadratic worst case. Supporting
slopes/intercepts bound LP vertex denominators by O(n^2), adding only
O(log n) bits to scaled oracle weights. The uncapped diagnostic has no
proved small iteration bound; observed call counts are not a theorem.

The complete transfer class still fails on the positive four-key instance
p=(1,1,2,1), q=(1,2,1,1,1): full OPT=24 but max transfer bound=23.
The full lower bound 24 follows from a unit baseline costing at least 20
and l_2+d_1>=4. At maximal shift 1, a fixed capacity assignment and a
fixed alphabetic tree give F(x,y)<=23-y<=23, and x=y=0 attains 23.
Thus no admissible additive transfer can close that particular separable
bound. Only one residual interior key has positive weight, exposing the
remaining internal-order coupling. This is not a general complexity bound.

The obstruction persists throughout an open box of radius 1/100: the
same supporting construction has total coefficient 20, while the largest
unit full-tree cost is 24, giving a remaining gap at least 1-44 epsilon.
All 512 integer corners of 100(p,q)+/-1 pass, with minimum actual gap 94
versus the proved lower bound 56. An all-distinct example has
p=(996,997,1998,999), q=(1000,2001,1002,1003,1004), OPT 23999 and maximal
bound 23004; a constant supporting plane certifies the latter in one call.

A new positive family has n=2^h-1 keys and a perfect optimum. Both endpoint
keys have weight 1; the smallest interior key has weightB=2^h. After the
maximal interior shift and endpoint absorption, the gaps are B+j+1 and
all residual-positive keys attain capacity. Huffman level pairing proves
that the perfect alphabetic tree is optimal because all transformed gap
weights lie in[B+1,2B]. Nearly every key and every gap has a distinct
original weight. The earlier uniform shift 1 leaves a strict bound deficit,
proved by a three-unit improvement in its last four shifted gaps.

Twelve complete constructions reach 262143 keys,262142 distinct key weights,
262144 distinct gap weights, and cost 4569830391807. The independent closed
form is ((8h-11)B^2+(13-7h)B)/2-1. The previous bound falls short by
8590000165 at the largest size. One alphabetic call performs 262143 merges,
7111153 priority comparisons,8924411 heap-item comparisons, and 1482369
key-sort comparisons; all preprocessing, reconstruction, depth, and cost
visits are retained. There are no LP vertices or interval-DP cells on this
family. Seven small sizes match Knuth and three match cubic.

The independent arrangement/transfer harness preceded the optimizer. It
checks 2052 literal transfer identities, exact rank 2n-2 through eight keys,
and 60 independently enumerated arrangement maxima across 5111 rational
points. On 600 mixed cases,1712 oracle calls match independent cubic values;
small cases also match literal trees. All 600 bounded full solves match
cubic/Knuth/direct costs:220 certificates, including 152 previous rejections,
and 380 fallbacks. No earlier certificate is lost in this finite suite,
but no preservation theorem is claimed for the bounded search. The
uncapped diagnostic certifies 228, rescues 160, and completes every price
maximum within ten calls. There are 358 strict bound gaps and 600 exact
clamped-monotonicity checks. Another 6000 seeded positive cases find no
fractional maximum; this is not an integrality claim. Intermediate prices
are fractional and remain exact (the obstruction queries y=1/3).

The benchmark retains 80 matched trials and 320 complete constructions in
four cyclic orders, on ten families at two sizes. At 511 keys, median
paired priced/Knuth ratios are 0.12608 new family,1.30491 random,1.15055
near-uniform, and 1.08209 geometric. Old profile, four-signature, and affine
routes cost 14.64,42.65,37.44 times the previous portfolio, respectively;
the 319-key old multilevel route costs 8.54 times it. This standalone route
is not promoted over the existing portfolio. All regressions remain.

The host was Apple M 4, Python 3.9.6, macOS 26.5 arm 64, with load averages
10.97/11.34/11.74 initially and 11.44/11.44/11.77 finally. Four observations
and same-process cycling under load are not precise isolated-machine
measurements. Mathematical bounds and logical counters establish scaling;
bit costs are additional. The original unrestricted objective remains open.


Checkpoint 23 publication audit: all five new result manifests match their
current source SHA-256 hashes (4, 4, 4, 7, and 17 source entries). All 80
benchmark rows and 20 aggregate rows were inspected, and their recorded
medians and paired ratios independently recomputed. The 79-page manuscript
compiled without warnings, overfull/underfull boxes, or undefined references.
Every page was rendered. Pages 2--74 are pixel-identical to the preceding
reviewed checkpoint; page 1 and pages 75--79 were visually inspected, with
footer separation additionally checked from PDF text coordinates. The proof,
full original-weight construction, negative controls, and regressions remain
explicit. Publication is a research checkpoint, not completion of the
unrestricted objective.


## Twenty-fourth checkpoint: a root partition crosses the transfer barrier

The previous goal turn was progress: checkpoint 23 was published and every
changed remote blob was verified. This turn pursued the remaining positional
coupling, starting with the one-positive-interior-key obstruction. It did not
replace the unrestricted full mixed-weight objective with the one-key problem.

A literal marked-boundary compatible-merge probe rejects greedy activation on
three keys. The residual input p=(0,4,0), q=(8,10,2,18) has optimum 80 but
strict greedy choices return 82. A unit inverse transfer yields all-positive
p=(1,5,1), q=(7,9,1,17), with optimum 77 versus 79. Delaying activation and
trying the cheapest crossing pair at each ordinary-merge prefix matched
17769 cases, including 15769 literal controls; 4134 controls also enumerated
all crossing choices. This remains a conjectural family, not an exact solver.
There were 20800 invalid reconstructed depth sequences across the attempts,
116 greedy failures, 65 merge-charge/positional-cost disagreements, and 6759
nonunimodal sequences. Positive gaps (17,83,93,11) with weight 92 on key 1
produce the exact activation costs 500,681,500. No single-valley search or
subquadratic complexity is claimed for the probe.

The usable advance is a rigorous root/nonroot dichotomy. For a maximum key
weight w at r and second-largest weight v, every tree not rooted at r has
key cost at least K+w-v, by exchanging r's weight with its root's weight.
A tree rooted at r pays the total mass plus independent key-capacity and
alphabetic bounds on its two ordered sides. The minimum of these two cases
is valid for every full mixed tree and dominates K+A at the chosen weights.
It closes checkpoint 23's four-key gap exactly. The implementation applies
the exact maximal interior shift and clamped endpoint residuals, evaluates
original costs, and uses at most three alphabetic calls over 2(n+1) leaves,
one sort, and linear scans. It takes O(n log n) arithmetic work and O(n)
space per attempt; exact Knuth fallback retains the quadratic general bound.

An infinite positive family has N=2^h gaps and n=N-1 keys. Its residual keys
follow perfect-tree capacity order except that the largest weight sits at
the left quarter separator, at comparison length two, and the second-largest
sits at the root. All transformed gaps lie in [C,C+N-1], C=4hN, so the perfect
alphabetic tree is optimal. Forcing the marked key to the root incurs an
alphabetic penalty greater than the capacity cost of leaving it at length two.
The nonroot case certifies the perfect full tree. A constant supporting plane
proves that the entire preceding additive-transfer class is lower by w-v.

The exact full cost is [(8h^2+6h-7)N^2+(12-5h)N]/2+1-3h; the full-class
deficit is [hN^2-(2h-1)N]/2. Every original weight is positive and has O(log n)
bits. There are n-2 distinct key weights and n+1 distinct gap weights.
Twelve full constructions reach 262143 keys, 262141 distinct keys, 262144
distinct gaps, and cost 92530765201355. The preceding maximum is 91912294498251,
a gap of 618470703104. The largest run records three alphabetic calls,
524285 compatible merges, 13894100 priority comparisons, 17365446 heap-item
comparisons, and 1482337 key-sort comparisons, plus all scans and output work.
There are no interval-DP cells. Seven sizes match Knuth, three match cubic,
and six independently complete the old two-price maximum. All larger sizes
match an independent explicit tree and the proved closed form.

The harness preceded the constructor. It checks 246480 literal conditioned
inequalities on 840 mixed instances; the bound improves K+A on 373 and is
exact on 324. The full constructor matches cubic/Knuth/direct cost on 1040
inputs, with 720 literal controls and 800 independent bound controls. It
certifies 505 including 240 tiny cases, falls back on 535, exceeds the completed
price maximum on 84, and rescues 11 price rejections. It loses 47 other price
certificates; the endpoint choice is fixed and the old portfolio is unchanged.

The 88-trial matched benchmark retains 352 complete constructions in four
cyclic orders across eleven families and two sizes. At 511 keys, median paired
new/Knuth ratios are 0.25899 new family, 0.12370 previous endpoint family,
1.21721 random, 1.31079 near-uniform, and 1.18771 geometric. Relative to the
previous portfolio, old profile/four-signature/affine cost 15.47/51.74/43.04
times as much; old multilevel costs 8.35 times as much at 319 keys. These
regressions remain explicit. Apple M4 / Python 3.9.6 / macOS 26.5 arm64 had
load averages 12.42/11.62/11.38 initially and 12.53/11.69/11.41 finally.
Four observations and same-process cycling limit timing precision. Arithmetic
proofs and logical counters establish scaling; bit costs are additional.

A targeted literature check found no basis for claiming priority for this
case-partition construction. Related alphabetic update work includes Belal,
Selim, and Arafat, [Towards a Dynamic Optimal Alphabetic Tree](https://citeseerx.ist.psu.edu/document?doi=a996f60380602c883bbb5a800a425878edbe62f7&repid=rep1&type=pdf), which describes
linear insertion/deletion under a neighboring-weight condition; it does not
supply the marked internal-key event theorem sought here. The new proof uses
standard capacity/exchange arguments and established Hu--Tucker machinery.
The full unrestricted subquadratic or impossibility objective remains open.


Checkpoint 24 publication audit: all five new manifests match their current
source hashes (5, 4, 9, 5, and 19 entries). All 88 matched rows and 22 aggregate
rows were inspected, with medians and paired ratios recomputed independently.
The 82-page manuscript compiled without warnings, layout-box diagnostics, or
undefined references. Every page was rendered; pages 2--77 are pixel-identical
to checkpoint 23. Page 1 and pages 78--82 were visually reviewed, and footer
separation was checked from PDF coordinates. The original unrestricted goal
remains active. The event conjecture is explicitly separated from the proved
root/nonroot certificate and is not used by the full solver.


## Checkpoint 25: audited Monge reduction and a linear-mass core lower bound

The sponsor requested an adversarial attack on representation size, rather
than treating small measured cores as evidence of tightness. Fixed-mass local
search, concentrated starts, and explicit patterns led to a contiguous ramp.
The simplified odd ramp has exact mass W=n, with n=m^2 and m a power of two.
A perfect-slot deletion argument converts fully exposed height-limited
intervals to a weighted ruler subsequence. An exchange proof shows that, for
slack s satisfying m>2s+D, the rightmost s zero coefficients are omitted.
Taking four-window differences gives the exact positive density 2 nu_2(b-2s).
Counting a band yields nm/16-9n/64-m/4 >= n^(3/2)/32 entries in one layer.
The proof is in RAMP_CORE_TIGHTNESS.md and the manuscript. It establishes
polynomial-exponent tightness for explicit intermediate cores, with a remaining
sqrt(log n) gap, not an unrestricted algorithmic lower bound.

The main proof now details every depth change in both rotations, proves the
maximal-tile parent boundary lemma with an explicit constant for arbitrary n,
and quotes ESA 2025 Theorem 1.2 with its core, condensed-form, finite-entry,
and witness definitions checked. The note CORE_SIZE_AUDIT.md records that audit.

The search records 145155 exact layer evaluations across 72 starts and 120
explicit-pattern evaluations. The odd-ramp audit records 445 literal subset
comparisons, 388 all-root slot-embedding comparisons, 42748 deletion formulas,
17688 independent subsequence density checks, and 1896 original-layer density
checks. Its larger formula rows are explicitly not independent DP runs.
The rotation/tiling audit records 2652 straight and 2652 bent identities,
894 partitions, and 4277 scale checks. Source hashes match the executed sources.

The paper was reordered around the Monge theorem and the new size lower bound.
Certificate families are organized under a common certificate theorem; window,
endpoint-response, ruler, and transfer limitations share one negative-results
section. Verification is in appendices. Python timings are removed from the
paper and retained only in the historical research records. The uniform-cost
identity and fixed-position weight convention are explicit. Sponsorship is
Joshuah Rainstar, and the title asterisk links to the requested dedication
at the end. The original unrestricted goal remains active.

Checkpoint 25 publication validation: all five new source manifests match
the executed current sources. All 57 prior mathematical statements remain
in the revised manuscript; labels are unique and every reference resolves.
The 77-page PDF compiles without warnings, missing glyphs, undefined
references, or layout-box diagnostics. All pages were rendered and reviewed
in contact sheets, with the new proof and dedication also inspected at full
resolution. The final bookmark-only change leaves page layout unchanged.
The exact dedication wording is checked in the TeX source, and the Hebrew
is visibly rendered with the bundled static regular font. Stable output
TeX/PDF copies match the repository artifacts byte for byte; a complete
TeX/font source bundle is also supplied. No general-complexity conclusion
is inferred from the new intermediate-representation lower bound.


## Checkpoint 26: per-outcome charging removes a construction logarithm

The early-layer penalty boundary c_h=2^h-1 grows geometrically. Instead of
paying the largest core H times, charge the mass of each accepted dyadic
tile to its individual outcome positions. Padding the input by zero weights
to a power of two, with q_n retained in place, removes the outer cut at n
from this counting argument. Every accepted tile's parent meets one of the
two diagonals. A fixed position belongs to at most 60(1+c_h/s) tile spans
at side s. Hence the scale support is at most
min(24ns,120hW(1+c_h/s)). The resulting bound is

    sum_h delta(E_h) = O(nH+n sqrt(WL)+WL^3+HWL).

At W=O(n), this is O(n^(3/2) sqrt(log(n+1))). The published products and
witness queries therefore construct the full tree in
O(n^(3/2) log^(3/2)(n+1)) arithmetic operations, saving one logarithmic
factor over checkpoint 25. Retained succinct witness structures use space
linear in the aggregate core bound. The old general bound remains available.
The proof is in AGGREGATE_CORES.md and the new manuscript Section 2.7.
The single-layer sqrt(log n) gap to the proved odd-ramp lower bound remains.

The independent harness ran on the selected M4 host. It checks 766 geometry
partitions, 4508 scales, 998378 tiles, and 1891752 per-position incidences.
Its own all-root recurrence checks 290 mixed inputs, 1977 original/padded
layer equalities, 452644 residual bounds, 28013 weighted tiles, 1367 weighted
scales, 548 early layers, and 1139 late layers. It records 685551 dense
diagnostic states and 8636426 candidate roots. No timing is used as a bound.
The exact executed source hash is retained in aggregate_core_audit.json.

Checkpoint 26 publication validation: the executed audit source hash matches
the local source. All 57 legacy statement labels remain, all labels are unique,
and every reference resolves. The 79-page PDF compiles without warnings,
missing characters, undefined references, or overfull/underfull boxes. Every
page was rendered and reviewed in contact sheets; the new proof and final
dedication were also inspected at full resolution. The dedication source is
unchanged byte for byte. Stable TeX/PDF output copies and the complete font
source bundle are refreshed from this revision.


## Checkpoint 27: a local charging obstruction and exact one-key cores

The previous turn made concrete progress by publishing the aggregate bound
and O(n^(3/2) log^(3/2)(n+1)) linear-mass construction. This turn attacked
the remaining per-layer logarithm by testing whether the local 2hW(J_T)
tile-density bound could lose its h factor. That shortcut is false.

The dyadic-mass probe evaluates 1199 inputs including 123 independent all-root
controls, with 19699184 dense states, 38539843 candidate roots, and 1169332
tiles. One concentrated key gives tile-mass ratios 2,3,4 at n=64,128,256.
The normalized family has W=1, h>=4, s=2^(h-2), n=8s, and key x=4s+1.
Its accepted tile [2s,3s) x [7s,8s) has exactly h-3 unit densities, at
(3s+2-2^d,7s), d=2,...,h-2. Both constant local mass charging and constant
local support charging are therefore impossible. The tile's parent meets
the capacity diagonal, so the example uses the actual upper-bound tiling.

The proof first gives an exact one-key layer formula, including intervals
above capacity: exposing c=2^h-1 keys forces a perfect skeleton, and the
weighted key can occupy a precisely bounded range of ruler slots. Four-window
differences of maximum valuations classify every ordinary density. Positive
pairs are consecutive multiples of a power of two, and every density equals
one. In the explicit family there are 2^h-2 below-capacity entries and
2^h-2h above-capacity entries, plus n-c penalty and n completion entries.
Thus the completed core has exactly 2n+2^h-2h-1 entries. More generally,
any one-key input has at most 3n completed entries in each layer. This is a
structural control for the charging approach, not a change of the full mixed
research objective. The existing upper and odd-ramp lower bounds stand.

The independent formula audit checks 700024 interval values, 697992 densities,
and 1023 penalty-line cells through 1024 keys. It uses literal all-root
recurrence through 64 keys and monotone-root recurrence above that. Another
1316 cases cover all key positions through n=16, two masses, and the tested
layers, with 88170 additional density checks. Totals are 6387678 states and
12975174 candidate roots. Larger formula-only evaluations are labeled.
The proof, code, source hashes, and exact records are retained. The new
negative result is grouped with the paper's barriers and verification remains
in an appendix. No empirical fit or timing supports the asymptotic claims.

Checkpoint 27 publication validation: both new manifests match the executed
sources. The dedication remains byte-identical, all 57 legacy statement
labels remain, all labels are unique, and every reference resolves. The
82-page PDF compiles without warnings, missing glyphs, undefined references,
or layout-box diagnostics. All pages were rendered and reviewed in contact
sheets; the new proof and audit were inspected at full resolution. Stable
TeX/PDF copies and the complete source/font bundle are refreshed.


## Checkpoint 28: full mixed slots and capacity-deficit construction

The previous goal turn made progress by proving and publishing the local
charging obstruction and exact one-key cores. The next step extends the
slot representation to the full mixed objective. A gap's depth is the maximum
of its neighboring key comparison lengths (Becker's Lemma 1); in ruler
coordinates this gives a pair reward q_i min(v(t_i),v(t_(i+1))). Both endpoint
gaps retain unary terms. Every height-limited tree embeds in the perfect
tree. Conversely, arbitrary selected slots can be repaired by deleting
unselected keys: surviving key depths do not increase, so the gap identity
also bounds every gap depth. This proves equality of the two optima.

Write t_i=i+y_i and r=2^h-1-n. The states are 0<=y_1<=...<=y_n<=r.
A prefix-by-valuation maximum and suffix maxima evaluate the pair reward.
Inserting valuation d updates d+1 suffix levels; querying valuation e scans
e lower levels. Their total cost is linear in n(r+1), since every ruler
position occurs at most min(n,r+1) times and sum_{t<=c} nu_2(t)=c-h.
Generation tags avoid a hidden h-per-row reset. Threaded BST deletion and
location arrays reconstruct in O(c+n), within the same bound. The concrete
implementation uses arrays, including membership, with no hashing assumption.

This gives exact O(n(r+1)) arithmetic work and words for the prescribed
height, including all original key/gap weights and full reconstruction.
Becker already gives O(n^2) for a near-minimum height; the capacity-deficit
form exposes the linear regime for constant r. The full unrestricted
objective is preserved: selecting a small height does not itself certify
global optimality. The main Monge bound remains unchanged. The positive
example p=(100,1,1,1), q=(1,1,1,1,1) has optimum 121 at height three and
minimum-IPL optimum 218, confirming the class includes more than the earlier
minimum-IPL construction family.

The complementary regime also has an exact formula. Above capacity c, the
exposed skeleton is perfect, all gaps reach depth h, and selecting c keys
maximizes sum_j p_(t_j) nu_2(j). Thus ordinary density cells strictly above
the capacity diagonal are independent of gap weights. The hard mixed
interaction remains below the boundary and on it. Both formulas are proved
in MIXED_SLOTS.md and the manuscript. Primary prior-work check: Becker,
arXiv:1011.1337v1, Lemma 1 and Section 4; no priority claim is inferred from
this targeted check.

The final harness checks 32902 arbitrary subset repairs, 717 full solves,
473 literal slot minima and literal tree minima, 23920 above-capacity
interval formulas, and 18000 gap-independent densities. Height-reference
work is 558638 states and 15547880 root candidates; the separate penalty
controls use 184056 states and 1300792 candidates. Small constructor runs
use 82568 slot states, 145171 suffix updates, and 69863 lower-level scans.
There are 53 scale rows through capacity 4095; 23 have independent all-root
controls. At n=4079, h=12, r=16, the constructor uses exactly 69343 states,
138516 suffix updates, 69190 lower-level scans, builds 4095 perfect nodes,
deletes 16, and outputs 4079. Large rows verify original cost, height, and
slot score, with independent_reference=false; no dense optimum is claimed
for those rows beyond the proved algorithm. Source hashes and operation
counters are retained in mixed_slots.json.

Checkpoint 28 publication validation: the executed source manifest matches
all four current sources. All 57 legacy statement labels remain, labels are
unique, and all references resolve. The dedication is byte-identical. The
85-page PDF compiles without warnings, missing glyphs, undefined references,
or box diagnostics. Every page was rendered and reviewed in contact sheets;
the new representation, amortized proof, complementary regime, and audit
were inspected at full resolution. Stable TeX/PDF copies and the source/font
bundle are refreshed from the final compiled sources.


## Checkpoint 29: binary search and an exact gap-core control

The previous goal turn published the full mixed slot representation and the
capacity-deficit constructor. This turn investigated interactions by restricting
individual weights to zero or one. The fixed-mass search performs 84 runs at
n=16,...,1024, with mixed, key-only, and gap-only placements and four starts.
It evaluates 117084 candidates and records every winner, seed, layer core,
and operational counter. The dense diagnostic uses 40476345560 states,
80519888452 root candidates, and 40301399592 density evaluations. The Python
reference independently audits 81 vectors, including all winners through
n=128 and all-root/all-shape controls on small vectors. These searches imply
no asymptotic mixed/key bound.

The gap-only results led to an exact identity. At capacity c=2^h-1<=n,
define Q_i=max(q_(i+1),q_(i+3),...,q_(i+c)) for i<n-c. The total ordinary
density mass strictly below the capacity line is
S_h=(h-2)W+q_0+q_n+sum Q_i. All above-line densities vanish and each
on-line density equals M-Q_i. The proof selects all but one perfect slot
for a length c-1 interval, then telescopes full rows and the remaining
triangular corner. It includes h=1, c=n, and arbitrary nonnegative real
gaps. Integer gaps give exact completed core 2n-c+S_h-X_h, where X_h is
the sum of positive density excess above one.

For n=2^s>=16, binary gaps with W=n/2 therefore have every layer core at
most (s+1)n/2+4. The early-layer bound is maximized at h=s-2,s-1; late
layers use a perfect skeleton plus one bottom cherry and whole-triangle
telescoping. The explicit family q_i=1 for even i<n, q_n=0, all other
weights zero, gives at least sn/2+1 entries. On intervals avoiding q_n,
its alternating-gap optimum has a closed formula. Four-corner subtraction
gives unit densities precisely for even rows and lengths 2^d-1. Counting
those entries proves the lower bound. Consequently the maximum in this
fixed-mass binary gap class is (1/2)n log2 n+O(n), with matching leading
term. The new theorem is a control for the full objective; it is not a
replacement for the mixed-weight theorem or a new alphabetic constructor.
The mixed odd-ramp core still grows as Omega(n^(3/2)).

The new all-root audit checks 2189 inputs, 5282 mass identities, 32899
one-missing-slot formulas, 22335 capacity densities, 157129 vanishing
above-capacity densities, 3976 whole-triangle identities, and 10524 explicit
family densities. It uses 492579 states and 8892512 root candidates. The
binary bound has 60 eligible layer checks. Search winners attain the proved
upper bound through n=512; the n=1024 winner is one below it. Explicit
alternating family members and search winners through n=128 are checked
against the independent all-root recurrence. Proofs are in GAP_CORE_IDENTITY.md
and Section 2.9; counts and the search table are confined to Appendix E.

Checkpoint 29 publication validation: the new source manifests and the
previous size-bound/slot manifests match current files. All 57 legacy
statement labels remain, labels are unique, references resolve, and the
dedication is byte-identical. The 87-page PDF compiles without warnings,
missing glyphs, undefined references, or box diagnostics. All pages were
rendered and reviewed in contact sheets; the new proof, audit, and dedication
were inspected at full resolution. Stable TeX/PDF copies and the complete
source/font bundle are refreshed. The main mixed-weight theorem and the
remaining sqrt(log n) core-bound gap are unchanged.


## Checkpoint 30: full mixed boundary identity and concentrated mass

The previous goal turn proved and published the binary gap-only leading term.
This turn returns to arbitrary mixed weights. At capacity c=2^h-1<=n,
the exact below-capacity density mass is
(h-1)P+(h-2)Q+q_0+q_n+sum_i G_i-B_tail. Here G_i is the maximum of
q_(i+2r+1)+sum_(l=1)^r nu_2(2l)(p_(i+2l)-p_(i+2l-1)), and B_tail is
the final c-key perfect ruler reward. Omitting one perfect slot and grouping
its reward changes proves this formula; even omitted slots are dominated
by the preceding odd slot. Telescoping rows and the remaining triangular
corner then proves the full identity. It includes arbitrary nonnegative real
weights, h=1, c=n, and the prior gap-only formula as a specialization.

At n=2^s>=16, h=s-1, c=n/2-1, keys alternating 2,1 and every gap equal
to 1 have W=5n/2+1 but below-capacity mass
n^2/8+n(h-3)/4+2((h-1)n+h-c). Exactly n/4+1 entries on the diagonal
j-i=c-1 have density c+1-h=n/2-h; other entries there vanish. Removing
that one diagonal leaves O(nh) density mass. Above capacity only the
j-i=c+1 diagonal can be nonzero, with density c-h on odd rows. Integrality
therefore proves O(n log n) completed support in the same layer. The proof
separates mass from support on strictly positive bounded mixed weights;
quadratic mass is not evidence of a quadratic core. It rules out a naive
global mass-only proof strategy without claiming an algorithmic lower bound.

The independent all-root audit checks 308 inputs, 756 mixed identities,
6656 one-slot formulas, 3376 lower-neighbor densities, 136680 above-capacity
densities, and 80 family formulas. Its reference work is 369396 states and
13048220 root candidates. The family checks cover n through 128 and four
baseline pairs. Source hashes and exact rows are retained.

A separate falsification probe studies T_(h,d), density mass outside the band
|j-i-c|<d. The candidate O(W(L+c/d)) bound remains unproved. If true, it
would give O(n+WL+sqrt(nWc)) support after charging the band directly, and
close the sqrt(log n) loss at W=O(n) after summing layers. The retained run
has 981 evaluations, 105 independent all-root controls, 16327392 states,
32066815 candidate roots, and 16062720 densities. Its largest tested ratio
is 342/151 on a single-key n=255 input at h=7,d=3. This finite result
supplies direction only. The identical diagnostic was rerun after a mirror
sync removed its first uncopied result; the recorded counts are per retained
run. Both final JSON files were copied back before publication.

A direct subadditivity shortcut for off-boundary mass fails: two adjacent
unit keys at h=2 create a length-one density absent for either key alone.
The proposed additive WL allowance must account for mixed/combined outcome
interactions. A proof or explicit growing counterexample for the tail bound
is the next concrete task; the full mixed-weight objective is unchanged.

The exact mixed identity and positive-weight obstruction are in Section 5.9,
with verification counts in Appendix F. The probe and conditional direction
are retained in MIXED_BOUNDARY_MASS.md, not promoted to a theorem. All legacy
statement labels and references remain valid; the dedication is byte-identical.
The 89-page PDF compiles without warnings, missing glyphs, undefined references,
or box diagnostics. Every page was rendered and checked in contact sheets;
new proof and audit pages were inspected at full resolution. The bibliography
starts on a fresh page to avoid leaving its last entry alone. Stable TeX/PDF
outputs and the complete source/font bundle are refreshed.


## Checkpoint 31: exact capacity bands and necessary tail terms

The previous goal turn made progress by publishing the full mixed boundary
identity and the concentrated-mass obstruction. This turn attacks the proposed
off-capacity estimate and develops an exact algorithm for the band itself.
For every retained parent length |k-c_h|<=d, maximum exposure forces both
child deficits (below capacity) or excesses (above capacity) to be nonnegative
and sum to the parent's deficit/excess. Both children therefore stay within
the preceding width-d band. This closes the recurrence without constructing
any off-band interval values.

At each layer the first retained length diagonal scans at most d+1 feasible
roots per interval. Later diagonals use the monotone leftmost roots from the
previous diagonal. Their candidate ranges telescope to at most 2n per length.
This proves O(n(d+1)(H+1)) arithmetic work and stored words for all band states,
roots, and four-corner densities. The implementation uses arrays and includes
prefix sums and initialization. Fully exposed retained states reconstruct
all original keys in linear output time. Width one computes all capacity-line
densities in O(n log n) across the early layers. This is a full mixed-weight
component, not a claim about the still-unbounded tail or an unrestricted
optimum at an insufficient height. It shares work across all interval starts,
unlike the earlier single-instance O(n(r+1)) slot constructor.

The all-root audit covers 272 mixed inputs, 253303 retained entry equalities,
1287 complete tree checks, and 4100 candidate bounds. Reference work is 94179
states and 924277 root candidates; band work is 199627 states and 366637
root candidates, plus separately counted initialization. Sixteen scale rows
include nonperfect n=2^h-1-d at d=0,1,4,16 and h=6,8,10,12. At n=4079,
h=12,d=16, all band intervals across the twelve layers use 1174685 states,
2621548 candidates, and 69224 base entries, then output all 4079 keys. Large
rows check reconstructed cost and counters; independent_reference=false is
explicit. The exact proof and implementation are CAPACITY_BANDS.md and
capacity_band.py; the source-hashed audit is capacity_band.json.

The tail investigation also has two explicit necessity proofs. For the prior
one-key family, r_0=ceil(log2(d+1)) gives exact outside mass
2^(h-r_0+2)-2(h-r_0)-4 when r_0<h, and zero otherwise. Arbitrary one-key
inputs have at most 4w(c+1)/(d+1) outside mass. Taking h=2r,d=2^r-1 gives
ratio to W(L+c/d) exactly (4*2^r-2r-4)/(2^r+2r+3), tending to four.
Thus a universal coefficient smaller than four is impossible. Scaling the
single weight gives the same ratio with W=n. Uniform positive mixed weights
instead give outside mass 2((h-1)n+h-c) at d=2^(h-1), with ratio to WL
tending to one although c/d<2. Hence the WL term is also necessary. The
independent audit checks 496 tail formulas from all-root layers through n=128;
larger rows are explicitly closed-form evaluations only.

The expanded C++ diagnostic evaluates every band width at every early layer.
There are 851 structured inputs and 11868 fixed-mass search evaluations in
18 runs. Structured work is 515067958 states, 991657809 root candidates,
513507096 density checks, and 1560862 band evaluations. Search work is
1044782928 states, 2074271291 candidates, 1037289648 densities, and 7493280
bands. All 133 small reference vectors agree with independent all-root layers.
The largest observed ratio is 20/7 at n=1024, again a one-key input; this
supplies no universal upper bound. A reporting error on the initial zero-tail
n=2 case was corrected before the complete retained run.

A separate all-root probe tests the stronger allowance
T(w)<=sum_x w_x T(e_x)+hW. It covers 3103 basis/input vectors and 46370
comparisons, with maximum normalized excess 17/26. The inequality is still
unproved. A possible structural route is to express a capacity density as
M-F_i-G_i, where G_i is the existing weighted-prefix maximum with gap reward
and F_i is the maximum negative prefix walk. Subadditivity of these maxima
may control interaction at d=1; extending that control to wider bands remains
a separate problem. This route has not been promoted to a theorem.

The band theorem is Section 2.10 and its counts are Appendix G. The necessary
tail terms and diagnostic records are kept in CORE_TAIL_EXTREMES.md, with the
full mixed tail estimate explicitly open. All new executed-source manifests
match, legacy theorem labels and references remain valid, and the dedication
is byte-identical. The 90-page PDF compiles cleanly and is rendered for visual
review. Stable TeX/PDF outputs and the complete source/font bundle are refreshed.
The main O(n^(3/2) log^(3/2)(n+1)) bound at W=O(n) is unchanged.

## Checkpoint 32: sharp width-one interaction and its extension barrier

The preceding turn was progress: checkpoint 31 published an exact full-mixed
capacity-band constructor and explicit necessary tail terms. This turn attacked
the interaction allowance needed for the remaining general tail bound. The
full mixed objective and the main construction bound remain unchanged.

The new exact capacity density is D_h(i,i+c)=M-F_i-G_i. Here G_i is the
previous one-missing-slot weighted-prefix maximum, while F_i is the maximum
negative prefix walk. The long c+1 interval omits one key; its reward relative
to omission of the first key is the negative walk. Combining it with the
short c-1 interval and the two perfect intervals proves the identity.

Summing all ordinary densities and removing the capacity line gives
T_1(w)=R_h(w)-P-2Q+q_0+q_n+sum_i(F_i+G_i), where R is the full interval's
comparison cost after removing terminal penalty. The two maxima are
subadditive and positively homogeneous. Therefore
T_1(w)-sum_x w_x T_1(e_x) <= R_h(w)-sum_x w_x R_h(e_x) <= (h-1)P.
The first inequality is exact in its dependence on the full-interval
interaction. The second follows because all gaps have depth h in the
saturated full interval, and each independent key reward is at most h-1.
This is a theorem for arbitrary nonnegative real mixed weights.

An explicit sharp family uses C=2^h,n=2C,p_even=1,p_odd=0,q=0. All prefix
walks are monotone, so the maxima are exactly additive. The full residual is
(h-1)C+h+1; the sum of unit full residuals is 2C-h-1. Thus the interaction
is exactly (h-3)C+2h+2, asymptotic to (h-1)P. Scaling keys by two gives W=n.
This rules out an O(P) allowance independent of height. The proof computes
the skeleton reward and unit-rank intervals explicitly; no fitted exponent
supports the claim.

A four-key counterexample prevents extending the first inequality merely
by enlarging the excluded band. At h=2,c=3,d=2,p=0,q_2=q_4=1, the tail is
one while both unit tails are zero. Full residual costs are additive, all
gaps having depth two. Thus tail interaction is one but full-interval
interaction is zero. It also defeats every all-width key-mass-only allowance.
The separate candidate T_d(w)<=sum_x w_x T_d(e_x)+hW remains open. Uniform
keys, d=2^(h-1), show its coefficient one would be asymptotically necessary:
unit tails vanish, while the combined tail is (h-1)n+h-c.

The independent all-root audit checks 3091 vectors, 28259 capacity identities,
6416 total identities, 5856 subadditivity bounds, and 5856 width-one bounds.
It uses 371731 states and 3302476 root candidates. Its first wider-band
counterexample is the four-key gap example retained above. The sharp-family
audit uses 194152 states and 6131120 candidates, with 28 unit controls, five
family formulas, three independent interaction differences, and five uniform
wide-tail formulas. Larger rows through h=128 are explicitly formula-only.

The directed C++ diagnostic changes the objective from total-tail ratio to
interaction/hW. It checks every width and early layer. There are 235 structured
inputs and 15 fixed-mass searches with 1200 mutations each; each size has
random, uniform-key, and uniform-gap starting modes. Small independent
all-root controls verify 150 optimized vectors. Including basis profiles,
structured work is 1296 evaluations, 157388626 states, and 313030555 root
candidates. Search work is 21006 evaluations, 1667827872 states, and 3310832256
candidates. Its maximum ratio is 1223/1536 on uniform keys. This does not
certify the open all-width upper bound. All weights, seeds, and source hashes
are retained in the new result records.

The paper adds the capacity interaction theorem and sharpness corollary in
Section 2.11, the wider-band barrier in the grouped negative-results section,
and operation counts in Appendix H. It compiles cleanly to 93 pages. The
previous 57 legacy labels and the verbatim dedication are preserved. The
full mixed tail estimate is still the outstanding upper-bound target; the
new theorem resolves its width-one interaction component and gives a concrete
reason that the same proof cannot cover arbitrary widths.

## Checkpoint 33: sparse weights falsify the all-width interaction route

The preceding turn was progress: it proved a sharp width-one interaction
allowance and isolated a small wider-band obstruction. This turn investigated
whether above-capacity tails could still be controlled by full-interval
interaction, then changed the search distribution to sparse weights.

An independent all-root diagnostic found a ten-key counterexample to the
one-sided control: h=3,c=7,d=2,unit keys at 3 and 6. The sole eligible upper
cell has density two, both unit tails vanish, and full-interval interaction
is one. The original skeleton rewards 3,3,3,1 give a direct proof. The audit
checks 2956 vectors and 91370 inequalities, using 1770275 states and 28876151
candidate roots.

The sparse search then falsified the broader proposed allowance
T_d(w)<=sum_x w_x T_d(e_x)+hW. It covers every unit pair on keys and gaps
through n=64, structured unequal-weight pairs, and small random supports
through n=512: 19614 inputs total. Growing ratios reach 6/5,23/12,22/7,85/16
at sizes 64,128,256,512. This is actual falsification of a previously open
candidate, not evidence for a theorem. The earlier dense-start searches
missed these pairs. Their historical records remain intact.

The winners yielded an explicit family with a closed-form proof. For h>=5,
C=2^h,c=C-1,n=2C, put unit key weights at C-5 and C and zero elsewhere.
At width four the combined tail is 21C/16-3h+1 and the sum of unit tails is
C-4h+4. The excess is therefore 5C/16+h-3. Since W=2, its ratio to hW tends
to infinity; no absolute constant multiple of hW repairs the rejected
allowance. Scaling both weights by C gives W=n with the same ratio.

The proof removes terminal penalties and forms the interval cost interaction
E. Summing density diagonals reduces the tail interaction to
E(0,n)+F_(c-3)-F_(c-4)+F_(c+3)-F_(c+4). Full interaction is h-3. The four
band sums are C-8,7C/8-8,5C/8-6,7C/16-6. They follow from explicit feasible
rank pairs, two periodic lower-side tables, and upper-side formulas involving
neighboring ruler valuations. Both clipping corrections are included. Thus
the growth is proved from exact rank formulas, independently of the search.

Independent all-root layers for the pair and both unit inputs through h=7
check 123585 eligible densities, 920 band entries, and all three family
identities, using 870624 states and 66536256 root candidates. Literal rank
choices check 32424 local formulas through h=12; 415042 feasible pairs are
counted. Rows through h=128 are explicitly closed-form-only. Source hashes
match all executed scripts. The sparse diagnostic includes unit-profile
construction and records 4587178568 states, 9062247119 root candidates,
and 19197336 band evaluations; retained winners through n=64 have independent
all-root controls.

The main O(n^(3/2) log^(3/2)(n+1)) construction theorem is unchanged. The
broader target T_d=O(W(L+c/d)) is not falsified: the new family's tail and
that target are both Theta(C) at d=4. What fails is assigning all interaction
to the logarithmic term. The c/d contribution must cover joint optimization
as well as independent unit-input tails. This closes the proposed additive
interaction route and changes the next proof target accordingly.

The paper adds the explicit sparse barrier in the grouped negative section
and puts search and formula counts in Appendix I. Current proof notes and
PR text identify the all-width allowance as false; earlier research-log
entries retain their historical status. The 94-page PDF compiles cleanly.
The 57 legacy labels and the verbatim dedication are preserved.

The same exact telescoping separates the excess: C/8 lies below the band
and 3C/16+h-3 above it. Each side individually defeats every O(hW)
interaction allowance. The all-root family audit additionally checks all
six one-sided equalities through h=7.


## Checkpoint 34: coupled rank-reward stability and periodic obstruction

The preceding turn was progress: an explicit sparse family disproved every
all-width additive O(hW) interaction allowance. This turn returned to the
broader target T_(h,d)=O(W(L+c_h/d)), retaining joint optimization instead of
trying to add separately optimized unit-input tails.

The expanded sparse diagnostic evaluates 23183 inputs through n=1024,
including every unit pair on keys and gaps through 64 keys, unequal pairs,
phase-changing combs, ramps, and random small supports. Its maximum exact
ratio to W(L+c_h/d) is 485/168. A separate repeated-cluster diagnostic checks
462 inputs through n=2048 and reaches 2828/1107. The first uses 17157958100
states, 33808959382 root candidates, and 47383400 band evaluations. The
second uses 3107692416 states, 5649382012 root candidates, and 3997440 band
evaluations. Five and two retained small winners, respectively, have
independent all-root controls. These finite searches neither certify nor
falsify the asymptotic target.

A new rank-coordinate stability theorem applies to any real skeleton-reward
template v and nonnegative key weights p. Let S_v(i,j) be the maximum reward
of a c-element subsequence, and U_d(v) the summed upper densities at interval
length at least c+d. Increasing any one rank reward by Delta changes this
tail by an amount in [-2P Delta,P Delta], where P=sum p. All input-weight
interactions remain inside the maximizing subsequence.

The proof gives canonical leftmost optima by componentwise lattice minima.
They are monotone in both interval endpoints. A tail telescope leaves two
alternating boundary sums and one full-interval score. As one reward varies,
the selected positions in the boundary sums interlace. Cancelling repeated
positions leaves coefficients in {-1,0,1}; the full score contributes a
single additional negative weight. Integrating the piecewise-linear
slope bound proves the theorem. This is an exact proof, not an extrapolation
from the perturbation audit.

For the ruler template of capacity C-1, clipping all rewards at t removes
exactly 2^(h-t)-(h-t)-1 reward units. The theorem therefore bounds the upper
tail by the clipped-template tail plus P times this exact quantity. Choosing
t=min(h-1,floor(log2 d)) makes the error at most 2PC/d. The original upper
OBST densities equal these subsequence densities even with arbitrary gap
weights, since all gap and interval-mass terms cancel above capacity.

The remaining periodic component cannot be absorbed into a height-only
allowance. For the alternating rank template v_r=1 at even r and zero at
odd r, take n=2C and unit keys at C-5,C. The width-two tail is C/2-4. This
falsifies every constant multiple of tP at d>=2^t with t=1,P=2. The proof
computes the two telescoped boundary sums as 2C-6 and 3C/2-4 and the full
reward as two. Thus both the clipping error and the retained periodic part
can need capacity-dependent control. This obstruction concerns the auxiliary
template, not a newly claimed original-layer identity.

The generic rank audit checks 432 small inputs, 3777 literal intervals,
27717 literal subsets, 6817 path-coordinate inequalities, 15930 perturbation
bounds, 45840 ruler-clipping bounds, and 540 mixed-layer identities. It
records 286337285 matching candidates and 1350475 interval scores. The
separate periodic-family audit checks 491 boundary entries and 20 family
identities through h=7, using 2429031 matching candidates. At h=3, 48620
literal subsets independently check all 55 interval scores. Rows through
h=128 are explicitly closed-form-only. Result records retain executed-source
hashes. A wording-only clarification of the rank audit's scope was followed
by rerunning that audit and its importing periodic-family audit.

The paper adds the stability theorem and clipping corollary in Section 2.12,
the periodic obstruction in the grouped negative section, and the audit
counts in Appendix J. The main construction bound is unchanged. The upper
periodic tail and the below-capacity mixed tail remain open components of
the broader target. The independent rank lemma does not assume the rejected
input-unit additivity route.

The 97-page manuscript compiles without warnings. All pages were rendered
and inspected in contact sheets, and the new proof pages and final dedication
were inspected at higher resolution. References resolve, all 57 legacy
labels remain, and the title-asterisk dedication and sponsor name are
preserved. Stable TeX/PDF outputs and the complete font-bearing source
archive are refreshed for publication.


## Checkpoint 35: width-sensitive alternating tails by matching augmentation

The preceding turn was progress: rank-coordinate stability controlled the
high clipped rewards and a two-key family showed why the periodic remainder
still required capacity-dependent control. This turn attacked that remainder,
starting with the alternating level-one template and retaining arbitrary
nonnegative real key weights.

A compiled generic rank-template probe evaluates 25683 inputs, including
exhaustive small binary vectors, structured periodic combs and sparse
clusters, and fixed-mass mutation searches through 256 keys. It tests the
ratio U_d/[P(t+(c+1)/d)] at every width. The largest ratio is 321/292 on
the full height-seven ruler template with unit keys at 123 and 132. This
falsifies coefficient one for the displayed inequality, but supplies no
asymptotic upper bound. The alternating-template maximum is 121/210, on
widely spaced unit keys. The engine records 84957303 interval scores,
4737828651 candidate transitions, and 82044166 densities. All 451 small
control vectors agree with the independent Python subsequence recurrence.

The new theorem proves, for every odd c=2m+1>=3 and all d>=1,

U_d <= P min(m, 2+(c-3)/d)

for the alternating template v_r=1 at even ranks and zero at odd ranks.
The subsequence problem is exactly maximum-weight matching of cardinality m
on the path with edge indices i+1,...,j-2. After deleting a selected first
edge and the first vertex, there are d+1 unmatched vertices. The d segments
between consecutive unmatched vertices are explicit augmenting paths with
disjoint matched-edge sets. One removes at most a 1/d share of the remaining
matched weight. This proves the endpoint inequality

d [S(i,j)-S(i+1,j)] <= (d-1)p_(i+1)+S(i,j),   j-i=c+d.

Tail telescoping and a k-2 interval-overlap count give the stated upper
bound. Classical augmentation is credited to Berge; the path packing and
tail charge are proved directly. Nonnegative real weights suffice, with
no independent-input additivity assumption.

Both scales are necessary. For C=2^h, K>=3, C>=4K, n=2C, place K unit keys
at x,x+3,...,C, where x=C-3(K-1). At width d=K the exact upper tail is
ceil(x/2)-1=ceil((C-3K+1)/2). The proof enumerates endpoint losses by parity
and telescopes their boundary corrections. K=2^floor(h/2) tends to infinity,
and U_K/(Pc/K) tends to 1/2. Scaling by n/K gives integer total mass W=n.
For the additive term, c=3 is an interior range maximum. K unit keys spaced
s positions apart give exactly K-1 unit densities at distance s-1; allowing
K,s to grow rules out a bound O(Pc/d) alone.

The independent audit compares generic subsequence and cardinality-matching
recurrences on 2887 inputs. It checks 147191 endpoint bounds and 58142 tail
bounds, and explicitly builds 41517 augmenting paths in 18703 packings.
Every repair is checked for cardinality, feasibility, removed weight, and
score. Sixteen cluster-family instances through C=128 include 1045 endpoint
formula checks and 32 terminal-score checks; eleven spaced-max families
check the additive term. Larger rows through h=128 are formula-only.
The generic recurrence records 14081433 candidates and 163010 scores; the
matching recurrence records 18877851 transitions and 219352 scores.

The first implementation of the independent matcher included the left
filler as a reward edge. The four-key input (0,1,0,0) exposed this off-by-one
error immediately. The corrected recurrence starts with edge i+1; all
reported counts come from the corrected and fully completed audit. A final
rerun additionally checks the higher-rank counterexample below. Executed
source manifests match both result records.

The exact obstacle to carrying the endpoint inequality unchanged to level
two is already visible on ten keys. With c=7,d=3,p_3=1 and template
(0,1,0,2,0,1,0), S(0,10)=2 and S(1,10)=1, whereas p_1=0. Thus the left
side of the proposed endpoint inequality is three and the right side is
two. Augmentations can change the rank-dependent reward of a retained key.
Accounting for those changes is the next proof problem. The alternating
upper theorem settles one component; it does not narrow the full mixed
OBST objective or change the main construction bound.

The manuscript places the upper theorem and its sharp-scale corollary in
Section 2.13, the retained-rank obstruction in the grouped negative section,
and all finite counts in Appendix K. It compiles without warnings to 99
pages. Contact-sheet review covers every page; the new proof, obstruction,
audit, and dedication pages also received detailed visual inspection.
All 57 legacy labels, references, the title asterisk, sponsor attribution,
and verbatim final dedication are preserved. The stable TeX/PDF files and
complete source/font archive are refreshed for publication.

## Checkpoint 36: exact rank accounting and a tie-independent repair barrier

The preceding turn was progress: an exact matching augmentation proof settled
the alternating upper tail, including both sharp scales. This turn pursued
higher ruler rewards by recording the signed reward change of every retained
edge during an endpoint augmentation.

The representation remains exact: the even-rank rewards of a length-2m+1
subsequence are rank-dependent rewards on an m-edge path matching. The loss
of an augmentation is the deleted first-edge reward, plus removed-edge
rewards, minus added-edge rewards, plus the signed changes on retained edges.
The new diagnostic checks that identity literally for every candidate repair.
Each canonical run evaluates 7225 inputs, with 6976 generic-subsequence
controls, 224622 endpoint checks, and 26402 global repair certificates.
Leftmost starts yield 1385304 paths and 13185 strictly excessive local losses;
rightmost starts yield 546117 paths and 7087 strictly excessive losses.

There is a useful positive canonical lemma: optimal matching tuples form a
lattice under componentwise min/max, and their rightmost member avoids the
first edge exactly when the true endpoint loss is zero. Thus rightmost
choices eliminate spurious repair charges at zero-loss endpoints. This
explains why the canonical runs differ without treating a measured difference
as a theorem about the nonzero losses.

A unique-optimum local family settles the latter issue. With u=(1,2,1),
p_2=p_3=2B, p_4=B, p_6=2B-1, and old interval [1,10), its unique optimum
is (2,4,6), score 6B-1. The shortened optimum (3,6,8) has score 6B-2.
The two available augmentations score 2B and 5B-2. Actual endpoint loss
is one while the best single augmentation loses B+1 for every B>=1.

The stronger global family uses C=2^h, c=C-1, n=4C, d=C, and one unit key
at x=C/2+1. Its true upper tail is zero, but the smallest endpoint-repair
certificate over all optimal old matchings and single augmentations is
(h-2)(h-3)/2. Rightmost optima attain this minimum. The unique optimal key
rank changes at i=x-2r+1 for powers r=1,2,...,2^(h-2). Each true loss is
one. At r>=2 the forced dense prefix permits no augmenting path before the
key: crossing it removes it, and repairing after it leaves odd rank r-1.
Every optimal starting matching therefore has best repair loss nu_2(r).
Summing these losses and subtracting the full score h-1 proves the formula.
The target scale P(t+(c+1)/d) is h, so the certificate ratio diverges.
Multiplying the unit weight by n gives W=n and the same ratio.

At the largest threshold, r=C/4, an optimal shortened matching places the
positive key at rank r/2. Its symmetric difference from the old remaining
matching must contain at least C/8-1 decreasing and C/8 increasing
alternating components. Counting edges before the shared positive edge
proves the lower bound. Explicitly removing the first C/8-1 remaining
zero-weight edges and inserting C/8 zero-weight edges after the key attains
it for a rightmost old witness. These component counts do not imply a
running-time lower bound; a compressed operation might shift many zero
edges at once. They rule out a bounded-component local repair continuation.

The independent exact-family audit checks 3786 canonical zero-loss statements
on 306 inputs, 16 unique-optimum parameter instances with 160 literal old
matchings, 4088 boundary witnesses and loss formulas through height ten,
and 225 independent scalar-DP witnesses. It enumerates all optimal old
matchings at both height-three thresholds and the largest height-four
threshold, giving 1023 tie-independent repair checks; the two smallest
optimum sets also agree with unrestricted literal enumeration. The audit
constructs 32352 repair paths and eight exact many-component optima. Full
generic subsequence tables verify the zero true tails through height five;
larger rows through height 128 are explicitly formula-only. Source hashes
match the completed Mini runs. No timing or fitted exponent is used.

The manuscript groups the new results in Section 5.13 and puts finite
counts in Appendix L. The main Monge construction and core-size bounds are
unchanged. The wider clipped tail and below-capacity mixed tail remain open;
the next matching route must allow joint or compressed rank shifts rather
than bounding this single-augmentation certificate.

The 102-page manuscript compiles without warnings. All pages were rendered
for contact-sheet inspection; the new section, appendix, and final dedication
received detailed visual review. All 57 legacy labels and all references
resolve. The title asterisk, Joshuah Rainstar attribution, and verbatim final
dedication are preserved. Stable TeX/PDF outputs and the complete source/font
archive are refreshed for publication.
