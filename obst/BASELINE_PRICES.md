# Optimizing the uniform baseline in the shape certificate

This extends COMPLETE.md without changing its shape class or fallback.
All original key and gap weights remain nonnegative. A sampled price can
certify global optimality; failure to certify retains the exact fallback.
The general quadratic barrier and mathematical priority remain unresolved.

## The baseline need not be the largest subtractable one

Set a0=min(p), b0=min(q), and let delta be an integer in
0..floor((a0+b0)/2). Use a=a0-delta and b=b0-delta. The residual weights
p-a and q-b remain nonnegative, and a+b>=0. One of a or b may be negative;
that is harmless because these are algebraic baseline terms, not input
probabilities. The coefficient of I in the exclusion argument is nonnegative.

Let I_* be the minimum unweighted internal path length and H_delta the
order-free optimum on those residual weights. Every tree with I>=I_*+1
has full cost at least

    B(delta) = (a0+b0-2delta)(I_*+1)
               + (a0+2b0-3delta)n + H_delta.

Thus the minimum-I candidate is globally optimal whenever its cost is at
most B(delta), for ANY allowed delta. The earlier certificate uses delta0.

For a fixed residual tree with path length I, increasing delta adds one
unit to every key and gap weight, changing its residual cost at rate
2I+3n. Accordingly B is the pointwise minimum of affine functions with
slopes 2(I-I_*-1): it is concave. A minimizing residual tree supplies a
supergradient g=2(I-I_*-1), meaning

    B(x) <= B(delta) + g*(x-delta).

If g>0, no smaller integer price can beat the current value; if g<0,
no larger price can beat it. If g=0, the sampled value is a global maximum.
Binary interval elimination, retaining the best sampled value, therefore
finds the integer maximum if run until its interval is exhausted.
We make no claim here to maximize over real-valued prices.

## Obtain the slope in the same linear oracle

Give every original outcome secondary weight1. Store a queue item as
(residual mass, number of original outcomes), and compare lexicographically.
An original external node has secondary weight1; merging two items under
an internal key adds one more. Sum both merge coordinates. The first is
the residual optimum. The second is 2I+3n, so it yields I exactly.

The same exchange proof as the mixed-node Huffman relaxation applies to
lexicographic weights (equivalently, an arbitrarily small positive common
perturbation on the finite set of shapes). Among minimum-cost residual
trees this chooses one with minimum I. Original weights are sorted once;
adding the common delta does not change their order. Nonnegative residual
masses and increasing internal weights keep merged items sorted, permitting
two queues and O(n) additional work per sampled price.

The original fixed-profile rejection test remains valid for the entire
search. If F is the freely permuted minimum-I profile cost on original
weights, then B(delta)<=F+a0+b0-2delta. Hence a candidate exceeding
F+a0+b0 cannot be rescued by ANY price in this family. Most failed
ordinary-random cases are rejected here without extra oracle calls.

## Production budget and fallback

The implementation first tries the existing delta0 certificate. Only if
it fails after passing the fixed-profile gate does it search positive
prices. It allows at most bit_length(n) additional linear oracle calls
and stops immediately on a successful certificate. Retaining the old
bound ensures that no previously certified input is lost.

With the existing logarithmic shape-width budget, this preserves
O(n log n) work and space for the attempted shortcut. If the call cap is
reached, the best sampled price remains valid but the search need not
have reached the integer maximum. The result metadata distinguishes
maximum-search completion from early certificate success. If no sampled
price certifies the tree, the exact fallback runs as before.

Use `complete.hybrid_solve(p,q,optimize_baseline=True)` for the combined
solver, or the same flag on `complete.solve` for a direct Knuth fallback.
The default remains False to preserve reproduction of earlier results.

## Exact checks

- 400 lexicographic oracle comparisons against independent enumeration of
  shape/depth profiles through eight keys, including ties and zero weights.
- 1,200 uncapped integer price searches compared with exhaustive evaluation
  of every allowed integer price.
- 3,000 full mixed-weight inputs through thirty keys checked against
  independent cubic DP and direct tree costs; 87 previously unsuccessful
  unrestricted certificates were recovered. Every earlier certificate was
  preserved, and both capped fallback versions matched the oracle.

The separate seeded size/perturbation sweep recovers the n=1,024,
amplitude2 instance with two extra oracle calls, and the n=2,048,
amplitude1 instance with three. Larger tested perturbations generally
exceed the fixed-profile ceiling and cannot benefit from this search.
The exact results and operation counts are in `results/baseline_prices.json`.

For the seeded 2,048-key amplitude1 case, the candidate cost is 43,032,446.
The fixed-baseline exclusion bound is 43,031,347 and cannot certify it.
The third additional price, delta125, raises the bound to 43,032,459,
which certifies the candidate. The shape DP uses 4,096 states and 6,142
transitions; sorting uses 20,784 comparisons. The original merge pass
uses 2,752 comparisons, and the three extra passes use 6,141 pair
comparisons and 6,144 contractions. Knuth uses 2,098,176 interval states
and 4,198,710 root candidates on the same input.

## Matched timing and controls

Six trials per fixture use every ordering of Knuth, the fixed-baseline
hybrid, and the price-search hybrid on identical inputs. The Apple M4 /
Python3.9.6 experiment includes all sorting, reconstruction, and price
work. Every output is checked for equal optimum and direct tree cost.

| Fixture | Median priced/Knuth time | Newly certified trials |
| --- | ---: | ---: |
| n=1,024, amplitude2 | 0.04953 | 6/6 |
| n=2,048, amplitude1 | 0.06128 | 6/6 |
| n=2,048, amplitude2 | 0.99391 | 0/6 |
| n=1,024, ordinary random | 1.06492 | 0/6 |
| n=1,024, gap spike | 1.12941 | 0/6 |
| n=768, near-uniform | 1.03472 | 0/6 |

The n=1,024 amplitude1 control already certified at delta0 and performs
no extra oracle calls. Nevertheless its median priced/unpriced time ratio
was1.13564, illustrating measurement variability despite matching
algorithmic work. These are exploratory six-trial timings, not a precise
estimate of small overheads or a broad performance guarantee. All raw
observations and counts are retained in `results/baseline_matched.json`.

This is a standard concave-price optimization applied to the new certificate,
not a claim to have invented Lagrangian optimization. It enlarges the
observed successful class but does not establish a general subquadratic
algorithm or a guarantee for all near-uniform inputs.

The next experiment should test an order-sensitive residual lower bound
inside the same exclusion certificate. The existing ordered depth-chain
bound is valid for this purpose even when it is not exact: the uniform
baseline supplies a positive exclusion margin. That combination is not
implemented in this checkpoint, and its extra work must be counted.

Follow-up: EXCESS.md records the ordered-residual experiment and its negative
result at the tested budget. The investigation then implemented a dyadic DP
for bounded excess path length, with an expanded exclusion certificate.
