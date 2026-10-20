# Adaptive coarse-optimal grammars and full original-weight construction

The integer-base certificate allows an exact solver to retain only subproblems
reachable through coarse-optimal roots. Global root ambiguity does not by
itself require a quadratic fine-weight table. This checkpoint supplies the
adaptive construction, its full work bound, and an explicit family with
two distant roots but a linear reachable grammar.

The full arbitrary-weight subquadratic objective remains open. The earlier
uniform family still forces quadratic intervals and cubic root triples.
An incremental expansion budget includes unsuccessful work and protects the
automatic constructor with an exact Knuth fallback.

## Preparation and original-weight refinement

For nonnegative integer base weights a, arbitrary nonnegative original weights
x, scale delta>0, and E=sum|x-delta*a|, the existing certificate

    (n-1) E < delta

implies that every original optimum is a coarse optimum. Its proof uses the
integer coarse cost gap and the comparison-length difference bound n-1.
Signed perturbations, zero coarse weights, and unrestricted ties are allowed.

Starting at [0,n), retain all optimal root rules on each reached interval and
deduplicate their children. Let V be the number of nonempty reached intervals,
A the number of retained root rules, and Q the sum of inclusive root-extreme
range lengths. Then V <= A <= Q.

The existing Monge construction and one additional unrestricted closure
product in each orientation provide minimum and maximum optimal roots.
The extra closure is essential: a sufficient height preserves some optimum
but may omit other unrestricted tied trees.

Index the final condensed cost matrix with one persistent column-sum tree per
core-row prefix. Each insertion and each entry query costs O(log(n+1)).
For each reached interval test every root between its extremes using

    C*(i,r) + C*(r+1,j) + Wbar(i,j) = C*(i,j).

There can be holes between optimal roots. Failed tests count in Q.
With aggregate coarse-core parameter Sbar, total preparation is

    O((Sbar + V + Q) log(n+1)).

A balanced dictionary gives the deterministic comparison bound during
preparation. The Python implementation uses dictionaries and counts their
explicit accesses as events; no claim equates those events with machine
instructions. Integer-length buckets order states in O(n+V), and compilation
replaces child endpoints by array indices. All preparation matrices, witnesses
and the cost index can then be released.

For each certified fine input, evaluate the ordinary root recurrence only on
retained rules, using original key weights and both endpoint gaps. The grammar
contains precisely all coarse-optimal trees, hence contains every fine
optimum. Array evaluation, certification and full traceback take

    O(n + V + A)

arithmetic work and storage. No query-time dictionary is needed. Retained
preparation data have the same space bound. Ordinary witness maps and the
persistent index use O(Sbar log(n+1)+n+V+A) peak preparation storage.

The automatic route tests the existing sixteen scales X/m. Every accepted
base has mass O(n). Extraction has a budget of 4*n*ceil(log2(n+1)) charges
for processed states, scanned candidate roots and retained rules, checked
before each charge. Each retained rule schedules at most two children.
Successful complete construction is subquadratic:

    O(n^(3/2) log^(3/2)(n+1) + n log^2(n+1)).

Rejection or budget exhaustion uses full Knuth, retaining all failed work in
the counters and giving O(n^2) worst-case work. A supplied base of unrestricted
mass retains the explicit Sbar term. These are arithmetic/comparison bounds;
operand bit costs are additional.

## A proved linear grammar despite full-interval ambiguity

Let m=2^k, k>=1, n=3m-1, a=m-1, c=2m-1. Every coarse key and gap has weight
one, except keys a,c have weight two. Total mass is 2n+3.

With unit mixed weights, cost is 2I+3n. Minimum-IPL shapes fill a perfect
(2m-1)-key upper skeleton and expand exactly m of its 2m bottom gaps.
The two additional key units contribute at least three to any full tree.
Both endpoint-root shapes attain three. An intermediate root contributes at
least four; a larger-IPL tree already loses on the baseline and cannot do
better than three on the added units.

Consequently there are exactly two coarse optima:

    T_a = a(P0, c(P1, P2))
    T_c = c(a(P0, P1), P2),

where P0,P1,P2 are the perfect (m-1)-key trees on the three intervening
intervals. The common-root partition stops at the full interval and retains
one size-n quadratic payload. The reachable grammar instead has exactly

    V = n+1, A = n+2, Q = 4m.

Proof: the three common perfect subtrees contribute 3(m-1) states, and the
full interval plus the two different (2m-1)-key intervals contribute three.
Every proper interval is unique, since an alternative would create a third
full optimum. Only the full interval has two rules. It scans m+1 candidate
roots; the other 3m-1 states scan one each.

Generic preparation therefore permits O(n) fine queries. Recognizing this
particular base also permits O(n) *total* construction without any Monge
preparation. Its exact choice formula is

    C_x(T_a)-C_x(T_c) = p_c + W_x(c+1,n) - p_a - W_x(0,a).

The middle subtree does not move in depth, while the marked keys and outer
subtrees each change depth by one. Check the same finite certificate, compare
the two mass sums, and write the selected tree. Original errors may differ at
every key and every gap. `two_tree_refine` implements this direct route.

## Verification and retained failures

`coarse_grammar_audit.py` establishes the family with independent all-root
recurrences before importing the new constructor. It checks:

- Five complete dense family references and two literal family enumerations.
- 2,869 independent condensed-matrix entry-index comparisons.
- 96 entire reachable grammars, including unrestricted zero-weight ties.
- 56 literal-family checks, evaluating 5,000 tree costs.
- 288 signed rational fine inputs sharing those preparations.
- 96 immediate budget-exhaustion controls and the known optimal-root hole.
- Seven two-tree sizes through n=383, with 21 complete generic and direct
  rational queries, fourteen deterministic endpoint-root exposures, and seven
  direct-constructor certificate rejections.
- Independent full Knuth references through n=191 for that family, plus six
  unstructured fine queries at n=32,64,128 and four automatic accepted solves.
- Dense uniform grammar controls: n=11 completes; n=23,47,95 exhaust the
  default budget and still return exact original-weight optima.

The largest two-tree row uses its proved classification and complete original
cost traversal, not an independent large Knuth reference. Source-hashed JSON
retains fine inputs, exact scales, reference scopes and preparation/query
counters separately. Large preparation constants are visible: at n=383,
preparation has 15,476,304 core visits and 32,590 index nodes. Each generic
query evaluates 384 states and 385 roots. These counters do not establish
a practical speedup.

The exchange probe is preserved separately. On nine keys, expand bottom
gaps 6,7 of the perfect seven-key skeleton. With residual key weights
(2,5,4,4,5,2,0,4,4) and gaps (3,4,4,6,8,7,1,1,7,2), the selected tree has
error cost 219, all fourteen coarse-preserving neighbors under descendant
promotion or one bottom-gap swap cost at least 224, and the optimum is 212.
Adding D>584 to every outcome supplies a positive full mixed instance.
Every promotion leaving the coarse family also loses by the certificate.
The full 4,862-tree enumeration and independent Knuth control at D=585
verify the trap. It is a local-move obstruction, not an OBST lower bound.

This construction combines the already proved integer-base certificate and
published condensed-Monge witness primitive with standard evaluation of an
acyclic optimal-choice graph. It makes no priority claim for perturbation
arguments or dynamic programming over such graphs.

Reproduction commands are in the repository-root `AGENTS.md`; the authoritative
sources are `code/coarse_grammar.py`, `code/coarse_grammar_audit.py`, and
`code/coarse_exchange_control.py`. Results are in the correspondingly named
JSON files under `results/`.
