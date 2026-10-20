# Residual-cost exclusion for full optimal BST cores

The height certificate charged all new light search cost against one saved
heavy comparison. The excluded trees also have to pay for light searches.
Crediting a lower bound on those unavoidable costs yields a stronger sufficient
condition for the same core. This remains a full mixed-weight method: no
original key or gap weight is removed from the final optimization.

## The certificate

Split the original weights into selected weights w_H and residual weights w_0.
Selected outcomes retain their original positive weight in w_H; all other
entries are zero. The necessary core A contains selected keys and adjacent
keys of selected gaps. Let theta be the smallest selected weight, P the exact
protected-only core optimum, and B_0 any valid lower bound for the full residual
problem on all n keys.

The preceding projection lemma implies, for every non-core-closed tree T,

    C_H(T) >= P + theta.

Independently C_0(T) >= B_0. Adding the two gives the excluded-class bound

    C(T) >= P + theta + B_0.

Thus any core-closed witness with cost U at or below this bound proves that
some global optimum is core-closed. If C_A is the exact optimum within the
closed class, C_A <= P+theta+B_0 proves C_A globally optimal. Equality is safe;
it does not exclude ties outside the class.

The implementation uses the already implemented order-free mixed-node
relaxation for B_0. This is not a new Huffman algorithm. The novel-status
question for the derived sufficient certificate remains open; a targeted
search is not a comprehensive priority search.

## Witness first; optional exact refinement

Optimize the protected core, attach balanced payloads, and evaluate its exact
residual cost U_0. Before any exact payload solve, test

    U_0 - B_0 <= theta.

If it passes, optimize the full-weight core and payloads exactly. For a fixed
selected set this contains the preceding height certificate: the witness has
U_0 <= (H+L)*W_light and the residual lower bound is nonnegative. A different
selector can still choose different sets, so this is not an implementation-wide
performance dominance statement.

An optional refinement computes C_A even if the witness fails. For
p=[0,0,1], q=[0,4,1,1], theta=4, the protected optimum is 8 and B_0=4.
The witness costs 17 and fails the exclusion bound 16. Exact closed optimization
costs 14 and certifies the global optimum. The refinement can recover a weak
witness without changing the proposed structural class.

## Candidate portfolio and cost accounting

A single proxy-minimizing threshold can select too many ordinary outcomes and
fail while a heavier threshold succeeds. The selector retains two representatives
for each dyadic core-size band: smallest Knuth-cell proxy and highest threshold.
Only core sizes m <= floor(sqrt(n*ceil(log2(n+1)))) and strict proxy improvements
are admitted. An activation/union-find sweep finds all representatives in
O(n log(n+1)) arithmetic work. There are O(log(n+1)) representatives, and their
squared core sizes sum to O(n log(n+1)).

Original key and gap profiles are sorted once. For a new threshold, replace
selected profile entries by zeros at the end of each descending profile; no
new sort is needed. Each residual two-queue bound and each witness construction
cost O(n), besides the protected core's O(m^2) exact solve. All witness screening
therefore costs O(n log(n+1)). Candidate order follows increasing proxy.

The default tries only witnesses, then falls back to the preceding full solver.
The optional `refine=True` mode, after all witnesses fail, refines only the first
candidate. Allowing every candidate an unsuccessful exact payload solve could
add a logarithmic factor to the quadratic worst case; the implemented one-refinement
limit avoids it. A successful plan costs

    O(n log(n+1) + K(m) + sum K(k_t)).

Both modes retain quadratic general worst-case work and storage. Protected
proof tables require at most O(n log n) space; exact final kernels can be
quadratic. Per-attempt counters are nested in `attempts`. Add executed
`kernel_short_states`, protected proof cells, and fallback cells as distinct
categories. `kernel_selected_short_states` repeats selection metadata and must
not be counted again as executed cells. These counters are not complete CPU
instruction counts. Direct cost checks are included in the timed solves.

## A proved linear-weight family

Let n=2^h>=8. All key and gap weights are one except q_1=q_(n-1)=theta>1.
The four-key protected core optimum is P=5*theta. Use original key 1 as root,
key 0 as left child, key n-2 as right child, and key n-1 as right-right child.
The n-4 payload hangs at depth two. Its balanced residual cost is

    U_0 = (2h+3)*n - 6h - 3.

For residual weights, E=I+2n rewrites the full cost as
sum (q_j+1)*depth_j - n. The order-free leaf weights are two ones and n-1 twos.
Huffman merges the two ones first; the remaining n equal twos form a perfect
height-h code. Therefore

    B_0 = 2nh - n + 2,
    U_0 - B_0 = 4n - 6h - 5.

So theta >= 4n-6h-5 certifies closure. The choice theta=4n passes, while the
previous height certificate requires (h+4)*(2n-1) and fails. At theta=4n,
the four protected-optimal core shapes have light costs 4n-1 or 6n-9; every
other shape has selected cost at least 6*theta > 5*theta+4n-1. This yields

    OPT = (2h+23)*n - 6h - 3.

The algorithm uses O(n log n) work and O(n) space on this strictly positive
mixed family. Its weights and intermediate integers have O(log n) bits. This
separates the certificates, not all previous algorithms: the fallback frontier
can itself omit states on these inputs.

## Exact checks and measured scope

- 22,140 exhaustive inputs in {0,1,4} through four keys; 17,054 nontrivial
  threshold cases checked against all shapes. There are 13,669 witness
  certificates and 15,181 exact-candidate certificates, including 1,512 rescues.
- 14,912 excluded-tree checks using arbitrary selected subsets, weights in
  {1,3}, and up to three keys.
- 6,560 full solves on 1,640 inputs through 40 keys: both kernels and both
  refinement settings against cubic DP and direct tree costs.
- 1,640 candidate portfolios checked by direct enumeration.
- 48 larger fixtures plus nine additional positive varying-background fixtures
  through 2,048 keys against Knuth and the preceding solver.
- 14 full power-of-two constructions through 65,536 keys, checked by the
  proved formula, independent cubic four-key core, and full tree evaluation.
- 80 matched trials and 320 complete timed solves, with all values agreeing.

At n=2048, interval/proof cell counts are:

| Fixture | Previous intervals | New intervals | New protected proof cells |
|---|---:|---:|---:|
| Two gaps of weight 4n, unit background | 568,350 | 10 | 10 |
| 45 gaps of weight 4n, unit background | 304,486 | 1,394 | 4,095 |
| 45 mixed outcomes, unit background | 305,421 | 1,250 | 2,346 |
| Two gaps, varying background | 951,851 | 307,541 | 30,941 |
| 45 gaps, varying background | 304,486 | 23,757 | 22,519 |
| 45 mixed outcomes, varying background | 305,421 | 24,163 | 27,558 |
| Random control | 308,860 | 308,860 | 33,380 |

Varying backgrounds independently draw all ordinary weights from [1,1000];
selected weights are 4000n. Both keys and gaps vary. These are finite tests,
not a guarantee that all draws certify. The random control fails and pays
additional screening before the unchanged fallback.

The 65,536-key full solve costs 3,604,381 and uses ten protected-core cells plus
ten full-weight core cells, fifteen root candidates in each. Counters include
196,799 selection comparisons, 131,204 bound-sort comparisons, 65,536 bound
contractions, 65,535 two-queue comparisons, 65,532 activations, 65,531 unions,
and 65,529 find steps. Every witness and output key is constructed. The
excluded-class lower bound is 3,604,482, leaving a margin of 101. A single full
solve took about 0.6574 seconds. The old plan selected 146,498,625 cells at
depth 11; that large old solve was not run.

## Matched timings

Eight balanced orders per fixture are four cyclic rotations and their reversals,
not all 24 permutations. All preprocessing and reconstruction are included;
M4/Python 3.9.6, default witness mode. Entries are median paired runtime ratios
to Knuth; smaller is better.

| n / fixture | Previous core/frontier | New/frontier | New/Knuth |
|---|---:|---:|---:|
| 1024 / linear_two_gaps_4 | 2.70316 | 0.01539 | 0.01965 |
| 1024 / linear_two_gaps_2 | 2.14252 | 2.12346 | 1.08928 |
| 1024 / linear_many_gaps | 1.21361 | 0.03458 | 0.03469 |
| 1024 / linear_mixed_outcomes | 1.47715 | 0.03594 | 0.03472 |
| 1024 / random | 1.58933 | 1.66642 | 1.17777 |
| 1024 / near_uniform | 1.47283 | 1.51952 | 1.06257 |
| 512 / geometric | 0.05133 | 0.24322 | 0.29896 |
| 1024 / linear_random_two_gaps | 3.16889 | 1.23537 | 0.87326 |
| 1024 / linear_random_many_gaps | 1.53202 | 0.15569 | 0.10279 |
| 1024 / linear_random_mixed | 1.50427 | 0.14830 | 0.11509 |

The new certificate gains on several structured families, but random inputs
remain slower than Knuth. Geometric input is about 4.91 times slower than the
previous core/frontier solver because unsuccessful witnesses precede cheap
endpoint fallback. Near-uniform input has no admitted candidate and still pays
selection cost. Ratios below one on failed-certificate comparisons do not
establish an algorithmic gain. These are scoped instrumented Python results.

## Remaining failure and experiment history

At n=2048 with selected gaps of weight 2n, the exact closed candidate equals
the global optimum 71,611, but the bound is only 67,586: both witness and exact
refinement fail. With weight n, the closed candidate is actually suboptimal:
61,371 versus the true 59,332. The method must distinguish an insufficient
certificate from an invalid proposed structure.

The first full harness caught a metadata error (Counter.update applied to
list-valued fallback metadata); direct assignment fixed it, then the final
harness was rerun. A completed single-threshold prototype missed several
certifiable heavier thresholds. It was superseded by the bounded portfolio;
all published final results carry the final solver's SHA-256. Raw results are
`results/core_exclusion.json`, `core_exclusion_mixed.json`,
`core_exclusion_scale.json`, and `core_exclusion_matched.json`.

The general subquadratic objective remains open. The next mathematical question
is how to couple the protected and residual lower bounds more tightly, rather
than requiring their independent minima to occur in the same tree. The current
exclusion inequality is valid precisely because it uses a lower bound, but
that independence can leave a large gap even when the proposed core is optimal.
