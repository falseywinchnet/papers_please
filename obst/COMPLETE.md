# A certified shortcut through minimum-path-length shapes

This is an exact shortcut for the full mixed-weight OBST problem. It either
certifies its constructed tree as globally optimal or delegates to an exact
fallback. It does not assume near-uniform weights imply a balanced optimum.
The global problem remains unresolved. Mathematical novelty is unestablished.

## Separate a uniform baseline from residual weights

Let I(T) be the sum of internal-node depths, with root depth0. A binary
tree with n internal nodes has external path length I(T)+2n. Thus if every
key has weight a and every gap has weight b, its cost is

    C_base(T) = (a+b) I(T) + (a+2b)n.

For an arbitrary instance choose a=min(p), b=min(q), and residual weights
p'=p-a, q'=q-b, all nonnegative. Let H(p',q') be the existing order-free
mixed-node Huffman lower bound. For every tree,

    C(T) >= (a+b) I(T) + (a+2b)n + H(p',q').

Let I_min(n) be the smallest possible unweighted internal path length and
let C_complete be the best weighted cost among all trees attaining I_min.
Every other tree has integer I(T)>=I_min+1. Therefore the following is an
exact, directly checkable certificate:

    C_complete <= (a+b)(I_min+1) + (a+2b)n + H(p',q').

When it holds, the best minimum-I tree is globally optimal. Equality is
sufficient; trees outside the class may tie but cannot improve it. When it
fails we make no assertion about the optimum's shape. The a+b=0 case is
also valid, though the baseline then gives no exclusion bonus.

## Optimize the shape class without interval tables

Write h=floor(log2(n+1)), S=2^h, m=S-1, and r=n-m. Every minimum-I tree
contains the complete upper skeleton with m keys, and expands exactly r
of its S external gaps into single-key cherries. The last level need not
be filled from left to right. Any missing shallower slot while a deeper
internal node exists could be filled by moving a deepest internal leaf,
strictly reducing I; this proves the shape characterization. Inorder labels
are reassigned after such a shape argument, so key-order feasibility is
preserved. These are elementary facts about unweighted binary trees.

    I_min(n) = (h-2)2^h + 2 + hr.

Scan the skeleton's gap slots j=0,...,S-1 in inorder. The only state is
(j,e): how many slots were processed, and how many were expanded. The
next input index is i=j+e. There are two transitions:

- Leave the slot external: charge h*q_i, then charge the next skeleton
  key p_i*d_j if this is not the final slot.
- Expand it: charge (h+1)*(p_i+q_i+q_(i+1)), then charge the next skeleton
  key p_(i+1)*d_j if present.

Here d_j=h-v_2(j+1) is the comparison length of skeleton key j, with v_2
the number of trailing zero bits. Feasibility requires that the remaining
slots can achieve exactly r expansions. At stage j the allowed e range is

    max(0, r-(S-j)) <= e <= min(r,j).

Its width is at most 1+s, where s=min(r,S-r). Thus the DP and its stored
backpointers use O(n(1+s)) time and space. The chosen depth sequence is
converted into a labeled tree by a linear Cartesian-tree construction.
The residual lower bound costs O(n log n), including sorting. All scans,
reconstruction, and bound construction are part of the work.

There is also an exact rejection test. Sort key and gap weights separately,
and assign the largest of each type to the shallowest depths of a minimum-I
shape. Let F be this order-free fixed-profile cost on the original weights.
That arrangement is feasible for the residual relaxation, so

    H(p',q') <= F - [(a+b)I_min+(a+2b)n].

Consequently C_complete>F+a+b proves that the certificate cannot succeed;
the fallback can begin without calculating H. This rejects only impossible
certificates, not possible ones. When the test passes, reuse the two sorted
weight lists. The original external weights and newly merged weights form
two sorted queues: all weights are nonnegative, successive internal weights
are nondecreasing, and each newly merged weight is at least the two leaves
it replaces. The sequence of merged weights is therefore nondecreasing.
Two queue heads implement the same Huffman bound with O(n) additional work.
This is a standard sorted-queue optimization, not a novelty claim.

The implementation attempts this route only if s<=bit_length(n), using 1
for the empty-input guard. Consequently a successful route costs O(n log n)
time and space. A skipped or unsuccessful attempt uses an exact fallback.
The total worst-case bound remains quadratic. This is an input-checkable
fast route, not a worst-case subquadratic theorem or a guarantee for all
near-uniform data.

`solve` uses Knuth as its fallback. `hybrid_solve` uses the previous recursive
contraction solver, preserving its benefit on heavy-separator inputs. The
new certificate is attempted only at the whole-instance entry point; the
earlier recursive solver is unchanged.

## Correctness evidence and boundaries

The harness compares minimum-I optimization against all independently
enumerated tree shapes through eight keys on 360 weighted inputs. A further
3,000 full mixed-weight inputs through thirty keys compare both fallback
versions with independent cubic DP and direct tree costs. The unrestricted
certificate succeeds on 768 of those inputs. Tests include zeros, ties,
near-uniform weights, ordinary random weights, and large weight ratios.

The first 1,024-key geometric run hit Python's default recursion limit in
the existing Knuth tree reconstruction. The harness limit was raised to
20,000, as in the existing recursive benchmark, and the full run repeated.
No mismatched cost preceded that harness failure.

On the seeded n=1,024 near-uniform input, with every weight in {999,1000,1001},
the shortcut uses 2,048 shape states, 3,070 transitions, 1,024 reconstructions,
10,511 sorting comparisons, and 1,350 merge comparisons. It certifies cost 19,479,590;
the lower bound for every nonminimum-I tree is 19,480,123. Knuth uses 524,800
interval states and 1,050,139 root candidates on the same input. These are
different work units; the shape-state ratio alone is not a runtime claim.

Every tested near-uniform offset near powers of two through 1,024 certified.
The selected perturbation sweep certified through amplitude8 at n=256,
amplitude4 at n=512, and amplitude1 at n=1,024; these are observations for
the fixed seeded cases, not universal thresholds. Ordinary random inputs
failed the certificate. Sizes384, 768, and 1,000 skip this route because
their shape-state width exceeds the deliberate logarithmic budget.

Exact results are in `results/complete.json`. The matched timing experiment
uses six trials, every ordering of the three solvers, identical inputs,
and direct correctness checks outside timing. It includes preprocessing,
bound construction, and reconstruction. Results are exploratory Python
measurements on one M4 host, not a production or cross-machine benchmark.
On Apple M4 with Python3.9.6, median per-trial hybrid/Knuth time ratios at
n=1,024 were 0.03934 for near-uniform, 0.10478 for heavy separators,
1.05454 for ordinary random, 0.91929 for log-uniform, and 1.03117 for gap
spikes. All six near-uniform cases certified. The n=768 and n=1,000
near-uniform controls skipped the route and had ratios1.17886 and1.04896.
At n=512 the hybrid was about21% slower than recursive contraction alone
on heavy separators, illustrating that even a rejected attempt has a cost.
Small differences in these six-trial timings should not be treated as
stable performance guarantees. Both per-trial times and operation counts
are retained in `results/complete_matched.json`.

The final gate is separately compared with the original heap-based
certificate on every one of the 3,000 correctness inputs: no certificate
is lost, and every computed two-queue bound matches the independent heap
value. This check caught a duplicated candidate-cost metadata update while
the gate was being added; the duplicate was removed and the full run repeated.

## What this changes next

The certificate isolates a measurable obstruction: a failed case has too
little baseline penalty for one extra unit of unweighted path length to
overcome the residual lower-bound gap. A possible extension is to optimize
all shapes with small excess I-I_min and certify exclusion of larger excess.
That extension needs its own representation, proof, and operation counts;
it is not implemented or claimed here. It may enlarge the successful class
without returning immediately to all intervals.

A cheaper preliminary experiment is to vary the subtracted baseline.
Starting with a0=min(p), b0=min(q), replace a=a0-delta, b=b0-delta while
a+b>=0. Residual weights remain nonnegative. The exclusion bound is a
concave function of delta; a minimizing residual tree with path length I
supplies slope 2*(I-I_min-1). This suggests a one-dimensional price search
using the same sorted queues. The optional implementation and exact checks
are now described in BASELINE_PRICES.md. The default remains delta=0 for
reproducibility; `optimize_baseline=True` enables the capped search.
