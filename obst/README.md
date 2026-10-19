# Full optimal binary search trees: research checkpoint

Research and exposition by OpenAI Codex Sydney, with sponsorship and problem
selection by the repository owner. The general research objective is ongoing.

- [Manuscript (PDF)](manuscript/main.pdf)
- [Manuscript (TeX)](manuscript/main.tex)
- [Research record and prior-work map](RESEARCH.md)
- [Contraction argument](CONTRACTION.md)
- [Minimum-path-length shape certificate](COMPLETE.md)
- [Concave baseline-price extension](BASELINE_PRICES.md)
- [Bounded-excess dyadic construction](EXCESS.md)
- [Split-height construction and taller-tree certificate](SPLIT_HEIGHT.md)
- [Exact variable mass frontier and uniform-width comparison](MASS_FRONTIER.md)
- [Dominant-gap separators and local mass frontiers](GAP_SEPARATOR.md)
- [Joint heavy-outcome cores and protected-height certificate](HEAVY_CORE.md)
- [Residual-cost core exclusion and linear-weight family](CORE_EXCLUSION.md)
- [Relaxation, counterexamples, and failed sparse search](RELAXATION.md)
- [Depth-sequence dual and exact tail compression](DEPTH_DUAL.md)
- [Exact depth ordering and arbitrary-window obstruction](DEPTH_ORDER.md)

The input has weights on **both keys and gaps**. The latest constructor credits
a residual search-cost lower bound when certifying a joint core for heavy outcomes,
then solves the intervening intervals on local mass frontiers. Single-outcome
separators remain available as fallback. An interior-gap certificate retains both neighboring key
weights and gives an exact two-orientation cost identity. Static range indexes
avoid repeatedly scanning shrinking components. Earlier contraction and
bounded-shape methods remain available as controlled comparisons. The general
worst case remains quadratic; no unrestricted subquadratic solution or
impossibility proof is claimed. Priority of the sufficient conditions has
not been established.

At 512 keys, a positive-weight instance with 22 randomly located heavy keys
needed 10,344 total DP states rather than 131,328. This includes the tables
inside collapsed blocks. Ordinary random mixed weights benefited little.
These are state counts, not wall-clock speedup claims.

## Reproduce

Python 3, standard library only. From the repository root:

```
python3 obst/code/research.py
python3 obst/code/sparse.py --max-n 128 --trials 2
python3 obst/code/contract.py --max-n 512
python3 obst/code/block_check.py
python3 obst/code/block_contract.py --max-n 512
python3 obst/code/recursive_contract.py --max-n 1024
python3 obst/code/benchmark_recursive.py
python3 obst/code/complete.py --max-n 1024
python3 obst/code/benchmark_complete.py
python3 obst/code/baseline_prices.py
python3 obst/code/benchmark_baseline.py
python3 obst/code/ordered_certificate.py --max-n 512 --iterations 32
python3 obst/code/ordered_obstruction.py
python3 obst/code/excess.py --max-n 1024
python3 obst/code/benchmark_excess.py
python3 obst/code/split_height.py
python3 obst/code/benchmark_split_height.py
python3 obst/code/mass_frontier.py
python3 obst/code/benchmark_mass_frontier.py
python3 obst/code/frontier_separation.py
python3 obst/code/gap_separator.py
python3 obst/code/benchmark_gap_separator.py
python3 obst/code/separator_obstruction.py
python3 obst/code/heavy_core.py
python3 obst/code/benchmark_heavy_core.py
python3 obst/code/heavy_core_scale.py
python3 obst/code/check_core_exclusion.py
python3 obst/code/check_core_exclusion.py --mixed-only
python3 obst/code/benchmark_core_exclusion.py
python3 obst/code/core_exclusion_scale.py
python3 obst/code/depth_dual.py --max-n 256 --iterations 300
python3 obst/code/depth_dual.py --max-n 256 --iterations 300 --unique-root
python3 obst/code/depth_order.py
```

The sponsor's host-specific remote commands are in the root AGENTS.md.
Exact integer correctness checks use an independent cubic oracle, Knuth DP,
and direct tree-cost evaluation. The basic harness also enumerates shapes.
Seeds and counts are in the code and JSON results. The sparse solver is
preserved as a failed performance experiment, not recommended as a fast solver.
`block_contraction.json` preserves the earlier fixed-cap experiment;
`block_contraction_adaptive.json` records the current adaptive implementation.

The recursive prototype accepts a decomposition only after a fixed fractional
reduction in its state estimate and tries a whole-component lower/upper equality
certificate before further work. Matched five-trial timings are exploratory
Python measurements, not a general performance guarantee. At n=1024 the
heavy-separator median runtime ratio is about 0.134 versus Knuth; ordinary
random and near-uniform inputs are roughly tied, and several n=512 controls
are slower. Full counters are retained alongside timings.

The additional `complete.py` shortcut optimizes every minimum-unweighted-
path-length shape within a logarithmic state-width budget, then certifies
that no other shape can improve its weighted cost. It retains both key and
gap weights. `hybrid_solve` combines it with the recursive contraction solver;
`solve` uses Knuth directly as fallback. Successful attempts cost O(n log n),
while failed or skipped attempts retain the quadratic worst case. It closes
the earlier near-uniform failure on the tested sizes near powers of two;
ordinary random inputs still fail the certificate. See COMPLETE.md for the
proof, exact operation counts, and the unsuccessful regimes.
The optional `optimize_baseline=True` flag on either solver searches a
concave family of valid exclusion bounds, capped at logarithmically many
additional linear oracle calls. It recovers some failed certificates while
preserving every earlier success and the O(n log n) attempted-shortcut bound.
The default remains False so earlier measurements remain reproducible.

The depth dual is a separate experimental lower-bound component. Its affine
tail permits exact O(n log n) oracle evaluations without bounding the unknown
optimal BST height. It does not yet give competitive general exact construction:
the root bounds leave 254/256 candidates on a random mixed instance, and a
five-key counterexample proves a structural gap in this relaxation family.
The extension in DEPTH_ORDER.md characterizes the missing global ordering
condition and proves that unique-minimum checks of any fixed window width
cannot repair the gap. A strictly positive family limits that relaxation's
bound to at most 113/128 of OPT, independently of multiplier optimization.
This is a limitation of one relaxation, not a general complexity lower bound.

Compile `manuscript/main.tex` with Tectonic or a compatible LaTeX installation.

The new `excess.solve(p,q,budget=2)` optimizes all trees within two units of
minimum unweighted internal path length, using aligned dyadic gap intervals
and retaining every key cost. It attempts this only when the bottom-level
shape width is logarithmic, certifies against all excluded trees, and falls
back to Knuth on failure. See EXCESS.md for the state-band proof and limits.

`split_height.solve(p,q,extra_height=1)` removes the shape-width restriction:
it optimizes all trees of external height at most ceil(log2(n+1))+1, then
certifies the result against all taller trees using their exact minimum
unweighted internal path length. It uses the known Karpinski--Larmore--Rytter
split-height/Monge mechanism, implemented with aligned dyadic tilings and
SMAWK. For any fixed extra height, attempted work is O(n^(3/2)) at every n;
fallback still makes the worst case quadratic. See SPLIT_HEIGHT.md for the
prior-art distinction, padding argument, verification, and failure controls.

`mass_frontier.solve(p,q,mode='adaptive')` instead selects a domain guaranteed
to contain an unrestricted optimum, using a directly proved mixed-weight
Fibonacci subtree-mass bound. It stores only admissible intervals and composes
them with an exact top skeleton. The work bound is
O(n log(n+1) + min_d [S_d+n*2^d]), where S_d counts admissible intervals at
depth d. The `uniform` mode implements the corresponding global-width
envelope as a controlled prior-architecture baseline. Every solve is exact;
the selector may choose the full Knuth table. The worst case stays quadratic.
The variable contour has a proved exponent advantage on a positive light-block
family relative to this uniform envelope, not relative to all earlier methods.
See MASS_FRONTIER.md for proofs, exact counts, matched timings, and the
counterexample that invalidated the initially imported mass-bound constant.

`gap_separator.solve(p,q)` combines certified endpoint, key, and interior-gap
splits with the local variable frontier. Its work is
O(n log(n+1) + sum_t min_d [S_(t,d)+m_t*2^d]), with local masses and contour
counts in the disjoint terminal components. If each terminal has at most b
keys, the bound is O(n log(n+1)+nb). An entirely endpoint-certified chain
takes O(n) arithmetic work; this includes the full mixed geometric family
p_i=q_i=2^i with q_n=2^n. The large weights preclude a linear bit-cost claim.
At n=2048, the heavy-gap fixture stores 153,582 terminal intervals versus
1,047,552 for the direct global frontier; hierarchical gaps store 22,333 versus
522,242. These are DP cells, not total operations or runtime ratios.
The `terminal='knuth'` variant isolates the effect of separator decomposition.
See GAP_SEPARATOR.md for the proof, counterexample, complete counters,
matched comparisons, and unchanged worst-case limitation.

In ten matched trials per fixture at n=2048, separator+frontier and
separator+Knuth runtime ratios to Knuth were 0.04608/0.01843 on hierarchical
gaps and 0.75211/0.49766 on a heavy gap in random background. The earlier
contraction solver remains much faster on a heavy-key fixture. Plain Knuth
terminals beat the local frontier on the tested smaller components. These
are scoped Python results; all 70 trials and competing baselines are retained.
A positive family with two equally heavy interior gaps proves that the current
combined constructor still selects the entire quadratic table. See the
obstruction proof and `separator_obstruction.py`; large rows count plans only.


`heavy_core.solve(p,q)` addresses several comparable heavy outcomes jointly.
Selected keys and neighboring keys of selected gaps form a certified top core;
intervening intervals become independent exact payloads. A protected-only
Fibonacci height bound strengthens the dominance test, and an ascending
threshold/union-find sweep chooses the smallest certified Knuth-state proxy
in O(n log n) arithmetic work. Failed certification uses the previous separator
constructor. Both original key and gap weights remain in the final solve.

The positive two-heavy-gap obstruction now takes O(n log n) with unit background
instead of the full quadratic table. At n=2048, the constructor uses ten core
DP cells plus linear payload construction and selection work. With random
mixed background it uses 306,506 cells instead of 2,098,176. A 45-gap fixture at
certificate equality uses 23,695 cells; the earlier size-based certificate fails.
These are scoped improvements. The unrestricted worst case is still quadratic;
see HEAVY_CORE.md for the complete proof, exact checks, counters, and limitations.

Ninety matched trials show core+frontier / core+Knuth runtime ratios to Knuth of
0.00700 / 0.00551 for unit-background two-gap inputs, 0.70676 / 0.79129 with
random background, and 0.08573 / 0.03229 for the moderate-gap equality fixture
at n=2048. Small random frontier solves and geometric screening overhead remain
negative controls. A full 65,536-key two-gap tree was constructed and checked
against an independent four-key cubic core plus the uniform closed form; its
exact cost is 1,407,374,885,846,941. The previous 2,147,516,416-cell table was
only planned, not executed. These scoped results do not complete the general
subquadratic research objective.


`core_exclusion.solve(p,q)` strengthens the fixed-core certificate with a
lower bound on unavoidable residual search cost. A non-core-closed tree costs
at least protected_OPT + theta + residual_LB. A protected-optimal core with
balanced payloads can certify closure before any exact payload solve. The
optional `refine=True` mode tries one exact closed candidate after all witnesses
fail. A bounded portfolio of thresholds and reused sorted profiles keep witness
screening at O(n log n); the general worst case remains quadratic.

On n=2^h>=8, unit background and q_1=q_(n-1)=4n admit O(n log n) construction,
although the previous height test fails. The exact cost is (2h+23)n-6h-3.
The full 65,536-key tree costs 3,604,381 and uses ten protected proof cells plus
ten full-weight core cells. The previous frontier's 146,498,625-cell plan was
not executed at that size. Nonuniform positive mixed backgrounds are also
checked, including selected keys as well as gaps. See CORE_EXCLUSION.md for
proofs, 6,560 full correctness solves, 57 larger fixtures, all 320 matched
measurements, and the explicit failure on an optimal-but-uncertified 2n-gap core.
