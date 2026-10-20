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

## Checkpoint 37: exact weighted cluster tails and input sensitivities

The preceding turn was progress: it proved that even the best local matching
repair certificate can overcharge a zero true tail. This turn tested a route
that measures the true tail directly, by charging its response to changes
in individual input weights.

A preliminary canonical-witness probe checks 5616 Euler identities on 608
inputs and eleven exact directional controls. Its coefficients sum against
the input weights to the true tail, but coefficients selected by canonical
ties need not equal right directional derivatives. The subsequent compiled
recurrence maximizes the pair (ordinary score, reward at the perturbed key)
lexicographically. This gives the exact right derivative in each interval.
An independent check scales integer input weights by t+1 and increments the
chosen key by one, where t is the largest template reward. No primary-score
gap can close under that perturbation, so the signed tail difference gives
the derivative exactly without floating-point approximation.

The full-ruler fixed-mass search evaluates 21020 inputs through 256 positions,
with 3119522724 candidate transitions, 20512788 scores, and 19108544 density
derivatives. All 29 independent scaled-perturbation controls agree. The
largest observed derivative ratio to h-1+2^h/d is 416/129 at n=128. This
finite value neither proves nor disproves an asymptotic full-ruler bound.
The search retains exact weights and source hashes.

The useful exact result comes from the alternating spacing-three family.
For C=2^h, K>=3, C>=4K, n=2C, c=C-1, x=C-3(K-1), put arbitrary nonnegative
real weights w_0,...,w_(K-1) at x,x+3,...,C. Then

U_K = (ceil(x/2)-1) min_r w_r.

The old boundary intervals reward every cluster key. At each interior bad
parity endpoint, the shortened interval must leave one key unrewarded, but
can choose any one. Its exact loss is the minimum weight. The final left
endpoint loses w_0 specifically; later endpoint losses and the terminal
score cancel that correction. Enumerating omission counts for first,
interior, and last unrewarded keys proves every case, including K=3.
This yields the fixed-mass maximum NP/K, attained exactly at equal weights,
where N=ceil(x/2)-1. It extends the earlier unit family rather than adding
a separate empirical scale claim.

The exact formula gives directional derivative N min_(r in I) z_r, where
I is the minimum-weight set. A unique minimum has individual derivative N.
At a tied minimum every coordinate increase alone has derivative zero, while
increasing all cluster weights together has derivative N. These responses
show why an aggregate charge can be valid without uniformly small individual
sensitivities.

An explicit linear-mass family makes this obstruction asymptotic. Take
K=2^r>=4, C=K^2, h=2r, n=2C, d=K, and cluster weights
(K,3K,2K,...,2K). Their total is exactly n and their unique minimum is K.
The true tail is NK and the first key's right derivative is
N=(K^2-3K+2)/2. Its ratio to h+C/d=2 log2 K+K tends to infinity.
This is an obstruction to pointwise sensitivity bounds for the alternating
auxiliary template. It leaves the proved aggregate alternating bound intact
and does not refute the corresponding full-ruler sensitivity question.
A charging argument covering the periodic auxiliary problems must handle
interacting groups of keys, as the exact minimum formula does.

The weighted-family audit compares independent generic-subsequence and
cardinality-matching tables on 81 inputs. These include all ternary weights
on a three-key cluster, arbitrary unequal weights, tied minima, and zeros.
It checks 3652 endpoint formulas, 162 terminal scores, 169 coordinate
derivatives, and 47 joint increments. Generic controls use 44724022
candidate transitions and 308926 scores; matching controls use 28460181
transitions and 187123 scores. Larger formula-only rows are labeled.
All executed-source manifests match the completed Mini results.

The manuscript now gives the weighted theorem in Section 2.13 and obtains
the earlier unit lower family as its corollary, replacing the duplicated
unit proof. Section 5.14 contains the pointwise-sensitivity obstruction;
Appendix M contains the finite diagnostics. The main construction bound,
explicit core lower bound, and full mixed-weight objective are unchanged.
The next theoretical work must retain joint weight effects; one concrete
question is whether nested threshold sets can supply a valid aggregate
charge, which has not yet been tested or proved.

The 103-page manuscript compiles without warnings. All pages were inspected
in rendered contact sheets; the weighted proof, sensitivity corollary,
new appendix, and dedication received detailed visual review. All 57 legacy
labels and references resolve, and the dedication is byte-identical to the
previous checkpoint. Stable TeX/PDF outputs and the complete source/font
archive are refreshed for publication.

## Checkpoint 38: threshold falsification and a direct local support target

The preceding turn was progress: the weighted cluster formula showed how
an aggregate charge can survive large individual sensitivities. This turn
first tested a nested-threshold transfer, then returned directly to the
remaining logarithmic factor in core size.

The nested-threshold proposal was U_d(p)<=A integral U_d(1_{p>=a}) da.
The exact diagnostic evaluates 14432 inputs and 35722 widths, including
exhaustive ternary interior vectors on ten positions. It records 1852
violations of the coefficient-one upper relation and 4003 of the reverse
relation. A separately retained zero-denominator example proves a stronger
failure, for every finite A.

Take n=10,c=7,d=1 and p=(0,0,0,0,2,1,1,2,1,0). The two nonempty binary
threshold sets are {4,5,6,7,8} and {4,7}. For the full height-three ruler,
the six boundary scores of p are (5,6,5;5,4,6), yielding tail one. The
threshold score rows are (3,3,4;3,3,4) and (2,3,1;2,1,3), each yielding
zero. The alternating template has the same tail pattern 1,0,0. Thus no
multiplicative transfer from binary threshold tails can hold. The proof
table is checked independently by 876 literal subsequences for 36 scores,
generic recurrence comparisons, and three original all-root terminal layers.
This is a falsification for the full ruler, not merely an auxiliary example.

The direct core-size target is an open local hypothesis:

K(T) <= A (s+W(J_T)),

for nonnegative integer weights, accepted maximal dyadic tiles of side s,
and inclusive outcome spans J_T. It counts support, not density mass. The
side term permits the known one-key logarithmic obstruction. Rescaling
shows why integer normalization matters. The target is not proved.

Its conditional consequences are now explicit. The established count of
24n/s tiles and span-mass overlap 60W(1+c/s) give
K_(h,s)<=min(24ns,A[24n+60W(1+c/s)]). Dyadic summation gives
K_h=O_A((n+W)L+sqrt(nWc_h)). Summing growing capacities and adding the
proved late-layer bounds yields
S=O_A(nH+(n+W)L^2+n sqrt(W)+HWL).
At W=O(n), this would be O(n^(3/2)) aggregate support and
O(n^(3/2) log(n+1)) construction work, matching the odd-ramp core lower
scale. The paper retains the existing main theorem; this is conditional.

A positive special case is proved. With one positive key and zero gaps,
any side-s ordinary square wholly off the capacity line contains at most
1+floor(log2 s)<=s nonzero densities, whether or not dyadically aligned.
The ruler-pair mapping puts its two endpoints in ordered intervals of
at most s integers with gap g>=2. Every contributing dyadic interval
crosses a common point, so at most one occurs at each scale. Pair lengths
lie in [g,g+2s-2], a ratio at most s, proving the bound. The old maximal-tile
family has log2 s-1 entries, so the leading logarithmic scale is sharp.
The proof resolves the dependence on side length rather than assuming that
a finite height test controls arbitrary h.

The broad boundary-plus-mass diagnostic evaluates 21436 inputs through 1024
keys, including non-power-of-two sizes, sparse unit outcomes, and fixed-mass
key/gap/mixed searches. It visits 87706185 accepted tiles. Its maximum
observed ratio is 121/136. There are 93 independent all-root input controls,
covering 15301 independently counted tiles. The compiled run records
3240243236 states, 6584091125 root candidates, and 3217996956 densities.

The maximum-over-all-tiles objective often settles on a tiny tile, so a
second diagnostic targets capacity-adjacent tiles with s>=4 and c>=4s.
It preserves mass n/4 or n, evaluates 37224 inputs through 512 keys, and
visits 212592240 tiles; its maximum eligible ratio is 11/14. Six retained
size-64 winner tiles have independent all-root checks. The run records
8185066752 states, 16269275134 candidates, and 8131873536 densities.
Neither finite search proves the open support hypothesis.

The one-key audit checks 1038774 maximal squares over every key position
at selected sizes through 128 keys, 1300 arbitrary squares including
non-dyadic sides, and 155 support sets against independent all-root layers.
All five new result records retain matching executed-source hashes.

Section 5.15 contains the threshold obstruction. Section 6.1 states the open
local hypothesis, proves the one-key square lemma, and gives the conditional
summation. Appendix N contains the diagnostics. The next proof obligation
is a height-independent support charge for interacting integer outcomes;
telescoping density mass alone still supplies only the older hW allowance.
The full mixed-weight goal and its current main bound remain unchanged.

Publication validation: Tectonic compiled the 106-page manuscript without
warnings, undefined references, or overfull/underfull boxes. All pages were
rendered and inspected in contact sheets; the new proofs, diagnostic appendix,
and final dedication were also inspected at reading resolution. All legacy
result labels and the exact dedication source were preserved. The five new
executed-source manifests match the committed-source candidates. Stable PDF,
TeX, and a self-contained source ZIP with the Hebrew font and license were
refreshed from this build.

## Checkpoint 39: exact full-ruler clipping sharpness

The preceding turn was progress: checkpoint 38 published the threshold-tail
obstruction, the one-key square lemma, and the conditional boundary-plus-mass
target. This turn attacked the open size question directly and tested a
second route through width-sensitive sequence-selection tails. The full
mixed-weight objective and the main construction bound remain unchanged.

A fixed-side variable-integer-mass search evaluates 40557 inputs through
256 keys, visiting 121969824 accepted tiles. It improves the observed local
ratio to 136/149 (side 32, core 136, local mass 117). All 15 retained small
winner tiles agree with independent all-root layers. Counts are 2806155040
states, 5480712131 root candidates, and 2774094048 density evaluations;
independent checks use 2266528 candidates and 109936 states. The winners
concentrate near the main diagonal, so they do not resolve the difficult
capacity-adjacent support charge. No upper bound is inferred.

The broader proposed general-template inequality
U_d <= A P(max v + sum v/d) is false for every constant A. A joint
input/template search tested 22212 inputs through 128 positions, with
maximum ratio 16/17, and missed the explicit family derived afterward.
That search uses 865917888 score transitions and 9089940 densities; three
small tails have 34560 literal-subsequence controls over 54 scores.

For the counterfamily take d>=1,m>=2,C=2d(m+1),c=C-1,n=2C, unit keys
at one-based C-3d,C, and binary rank rewards at 2d,4d,...,2dm. The long
boundary sum is C-3d+m+1, the short sum C-3d, and full reward two. Thus
U_d=m-1. Taking m=d gives unbounded ratio (d-1)/4. This is a sparse
auxiliary-template obstruction, not a disproof of the full-ruler tail target.

The same aligned input yields a new exact full-ruler theorem. For
a>=0,b>=3,d=2^a,Q=2^b,C=dQ,h=a+b,n=2C, place unit keys at C-3d,C.
Then the full ruler has U_d=5Q/4-3b+2, while clipping at level a gives
zero tail. Any gap weights cancel above capacity. Scaling key weights
scales mass but preserves support; this is not a new core-cardinality
lower bound. The ratio to the existing clipping allowance P(Q-b-1) tends
to 5/8, proving that allowance has the necessary PC/d order.

The proof checks compatible low/high optimizers on every boundary interval
rather than assuming additivity. At slack d or d-1, feasible two-key ranks
are r-u,r+3d-w with 0<=u<=w<=e. Rounding to multiples of d preserves
feasibility and an optimal high reward while attaining the low optimum;
the near-endpoint case and full interval are handled explicitly. Dividing
multiple ranks by d makes every non-phase boundary score cancel, leaving
a width-one coarse ruler on Q-1 ranks. Its even-start contributions sum
to Q-b-2, odd-start contributions to Q/4-b+4, and full reward is b.
The low clipped tail vanishes because its one-key densities lie strictly
inside width d and its two-key boundary scores are compatible sums.

A preliminary guess Q-b-2 matched the first two small coarse sizes but
was not retained: the parity calculation gives 5Q/4-3b+2, confirmed at
all subsequent sizes. The closed-form statement and final artifact use
only the latter formula.

The final audit covers 16 parameter pairs through 1024 keys, checking 3544
compatible score decompositions and 3544 coarse mappings. Twenty generic
subsequence tails through 128 keys use 2370068 transitions and 20424
densities. Twelve original all-root controls through 64 keys include
nonzero gaps and scale-seven key weights, using 1473440 candidates and
71664 states. Literal enumeration checks 11520 subsequences for 18 full-
ruler scores, plus 840 subsequences for 14 sparse-template scores. There
are 28 independent sparse-template boundary-sum controls. Overall explicit
rank enumeration uses 174756 single-rank and 433864 pair-rank candidates
for 14276 scores. Formula-only large rows are separately marked.

The manuscript places the exact theorem beside rank clipping, the sparse
template obstruction with the negative results, and counts in Appendix O.
RULER_CLIPPING_SHARPNESS.md gives the expanded proof. All four new JSON
records have matching executed-source manifests. The next outstanding
proof obligation remains the height-independent local support charge,
or a genuinely larger explicit core family; the new tail formula prevents
trying to eliminate the necessary clipping term along that route.

Publication validation: Tectonic compiled the 108-page manuscript without
warnings, unresolved references, or overfull/underfull boxes. All pages were
rendered and inspected in contact sheets; pages 17--19, 83, 106, and the
final dedication were additionally inspected at reading resolution. All
57 legacy result labels and the exact dedication source are preserved.
The four new result manifests match their executed-source files and the
recorded independent-input artifact. Stable TeX, PDF, and the self-contained
source ZIP with its Hebrew font and license were refreshed from this build.

## Checkpoint 40: a sharp unit-support envelope and surviving interactions

Checkpoint 39 established exact full-ruler clipping sharpness and left the
local support target open. This turn continued the size-bound investigation
by isolating every possible single-outcome contribution. The full mixed-weight
objective and the main construction bound remain unchanged.

An initial zero-run compression check found that unrestricted removal of
zero-weight keys was already covered by the existing contraction certificate.
Height-constrained layers retain the lengths of those runs. No duplicate
solver or new unrestricted compression claim was introduced.

The new single-gap classification is exact. Below capacity c=2^h-1, put
g=c-(j-i)>0. A unit gap at x gives density one at x=i or x=j+1 precisely
when g+1 is a power of two. For i<x<=j it gives one precisely when
g+2=2^r and x-i-1 is congruent to 2^(r-1) modulo 2^r. All other
off-capacity densities vanish, including every above-capacity density.
The proof expresses gap reward as the largest aligned dyadic block in an
integer window and explicitly accounts for the one-block and two-block
endpoint differences. The scale contributions cancel except for the stated
residue class.

Combining this with the key ruler-pair formula gives a universal envelope:
below capacity its distances have g+1 or g+2 a power of two; above capacity
g+1 is a power of two. Every dyadically aligned side-s square off capacity
contains at most 2s envelope cells, with the stronger 2s-1 below capacity.
The proof enumerates the possible powers in the tile's distance window,
including C<s and non-power-of-two input boundaries. The union over all
unit outcomes attains 2s-1 in [0,s) x [2s,3s) at n=C=4s. This is a
union across inputs, not a simultaneous single-input core claim. Over early
layers the entire envelope has O(nL^2) cells. The expanded note also gives
the weaker 8s bound for arbitrary integer-aligned squares.

Removing every envelope cell still does not restore a constant-per-weight
charge. For s=2^t, t>=3, n=8s, C=4s, c=C-1, h=t+2, place unit keys at
one-based X=3s+3 and Y=4s+2. The maximal tile [0,s) x [5s,6s) has
local mass two. For r=2,...,t-1, its cell

    i=s+3-2^r, j=5s+2^(r-1)

has density exactly one and capacity distance 3*2^(r-1)-2, outside the
entire unit-outcome envelope. The proof reduces every feasible positive
rank pair to one containing 2s or 3s. At the four witness corners its
score is t+max(floor(log2 x),1+floor(log2 y)), with
X-a=2s+x and Y+c-b=3s-y. The four-corner difference is one. Hence
off-envelope support divided by local mass is at least (log2 s-2)/2,
which diverges. No exact formula for the tile's total support is claimed.
The proposed K(T)=O(s+W(J_T)) bound remains compatible and unproved.

The single-gap audit checks 274066 original-layer densities, using 3079878
root candidates and 307625 states. It also checks 78240 maximal envelope
counts, 688 literal counts, 248 key-support sets, and 1222 arbitrary squares.
The directed off-envelope search examines 819 two-outcome inputs through
2048 keys, using 3760248528 states, 7001021069 root candidates,
3755113776 density evaluations, and 22696956 tile visits. Six small
winner tiles agree with independent all-root layers (718432 candidates,
35984 states). The search supplied direction; the explicit theorem above
provides the asymptotic obstruction.

The final witness audit covers s=8,...,1024 and n=64,...,8192. It checks
36 density witnesses and 144 score formulas by feasible-rank enumeration,
with 23808 single-rank and 2090940 pair-rank candidates. At n<=128,
twelve generic subsequence score controls use 302446 transitions and 2806
score entries; three original-layer density controls use 2375360 all-root
candidates and 59936 states. The larger cases retain independent rank
enumeration, rather than being formula-only rows. All three new records
have matching executed-source SHA-256 manifests.

The manuscript places the interaction obstruction in Section 5.17, the
single-gap formula and envelope in Section 6.1, and counts in Appendix P.
UNIT_SUPPORT_ENVELOPE.md gives the expanded proofs. The next unresolved
obligation is still a height-independent local support bound for interacting
integer outcomes. The new results identify a small universal single-outcome
part and show explicitly why the residual interaction needs a scale-aware
charge as well.

Publication validation: Tectonic compiled the 112-page manuscript without
warnings, unresolved references, or overfull/underfull boxes. All pages were
rendered and inspected in contact sheets; pages 84--87, Appendix P, and the
final dedication were additionally inspected at reading resolution. All
73 existing sec:legacy labels and the exact dedication source are preserved.
Stable TeX, PDF, and the self-contained source ZIP with its Hebrew font and
license were refreshed from this build.

## Checkpoint 41: exact binary dilation and a replication barrier

The preceding goal turn was progress: checkpoint 40 published the unit-support
envelope and explicit off-envelope interaction witnesses. This turn attacked
their amplification inside one maximal tile. The general mixed-weight goal
and its main complexity bound remain unchanged.

A directed fixed-tile search evaluates 2470 inputs through 1024 keys. It
replicates and translates the original pair, shares endpoints, varies the
two sides' integer weights, and mutates keys in the two-cluster region. The
largest observed K/(s+W(J_T)) is 12/25. The compiled recurrence uses
1858339360 states, 3315818765 root candidates, and 6790720 density
evaluations. Six retained tiles agree with independent all-root layers,
using 7126080 candidates and 179808 states. These finite maxima establish
no support bound; they redirected attention to exactly aligned replication.

There is an exact reduction for arbitrary binary key patterns. Fix coarse
capacity c=2^h-1 and replicate every key into d=2^ell identical copies,
with fine capacity d(c+1)-1. On a fine interval [a,b) that is at or above
fine capacity, cuts no positive block, and contains m<=c positive blocks,

    S_fine(a,b)=m(d-1)+S_coarse(ceil(a/d),floor(b/d)).

The proof first establishes binary saturation for arbitrary nonnegative
rank rewards: an optimum retains min(P,c) ones. A missing one can replace
the nearest selected zero across selected ones, increasing the selected
binary word componentwise. A block of d consecutive ones then has ruler
reward d-1+nu_2(floor(r/d)+1), where r is its starting rank offset.

Fine feasible ranks map to coarse ranks by floors. The converse needs
compatible phases, rather than independent rounding. If the endpoint
phase ranges intersect, one common phase works. Otherwise the phase must
increase once. An edge whose coarse rank gap is smaller than its input
gap permits that increase. If no such edge exists, the endpoint phase
difference equals fine capacity minus interval length and is nonpositive,
a contradiction. This proves that every coarse choice lifts. Empty-positive
and single-positive cases are included explicitly.

On rectangles with a fixed positive set and the stated capacity separation,
the exact density transport is

    D_fine(di,d(j+1)-1)=D_coarse(i,j),

with all other fine densities zero. Core cardinality and density mass are
preserved. Arbitrary nonnegative gap weights cancel above capacity on both
grids. With zero gaps, side and local input mass both multiply by d, so the
local support ratio decreases by exactly d. For d>=2 every transported
positive density lies outside the fine unit-outcome envelope. Thus removing
that envelope can leave the entire transported core, while replication
still supplies no amplification in these interior rectangles.

The two hypotheses are necessary. Cutting a positive block in the replicated
(1,0,0) input gives fine score one but rounded prediction zero. Taking more
positive coarse blocks than capacity in the replicated (1,1) input gives
fine score one but prediction two. Both are checked by literal subsequences.
The identity does not assert control of densities whose endpoints cut
positive blocks, or of unequal positive weights. These are possible places
for a different amplification to arise; the O(s+W(J_T)) target remains open.

Independent verification includes 1536 binary-saturation cases with 21588
literal subsequences and twelve literal choices for the two scope examples.
Forty dilation instances give 6142 score controls and 4392 density controls,
using 416654 generic subsequence transitions and 8958 score entries.
Original all-root layers with arbitrary nonzero gap weights check 2286
entries and 1434 densities (398656 root candidates, 38304 states).
All 42 positive controlled fine densities lie outside the unit envelope.
The tests include unaligned endpoints inside zero blocks.

Twenty-seven larger pair, alternating, and three-block controls through
1024 keys preserve core cardinality and density mass exactly. They use
22874208 states, 40616815 root candidates, and 84672 density evaluations.
This larger audit uses monotone roots, independently controlled at smaller
sizes by the preceding all-root recurrence. All three result records have
matching executed-source SHA-256 manifests. The final C++ source compiles
without warnings; its initial unused-variable warnings were removed before
the final recorded search was rerun.

The theorem and support-transport corollary are in Section 5.18, with
verification counts in Appendix Q. BINARY_DILATION.md contains the expanded
proof. This checkpoint preserves the full research objective and identifies
an exact obstruction to amplifying the known pair by aligned binary blocks.

Publication validation: Tectonic compiled the 113-page manuscript without
warnings, unresolved references, or overfull/underfull boxes. Every page was
rendered and inspected in contact sheets. The new proof and corollary on
pages 85--86, Appendix Q, and the final dedication were additionally inspected
at reading resolution. All prior labels and the exact dedication source are
preserved. The three new executed-source manifests match their source files.
Stable TeX, PDF, and the complete source ZIP with its Hebrew font and license
were refreshed and checked against this build.


## Checkpoint 42: a linear plateau core and incompatible ruler levels

This turn continued the size-bound objective from checkpoint 41. It targeted
positive endpoint cuts and unequal blocks, then derived exact structure for
one constant positive block. The full mixed objective, main complexity
bound, and general local boundary-plus-mass hypothesis remain unchanged.

The endpoint-cut probe evaluates 1960 inputs through 1024 keys, including
replicated random coarse templates, positive endpoint fringes, unequal
weights, and integer mutations. Its maximum observed K/(s+W(J_T)) is 20/37.
The compiled run uses 1707458304 states, 3241769152 root candidates, and
6204928 densities. Fourteen retained tiles agree with independent all-root
layers, using 16627520 candidates and 419552 states. This finite result
establishes no upper bound.

For one contiguous block of m equal positive keys and arbitrary nonnegative
gaps, the above-capacity core has at most max(0,c-m-1) entries, where
c=2^h-1. A linear constructor returns their coordinates and values. The
proof has three separate reductions:

1. Binary saturation retains all available positive keys up to capacity.
   If a density endpoint removes or adds a positive key inside the plateau,
   all relevant scores either saturate or depend on only one endpoint.
   Reflection uses nu_2(2^h-r)=nu_2(r). Thus these densities vanish.
2. Whole-block intervals optimize a single sliding block reward
   R_m(r)=m+s_2(r)-s_2(r+m), equivalently a constant plus the number of
   binary carries in r+m. Feasibility is one interval of possible r.
   The four-corner density is the positive part of the smaller endpoint
   height minus the largest interior height.
3. These strict horizontal visibility pairs cannot cross. The usual
   polygon count gives at most N-2 nonadjacent pairs for N=c-m+1.
   A decreasing stack enumerates them with their exact density values;
   computing the ruler by its even/odd recurrence and sliding sums costs
   O(c) arithmetic operations. Since nonempty above-capacity regions have
   c<n, total construction is O(n). No population-count instruction is
   assumed in the operation bound.

The horizontal visibility geometry is established prior work, credited to
Luque et al. (2009) and Gutin, Mansour, and Severini (2011). The manuscript
supplies a self-contained count and stack proof and identifies the exact
OBST block-reward reduction. It makes no novelty claim for the graph fact.
The one-key family n=2C, z=C+1 has C-2h above-capacity entries against
bound C-3, proving that the global leading coefficient one is sharp.

The same representation yields a local corollary: every s-by-s square
strictly above capacity has at most 2s-1 positive densities. The visibility
endpoints lie in two ordered disjoint index intervals of size at most s.
Neighbor sets in successive left rows have decreasing, internally disjoint
spans and can share at most one endpoint; at most k+t-1 pairs occur for
k left and t right endpoints. This proves the desired boundary charge for
one plateau above capacity, independently of its amplitude. Multiple
unequal blocks and the below-capacity mixed region remain unresolved.

The plateau audit compares 5561 complete support sets, including values,
with the original all-root recurrence through 64 keys and nonzero gaps.
It checks 1143360 densities, 635883 positive-endpoint zeros, 193533 literal
visibility pairs, and 23375 block-reward identities. It also checks 50032
local square bounds, exhaustive through twelve keys and sampled at larger
sizes. The original recurrence uses 33319148 candidates and 2723869 states.
Twelve sharp-family constructor rows reach 32768 keys; these are explicitly
not original-recurrence runs. The largest row computes 16383 ruler values,
16382 sliding updates, 16383 pushes, 16369 pops, 32738 pair candidates,
and 16356 output densities.

A separate probe asked whether the full ruler optimum equals the sum of
individually optimized binary rank thresholds. It does not. The search
checks 65454 inputs using 15176940 transitions and finds a 22-key example
with full reward seven against threshold optima (5,2,1). Literal enumeration
checks all 170544 length-15 subsequences. A reduced 16-key example has
unit keys at one-based positions 9,12,14, full score three, and separate
threshold optima (2,1,1). No minimality claim is made.

An explicit family turns that mismatch into a theorem. For h>=5, n=C=2^h,
c=C-1, put unit keys at X=C/2+1 and Y_r=C/2+4r+2 for 0<=r<h-1.
Every subsequence deletes one key. Deleting before X gives one rank reward
h-1; deleting after X gives up to h-1 rank rewards of value one. Deleting
X gives zero. Thus the full optimum is h-1, but the threshold optima are
h-1,1,...,1, summing to 2h-3. Their ratio tends to two. This excludes
independent exact level optimization and any universal comparison constant
smaller than two for that upper estimate. It does not prove a universal
factor-two upper bound, an OBST approximation barrier, or a core lower bound.
The earlier nested input-threshold tail obstruction concerns a different
operation; the new theorem holds with the input already binary.

All 32752 single deletions in the small example and explicit family through
16384 keys are enumerated, with 425838 retained rank evaluations and
5176333 threshold comparisons. Smaller instances have 22 generic subsequence
controls (145386 transitions, 66 score entries) and four original all-root
controls with nonzero gaps (2812064 candidates, 73456 states). Larger rows
are exhaustive deletion checks, not original all-root layers.

The first plateau audit attempt used int.bit_count, unavailable in the
Mini's Python, and stopped before emitting results. Its independent formula
control was changed to bin(x).count('1'); the production constructor already
used the linear even/odd recurrence. The final rank audit computes each
retained valuation once and counts all threshold comparisons. Both final
audits were run after these corrections, and the plateau audit was rerun
after adding the local-square corollary. Their manifests identify the
executed sources.

The constructive theorem and local corollary are in Section 2.14, the
rank-threshold obstruction in Section 5.19, and all new verification counts
in Appendix R. PLATEAU_CORE.md and RANK_THRESHOLD_OBSTRUCTION.md give
standalone arguments. The next general obstacle is a support charge for
several interacting blocks, where a single range-maximum sequence no longer
represents the full joint optimization.

Publication validation: Tectonic compiled the 118-page manuscript without
warnings, unresolved references, or overfull/underfull boxes. Every page was
rendered and reviewed in contact sheets; the new proof pages 21--23,
rank-threshold theorem on page 89, Appendix R, and final dedication were
also inspected at reading resolution. The final sharpness proof explicitly
starts at h>=3, and the shortened appendix heading avoids a split word.
All 317 prior labels and the exact dedication source are preserved. The
three new audit manifests match their executed sources. Stable TeX/PDF
outputs and the self-contained source archive, including the Hebrew font
and license, were refreshed and checked against the final build.


## Checkpoint 43: complete two-block cores and finite band dominance

The previous turn was progress: checkpoint 42 published a linear one-block
core and an exact rank-threshold incompatibility. This turn attacked the
interaction of positive blocks. It first obtained a whole-block product
identity, then expanded the endpoint analysis to cover the entire ordinary
above-capacity core for two equal positive key blocks. Arbitrary nonnegative
gap weights remain in the objective and cancel only on this side. The full
mixed-weight research goal and main complexity theorem remain unchanged.

The core algebraic component is a finite representation of

    H(A,B)=max {f_1(u)+f_2(v):u<=A, v>=B, 0<=v-u<=d}.

For sequences of length N, set K=1+range(f_1)+range(f_2). Prefix and suffix
penalties are K max(u-A,0) and K max(B-v,0). The middle matrix is
K[max(u-v,0)+max(v-u-d,0)]-f_1(u)-f_2(v). Its two hinge diagonals are
its whole core; all operands are finite. Any inadmissible pair pays at
least K and loses to every feasible pair's worst possible score. Thus the
product equals -H on B<=A+d. The published core-product inequality gives
at most 14(N-1) core entries and O(N log(N+1)) construction work.

A local bound is stronger than merely restricting this global count.
For an s-by-s output square, aggregate all earlier input rows into the
first row and all later columns into the last column, leaving the middle
indices as singletons. Blockwise minima preserve Monge. The grouped
kernel has at most 4s core entries: two interior hinge diagonals and one
boundary row and column. Its two selectors have at most s entries each.
Two uses of the product inequality give 22s output entries. The proof
specifies the finite penalties and admissible groups, rather than assuming
that an infinite-entry band satisfies the published interface.

For blocks [z,z+m) and [z+m+g,z+m+g+k), binary saturation retains all
m+k positives whenever m+k<=c. With N=c-m-k+1, feasible offsets satisfy
0<=v-u<=g, u<=z-i, and v>=c+z+g-j. Rewards are R_m(u)+R_k(m+v).
This gives the finite band model and the density map

    i=z-a-1, j=c+z+g-b-1.

For m+k>c every whole-block interval saturates, so its ordinary densities
vanish. This initially established only the interaction of complete blocks.

The endpoint cases extend it to the whole above-capacity region. A left
cut leaves a=z+m-i positive keys in the first block, all at the first a
selected ranks. With B=c+z+m+g-j, its exact unsaturated score is

    F(a)+max_(max(a,B)<=t<=min(a+g,c-k)) R_k(t).

Outside the two diagonals j-i=c+g-1,c+g, either it is independent of the
right endpoint or it is a single range maximum and has visibility support.
Reflection handles right cuts. When both endpoints cut positives, the score
is F(c) if their combined count reaches c, otherwise F(a)+F(b). Its density
vanishes except on the same two diagonals. Eight block-boundary row/column
lines cover changes between endpoint pieces. One-block regions use the
previous theorem.

Adding these disjoint cases gives at most 28n above-capacity entries and
40s entries in every side-s square, independently of the common positive
weight. These constants are conservative. This is a proved local boundary
charge for the interaction, including all positive cuts. It leaves unequal
block weights, additional blocks, and the below-capacity mixed region open.

The implemented constructor enumerates the O(n) proof candidates. Scalar
and range-maximum formulas evaluate all endpoint cases. Complete-block
scores query the condensed product via an offline sweep of weighted core
prefix sums, using a Fenwick tree. Thus both construction and exact values
cost O(n log(n+1)) work. The reused multiplication builds ordinary witness
arrays, so the conservative implemented space bound is also O(n log(n+1));
no linear-space claim is made for those arrays. The output itself is linear.

Verification was staged before the theorem was added to the manuscript.
The generic band audit checks 1332 inputs, 28024 finite product entries,
2098072 literal pair candidates, and 23821 feasible scores, including signed
arrays and infeasible completion entries. The first run checked grouped
core sizes; a second audit added 11808 exact grouped-product entries, on
3996 groupings, to test the local representation rather than only its loose
support bound. The constructor was then expanded to all endpoint cases,
and both final audits were rerun against the final source.

The interior control has 576 support sets on 168 mixed inputs through 32
keys, 5690 densities, and 672 literal subsequence intervals from 20517 choices.
It uses 1345248 all-root candidates and 146592 states. Twenty-four larger
condensed constructions reach 16384 keys and supply 661 square controls;
those are constructor checks, not original all-root references.

The complete audit checks 952 mixed inputs through 64 keys: all 792 binary
words with exactly two positive runs through ten keys, plus 160 seeded
larger patterns with common positive key weight three. Gap weights are
nonzero. All 2953 above-capacity support sets, including values, and 334032
density cells agree with the original recurrence. It uses 12507215 root
candidates and 784506 states. Fourteen larger full constructions reach
8192 keys, with 864 local square checks at sides at least 64, where the
40s bound is smaller than the square's area. The largest two-unit-key row
considers 31017 distinct density candidates and outputs 3219 entries, with
26527 range queries and 15631 condensed value queries. All sparse-product
operations are recorded separately. The bounds rely on the proofs, not on
these counts or a fitted exponent.

The new constructive section is 2.15 and the verification appendix is S.
TWO_BLOCK_CORES.md supplies the complete standalone argument. The one-block
and two-block results now give exact control of two successive levels of
interaction. The next general obligation is to control additional interacting
blocks or unequal weights while preserving their joint rank optimization.

Publication validation: the 121-page manuscript compiled cleanly with Tectonic.
All pages were rendered and inspected in contact sheets; the new proof pages
23--26, verification appendix on page 119, and final dedication on page 121
were also inspected at reading scale. All 326 prior labels remain, all 333
current labels are unique, and references resolve. The dedication source is
byte-identical to the previous checkpoint. Both final audit source manifests
match the committed sources. The stable TeX and PDF were refreshed byte for
byte, and the five-member source archive includes the matching source and
bundled Hebrew font with its license.


## Checkpoint 44: arbitrary-key rank transfers and two dense-core barriers

The previous turn was progress: checkpoint43 published the complete two-block
above-capacity theorem and constructor. This turn tested the next extension,
namely whether finite band products alone could give a boundary charge that
remains uniform as the number of interacting blocks grows.

The exact representation now covers arbitrary nonnegative key weights.
Partition them into r constant runs (w,m), and let F(t)=sum_{j<=t} nu_2(j).
A run's finite transfer matrix is

    Q(u,v)=K[max(u-v,0)+max(v-u-m,0)]+w F(u)-w F(v),
    K=1+F(c) sum_runs w.

Its only core entries are on the two band boundaries. Feasible paths select
counts per run and preserve their original order and exact weighted ruler
reward. Every invalid path costs at least one while a feasible path costs
at most zero. This proves that the finite product preserves every feasible
rank transfer, including the (0,c) entry determining an original interval's
above-capacity layer value with arbitrary nonnegative gap weights.

A balanced product tree avoids exponential repeated core doubling: its final
core is at most 2r*2^ceil(log2 r)*c and its total construction work is
O(n+r^2 c log(c+1)). Ordinary witness arrays justify the conservative
O(r^2 c log(c+1)) auxiliary-space claim. This is a representation parameterized
by runs, not a general subquadratic all-interval BST algorithm. The matrix
multiplication inequality and algorithm remain credited to the published
ESA 2025 primitive; its primary source was checked again this turn.

The expected obstacle is exact. With r input keys weighted 1,...,r, the
rightmost t keys maximize every nonnegative rank reward simultaneously.
Writing G(t)=sum_{j<=t} j nu_2(j), the transfer equals

    -[(r-v)(F(v)-F(u))+G(v)-G(u)].

Every strictly feasible density is nu_2(u+1). Thus r=2s gives exactly
s floor(s/2) entries in an s-square, and c=2r-1 gives exactly
3r^2/4-3r/2+1 positive entries in the full strict feasible strip.
All these entries use feasible corners, so no choice of finite completion
removes the lower bound. The coordinates are ranks; the weight mass is
r(r+1)/2. It is not an original interval-core counterexample.

The binary-block interior also extends to a chain of arbitrary unary
functions and bounded monotone state increments. Its balanced bound is
O(r^2 N), with O(r^2 N log(N+1)) construction. However, even width-one
bands admit a dense local square: use f_1=...=f_(r-1)=u and
f_r=-(r-1)u. The optimum is -d(d+1)/2 for d=max(B-A,0).
At r=N=2s+1 every cell of the indicated s-square has density one.
This counterexample is not a ruler-block input. It identifies precisely
why the factorization alone cannot prove a uniform boundary charge; the
special carry rewards or original weight budget must enter a stronger proof.

The audit first ran with integer finite products, literal subsequences,
original mixed all-root layers, arbitrary unary chains, and both explicit
dense families. Every control passed. It was then expanded to rational
weights and varied many-block lengths and rerun against the final sources.
No empirical maximum or timing is used as a bound.

The final run exhausts 363 inputs over {0,1,3} through five keys, with 23232
finite product controls against 459456 candidate additions. Its 11385 feasible
entries also match an independent subsequence DP and 52245 literal choices.
Thirty-two rational inputs add 1048 exact controls. Seventy mixed inputs
through 32 keys have 1172 original all-root layer identities. Thirty-two
many-block inputs have 128 original support sets and 3544 density controls;
together the original recurrences use 987840 candidates and 104460 states.

One hundred generic signed-function chains have 3850 independent feasible
scores. The width-one family has 1493 entry controls against the DP and
product, plus 341 density-one cells. Six weighted-ramp products through
c=255 have 33138 formula entries and 32136 density checks. The four smaller
rows through c=63 also have 2130 independent DP entries. The larger rows
are explicitly formula/product controls. At c=255,r=128 the strict core
has 12097 entries and its side-64 square has 2048.

The next general obligation remains a proof using the ruler structure or
original integer weight units to bound interval cores. Neither new transfer
barrier changes the main aggregate bound or settles the open local hypothesis.
The complete proof is RANK_TRANSFER_BARRIER.md; manuscript Section 5.20
groups it with the representation barriers, with counts in Appendix T.

Publication validation: the final 124-page manuscript compiles cleanly with
Tectonic, without layout or reference warnings. All pages were rendered and
reviewed in contact sheets; new proof pages 92--94, Appendix T on page 122,
and the final dedication on page 124 were also inspected at reading scale.
All 333 prior labels remain; the 342 current labels are unique and all
references resolve. The dedication source is byte-identical. The final audit
manifest matches every executed source. Stable TeX and PDF copies match the
manuscript byte for byte, and the five-member source archive includes the
matching TeX, build instructions, Hebrew font, license, and font README.


## Checkpoint 45: a near-linear unimodal construction and exact certified spans

Checkpoint44 was progress: it extended finite rank transfers to arbitrary
key weights and proved two dense-transfer barriers. This turn returned to
original interval coordinates and sought a structured representation of
cores rather than listing dense rank-transfer supports.

The key new lemma is elementary and stronger than binary saturation. Every
subsequence of a unimodal weight word is componentwise dominated by a
contiguous word of the same length. With b selected positions at or before
a peak z, compress those to end at z and the rest to start at z+1. Every
coordinate moves toward the peak inside a monotone side. This holds for
arbitrary nonnegative reward templates, not only ruler rewards.

Consequently, on any unimodal key interval above capacity, the optimal
c-subsequence ruler score is the maximum of contiguous window values B_h.
The window envelope has exactly the strict nonadjacent visibility core,
with pair (a,b) mapping to original cell (a,c+b-1). Thus globally unimodal
key inputs have at most max(0,n-c-1) above-capacity entries per layer and
at most 2s-1 per above-capacity square. Key weights may be unequal real
numbers; gap weights are arbitrary nonnegative reals and cancel from the
ordinary densities. The existing isolated-unit-key family attains a ratio
tending to one in the global bound.

All window arrays are constructed jointly using

    B_h(a)=B_(h-1)(a)+B_(h-1)(a+2^(h-1))+(h-1)p_(a+2^(h-1)-1).

There are O(n) entries per layer and O(log(n+1)) layers. Visibility stacks
construct all their cores in O(n log(n+1)) work and space. Maximum segment
trees preserve that preprocessing bound and give O(log(n+1)) exact interval
queries, including an implicit contiguous optimal selected-block witness.
Emitting the c keys or perfect partial skeleton has O(c) output work.
The component does not claim to solve the below-capacity mixed region.

For arbitrary input weights, the same construction is an upper envelope
for original layer costs. A one-scan index records the latest decrease
followed by an increase and tests interval unimodality in O(1) time. Filter
the envelope's O(n) core entries by unimodality of their outer interval.
This recovers every positive original density with a certified outer span,
not merely a sufficient subset of those positive densities. It also gives
the 2s-1 local tile charge whenever the tile's full key span is unimodal.
The unhandled above-capacity cells necessarily span a weight valley.

The correction E=S-S_hat is nonnegative in value but has both density signs.
At capacity seven, binary words (0,0,0,1,0,0,0,1,0) and
(0,0,0,1,0,0,1,0,0,0) give correction corners (0,1,0,0) and (1,1,0,1),
respectively. Their densities are +1 and -1. The score tables have direct
proofs from selected ranks in (0,1,0,2,0,1,0). Concatenating the two words
gives both signs in one binary input by interval locality. This preserves
the exact remaining obligation instead of assuming a Monge residual.

The harness first exhausted the domination lemma and checked all original
above-capacity values and support sets on mixed unimodal inputs. It then
added arbitrary-input certificate/envelope controls and found the two signs.
The first negative-density witness used general integer weights; a final
expanded binary search replaced it by the ten-key binary word above. All
final audits were rerun against the final source, with exact arithmetic.

Final verification exhausts 920 unimodal ternary words through eight keys,
136802 subsequences, and 1589 arbitrary reward-template controls. Original
recurrences on 236 mixed inputs through 32 keys check 31438 interval values
and witnesses, 560 complete support sets, 24032 densities, and 99398 squares.
Those recurrences use 565705 root candidates and 65081 states. The separate
arbitrary-input audit has 1636 inputs, 101300 independent span decisions,
200892 upper-cost inequalities, 91143 exact certified intervals, 130408
envelope densities, 38221 certified original densities, and 4988 support sets.
It uses 2345440 original candidates and 435040 states. Eight literal score
controls from 253 subsequences verify both signed-correction tables.

Fourteen larger sparse constructions reach 65536 keys. Their 1168 sampled
literal windows and 2780 local square counts are separately labeled; they
do not have large all-root references. Five isolated-key cases also match
the sharp exact formula. At 65536 keys both fixtures construct 917538 ruler
windows and perform 983026 range-tree build-node operations. The isolated
peak outputs 65294 entries across all layers; the irregular rational mountain
outputs 1201. No timing or fitted exponent supports the bounds.

The new positive construction is in Section 2.16, its signed-correction
barrier in Section 5.21, and verification in Appendix U. The complete
standalone argument is UNIMODAL_ENVELOPE.md. The main full mixed-weight
bound is unchanged. Further progress must address the below-capacity mixed
region or the signed interactions across nonunimodal spans.

Publication validation: the final manuscript compiles cleanly to 128 pages.
All 342 previous labels remain among 352 unique labels, and every reference
resolves. All pages were rendered and inspected in contact sheets; the new
proof on pages 26--27, signed-correction argument on page 96, audit on page
126, and unchanged final dedication on page 128 received detailed review.
The final audit's four source hashes match the committed source candidates.
The stable PDF and TeX exports are byte-identical to the manuscript, and
the five-member source archive was rebuilt and checked member by member.


## Checkpoint 46: valley queries and quadratic original interval cores

The previous goal turn was progress: checkpoint 45 was committed, pushed,
and checked against the remote Git blobs. This turn attacks extension beyond
one peak, while preserving the full mixed-weight objective. Replacing a peak
by a valley yields both a new exact implicit representation and a sharp
obstruction to extending the linear explicit-core bound.

For any nonincreasing-then-nondecreasing key sequence, the c largest values
can be selected as a prefix and suffix, with deterministic left ties. This
single selected word componentwise dominates every c-subsequence, for every
nonnegative rank-reward vector. Compress a candidate independently toward
the ends of the two monotone wings. Consecutive feasible end-block splits
differ in only one component, and its replacement difference decreases
monotonically across the feasible split range. The common best split is
therefore found by binary search. The feasible-range restriction handles
flat wings correctly; an unrestricted comparison predicate is not assumed.

All perfect-ruler windows, in both orientations, give arbitrary ruler-prefix
queries by peeling descending powers of two. Ruler symmetry turns the
selected prefix and suffix into two such queries. This proves O(n log(n+1))
preprocessing and storage for every above-capacity layer, O(log(n+1)) exact
interval queries including arbitrary nonnegative gap weights, and a two-block
selected witness. Emitting its c keys or partial skeleton costs O(c). The
implementation does not enumerate interval pairs or construct any core.

The same class has quadratic original interval cores. For s a power of two
at least four, n=4s, m=2s, c=m-1, take decreasing even weights 2m,...,2 and
increasing odd weights 1,...,2m-1. On [0,s) x [3s,4s), the exact ordinary
density is nu_2(3s-ceil((i+j)/2)). The proof computes all four corner scores
as left and reversed-right prefixes. All common terms cancel, leaving the
difference between the two smallest retained weights, multiplied by one
ruler valuation. Each row has s/2 positive entries, so the square has exactly
s^2/2=n^2/32. These are original interval coordinates, not transfer states.
The density also equals a sum of log2(s) modular diagonal indicators.

The integer family has mass n(n+1)/2 when gaps vanish. Scaling by 1/n leaves
the same support at rational mass (n+1)/2, with O(log n)-bit numerators and
denominators. This explicitly blocks removing integrality by normalizing
weights. It does not contradict the integer-mass theorem or its open local
support target. Logarithmic queries remain available even for the dense
family, so it is not an unrestricted OBST lower bound.

Harness first: a small exhaustive domination probe preceded the optimized
query implementation. It also tested the density expression at several
sizes; the support count has a small s=2 exception, so the theorem explicitly
starts at s=4. The first complete audit tested the integer family; a second
complete run added original-recurrence checks for the normalized rational
family. The final record matches all four executed-source hashes.

Final counts: 920 exhaustive ternary valleys; 136802 subsequences; 6198
arbitrary reward vectors; 8920 independently rejected nonvalleys. Original
all-root controls on 256 mixed inputs through 64 keys check 56076 interval
values and witnesses, and 672 density-formula cells across the integer and
rational families. They use 1396993 root candidates and 113799 states.
Fourteen larger implicit constructions through 65536 keys have 896 sampled
literal top-key controls, 896 literal ruler-prefix controls, and 640 sampled
dense-formula cells. They have no large all-root references. At the largest
size the two orientations use 1835076 window updates and 1966150 stored
window entries. No timings or fitted exponents enter any theorem.

The standalone proof is VALLEY_QUERIES.md. The positive query theorem is
in Section 2.17, the dense-core barrier in Section 5.22, and the new audit
in Appendix V. The next general obligation is an implicit representation
that composes through the mixed below-capacity region; the current oracle
alone does not provide that operation or a full-tree constructor.

Publication validation: the manuscript compiles without warnings to 131
pages. All 352 prior labels remain among 363 unique labels; references
resolve. All pages were rendered and reviewed in contact sheets, with detail
inspection of the new query proof on page 28, dense proof and interpretation
on pages 97--99, audit on page 129, and final dedication on page 131. The
dedication's source remains byte-identical to the previous checkpoint.
Both new and reused-source audit manifests match the final source files.
The stable PDF and TeX exports match the manuscript byte for byte; the
five-member buildable source archive was rebuilt and verified individually.


## Checkpoint 47: direct endpoint-weight charges for valley cores

The previous goal turn was progress: checkpoint 46 published the valley
query oracle and a quadratic original-coordinate core family. This turn
began by examining the mixed below-capacity slot representation. A useful
intermediate question from the valley oracle instead led to a direct
individual-unit support charge, addressing the open local mass target on
valley spans without changing the full mixed-weight objective.

Let T_c be the sum of the c largest key weights in an interval, and let
Gamma_c be its four-corner difference with the score sign convention.
For any input, with endpoint weights x,y and the two smallest retained
inner weights z<=w, Gamma_c=max(0,min(x,y,w)-z). The decisive valley lemma
is 0<=D_Ah<=(h-1)Gamma_c. Its proof uses the universal selected word and
handles ineffective endpoints, an endpoint between z and w, both endpoints
at least w, and ties. In the last case the original density is exactly
(w-z)nu_2(r), with r the selected rank of z. Explicit prefix-score
cancellation covers the two left-minimum cases; reversal covers the others.

The top-c endpoint difference is max(0,p_i-z_i(j)), where z_i(j) is the
inner c-th-largest cutoff. Its changes telescope to at most p_i along a
row; reversal gives the column bound p_j. Integer positive auxiliary
densities are at least one. Consequently a valley layer's entire original
above-capacity core has at most P=sum p_i entries, and every rectangle
has at most min(row-endpoint mass,column-endpoint mass). This proves the
local boundary-plus-mass target on valley above-capacity spans with no
additional side term. Gap weights may be arbitrary nonnegative reals.

The dense valley family proves the mass dependence necessary up to constants.
Its square has s^2/2 entries, row mass 3s^2+s, and column mass 3s^2. Thus
the local bound is attained within a factor of six. Scaling the weights
preserves auxiliary support but makes its densities fractional, explaining
why the integer count does not extend to normalized real mass.

The new constructor enumerates auxiliary cutoff changes without scanning
interval pairs. If the current cutoff z has m retained copies, find the
first future right-wing value greater than z at k. The first actual cutoff
increase occurs at k+m-1. Binary search in the monotone wings gives each
event in logarithmic work; four existing ruler queries filter the original
core. Across all layers, the event count is at most P log(n+1). Total work
is O((n+P) log^2(n+1)), with O((n+P) log(n+1)) storage including outputs.
The real-weight output-sensitive form uses the actual auxiliary-event count.

The inclusion has a concrete obstruction outside valleys. The previously
proved nine-key word p+=(0,0,0,1,0,0,0,1,0), at capacity seven and cell
(0,8), has original score corners (2,3,0,2), hence density one, but all
four top-c sums equal two. Its auxiliary density is zero. The existing
rank proof supplies the counterexample without a new search or duplicated
weight pattern. A separate original recurrence confirms its score table.

Harness first: a preliminary exhaustive probe checked the inclusion before
implementing event enumeration. The full final audit checks 1513 small
inputs, including all 1461 ternary valleys through nine keys. Literal sorted
sums control 73082 auxiliary densities, 32810 two-threshold formulas, and
4267 support sets. The same number of original ruler support sets agree
with the independently audited query representation; 198321 eligible small
squares satisfy the mass bound. Original all-root layers on 972 mixed inputs
check 49278 densities and 2644 complete support sets, using 1006805 root
candidates and 163435 states. The nonvalley counterexample has a separate
495 candidates and 135 states.

Twelve larger complete constructions through 16384 keys have 3264 sampled
literal density controls. At that size binary end blocks output 4084 original
entries from 8178 auxiliary events, and bounded valleys output 16477 from
32995. Five complete dense-family constructions check 5456 formula cells
through side 64. Large controls are explicitly distinct from all-root
references. Final source hashes cover the constructor, audit, and three
reused modules. No timings or fitted asymptotics are used.

The standalone proof is VALLEY_CORE_MASS.md. The new positive section is
2.18, the existing negative Section 5.21 now includes the failed support
extension, and the audit is Appendix W. The general local target and mixed
below-capacity composition remain open. The next proof must handle joint
rank changes across multiple peaks or the gap interactions below capacity.

Publication validation: the final manuscript compiles cleanly to 134 pages.
All 363 prior labels are preserved, the 374 current labels are unique, and
all references resolve. All pages were rendered and visually reviewed, with
full-size checks of the new proof on pages 29--30, counterexample on page 99,
audit on page 132, and final dedication on page 134. The dedication source
is byte-identical to the previous checkpoint. All 13 source-hash entries
across the new valley-core and prior valley/unimodal audits match. The stable
TeX and PDF outputs are byte-identical to the manuscript, and the five-file
source archive was refreshed and checked member by member.

## Checkpoint 48: a cyclic quotient for full mixed construction

The previous checkpoint was progress: the valley support theorem, sparse
constructor, exact audit, and manuscript were published at bd4f3cc. This
turn first revalidated the clean checkout and the unresolved arbitrary-input
local support hypothesis. No subagents were used.

The directed next experiment padded short unequal valleys with long zero
regions. Across the tested sizes through 2048 their above-capacity cores
stayed much smaller than an n^(3/2) scale; this is finite direction only.
Unrestricted fixed-mass mutations found a 128-key, mass-128 input with 270
above-capacity entries at h=5. The independent all-root recurrence confirms
all 270, using 1788800 candidates and 41280 states. This refutes coefficient
one in K_above<=n+P and does not refute an arbitrary constant in O(n+P).
The exact input is retained in periodic_obst_audit.json.

Periodic probes suggested a better representation than explicit core output.
For the repeated binary word 001, the observed positive diagonals obey a
simple two-height recursion through h=10: retain the h-2 diagonals and add
excess lengths 2^(h-1)-2 and 2^(h-1). Their displayed nonzero phase densities
are two and one. This remains an unproved pattern. The above-capacity
Omega(n log n) conjecture and general local support bound remain open;
no fitted growth statement is promoted to a theorem.

The proved result from this investigation is a full, unrestricted-height
mixed OBST construction in O(nb) arithmetic work and space, where b is the
common period of key and gap weights. It applies to arbitrary nonnegative
reals, permits zeros, and reconstructs every node. Translation identifies
intervals by starting phase a and length l. Knuth's leftmost roots restrict
phase a to [rho_a(l-1),1+rho_(a+1)(l-1)]. Summing these inclusive lengths
around all b phases telescopes to exactly 2b. Including length one gives
exactly b(2n-1) root candidates. Synthetic intervals beyond the input end
are essential to this cancellation and are computed explicitly.

The detector computes the shortest finite period of signatures
(p_i,q_i,q_(i+1)). A proper signature period enforces final-gap consistency.
If only period n remains, q_n=q_0 decides between common period n and n+1;
the latter uses one unobserved padding key. The ordinary prefix-function
algorithm gives linear detection. An iterative reconstruction handles even
an all-zero leftmost-optimal chain without a recursion limit. The method
is a direct cyclic use of Knuth, not a claim to a new monotone-root theorem.
Targeted literature searches combining optimal/optimum binary search trees
with periodic weights did not locate a directly applicable primary statement;
no claim of priority or exhaustive absence is made.

Harness first: independent all-root tables and ordered-shape enumeration
were in the audit before the first remote run. The final audit checks 1042
small inputs, including all binary mixed inputs through four keys and every
binary key/gap period through three, plus rational, geometric, gap-only,
key-only, final-gap-defect, and nonmultiple lengths. It checks 62376 original
interval values, 54672 leftmost roots, and 38756 synthetic phase states.
References use 1993994 all-root candidates and 154391 states. Separate
shape enumeration checks 7882 shapes. Twenty ordinary Knuth controls
through 512 keys examine 1744227 candidates. Sixteen larger constructions
through 262144 keys traverse every key and gap independently. At that size
period five has exactly 2621435 candidates; period three has 1572861.
Large rows have no independent quadratic optimality reference. All four
executed-source hashes match; no timings are used.

The proof is PERIODIC_OBST.md, the implementation periodic_obst.py, and the
audit periodic_obst_audit.py. The manuscript adds the theorem after the
valley charge and puts verification counts in Appendix X. The original
Monge result still leads, and the general nonperiodic objective remains
active. The next avenues are proving the periodic density pattern and
finding a useful exact compression beyond a single global period, while
continuing the arbitrary-input local support problem.

Publication validation: the final manuscript compiles cleanly to 136 pages.
All 374 previous labels are preserved, all 381 current labels are unique,
and all references resolve. All pages were rendered and visually reviewed;
full-page checks covered the new theorem/proof on pages 31--32, Appendix X
on page 134, and dedication on page 136. The dedication source is byte-identical
to the previous checkpoint. Seventeen source-hash entries across the new
periodic and prior valley-core, valley-query, and unimodal audits match.
Stable TeX/PDF outputs are byte-identical to the manuscript. The five-member
TeX/font archive was rebuilt and verified member by member. Exploratory
probe sources and raw records are preserved outside the repository in the
local revision48-probes work directory; the independently verified 128-key
counterexample is included in the committed audit record.

## Checkpoint 49: linear boundary extension around an exact middle

Checkpoint 48 was progress, published at d081795: a full periodic mixed
solver and an independently confirmed fixed-mass support counterexample.
This turn extends the exact full-tree representation to arbitrary boundary
fringes. No subagents were used. The arbitrary-input objective remains active.

The initial boundary-envelope idea gave O(n log n) work per new column by
binary searching a one-crossing condition. Checking the primary literature
identified Wilber's 1988 linear concave LWS algorithm, which removes that
logarithm. It is credited as prior work and implemented directly from its
Figure 1. The new reduction is w(s,t)=C(J-t,J-s-1)+W(J-t,J). Every old cost
has endpoint below J; the original OBST Monge inequality gives exactly the
required concave quadrangle after mass terms cancel. Reflection extends
left rows as well. No unfinished oracle values are queried.

A periodic middle of m keys and period b with d=n-m arbitrary fringe keys
therefore supports full exact construction in O(mb+nd) work and space. The
number of added nonempty interval states is exactly dm+d(d+1)/2. Inclusive
central gaps are required to repeat; the fringe magnitudes are unrestricted
nonnegative reals. All original interval costs and optimal roots have
constant-time access. Complete iterative reconstruction is included.
Any central constant-time exact oracle of cost T similarly extends in
O(T+nd+n). Sparse arbitrary interior defects are not solved by this lemma.

A signature scan finds a longest period-b middle in O(n); the signature
includes both adjacent gaps. The automatic planner scans b through the
logarithmic threshold and compares mb+n(n-m) with the whole-period proxy.
It may skip the scan when the whole period is already within the threshold.
Thus constant supplied period and fringe count give linear construction;
automatic recognition adds O(n log(n+1)). No empirical exponent is used.

The independent audit was written before execution. Its first run stopped
at a syntax typo in the harness; that was corrected before any results were
accepted. The complete remote audit then passed: 768 generic signed LWS
instances with 549120 literal candidates, 980 small full mixed inputs,
57416 interval costs, 44230 optimal root witnesses, 6944 standalone boundary
root controls, and 3324 literal middle decisions. The all-root references
use 351256 candidates and 49492 states; enumeration checks 7880 shapes.
Sixteen ordinary Knuth controls through 512 keys use 1847784 candidates.
Twelve larger full constructions reach 65537 keys and traverse every key
and gap, with no separate quadratic optimality reference at that size.
The seven-fringe period-five row has exactly 458738 new states, 655295
central candidates, and 8264895 valid LWS arc queries. The six source hashes
match the executed files. Timing is neither reported nor used as evidence.

The proof is FRINGE_OBST.md. The manuscript places the boundary lemma and
full composition after the periodic theorem and puts all verification
counts in Appendix Y. The original Monge result still leads. The unresolved
local core-support theorem and the remaining square-root-logarithmic gap
are unchanged; a restricted-family result does not complete the full goal.

Publication validation: the final manuscript compiles without warnings to
139 pages. All 381 prior labels remain, all 390 current labels are unique,
and all references and citations resolve. All pages were rendered and
visually reviewed, with detailed checks of the new proof on pages 32--33,
Appendix Y on page 137, and dedication on page 139. The dedication source
is byte-identical to checkpoint 48. Twenty-three source-hash entries across
the new and four preceding audits match. Stable TeX/PDF outputs match the
manuscript byte for byte; the five-member TeX/font archive was rebuilt and
verified member by member. An initial compile invocation used the repository
root's unrelated main.tex and failed on its missing figure; its generated
log was removed and the correct obst/manuscript source was then compiled.

## Checkpoint 50: a finite affine quotient for full mixed weights

Checkpoint 49 was progress: the exact linear boundary extension and its
periodic-middle composition were published at 356a21d. This turn revalidated
the clean checkout and the full mixed-weight objective. No subagents were
used. An arbitrary join between different interior patterns remains open;
the endpoint-response barriers do not supply such a join. The productive
extension here is a broader exact translation symmetry.

The external/internal path-length identity gives a shape-independent rule:
p->lambda p+alpha, q->lambda q-alpha changes the cost of every ell-key tree
to lambda times its old cost minus alpha ell. With lambda>0, every optimal
shape and leftmost root is preserved. Thus inputs satisfying this law under
translation by b support a phase/length quotient even when neither sequence
is literally periodic. Pure geometric scaling and opposing arithmetic drifts
are included. No height restriction or certificate is needed.

The finite domain requires care: an affine continuation can become negative.
The construction computes all b phases only through m=n-b+1, where every
interval is inside the original input. The inclusive Knuth ranges telescope
to 2b candidates at every length after the first. The remaining b-1 lengths
use ordinary actual-input diagonals. Their total candidate bound is
(b-1)n+(b-1)(b-2)/2 and their state count is b(b-1)/2. The complete quotient
stores exactly nb-b(b-1)/2 nonempty states. Full construction, all interval
queries, and iterative reconstruction take O(nb) arithmetic work and space.

An O(n) feasibility test for b uses proportionality of the adjacent sums
p_i+q_i and p_i+q_(i+1), then checks the original equations. A first positive
component determines lambda; the all-zero constrained case and b=n are
handled explicitly. Scanning periods until the first success b_* costs
O(nb_*), so recognition has no extra asymptotic overhead. An initial capped
planner was replaced by this complete scan after observing that the scan's
work is already within the construction bound. The final harness independently
solves the two-variable original equations to check recognition completeness.

Harness first: literal shape transformations were placed before solver
controls. The completed audit passes 6250 shape identities, 1063 small mixed
inputs, 84584 interval values, 74877 leftmost roots, and 28534 phase states.
It checks 8644 independent period decisions, 860 minimum periods, and 21
negative-continuation cases. Reference tables use 640661 candidates and
74877 states; separate enumeration checks 7882 shapes. Sixteen ordinary
Knuth controls through 512 keys use 1393110 candidates. Nine complete
arithmetic-drift constructions reach 65537 keys and two geometric cases
reach 4095, with every output tree independently traversed. The largest
period-five case has 655325 phase and 18 terminal candidates. Geometric
rows retain exact growing integers and claim arithmetic, not bit, bounds.
All four final executed-source hashes match. No timings are reported.

AFFINE_PERIOD_OBST.md gives the proof. The manuscript adds the theorem
after the boundary extension and puts verification in Appendix Z. A simple
strictly positive family p_i=i+1, q_j=n+1-j has mass (n+1)^2 and exactly
2n-1 root candidates, yielding linear work on O(log n)-bit words. The
general central-oracle lemma also extends an affine middle through arbitrary
fringes. The implemented audit covers the global affine constructor; the
fringe corollary is a composition of the already proved lemmas.

Targeted literature searches on static OBST, geometric probabilities,
periodic weights, and arithmetic progressions did not locate a directly
applicable primary statement for this finite affine mixed quotient. This
is not an exhaustive absence or priority claim. The proof explicitly uses
the classical path-length identity and Knuth monotonicity. The arbitrary
nonperiodic objective, interior changes, and local core-size gap remain open.

Publication validation: the final manuscript compiles without warnings to
142 pages. All 390 prior labels remain, all 399 current labels are unique,
and every reference and citation resolves. All pages were rendered and
visually reviewed; detailed checks covered the theorem on pages 34--35,
Appendix Z on page 140, and dedication on page 142. The dedication source
is byte-identical to checkpoint 49. Twenty-seven source-hash entries across
the new and five preceding audits match. Stable TeX/PDF outputs match the
manuscript byte for byte, and the five-member TeX/font archive was rebuilt
and verified member by member. The appendix insertion initially used a
repository-relative path from the manuscript directory and made no edit;
it was reapplied from the repository root before the final clean build.


## Checkpoint 51: legal endpoint information loss and exact signed recovery

The boundary representation question now has a proved distinction. A
strengthened four-key collision has identical responses under every legal
nonnegative reassignment of its two endpoint gaps, not merely under added
nonnegative penalties. Transferring the old unit outer gaps to their adjacent
keys preserves every shape intercept. The resulting positive inputs have
keys (2,1,2,4), unit endpoint gaps, interior gaps (4,2,1) or (4,1,2), and
mass 18. Their complete legal envelopes coincide. A common eight-key context
has optimal costs 101 and 100. Complete intercept domination and independent
shape enumeration certify both statements.

The complete endpoint-depth profile behaves differently. Its n extreme
states, where the endpoint depths sum to n+1, are unique two-sided chains.
Their costs C_r form a convex sequence with second differences
2p_r+q_r+q_(r+1). The first difference and total mass recover q_1; successive
second differences recover the interior gaps; mass recovers the last gap.
Given p, W, and q_0, these n coefficients determine the entire gap vector in
linear arithmetic work, for arbitrary nonnegative real weights. A collision
preserving this full profile and these metadata is therefore impossible.
Initial small profile-rank probes suggested this direction but are not used
as proof or published as evidence of unknown-key injectivity.

A bounded signed endpoint line exposes exactly these chains: a sufficiently
large common negative endpoint price rewards maximal boundary-depth sum.
The proof bounds the entire non-chain class explicitly. For integer input,
a rational perturbation encodes the active chain index in a scalar value's
residue modulo n+1. Recursive chord queries recover every coefficient with
at most n value-only calls, O(n) further arithmetic work and space, and
rational denominators at most n^2-1. The collinear stopping rule compares
scores: its decoded minimizer can lie outside the current interval. This
avoids an incorrect membership-based test. No witnesses or infinitesimal
limits are required. The oracle is specified, not supplied by a faster
general signed-OBST algorithm. The chain-only oracle is implemented separately.

The final remote exact audit passes 800 small integer inputs, 3968 independent
signed all-root queries, 107608 literal signed shape evaluations, 19184
boundary-union controls, and 2792 unique-chain checks. All-root references
use 1926832 candidates, including the signed collision probes. Whole-quadrant
equality uses 18 domination checks; the two contextual inputs use 2860 shape
evaluations. Twelve larger rows through 65536 keys recover every gap using
the proved chain-line oracle, with no claim of a large independent signed
reference. Random and uniform cases use n queries; zero cases use three.
All five executed-source hashes match. No timings are reported.

SIGNED_BOUNDARY_RECOVERY.md and the manuscript contain the full proofs.
Verification is added to the existing endpoint-response appendix, keeping
the theorem's information claim separate from oracle construction costs.
The arbitrary-weight OBST objective and the local core-support bound remain
open; this checkpoint closes a precise interface-information question.

Publication validation: the manuscript compiles without warnings to 144
pages. All 399 prior labels remain; all 408 current labels are unique and
all references and citations resolve. All pages were rendered and visually
reviewed, with detailed inspection of the new proofs on pages 80--82,
verification on page 117, and dedication on page 144. The dedication source
is byte-identical to checkpoint 50. Thirty-two executed-source hash entries
across seven audits match. Stable TeX/PDF deliverables match the manuscript;
the five-member source/font archive was rebuilt and checked byte for byte.


## Checkpoint 52: below-capacity plateau cores and excess-directed search

Checkpoint 51 was progress: the signed-recovery theorem, legal-domain
collision, audited sources, TeX and PDF were published at 26d8c55. This turn
returned to the open local support bound rather than treating information
recovery as a solution of the general construction problem.

The new diagnostic optimizes K(T)-W(J_T) on fixed accepted tiles instead of
the previous ratio objective. It uses integer additions, deletions, transfers,
and swaps, with sparse, alternating, flat, and odd-ramp starts; both sides
of capacity and key-only, gap-only, and mixed modes are included. It evaluates
34692 inputs through 640 keys, using 5798865516 states, 11439157710 optimized
root candidates, and 22971840 tile densities. All 27 retained small controls
agree with independent original all-root layers using 9000132 candidates
and 330330 states. The maximum normalized excess is 39/64 (K=63,W=24,s=64).
This neither proves the local hypothesis nor falsifies it. Its objective and
full winners are preserved in tile_excess_probe.json. Compiler-only cleanup
removed an unused variable and vector and clarified loop indentation; the
final executed source was rerun to retain a matching source manifest.

A distinct proof closes the complementary below-capacity region for one
constant positive key block with zero gaps. On intervals retaining the whole
block, the weighted slot problem is a top-m sum of ruler valuations. Its
threshold-count identity gives exact support when ruler endpoints u,v are
multiples of 2^r separated by m*2^r. Intervals cutting one block endpoint
reduce to the change of a kth prefix order statistic; their events are
b=k*2^r. Reflection covers the other endpoint. Intervals with both changed
keys inside the block give the usual minimum-IPL diagonals. These four cases
are disjoint and exhaust the below-capacity ordinary core, including empty
shortest intervals and heights whose capacity exceeds n.

Every positive density equals the common weight alpha. Let
U_h(m)=sum_(r=1)^(h-1) max(0,m-2^r+1). Complete construction takes
O(n+U_h(m)) arithmetic work and space, with at most 2(n-m)+U_h(m) entries.
No capacity-sized array is built when c>n. Removing the unique maximum
ruler valuation from any s consecutive indices leaves valuation sum at most
s-1. Charging all other rows or columns to that sum, and the exceptional
one to its s available neighbors, proves a 2s-1 bound for each of the first
three cases. Dyadic geometry bounds the uniform diagonals by 2s-1. Hence
K(T)<=8s. With the earlier above-capacity plateau theorem, the local charge
is proved on both sides for this key-only family independently of alpha,
even for real alpha. The general mixed hypothesis remains open.

The audit begins with literal arbitrary-template top-sum controls, then
compares complete sparse outputs against the original all-root recurrence.
It checks 1025 block inputs, every block through 17 keys, selected instances
through 64 keys, rational common weights, and heights through twice the
binary length. The 8812 complete core comparisons cover 1070212 densities,
88033 interval values, and 222434 local tiles. There are 336 literal top-sum
controls; reference recurrences use 18032986 candidates and 1556996 states.
Sixteen larger sparse constructions through 65536 keys check coordinate
identities on every emitted entry and every layer through twice the binary
length. Those rows have no independent large all-root reference. No timing
or empirical scaling exponent enters the theorem.

PLATEAU_BELOW_CORE.md contains the complete proof. The manuscript places it
next to the earlier above-capacity plateau construction, with both new audits
in the existing plateau appendix. The odd-ramp lower bound, main mixed Monge
construction, and unrestricted research objective are unchanged.

Publication validation: the final manuscript compiles without warnings to
145 pages. All 408 previous labels remain; all 414 labels are unique, and
references and citations resolve. Every page was rendered and visually
reviewed, with detailed checks of the theorem on pages 23--25, both audits
on page 135, and dedication on page 145. The dedication source is unchanged
from checkpoint 51. Forty-one executed-source hash entries across ten audits
match, including both new final runs. The TeX/PDF deliverables and five-member
font/source archive were refreshed and verified byte for byte. The final
proof wording explicitly includes empty endpoint fringes in its non-strict
candidate bounds.

## Checkpoint 53: finite slot windows and complete prescribed-height run trees

Checkpoint 52 was progress, published at 8a341d3: it proved the complete
below-capacity plateau core and a local side charge, and preserved the
excess-directed falsification search. This turn tested whether the same
threshold identity could compose unequal runs without losing exactness.

The new slot-window factor retains every key of a run of weight w and
length m. With slot boundaries a,b, it is
K max(m-b+a,0)-w sum_t min(m,floor(b/2^t)-floor(a/2^t)), where
K=1+(h-1)P, P is total key weight, and c=2^h-1. This formula defines an
entire finite square, including reversed windows. Its complete density
list has K on b-a=m and w at (kd-1,(k+m)d-1), d=2^t>=2. These supports
are disjoint and have fewer than 2c entries. The top boundary has a linear
threshold-update sweep, so condensed factors require O(c), not a dense
conversion.

Every invalid product path has penalty at least K, while even a reversed
path's reward is bounded below by -(h-1)P. It therefore costs at least
one, strictly more than every feasible path. Feasible paths partition the
outer slot window between the runs and represent every increasing all-key
selection. Balanced products using the published core-sparse primitive
have O(r^2 c) aggregate core size and O(n+r^2 c log(c+1)) work. Retained
witnesses recover the leaf windows; bucket selection visits their disjoint
slots twice in total. The established threaded slot repair returns a full
optimal tree at the prescribed height, within the same construction bound.

A tree identity extends this to arbitrary nonnegative keys, equal internal
gaps b, and arbitrary endpoint gaps. Set w_0=p_0+q_0,
w_(n-1)=p_(n-1)+q_n, and w_i=p_i+b internally. The mixed cost of every
tree is exactly sum_i w_i ell_i+bn, by E=sum_i ell_i+n and the endpoint
gap-depth identities. Thus no negative transformed weights are needed.
The number of runs increases by at most two. The capacity c remains
explicit; minimum feasible height gives c=O(n), but no unrestricted
optimal-height certificate follows. This is an additional exact family,
not a replacement for the full arbitrary mixed-weight objective.

The attempted direct inclusion of a gap transition has an exact obstruction.
B_q(u,v)=-q min(nu_2(u),nu_2(v)) has density
(-1)^(u+v) q min(nu_2(e(u)),nu_2(e(v))), e(u)=u+(u mod 2).
For c=4s-1 and power-of-two s>=2, rows 1..s and columns 2s+1..3s form a
fully feasible square with s^2 nonzero densities, half of each sign, even
for q=1. The four-corner proof has only one nonzero entry per cell. No
finite Monge or anti-Monge completion or added unary potentials can remove
these signs. This only obstructs the stated consecutive-slot coordinates
and explicit signed-density lists; it does not give an original interval
core lower bound. The equal-gap identity demonstrates an alternative
representation on its own family. The general local tile hypothesis and
remaining square-root-logarithm gap are unchanged.

Harness-first validation: all 23232 entries of finite products on 363
ternary inputs agree with an independent dense product, using 459456
candidate additions. All 2946 feasible entries also agree with a separate
weighted-subsequence DP and 20340 literal subsets. Twenty-five rational
single-run cases add 6820 finite entry checks, including overlong runs.
An initial constructor run exposed that the old shared weight validator
accepts integers only; the new real-weight interface now validates lengths
and nonnegativity directly. The full final audit was then run successfully.
No theorem was changed in response to that interface correction.

One hundred mixed inputs through 24 keys give 200 original all-root height
optimum controls, with complete tree order, height, and original-cost checks.
The references use 235160 candidates and 34270 states. There are 220
insufficient-capacity checks and one unequal-internal-gap rejection. Nine
signed-transition squares through side 512 check 349524 densities.
Eight larger full constructions through 8192 keys use uniform or three-run
keys and nonzero gaps. Uniform rows have closed minimum-IPL optimum checks;
large three-run rows verify output trees but have no independent dense
optimum oracle. The largest three-run input has 61431 leaf core entries,
two run products, final core size 20147, and two total scans of 16383 leaf
slots. Exact operation counters and seven final source hashes are saved.

SLOT_RUN_CONSTRUCTION.md contains the complete argument. The manuscript
places the positive results in Section 2.16, the signed obstruction in
Section 5.20, and the counts in existing Appendix T. It compiles without
warnings to 148 pages. All 414 prior labels survive among 424 unique
labels, and every reference and citation resolves. The dedication source
is byte-identical to checkpoint 52. All pages were rendered and visually
reviewed, with detailed formula checks on pages 25--27 and 107, the audit
on page 140, and dedication on page 148. Fifty-three executed-source hash
entries across eleven audit records match the local sources. The final
TeX/PDF deliverables and five-member source/font archive are refreshed and
verified byte for byte before publication.

## Checkpoint 54: mixed prefix vectors remove quadratic run dependence

Checkpoint 53 was progress, published at 0de1687: it provided a finite
slot-window product and full prescribed-height equal-internal-gap constructor,
plus an exact signed gap-transition obstruction. Initial inspection this turn
confirmed that the common-gap shift already follows from the established
shape-independent cost identity. More consequentially, complete construction
needs only prefix vectors, not the full product matrix. The implementation
and proof now use that smaller object while retaining arbitrary mixed weights.

Normalize with b=min of the internal gaps, endpoint keys w_0=p_0+q_0 and
w_(n-1)=p_(n-1)+q_n, interior keys w_i=p_i+b, residual internal gaps
g_i=q_i-b and zero endpoint gaps. Every tree's original cost is its
transformed cost plus bn. All weights remain nonnegative, even for endpoint
gaps below b. Let r count transformed key runs and e count positive residual
gaps. Every original nonnegative mixed input is accepted.

The prefix vector records the minimum negative slot reward ending at each
slot. An equal-key run with m>=2 forces its final key to the destination
slot and chooses its other m-1 slots from the intervening open window. The
finite matrix is the prior (m-1)-window factor shifted one column, plus the
last-slot potential. Transposition and addition of the arbitrary prefix
vector preserve Monge. With K=1+(h-1)(sum w+sum g), every invalid candidate
costs at least one and every feasible candidate costs at most zero. Each
row has a feasible candidate; the SMAWK search therefore returns the exact
prefix value and predecessor using O(c) queries of cost O(h) each.

An arbitrary residual gap followed by one key is processed by a sweep.
Exact-valuation minima and suffix minima give the best predecessor among
slots a<z for the reward g min(nu_2(a),nu_2(z)). Insertion and querying
cost 1+nu_2(a) and 1+nu_2(z), respectively. Their sums over the ruler are
O(c), giving a linear pass including all predecessors. Thus the signed
checkerboard from checkpoint 53 obstructs that matrix's density list but
does not obstruct linear vector application. The valuation-group mechanism
is related to the previous capacity-deficit solver and is credited as such
through the existing slot representation; SMAWK itself is prior work.

Isolate the first key after each positive residual gap and otherwise batch
maximal constant-key zero-gap segments. There are at most r+2e stages.
For R_2 long-run and S_1 singleton stages, full work is
O(n+c(1+h R_2+S_1)) and storage O(n+c(1+R_2+S_1)). This gives
O(n+(r+e)c log(c+1)) work and O(n+(r+e)c) words, including every
backpointer, bucket traceback over disjoint windows, and threaded full-tree
repair. When e=0 this improves complete construction from quadratic to
linear run dependence. The all-entry product theorem is preserved because
it provides a different object. If all stages are singletons the implemented
bound is O(nc), without a hidden logarithm. A prescribed height remains a
constraint and c=2^h-1 remains explicit; the main unrestricted mixed bound
and original local support hypothesis are not replaced or declared solved.

Harness-first checks exhaust 680 mixed binary inputs through four keys.
They verify 7880 literal tree normalization identities, 12496 prefix values
and attaining predecessors using 53824 literal selected-slot sequences,
and 1184 insufficient-capacity decisions. Forty-eight forced-end finite
factors, including rational and infeasible cases, give 15600 comparisons
against the earlier condensed factor and 14256 Monge density checks.
Another 84 mixed inputs through 32 keys include geometric and rational
weights, arbitrary gaps, and long key runs with isolated gap changes.
There are 1528 combined original all-root height-optimum controls with
complete tree order, height, and original-cost verification. The independent
references use 828560 candidates and 107736 states.

Twelve larger full constructions through 8192 keys include uniform keys,
three runs, and unequal internal and endpoint gaps. Only uniform rows have
a separate closed minimum-IPL optimum; other large rows independently check
the returned tree but have no dense optimum oracle. At 8192 keys and h=14,
three exceptional gaps and modified endpoints give five transformed runs,
six long-run and five singleton passes, 752788 finite run-entry queries,
61437 singleton states, and 180224 stored predecessor slots. The final
successful run records eleven source hashes and exact operation counts.

The primary SMAWK source was checked through IBM Research and the authors'
Technion record: Aggarwal, Klawe, Moran, Shor and Wilber, Algorithmica 2,
195--208 (1987), DOI 10.1007/BF01840359. Its finite-real totally-monotone
matrix-search interface applies; each new matrix is explicitly finite
Monge, and the O(c) query bound includes its rectangular dimensions. The
new paper citation credits the primitive rather than claiming its invention.

SLOT_VECTOR_CONSTRUCTION.md supplies the full proof. The manuscript's new
Section 2.17 states the mixed vector theorem; verification remains in
Appendix T. Compilation is clean at 151 pages. All 424 previous labels are
preserved among 430 unique labels, and references and citations resolve.
The dedication source is byte-identical to checkpoint 53. Sixty-four
executed-source hash entries across twelve audit records match local sources.
Every page was rendered and visually reviewed, with detailed checks of the
new proof on pages 27--28, the audit on pages 142--143, and dedication on
page 151. The final PDF, TeX and five-member source/font archive are refreshed
and byte-verified before publication. No elapsed-time result is used.

## Checkpoint 55: sufficient unrestricted height by exceptional-outcome charges

The previous turn was progress: checkpoint 54 at 7e67c22 published the
arbitrary mixed prefix-vector constructor and its independent audit. This
turn examined its unresolved sufficient-height dependence. The existing
minimum-tall-IPL plus residual-Huffman exclusion certificate was inspected
first. The resulting development is instead an a priori height bound, so
the new full constructor has no posterior failure of that certificate.

Let mu be the least positive singleton mass p_i+q_i+q_(i+1), z the longest
consecutive zero-singleton run, and ell=ceil(log2(z+1)). Any positive internal
interval contains a positive singleton, so its mass is at least mu. Mark
any k outcomes and let V be the total unmarked mass. With t(V) the first
j>=0 such that F_(j+1)mu>V, every positive internal subtree of every optimum
has root depth below t(W) when k=0, and below t(V)+k+1 otherwise. Balancing
maximal zero-mass subtrees gives a sufficient full height P+ell, capped by n.

For the proof, ascend from a positive subtree, writing A_j for accumulated
mass and B_i=A_i-A_(i-1) for the new ancestor key and off-path sibling.
The detailed mixed rotation lemma gives B_i>=A_(i-2). Let j be the first
index with A_j>V; the Fibonacci lower bound gives j<=t(V). The subtree
A_j contains a marked outcome, and every disjoint B_i for i>=j+2 contains
another. Thus d-j<=k. The increment B_(j+1) is explicitly uncharged, since
its lower bound only involves A_(j-1). No dominance or placement assumption
on the marked outcomes is used. This is a consequence of the already
proved sufficient mixed rotation lemma, not a transfer of a sharper
literature constant. The Fibonacci method remains credited to prior work.

For fixed k the largest weights minimize V. Sorting and a monotone scan
select the best stated height in O(n log n) work and O(n) space. The
Fibonacci mass table stops at the first entry above W or at n, and its
largest value is at most 2W. No irrelevant n-bit Fibonacci tail is built.
The same global height works for every contiguous interval: marked count,
unmarked mass and zero-run size can only decrease, while positive singleton
mass can only increase. It can therefore also replace the sufficient
budget in the original terminal-penalty iteration on a fixed original or
normalized instance, with its penalty recomputed.

Apply the exact common-gap normalization and construct at this sufficient
height using the prefix vectors. For c=2^h-1 and r transformed key runs,
e positive residual gaps, complete unrestricted work is
O(n log(n+1)+(r+e)c log(c+1)), with O(n+(r+e)c) words. Before allocating
slots, compare c(1+h R_2+S_1) with n^2 and select Knuth when smaller.
Both paths are globally exact. The new fallback reconstructs iteratively,
including chains longer than Python's default recursion limit.

For normalized keys at least a>0, a bounded-ratio background of r_0 constant
runs, s exceptional keys, and e positive residual gaps, mark the s+e
exceptional outcomes. The unmarked mass is at most Cna and mu>=a. Hence
c=O(2^(s+e)n^alpha), alpha=log_phi 2 approximately 1.44042. For fixed
r_0,s,e this proves O(n^alpha log n) full unrestricted construction,
independently of the exceptional magnitudes. Existing dominant-core
methods can be faster on their accepted families. The theorem does not
claim a practical improvement at the finite forced-kernel audit sizes,
nor a general arbitrary-weight subquadratic bound. The original local
interval-core support question is unchanged.

The exhaustive audit covers 22,140 mixed inputs over {0,1,9} through four
keys. With 72 extra inputs through eight keys, it examines 323,604 shapes
and 30,955 optimal shapes, 152,072 sorted cuts and 790,245 positive-node
assertions. Another 287,760 arbitrary marked sets through three keys
test the stronger set-independent statement. It independently obtains
mu and z from every literal interval. There are 6454 complete small
constructor controls and three empty cases. Twelve forced full vector
constructions through 384 keys all match independent Knuth optima; a
1024-key geometric chain matches the endpoint-dominance closed form and
checks iterative fallback reconstruction. The initial harness used an
integer bit-count method unavailable on the host's Python version; it was
replaced by a portable population count before the successful runs.

At 384 keys with one 2^192 key and one 2^128 gap, the sufficient height
falls from 278 to 18. The forced vector kernel uses 12,489,698 finite
run-entry queries, 524,018 singleton states and 1,835,008 predecessor
slots. Its proxy exceeds Knuth's, as do all twelve larger forced rows;
they are correctness controls, not performance wins. Twelve larger
height-only plans through 65,536 keys keep the same selected height as
exceptional exponents rise from 64/80 to 4096/4112. No unexecuted large
construction is claimed. The final constructor audit records seven
executed-source hashes and separate operation categories.

The independent all-interval audit checks 145,424 interval heights across
1552 original or globally normalized inputs, using 2,551,952 all-root
candidates and minimizing height among tied optimal costs. It includes
rational and large exceptional weights and records three source hashes.
TRIMMED_HEIGHT.md supplies the proof; the manuscript adds Section 2.18,
Lemma 31, Theorem 32 and Corollary 33, with the verification in Appendix T.

The final manuscript compiles cleanly at 153 pages. All 430 previous labels
are retained among 436 unique labels; references and citations resolve.
The dedication source is byte-identical to checkpoint 54. Seventy-four
executed-source hash entries across fourteen audit records match local
sources. Every page was rendered and reviewed, with detailed proof checks
on pages 28--30, the new audit on page 145 and dedication on page 153.
The PDF, TeX and five-member source/font archive are refreshed and verified
before publication. No elapsed-time result is used.

## Checkpoint 56: prefix records without perfect-tree expansion

The preceding turn was progress: it supplied the unrestricted height theorem
and independent full-tree/interval audits. This turn attacks the remaining
explicit 2^h factor in the run-vector route. The harness was written before
the compressed kernel; no delegation or subagents were used.

For a fixed ending-slot valuation, prefix cost can only decrease as the slot
moves right: move the last chosen slot without changing either adjacent
reward. An earlier equal-cost state of the same valuation dominates every
later equal-cost state for both singleton gap transitions and zero-gap run
transitions. Retain only the first feasible state and strict decreases.
For integer normalized mass M, each value lies in [-(h-1)M,0], giving at most
h[1+(h-1)M] records per stage. This is a proved score-range bound.

Singleton transitions scan record eligibility events for each destination
valuation. Long runs retain the complete finite Monge factor, restricted to
record columns. Adaptive bisection of each destination valuation progression
certifies equal intervals from their endpoints; all required midpoints at a
level share one SMAWK call. At most h levels, each with at most a constant
multiple of the new record count, give O(h^2(B_old+B_new)) work. Only active
endpoints and discovered records are stored. The predecessor saved at the
start of a constant interval remains attaining throughout that interval.

Traceback selects highest valuations from two arithmetic progressions in
O(m+h) per recovered run. Repair retains only the union of ancestor paths
of selected slots, at most nh vertices. Standard successor deletions never
increase surviving key depths; the mixed gap-depth identity then recovers
the exact original cost. Deterministic ordered organization gives O(nh^2)
work and O(nh) words, with iterative output. The prototype's dictionaries
are implementation choices, not a hash-table assumption in the theorem.

With stage counts B_j and B_0=1, complete work is
O(h^2(n+sum B_j)), space O(nh+sum B_j). For integer mass M this becomes
O(nh^2+s(M+1)h^4) work and O(nh+s(M+1)h^2) words. For original W=O(n),
a sufficient unrestricted height is O(log n), even with zero runs. Fixed
normalized run and residual-gap counts therefore yield O(n log^4 n) complete
unrestricted construction and O(n log^2 n) words. Arbitrary nonnegative
exact weights remain valid inputs with the record-sensitive guarantee.
General arbitrary-weight subquadratic construction and the original local
core-support bound remain open; this route does not alter either objective.

The M4 audit passed on the first algorithmic run. It checks 135 nonempty
slot subsets, 461 selected-key depth bounds, and 6231 independent highest-
valuation selections. All 680 exhaustive binary inputs through four keys
and 60 additional mixed/rational/geometric inputs through 32 keys give
1540 complete prescribed-height controls against dense vectors AND original
all-root recurrences. Every one of 226,280 prefix values and compressed
predecessors agrees; 6778 exact breakpoint sets agree. Small-height literal
controls enumerate 53,824 selections. Original references use 881,564 root
candidates. No empirical count is substituted for a theoretical bound.

Eight complete unrestricted constructions through 1024 keys match independent
Knuth optima. The 1024-key zero-middle row has h=25 and implicit capacity
33,554,431, but retains 93,615 records across three stages and 1034 ancestor
vertices. It uses 8,405,286 finite entries and 201,726,864 threshold terms;
these are distinct operation categories, not an asserted practical speedup.
Three uniform 16-key constructions at h=16,32,64 all match the closed optimum
54. At h=64, implicit capacity 2^64-1 uses 15,120 records and 16 ancestor
vertices, directly checking that the full perfect tree is never expanded.
The source-hashed JSON contains seven hashes; all match the authoritative
local sources after the result is copied back from the Mini.

Proof review gave a stronger magnitude-independent extension before
publication. Mark t outcomes, leaving INTEGER unmarked mass V. Each marked
outcome has one of h reward coefficients; there are at most h^t coefficient
vectors, and at most 1+(h-1)V unmarked integer rewards. Hence each stage
has at most h^(t+1)[1+(h-1)V] records, even when marked weights themselves
are arbitrary nonnegative reals. If all normalized weights are integers,
s,t are fixed and V=O(n), the trimmed height is O(log n+t), proving
O(n log^(t+4) n) complete unrestricted construction and O(n log^(t+2) n)
words. This removes exceptional magnitudes from the arithmetic bound.
The prior n^(log_phi 2) theorem still covers nonlattice positive backgrounds.

The separate marked-spectrum harness passes 60 literal inputs and 1428
slot selections, with rational marked weights included. Six complete
unrestricted mixed trees through 192 keys match independent Knuth optima.
Each has one large key and one large gap; exponents 64/80 and 512/528 give
the same height and record counts at each size. At n=192, h=17, there are
45,729 records across five stages and 192 ancestor vertices. Equality of
those measured counts is a control, not the proof. Its six executed-source
hashes match local files. All tests use exact arithmetic and no timings.

The final manuscript compiles without warnings at 156 pages. Section 2.19
contains Lemma 34, Theorem 35 and Corollaries 36--37 on pages 30--33;
Appendix T carries the new audits on page 148. All 436 previous labels are
retained among 445 unique labels; references and all 20 bibliography entries
resolve. Eighty-seven source-hash entries across sixteen audit records match
the authoritative files. Every final page was rendered and visually reviewed,
with detailed checks of the new proof, audit and unchanged dedication. The
first compile attempt targeted the unrelated root TeX project and failed on
its missing image; its generated log was removed, and all successful builds
used the OBST manuscript directory. The final PDF, TeX and five-file source
archive are byte-checked before publication. The full research goal stays active.

## Checkpoint 57: exact exponential prefix-record support

The preceding turn was progress: it published complete record compression,
its integer and exceptional-magnitude bounds, sparse reconstruction, and
independent audits. This turn attacks the missing universal record-size bound
on unrestricted magnitudes. The current worktree and publication head were
clean at 4e3601a. No subagents or delegation were used.

An explicit family gives a stronger obstruction than an asymptotic search
trend. For A=n+1 set p_i=A^(n-i)-1 and every q_j=1. All original outcomes
have strictly positive integer weights. Normalization gives geometric keys
w_i=A^(n-i), zero gaps, and constant n. Since n times every suffix tail
mass is less than its first key, the unique optimum is the right chain;
height n is necessary and cannot be improved by a sharper certificate.

The weights dominate all later valuation rewards, so optimization is
lexicographic in the ruler valuations. The unique greedy tuple with m keys
in [1,U] ends at U exactly when popcount(U)<=m. To prove this, split
U=P+s at its largest power of two. If m<=s+1, choose P and recurse on
the translated suffix; if m>s+1, feasibility holds the early choices below
P until exactly s+1 remain, after which P and the entire suffix are forced.
Uniqueness identifies the strict prefix-maximum increments.

Within a fixed ending valuation d, successive slots b=(2j+1)2^d advance
the prefix window over a dyadic interval whose minimum popcount is popcount(j).
Thus b is retained after k keys iff b>=k and popcount(b)<=k. Consequently
B_k=sum_(r=0)^k binomial(n,r)-k, B_n=2^n-n, and the total stage count is
(n+2)2^(n-1)-1-n(n+1)/2. The complete explicit predecessor representation
can require Theta(n 2^n) states. Its support nevertheless has a short binary
membership predicate. This rules out a weight-independent polynomial bound
for explicit prefix records; it does not rule out implicit representations
or any general subquadratic OBST algorithm.

The first harness checked an independently derived binomial subfamily of
strict records, every dense prefix value, exact record sets and full output
trees. Its counts led to the stronger exact popcount characterization. The
second run added a check of that characterization and every prefix-maximum
jump, with no change to the constructor. Both runs passed. Subsequent extensions added the universal envelope
controls described below, and also passed. The final source-hashed result
supersedes the earlier runs and was copied back before further mirroring. The summed binomial identity was also checked from every retained
stage count in the authoritative JSON.

Across n=2,...,16 the final audit checks 1,965,265 prefix values and attaining
compressed predecessors, the same number of binary support and prefix-jump
assertions, and 135 exact record sets. There are 65,519 separate subset-of-
scales witnesses, 208,376 literal slot selections through five keys, and
2055 literal BST shapes through eight keys proving uniqueness in those
controls. Nine complete record-kernel trees through ten keys match the
closed unique-chain cost. At n=16, B_8=39,195 and B_16=65,520; formula-only
rows extend the proved counts through n=1024 without enumerating them.
Thirty additional magnitude-order diagnostics retain their exact counts
without treating them as an upper-bound proof.

The existing affine-period constructor solves the same original mixed family
with lambda=1/A and alpha=1/A-1, using 2n-1 root candidates. Six full output
controls through 1024 keys match the closed chain optimum and independent
output checks; ordinary Knuth is additionally used through 256 keys. At
1024 keys the largest integer has 10,242 bits, the complete tree is a chain,
and the affine route uses 2047 root candidates. This is a control of an
existing method, not a new solver claim. The eight executed-source hashes
match the authoritative code. All validation uses exact arithmetic and
operation counts, with no elapsed-time inference.

The stronger positive result is the sharp universal binary envelope
B_k <= E_h(k) = sum_(r=0)^min(k,h) binomial(h,r)-k, for arbitrary
nonnegative mixed weights. Earliest embeddings preserve every valuation,
and therefore every key and adjacent-gap reward. Each successor raises
popcount by at most one. A forced endpoint with popcount above k thus has
an earlier equivalent endpoint and cannot be a record. Geometric weights
of base h+1 attain this envelope for every feasible prefix, even k>h.

The structural audit covers all 32,902 nonempty slot subsets through height
four, with 246,221 selected positions. Seventy-two mixed rational inputs
check 12,424 records and 18,088 dense prefix values, plus complete output
trees. A full grid of heights one through six and all feasible key counts
checks exact sharpness on 2,667 stage sets and 97,155 dense states. All
extensions passed on the selected M4 host; the final eight source hashes
match the authoritative files. The envelope is proved independently of
these finite checks.

Publication validation: Tectonic compiled the final manuscript to 159 pages
without warnings. All pages were rendered and reviewed in contact sheets;
the new proofs, audit pages, and dedication were reviewed at readable size.
All 445 previous labels are retained among 453 unique labels, every cross-
reference and citation resolves, and the 20 bibliography entries and exact
dedication are preserved. Seventeen retained audit records match 95 executed-
source hashes. The TeX, PDF, and five-file source bundle match their
respective authoritative sources. The general goal stays active: this
checkpoint establishes the sharp record envelope and its limitation; the
remaining general construction and interval-core size gap are unresolved.

## Checkpoint 58: implicit mixed prefixes and the monotone minimum obstruction

The preceding turn was progress: it published the sharp binary record
bound, its explicit geometric extremal family, and independent audits.
The authoritative checkout was clean at ff63e38415c3db1eb2d57196f3e5f335dbc8e615.
This turn changes the representation used for the arbitrary mixed problem,
without restricting key runs or gap weights. No subagents were used.

An exact additive-normalized binary decision diagram now supports every
mixed slot prefix function. Masks partition predecessors by valuation;
exclusive prefix minima enforce a<b, and pointwise minimum incorporates
all gap penalties. Prefix roots support complete attaining traceback and
sparse tree repair. Setting h=n gives an unrestricted optimum. The data
structure is established prior work: Bryant's author-hosted 1995 paper,
Section 7.2, describes edge-valued diagrams and attributes them to Lai and
Sastry. This work claims the stated OBST reduction and proofs, not invention
of edge-valued diagrams.

The key primitive has a theoretical bound: exclusive prefix minima on a
D-node height-h diagram take O(hD) arithmetic/node/dictionary operations.
For F=L||R, PF=PL||min(min L,PR). Prefix functions are nonincreasing;
capping one by a constant follows only one crossing per level. Normalized
node memoization reuses every input node independently of its root offset.
An initial implementation passed all small correctness controls, but its
unpruned generic minimum explored unnecessary relative-offset contexts.
The observed live M4 process was explicitly interrupted, then verified
terminal. Exact min/max range pruning was added before restarting the
full audit. No observation timeout was treated as process termination.

A new explicit obstruction rules out a generic polynomial minimum bound,
even for strictly decreasing inputs. For N=2^m and b=NX+Y, use
F=-2b+X and G=-2b+Y. Each is a weighted sum of bits with 2m+1 additive
nodes. Their minimum has N distinct normalized low-bit residual functions,
whose consecutive differences switch from -1 to -2 at Y=X. It therefore
requires at least 2^m nodes at level m in MSB-first address order. This
is an operation/representation barrier: these functions have not been
realized as mixed OBST prefixes. The actual transition's additional
structure remains the necessary target, and the full goal stays active.

The pruned solver completed full geometric controls through 48 keys. The
64-key run was deliberately interrupted while still constructing its
prefixes, after intermediate structures grew substantially; no 64-key
completion or operation count is claimed. The final audit limits this
scale series to 48 keys and reruns it to retain source-hashed counters.
This changes the finite experiment, not the arbitrary-weight objective or
the mathematical correctness scope of the constructor.

The final primary DAG audit passed 72,880 direct prefix-value comparisons
and 1392 complete original all-root optimum/tree controls, including all
680 binary mixed inputs through four keys at two heights. The reference
examines 486,336 predecessors. Five geometric full constructions through
48 keys match the closed chain optimum and independent Knuth. The 48-key
final function has 45,391 nodes versus 2^48-48 explicit records, while the
constructor creates 3,069,517 nonterminal nodes and retains 1,145,477
history nodes. It makes 3,282,551 minimum calls, 2,290,986 additions, and
2,200,220 prefix calls. These are exact counters, not speed claims. All
seven executed-source hashes match the authoritative files; the JSON was
copied back before mirroring for the separate probe.

The mixed transition now has an explicit operation bound: O(h^3 D) with
zero residual gap, and O(h^5 D + X) with a general gap, where X is the
number of expanded relative-offset minimum contexts. These conservative
powers follow from mask size O(h), valuation-function size O(h^2),
node-pair addition, and the O(hD) prefix lemma. They isolate the unresolved
minimum parameter rather than inferring work from final graph size.

The separate probe passed 108 signed prefix-function controls on 12,264
addresses, including infeasible patterns. The monotone minimum construction
has exact total size 3*2^m-2: lower levels have 2^d clipped kink functions,
upper high-bit prefixes stay distinct, and there is one terminal. The
proof was expanded to this exact count and the probe rerun with an explicit
assertion. It checks m=1,...,12 and 45,744 address triples, exhaustive
through m=6 and sampled at the kink boundaries thereafter.

All nine additional full mixed controls pass independent Knuth and output
tree checks. At 64 keys the random row uses certified h=11, 413 final
nodes and 187,957 total nodes; the near-uniform row uses h=10, 230 final
nodes and 50,714 total nodes. The nonaffine geometric mixed rows go through
16 keys, where h=16, final nodes=1283, and total nodes=199,887. The final
JSON retains each p,q vector, operation categories and Knuth counters.
No practical speedup or universal size bound is inferred from these rows.

Final publication validation: the final probe's six executed-source hashes
match, and all 19 selected audit records match 108 source-hash entries.
The 162-page manuscript compiles in Tectonic without warnings. Every page
was rendered and reviewed in contact sheets; new proofs, audit text, and
the dedication were also reviewed at readable resolution. All 453 previous
labels survive among 460 unique labels, with 21 bibliography entries and
all references resolved. The dedication bytes are unchanged. New results
are in Section 2.20, the grouped negative-results section, and Appendix T.
The general arbitrary-weight subquadratic goal remains active.

## Checkpoint 59: actual-prefix searches and one-path mixed traceback

The preceding turn was progress: checkpoint 58 was published as 539e300,
with an exact full mixed implicit constructor and a generic minimum barrier.
The current checkout and published state were inspected before this work.
The full arbitrary-weight subquadratic objective remains active.

This turn attacks actual OBST diagram growth instead of reusing arbitrary
monotone functions as though they were realizable prefixes. A seeded local
search evaluates 204 mixed inputs at n=h=6,8,10,12,14,16. It shuffles
geometric keys, varies geometric gaps, and mutates/swaps weights while
maximizing the largest diagram across stages. Each diagram size is counted
by a separate bottom-up normalization of every dense dyadic block. Every
input's optimum has an independent Knuth reference; every size winner has
all prefix values checked against the implicit solver. The largest sizes
are 58,157,310,548,1335,2479, with final sizes 49,81,140,311,341,1920.
Thus measuring only the final prefix can hide larger intermediate functions.
No exponent follows from these finite observations. Height n is sufficient
but is not certified necessary in this first search.

A separate 48-input search enforces necessary height n, while keeping both
key and gap weights positive and allowing unrelated gap coefficients.
Let A=8(n+1)^2, p_i=alpha_i A^(n-i), and
q_j=beta_j A^max(0,n-j-1), with all coefficients integers in [1,n].
For suffix i, its remaining mass R satisfies
R < 2n A^(n-i)/(A-1)+n. Therefore p_i > nR. A right-chain suffix costs
at most p_i+nR; any other root costs at least 2p_i. Recursion proves the
unique full chain, so height n is necessary independently of the search.
The maximal observed sizes at the same six n are 48,123,266,495,829,1283;
they are also the winners' final sizes. These match the earlier geometric
sizes through 16; no general diagram-size theorem is inferred. Each winner
returns the exact full chain and agrees with its closed cost and Knuth.

The positive structural result is stronger endpoint dominance. Moving the
last key of a prefix from a to a later c with v(c)>=v(a) cannot reduce
its key or preceding-gap reward. Thus f_k(c)<=f_k(a). Write b-1 as the
sum of its descending set-bit powers; the successive partial sums form a
skyline. Every positive a<b lies in an interval ending at one of these
partial sums, whose valuation is at least v(a). The skyline therefore
contains an attaining predecessor even after adding any nonnegative new
gap penalty -g min(v(a),v(b)). Slot zero is retained separately.

Augment each additive node with its first-address value, including infinity.
This is computed from the left child in constant work at node creation.
Walking the bits of b-1 visits every skyline point: each 1-bit enters a
right child starting at that point, whose first value is immediately known.
This proves O(h) arithmetic/address operations per mixed predecessor query,
without new diagram nodes. Query the global sentinel 2^h at gap zero, then
follow n-1 predecessor queries. Selected-slot traceback is O(nh); sparse
ancestor repair remains the separately proved final tree-construction step.
Ties need not yield the globally earliest minimizer, only an attainer.
The new implementation retains the original forward operations unchanged;
no general bound on their intermediate diagrams or minimum contexts follows.

The skyline audit passes 42,144 direct all-predecessor prefix comparisons,
168,576 literal predecessor-query controls with integer/rational gap prices,
and 185,856 full endpoint-dominance comparisons. All 680 binary mixed inputs
through four keys and 24 rational inputs through 12 keys give 704 complete
original all-root optimum/tree controls. Six full constructions on the
unconstrained size-search winners match their independent stage sizes and
Knuth optima. At height n they use exactly n^2 traceback path steps and
create zero traceback nodes. Total forward nodes are still counted; the
16-key unconstrained winner creates 144,500 nodes, far more than its
largest live prefix size of 2479. This is a traceback improvement, not a
claim that the complete constructor beats Knuth.

All three new result records retain exact counts and executed-source hashes;
the skyline audit also records the consumed size-search JSON hash. The
first search normalizes 15,155,304 dyadic blocks and evaluates 15,146,188
mixed prefix states. All compute ran through m4build, and each completed
JSON was copied back before another mirror operation. No timings are used.
The manuscript adds the endpoint-dominance lemma, the one-path query theorem,
and appendix verification. All earlier source files remain unchanged.

Final validation for checkpoint 59: all 22 source-hash entries across the
three new audit records match the authoritative files, and the consumed
search-record hash matches. The final 164-page manuscript compiles without
warnings, overfull boxes, underfull boxes, or unresolved references. All
460 prior labels survive among 463 unique labels, with 21 bibliography
entries and all citations resolved. All pages were rendered and reviewed
in nine contact sheets; pages 35--36, 156, and 164 were also reviewed at
readable resolution. The dedication is byte-for-byte unchanged. The PDF,
TeX, and five-file source/font bundle were copied to the user outputs and
verified against the manuscript. A compiler invocation initially used the
repository root; its newly generated untracked log was removed, and all
publication validation uses the correct obst/manuscript build.

## Checkpoint 60: polynomial scalar-carry forward updates

The preceding goal turn was progress: checkpoint 59 published the actual
prefix skyline theorem and O(nh) slot traceback as b75ccf4. The clean
local branch and head were inspected before continuing. This turn uses
endpoint dominance in forward construction, addressing the previously
uncontrolled generic minimum parameter X. The full objective remains active.

For a dyadic input block [B,B+2^d), the scalar carry p_B is the inclusive
prefix minimum through B. For B>0, every earlier low-valuation candidate
is dominated by B, so an attaining outside candidate has valuation at least
d. At every interior target b, its gap-adjusted value is p_B-g v(b).
For a nonempty prefix B=0 has infinite carry; the empty prefix is handled
by the initial zero-gap transition. This distinction preserves the actual
zero-slot valuation and avoids an invalid positive-gap empty-prefix rule.

The block summary E_g(R)=min_(t>0)[R(t)-g v(t)] excludes the first address.
For children L,U it is min(E_g(L),E_g(U),U(0)-g(d-1)), allowing O(D)
summary work by normalized-node memoization. The new midpoint value is
min(p_B-g(d-1),E_g(L))-w(d-1); the right carry is
min(p_B,min L,U(0)). Recurse and set the right output's first address.
If p_B<=min R, a shared valuation template emits the whole interior.
No generic pointwise minimum, addition, or prefix diagram operation is used.

The critical bound comes from the global inclusive prefix function Q of
F, which has O(hD) nodes by the established monotone-cap proof. In every
non-pruned block, p_B>m=min R, so Q has first value p_B and minimum m.
The normalized Q node's first-address value is exactly p_B-m, including
infinity. Thus the input-node/Q-node pair determines the normalized carry
context. There are O(hD^2) expanded contexts, each requiring O(h) persistent
first-address replacement work. Summaries and templates yield a proved
O(h^2D^2) arithmetic/dictionary bound per arbitrary mixed update, replacing
X with a polynomial parameter. Q is a proof object, not required by the
constructor. A useful bound on D across all n stages is still missing.

The first implementation passed every small prefix and retained winner.
The final audit adds minimum-feasible-height controls to the larger-height
binary controls, exercising infeasible states near capacity. It passes
60,336 direct prefix-value comparisons and 1384 complete original all-root
optimum/tree checks: all 680 binary inputs through four keys at two heights,
plus 24 rational inputs through 12 keys. A separately constructed inclusive
prefix graph checks all 15,993 expanded contexts against the claimed
input/prefix-node injection, including infinite carries. All needed weighted
summaries are bounded by the input reachable-node count in each control.

Twelve full constructions reuse both sets of adversarial size-search winners.
Every stage size matches the independent dense normalization, and every
output matches Knuth and complete-tree checks. At 16 keys the unconstrained
winner creates 14,124 total nodes instead of 144,500 for the same input in
the earlier constructor, with 3829 expanded carries. The necessary-chain
winner creates 19,090 versus 199,603 nodes, with 10,110 carries. These are
matched node counts, not running-time or universal complexity claims.
All twelve new runs make zero generic diagram min/add/prefix calls.

The separate scale run completes full positive mixed, nonconstant-gap
unique chains at necessary h=n for n=24,32,48,64. It checks the explicit
strict suffix inequalities, closed chain costs, independent Knuth costs,
and every output link/depth/gap. At 64 keys it has 111,668 final nodes,
6,355,399 total nodes, 3,722,796 retained history nodes, and 3,567,441
expanded carry contexts. It also records 38,536,277 first-address
replacement visits. That substantial intermediate work remains visible.
These inputs are distinct from the earlier interrupted 64-key run.

All compute ran through m4build. The final primary audit was rerun after
adding the tight-height controls; its prior output is superseded. Each
completed remote JSON was copied back before another mirror operation.
The scale process was observed live with its PID while computing 64 keys,
and then its tool session reported normal completion. No process was
restarted on an observation timeout. The new proof and appendix counts
are incorporated in the manuscript, with prior solver sources unchanged.

Final checkpoint-60 publication validation: both new result records match
all 17 executed-source hashes and both consumed search-record hashes. The
167-page manuscript compiles without warnings or unresolved references;
all 463 previous labels survive among 468 unique labels, and all citations
resolve to the 21 bibliography entries. Every page was rendered and
reviewed in contact sheets, with pages 36--37, 158--159, and 167 reviewed
at readable resolution. The dedication remains byte-for-byte unchanged.
The TeX, PDF, and five-file source/font bundle in the user outputs match
the final manuscript. The general arbitrary-weight objective remains open.


## Checkpoint 61: linear-in-diagram-size forward work

The preceding turn made progress: checkpoint 60 published the scalar-carry
constructor and its O(h^2 D^2) bound as 59797c7. This turn sharpens the
bound on the unchanged implementation to O(h^2 D), without resolving the
all-stage diagram-size question or the full arbitrary-weight objective.

At a normalized parent node with children L,U and incoming carry p, put
C=min(min L,U(0)). Classify the right edge as a reset when C<=p, including
ties and infinite ties. Its normalized carry C-min U then depends only on
the parent node, so there is at most one reset seed per reachable input
node. Infinity is a separate symbol. If the right edge inherits p instead,
p<C<=min L prunes the left child. Hence every expanded context has at most
one inherited expanded child. Paths from the root and all reset seeds cover
every expanded context, even when memoization merges paths. Depth decreases
on every edge. This proves Z<=h+sum_u max(d(u)-1,0)=O(hD), and depth sum
at most h(h+1)/2+sum_u d(u)(d(u)-1)/2. Including templates bounds both
node-assembly calls and first-address replacement visits by
h(h+1)+sum_u d(u)(d(u)-1)/2. All forward stages take O(h^2 sum_k D_k).

A generic sharp family has N=2^m, h=2m, A(X)=2X-popcount(X), and
F(NX+Y)=-A(X)/(m+1)-Y. Its weighted-bit representation has D=2m+1 nodes.
At every low level there are m+1 carry contexts: m fractional values
(s+1)/(m+1), indexed by the valuation of X, and the initial-block value.
At upper depth m+r there are m-r+1 states. This gives exactly
Z=3m(m+1)/2. The depth sum plus all templates gives exactly
M=m(7m^2+15m+2)/6 for both assembly calls and replacement visits.
Thus the general O(hD) context and O(h^2D) work bounds are sharp. However,
F(N)>F(N-1) violates endpoint dominance, proving the family cannot arise
as an actual mixed OBST prefix. Actual-prefix improvements remain open.

The reset audit passes 1416 updates, 34,186 expanded contexts and 18,513
reset edges. It checks seed uniqueness, the inherited-child property,
exact coverage, path lengths, weighted depth charges, both work bounds,
recursive call counts, summary bounds, and zero generic diagram operations.
Its 148 arbitrary-diagram controls include rational, signed and infinite
entries and compact inputs through height 128; these are count-only
controls. Its 372 complete trees comprise 336 binary controls at two
heights, 24 rational controls through 16 keys, and twelve retained search
winners. The first 360 use original all-root references; winners use
Knuth and independent stage sizes. Every tree's original cost is checked.
One rational stage has two distinct carries for the same input node, so
an at-most-one-carry assertion for actual prefixes is already false.
No stronger asymptotic actual-prefix claim follows from these counts.

The sharp audit checks m=1,...,16,24,32,48,64, all 14,700 contexts,
and 7085 explicit input values (exhaustive through m=6, sampled thereafter).
At m=64 it verifies D=129, Z=6240 and M=316096. Every row checks the
endpoint-dominance violation. The initial sharp run stopped on the remote
Python 3.9 absence of int.bit_count; replacing that call with
bin(x).count('1') preserves the formula, and the final source-hashed run
completed. All mathematical assertions pass. Both final results were
copied from the Mini before another mirror. The two new records retain
16 matching source hashes and two input-record hashes. Earlier solver
sources and historical audit records remain unchanged.

The manuscript replaces the old node-pair complexity proof with the
explicit reset-path lemma and weighted operation charge. It retains the
older injection audit as a check of the weaker bound, adds the generic
sharp family to the grouped representation barriers, and confines all
finite verification counts to the appendix. The Monge result still leads;
its core-size theorem and the exact title dedication are preserved.

Final checkpoint-61 validation: the 169-page manuscript compiles without
warnings, overfull/underfull boxes or unresolved references. All 468 prior
labels survive among 475 unique labels; the 21 bibliography entries resolve
all citations. All pages were rendered and reviewed in nine contact sheets;
pages 36--38, 126--127, 161 and 169 received readable-resolution review.
The dedication remains byte-for-byte unchanged. The final TeX, PDF and
five-file source/font bundle in the user outputs match the authoritative
manuscript. All new and prior forward-audit source hashes match. The full
arbitrary-weight objective remains active; all-stage diagram growth is open.


## Checkpoint 62: constant boundary assembly and full construction

The preceding turn was progress: checkpoint 61 published the O(h^2 D)
reset-path bound and generic sharpness as 2e71fbc. The clean authoritative
checkout and head were inspected before continuing. This turn changes the
representation to remove persistent first-address replacement, while retaining
the full arbitrary-weight mixed OBST objective.

A punctured diagram represents only local addresses 1,...,2^d-1. Its node
contains the left interior, midpoint scalar, and right interior, normalized
by the minimum finite interior value. Canonicity follows by induction.
An ordinary node L||R converts to (puncture(L),R(0),puncture(R)); memoized
first values and conversion take O(D_standard) work and create at most one
punctured node per ordinary nonterminal. The first full-block value is kept
outside the representation. Actual nonempty prefix roots have infinite
first value; the empty initial prefix has no interior and first value zero.

The inclusive carry p_B<=F(B) already dominates the omitted first entry.
For P=(L,c,R), the right carry is min(p,min L,c), the left carry is p, and
the new midpoint is min(p-g(d-1),E_g(L))-w(d-1). The weighted interior
summary is min(E_g(L),c-g(d-1),E_g(R)). Thus the forward update assembles
one node directly instead of replacing a first-address path. Pruned valuation
templates also cost one node per depth. The same reset-path argument gives
Z<=h+sum_u(d(u)-1), and exact assembly count Z+T with T<=h. This proves
O(h(D+1)) per arbitrary mixed update, counting all intermediate work.

The skyline walk reads candidates directly from midpoint scalars, retaining
O(nh) selected-slot traceback. For full repair, the union of selected slots
and perfect-tree ancestors is ancestor-closed and has at most nh vertices.
An inorder traversal restricted to dictionary members enumerates it in order
in O(nh), removing comparison sorting. The existing linked sparse deletion
then returns the same complete tree. All forward work, traceback and repair
therefore take O(h(n+sum_k D_k)) arithmetic/address/dictionary operations
and at most that many stored words. The all-stage sum remains unbounded by
a useful universal theorem; the unrestricted subquadratic goal stays active.

The previous generic weighted-bit family has exactly 2m punctured nodes
at h=2m. Every nontrivial block minimum is at its last address, and its
first value is dominated by the carry, so the same exact Z=3m(m+1)/2
contexts expand. Its m-1 templates now contribute only m-1 assembly calls.
This proves a sharp Theta(hD) family for the new mechanical recursion. The
explicit endpoint-dominance violation still excludes actual OBST prefixes.

The harness was written before the new implementation. Its first version
passed the direct prefixes and queries, complete trees, retained winners,
and generic sharpness. The repair change was then added with its own
independent subset controls; both the main and scale audits were rerun on
the final source. All final runs completed normally on the Mini through
m4build, and completed JSON records were copied before another mirror.
The preliminary scale record is retained only in local scratch work.

The final audit passes 60,336 direct prefix entries, 94,640 direct
predecessor queries, and 1384 full original all-root optimum/tree controls.
It verifies conversion against dense canonicalization on 96 arbitrary signed,
rational and infinite inputs, including all 6024 nonzero address values.
Twelve retained adversarial winners have every prefix compared by canonical
equality to conversion of the previous full constructor, and complete
optima checked by Knuth. All 32,902 nonempty slot subsets through height four
produce exactly the sorting-based repair's tree; ancestor enumeration uses
exactly two visits per collected vertex. Across all operation controls,
5456 updates inspect 59,358 expanded contexts and 26,108 reset edges.
The generic sharp family is checked through m=64, where D=128, Z=6240
and the exact assembly count is 6303. No empirical exponent is claimed.

The scale audit reuses the identical prior necessary-height mixed chains
at n=24,32,48,64, checking strict dominance, unique-chain costs, independent
Knuth and the full output trees. At 64 keys the new representation has
72,235 final nodes, creates 2,636,579 nodes and uses 3,569,521 assembly calls.
The earlier representation on that exact input creates 6,355,399 nodes and
uses 38,536,341 assembly calls and 38,536,277 replacement visits. The
64-call difference is its initial ordinary point diagram. The new
routine performs no first-address replacements. Four further arbitrary mixed
integer inputs at n=32,64,128,256 use the proved height selector and match
Knuth and full-tree checks. Their heights are 11,13,14,16; the 256-key run
has 460 final nodes, 73,226 total nodes and 114,633 assembly calls.
These are finite exact counts, not a bound on all-stage growth.

The manuscript adds the canonical-interior lemma, complete-construction
theorem including sorting-free repair, and generic sharpness corollary.
Finite verification counts remain in Appendix T. The Monge result continues
to lead, and the dedication and sponsor attribution remain unchanged.

Final checkpoint-62 publication validation: all 16 new source-hash entries
and three consumed-record hashes match, as do all four preceding reset and
forward audit records. The 172-page manuscript compiles without warnings,
overfull/underfull boxes or unresolved references. All 475 prior labels
survive among 484 unique labels, and all citations resolve to the same
21 bibliography entries. Every page was rendered and reviewed in nine
contact sheets; pages 38--40, 129--130, 163--164 and 172 were also reviewed
at readable resolution. The dedication is byte-for-byte unchanged. Final
PDF, TeX and five-file source/font bundle in the user outputs match the
authoritative manuscript. The full arbitrary-weight goal remains active.
