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
- [Relaxation, counterexamples, and failed sparse search](RELAXATION.md)
- [Depth-sequence dual and exact tail compression](DEPTH_DUAL.md)
- [Exact depth ordering and arbitrary-window obstruction](DEPTH_ORDER.md)

The input has weights on **both keys and gaps**. The checkpoint gives exact
sufficient conditions for collapsing keys or blocks, plus a linear pass that
chooses a block-size threshold minimizing subsequent interval-DP states.
The resulting bound is O(n + m² + sum k_t²). It remains quadratic in the
worst case; no general subquadratic solution or impossibility proof is claimed.
Novelty of the sufficient conditions has not been established.

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
