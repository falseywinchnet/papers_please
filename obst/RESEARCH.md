# Full optimal binary search trees: research record

Started 2026-10-18, America/Chicago. Research and exposition by OpenAI Codex
Sydney, with sponsorship and problem selection by the repository owner.

## Objective and status

Find a substantively useful improvement for the full optimal binary search tree
problem, or prove an appropriate barrier to subquadratic construction. The
general exact subquadratic problem remains unresolved by this project.
The current checkpoint gives exact sufficient contraction rules and an
adaptive linear preprocessing pass. Its bound is O(n+m^2+sum k_t^2), where
m is the surviving core size and k_t are independently solved block sizes.
This improves state counts substantially on a seeded heavy-separator input,
but little on ordinary random mixed weights. Novelty is unestablished;
no general subquadratic bound or complexity lower bound is claimed.

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

## Completion requirements

- A fully stated, proved result or substantively validated algorithm for the
  requested mixed-weight problem, with honest scope and prior-art comparison.
- Reproducible correctness and adversarial evidence; practical claims require
  appropriate matched benchmarks against Knuth and relevant alternatives.
- TeX manuscript and compiled, visually checked PDF uploaded to papers_please.
- Continued pursuit of the full objective; intermediate notes are not completion.
