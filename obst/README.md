# Full optimal binary search trees: research checkpoint

Research and exposition by OpenAI Codex Sydney, with sponsorship and problem
selection by Joshuah Rainstar. The general research objective is ongoing.

- [Manuscript (PDF)](manuscript/main.pdf)
- [Manuscript (TeX)](manuscript/main.tex)
- [Research record and prior-work map](RESEARCH.md)
- [Expanded mass, tiling, and primitive audit](CORE_SIZE_AUDIT.md)
- [Linear-mass odd-ramp core lower bound](RAMP_CORE_TIGHTNESS.md)
- [Per-outcome charging and the aggregate core bound](AGGREGATE_CORES.md)
- [Single-weight obstruction to constant tile charging](LOCAL_TILE_OBSTRUCTION.md)
- [Full mixed ruler slots and capacity-deficit construction](MIXED_SLOTS.md)
- [Exact gap-core mass and sharp binary leading term](GAP_CORE_IDENTITY.md)
- [Full mixed boundary mass and the bounded-positive obstruction](MIXED_BOUNDARY_MASS.md)
- [Exact computation of all capacity-band intervals](CAPACITY_BANDS.md)
- [Necessary tail terms and targeted adversarial diagnostics](CORE_TAIL_EXTREMES.md)
- [Capacity densities, sharp interaction allowance, and wider-band obstruction](CAPACITY_INTERACTION.md)
- [Explicit two-key disproof of logarithmic interaction allowances](SPARSE_INTERACTION_BARRIER.md)
- [Coupled rank-reward stability and periodic clipping obstruction](RANK_REWARD_STABILITY.md)
- [Exact full-ruler tail and sharp clipping scale](RULER_CLIPPING_SHARPNESS.md)
- [Alternating-tail matching bound and exact growing-width families](ALTERNATING_TAIL_BOUND.md)
- [Rank-weighted repair certificates and tie-independent barriers](RANK_REPAIR_BARRIER.md)
- [Exact weighted cluster tails and pointwise-sensitivity obstruction](WEIGHTED_CLUSTER_TAIL.md)
- [Nested threshold-tail obstruction](NESTED_TAIL_OBSTRUCTION.md)
- [Single-key square bound and the open boundary-plus-mass target](BOUNDARY_TILE_TARGET.md)
- [Unit-outcome support envelope and the surviving two-key interaction](UNIT_SUPPORT_ENVELOPE.md)
- [Exact binary-block dilation and the replication barrier](BINARY_DILATION.md)
- [Linear one-block core construction and local boundary charge](PLATEAU_CORE.md)
- [Complete two-block above-capacity cores and a finite band factorization](TWO_BLOCK_CORES.md)
- [Unimodal above-capacity cores and certified spans in arbitrary inputs](UNIMODAL_ENVELOPE.md)
- [Valley interval queries and quadratic original-coordinate cores](VALLEY_QUERIES.md)
- [Individual-weight charges and all above-capacity valley cores](VALLEY_CORE_MASS.md)
- [Exact full mixed construction by periodic phase](PERIODIC_OBST.md)
- [Arbitrary fringes around a periodic middle](FRINGE_OBST.md)
- [Positive affine translation and finite phase construction](AFFINE_PERIOD_OBST.md)
- [Arbitrary-key rank transfers and exact dense-core barriers](RANK_TRANSFER_BARRIER.md)
- [Incompatible binary rank-threshold optimizers](RANK_THRESHOLD_OBSTRUCTION.md)
- [Contraction argument](CONTRACTION.md)
- [Minimum-path-length shape certificate](COMPLETE.md)
- [Concave baseline-price extension](BASELINE_PRICES.md)
- [Bounded-excess dyadic construction](EXCESS.md)
- [Split-height construction and taller-tree certificate](SPLIT_HEIGHT.md)
- [Exact variable mass frontier and uniform-width comparison](MASS_FRONTIER.md)
- [Dominant-gap separators and local mass frontiers](GAP_SEPARATOR.md)
- [Joint heavy-outcome cores and protected-height certificate](HEAVY_CORE.md)
- [Residual-cost core exclusion and linear-weight family](CORE_EXCLUSION.md)
- [Coupled two-gap skeletons and arbitrary nonuniform key placements](PAIR_SKELETON.md)
- [Terminal-penalty layers and core-sparse Monge reduction](MONGE_PENALTY.md)
- [Centered core bounds for large integer baselines](CENTERED_MONGE.md)
- [Ruler-pattern identities, dense-core barrier, and exchange shortcut](RULER_REPRESENTATION.md)
- [Affine-regret corridors and arbitrary signed perturbations](RAMP_CORRIDOR.md)
- [Joint key/gap signature transfers and linear-space reconstruction](RUN_SHAPES.md)
- [Global alternating-gap bound and linear full construction](GAP_PARITY.md)
- [Interlaced parity intervals for key-profile attainment](PROFILE_INTERVALS.md)
- [Arbitrary-gap threshold bound and linear Cartesian certificate](THRESHOLD_CERTIFICATE.md)
- [Shifted alphabetic certificate beyond key-capacity equality](SHIFTED_ALPHABETIC.md)
- [Exact endpoint prices and the complete additive-transfer obstruction](ENDPOINT_PRICES.md)
- [Root/nonroot coupling beyond the entire transfer class](ROOT_PARTITION.md)
- [Joint-profile coupling and strict compatible-merge obstruction](JOINT_MERGE_OBSTRUCTION.md)
- [Endpoint-response insufficiency, facet bounds, and exact factorization](BOUNDARY_RESPONSE.md)
- [Legal-domain collision and exact signed-response recovery](SIGNED_BOUNDARY_RECOVERY.md)
- [Relaxation, counterexamples, and failed sparse search](RELAXATION.md)
- [Depth-sequence dual and exact tail compression](DEPTH_DUAL.md)
- [Exact depth ordering and arbitrary-window obstruction](DEPTH_ORDER.md)

## Main result and the size bounds

The boundary-interface analysis now separates [legal endpoint assignments
from signed responses](SIGNED_BOUNDARY_RECOVERY.md). Two strictly positive
four-key inputs have identical responses for every nonnegative reassignment
of their endpoint gaps, but the same surrounding context has optima 101 and
100. Conversely, the complete endpoint-depth profile determines every gap
when the keys, total mass, and left gap are known. For integer weights,
a bounded signed-response line permits recovery in at most n exact
value-only queries, without minimizer witnesses. This establishes which
information survives; a fast general composition algorithm remains open.

The phase quotient now supports [positive affine translation](AFFINE_PERIOD_OBST.md):
p_(i+b)=lambda p_i+alpha and q_(j+b)=lambda q_j-alpha, with lambda>0.
Every tree's translated cost is lambda times its old cost minus alpha times
its number of keys. This preserves every optimal shape and gives O(nb)
full construction, including exact recognition of the smallest admissible b.
The proof uses only finite nonnegative input intervals; the last b-1 lengths
are handled directly. Geometric mixed weights and opposing arithmetic drifts
are included. For b=1, exactly 2n-1 root candidates suffice. The general
nonperiodic worst case remains quadratic.

A periodic middle of length m and period b now tolerates d=n-m arbitrary
fringe keys in [O(mb+nd) full construction](FRINGE_OBST.md). Each boundary
extension reduces exactly to Wilber's linear concave least-weight-subsequence
algorithm. The number of added nonempty states is exactly dm+d(d+1)/2;
no mass or height restriction is used. Automatic recognition scans small
periods and selects between a middle extension and the whole-period route.
The largest complete constructions reach 65537 keys with arbitrary large
boundary weights. Independent quadratic optimality controls have a separate
scope; all work bounds follow from the proof. Interior defects and the
general nonperiodic objective remain open.

A joint key/gap period b now gives an [exact full-tree construction in
O(nb) work](PERIODIC_OBST.md), with arbitrary nonnegative real weights.
Intervals are represented by starting phase and length. Knuth root ranges
cancel around the complete phase cycle: exactly 2b candidates per length
after the first, hence b(2n-1) overall. Linear period recognition includes
the terminal gap; iterative reconstruction emits every key and gap. The
method is linear for fixed period and remains quadratic on arbitrary inputs
whose shortest common period is linear in n. The independent audit includes
all synthetic phases and complete constructions through 262144 keys.

Valley cores now have a [direct integer-weight charge and a sparse
constructor](VALLEY_CORE_MASS.md). With integer key mass P, each layer has
at most P above-capacity entries, and each rectangle has at most the smaller
of its row-endpoint and column-endpoint key masses. All such cores across
all layers are constructed in O((n+P) log^2(n+1)) work. The ruler support
is contained in the support of the sum of the c largest keys; each row of
the latter telescopes to at most its endpoint key weight. An explicit
event jump handles repeated weights without scanning zero cells.

The local mass dependence is tight within a factor of six on the proved
dense valley family. The top-c support inclusion itself fails on a nine-key
two-peak binary word, whose original density is one while the auxiliary
density is zero. The general local target and mixed below-capacity region
remain open; the valley result supplies the individual-weight charging
mechanism on a class that can have dense cores at larger mass.

Valley key weights now have an [exact implicit above-capacity query
representation](VALLEY_QUERIES.md): O(n log(n+1)) preprocessing and storage,
with O(log(n+1)) interval queries and two-block witnesses, for arbitrary
nonnegative gaps. A single selection of the largest end keys componentwise
dominates every subsequence of the same length. Ruler-prefix queries then
evaluate its reward without scanning the selected keys.

A valley can nevertheless have a quadratic core in the original interval
coordinates. An explicit permutation of weights 1,...,n gives exactly s^2/2
positive densities on a side-s square, with n=4s, and an exact ruler formula.
Normalizing by n preserves that support at rational total mass (n+1)/2;
the integer-mass hypothesis therefore cannot be replaced by normalized real
mass. The square's densities also have a logarithmic modular-pattern
description. This is a barrier to explicit-core sparsity, while the query
representation remains compact; the full mixed BST objective is ongoing.

All above-capacity cores for **arbitrary unimodal key weights** now have an
[O(n log(n+1)) total constructor](UNIMODAL_ENVELOPE.md), including unequal
real weights, arbitrary nonnegative gaps and every endpoint cut. Each layer
has at most max(0,n-c-1) entries, and every above-capacity side-s square has
at most 2s-1. Every subsequence of a unimodal weight sequence is componentwise
dominated by a contiguous block. The original scores therefore become range
maxima of ruler-weighted windows, constructed for every layer by a dyadic
recurrence. The leading global support coefficient one is sharp.

The same window envelope is useful on arbitrary key inputs. A linear scan
supports constant-time interval-unimodality tests, and filtering its sparse
cores recovers every original density with a unimodal outer span. It also
certifies the 2s-1 local bound for those tiles. The remaining nonnegative
value correction has both density signs, already on two small binary words;
concatenating them gives one input with both signs. The below-capacity mixed
region and interactions across uncertified spans remain open.

The finite-product method now has an [exact arbitrary-key rank-transfer
representation](RANK_TRANSFER_BARRIER.md). A constant-weight run is a band
matrix with a ruler potential; a balanced product preserves every feasible
weighted subsequence optimum with polynomial dependence on the run count.
This extension also has a proved limitation: increasing weights 1,...,2s
give s floor(s/2) positive densities in one side-s transfer square. A second
family makes all s^2 cells positive using only width-one bands and arbitrary
unary rewards. Both are explicit density formulas. These transfer-coordinate
barriers leave the original interval-core bound and its open local target
unchanged; they show where additional ruler and weight structure is needed.

The complete above-capacity core for **two equal positive key blocks** now
has a [linear support bound and an O(n log(n+1)) constructor](TWO_BLOCK_CORES.md),
including every positive-endpoint cut and arbitrary nonnegative gap weights.
The global bound is 28n; every side-s square strictly above capacity has at
most 40s entries, independently of the common positive weight. Whole-block
interactions factor through three explicit finite Monge matrices. Grouping
only the boundary rows and columns gives a local side charge; single cuts
reduce to visibility pairs, and double cuts contribute on two diagonals.
The conservative constants come from the proof. The general mixed-weight
core bound remains unchanged.

One constant positive key block now has a [linear above-capacity core
constructor](PLATEAU_CORE.md), with arbitrary nonnegative gap weights.
At capacity c=2^h-1, a block of m keys has at most max(0,c-m-1) positive
densities there, and any side-s square has at most 2s-1. Its ruler rewards
are m+s_2(r)-s_2(r+m); range-max densities become noncrossing horizontal
visibility pairs. A monotone stack constructs their coordinates and values
in O(n) work and space. The global leading coefficient one is sharp.
The paper credits the known visibility geometry and proves the exact
OBST reduction, including partial-block endpoints.

A separate [explicit binary family](RANK_THRESHOLD_OBSTRUCTION.md) shows
why ruler levels cannot simply be optimized independently. At n=2^h and
capacity n-1, its full ruler reward is h-1 while the sum of separately
optimized rank thresholds is 2h-3. Their ratio tends to two. This is a
reward-compatibility obstruction; it leaves the main construction bound
and the general local support hypothesis unchanged.

Aligned replication has an exact [binary-block reduction](BINARY_DILATION.md).
For complete positive blocks of length d=2^ell above capacity, the ruler
score is the rounded-endpoint coarse score plus m(d-1), provided the
number m of positive blocks does not exceed coarse capacity. On rectangles
with a fixed set of positive blocks, every coarse density moves to exactly
one fine cell. Core cardinality and density mass stay unchanged; arbitrary
gap weights cancel there. Thus this replication cannot amplify the local
support ratio. The proof includes compatible phase choices and explicit
counterexamples to dropping either restriction.

An exact single-gap density classification now complements the single-key
classification. Together they put every possible unit-outcome support inside
an explicit envelope occupying at most 2s cells in any dyadically aligned
side-s square off capacity; the coefficient two is sharp for their union.
Removing that entire envelope still does not give a constant-per-weight
charge: two unit keys have at least log2(s)-2 explicit density-one cells
outside it in one maximal tile. Both conclusions have closed-form proofs in
[the unit-support note](UNIT_SUPPORT_ENVELOPE.md). The open bound
K(T)=O(s+W(J_T)) and the main construction theorem remain unchanged.

The paper now leads with the exact core-sparse Monge construction for arbitrary
nonnegative integer weights on keys and gaps. At total mass W=O(n), its bound is
O(n^(3/2) log^(3/2)(n+1)) arithmetic operations, including full reconstruction.
The sparse product and succinct witnesses are the published ESA 2025 algorithms
of Gawrychowski, Gorbachev, and Kociumaka.

All intervals within width d of every capacity boundary can now be computed
exactly in O(n(d+1)H) work, with minimizing roots and complete reconstruction
for retained fully exposed intervals. At H=O(log n), width one gives every
capacity-line density in O(n log n) work for arbitrary mixed weights. See
[the band construction](CAPACITY_BANDS.md). The separate
[tail investigation](CORE_TAIL_EXTREMES.md) proves that both proposed tail
terms are necessary; its general upper estimate remains open.

The capacity density also has an exact two-maximum formula. It proves a
sharp (h-1)P allowance for the interaction in total off-capacity mass, where
P is key mass. An explicit alternating family attains the leading constant;
a four-key gap example prevents the same argument from covering wider bands.
See [the interaction theorem](CAPACITY_INTERACTION.md). A later
[two-key family](SPARSE_INTERACTION_BARRIER.md) disproves every all-width
additive O(hW) allowance over the unit-input tails. Its interaction grows
like the leading c/d term, so that term must cover joint optimization as well.

A rank-coordinate stability theorem now controls joint optimization above
capacity: increasing one skeleton reward by Delta raises any upper tail by
at most P Delta. Clipping the ruler rewards at level t therefore costs at
most P(2^(h-t)-(h-t)-1), which is O(Pc/d) for t near log2 d. The remaining
periodic template needs capacity-dependent control: its alternating 0,1 version has
an explicit two-key family with tail 2^(h-1)-4 at width two. See
[the stability proof and periodic obstruction](RANK_REWARD_STABILITY.md).
An [exact full-ruler family](RULER_CLIPPING_SHARPNESS.md) now proves the
clipping error has the necessary order: for d=2^a, Q=2^b, C=dQ, and two
unit keys at C-3d,C, the full tail is 5Q/4-3b+2 while the level-a clipped
tail is zero. Its ratio to the proved allowance tends to 5/8. A separate
sparse periodic template disproves every general bound based only on
P(max v+sum v/d). These are density-mass results; the support-size gap
and the main complexity theorem remain unchanged.
Expanded sparse and repeated-cluster searches retain the broader mixed
tail estimate as an open target.

The alternating clipped template now has a proved width-sensitive bound
for arbitrary nonnegative real key weights:
U_d <= P min((c-1)/2, 2+(c-3)/d). Its fixed-cardinality path-matching
representation provides d explicit repairs after an endpoint deletion;
their disjoint matched-edge costs give the 1/d factor. Both P and Pc/d
are necessary. K unit keys at spacing three have an exact tail near c/2
at d=K, including K near sqrt(c). See
[the matching proof and sharp scales](ALTERNATING_TAIL_BOUND.md).
Higher clipped levels change rewards on retained matching edges. The exact
accounting now gives a [tie-independent repair barrier](RANK_REPAIR_BARRIER.md):
with one unit key, the true tail is zero but even the best one-augmentation
certificate equals (h-2)(h-3)/2, against target scale h. At one endpoint,
an optimum requires 2^(h-3) augmenting components and one fewer decreasing
components. This route needs joint rank changes; the actual tail target
remains open.

The spacing-three family now has an exact formula for arbitrary nonnegative
cluster weights: U_K=(ceil((C-3(K-1))/2)-1) min_r w_r. Equal weights maximize
the tail at fixed cluster mass. A unique minimum can have an individual
sensitivity far above h+C/d, even at W=n, while the aggregate bound remains
valid. The next charge must accommodate groups of interacting weights.
See [the weighted formula and exact sensitivity proof](WEIGHTED_CLUSTER_TAIL.md).

A ten-key full-ruler counterexample has positive weighted upper tail while
both binary threshold tails vanish, so a constant-factor threshold transfer
cannot supply the missing charge. A more direct core-size target is the open
local bound K(T)=O(side(T)+W(span(T))). It would imply aggregate core size
O(n^(3/2)) at W=O(n), removing the remaining sqrt(log n) factor. The proved
one-key special case is stronger: every side-s square off capacity contains
at most 1+floor(log2 s) positive densities, with sharp leading logarithmic
scale. See [the threshold obstruction](NESTED_TAIL_OBSTRUCTION.md) and
[the local target and conditional summation](BOUNDARY_TILE_TARGET.md).
The general local hypothesis remains unproved.

The sharper time bound charges each individual outcome weight to covering
tiles and sums their geometrically spaced layer boundaries. It proves total
core size O(n^(3/2) sqrt(log(n+1))) at linear mass, saving one logarithmic
factor in construction time. See [the aggregate proof](AGGREGATE_CORES.md).
The independent audit checks 290 mixed inputs and 1,891,752 geometric
position/scale incidences, including non-power-of-two sizes.

An explicit new family attacks the intermediate size bound. Put n=m^2, where
m is a power of two at least 32, and put weights 1,3,...,2m-1 on a centered
block of m keys, with every other key and gap weight zero. Its mass is exactly
W=n. One layer has at least nm/16-9n/64-m/4 >= n^(3/2)/32 positive densities.
Their formula is 2 nu_2(b-2s) on an explicitly counted band. A perfect-slot
embedding and rightmost-zero deletion lemma prove the formula. This excludes
a uniform n polylog n bound on these explicit cores. The sqrt(log n) gap in
the upper core bound remains; this is not a general OBST complexity lower bound.

A separate control theorem settles fixed-mass binary gap inputs: for n=2^s
and W=n/2, their largest completed core over every input and layer lies between
sn/2+1 and (s+1)n/2+4. An exact telescoping identity proves the upper bound;
an explicit alternating family has unit densities on specified ruler diagonals
and proves the lower bound. Thus this maximum is (1/2)n log2 n+O(n), whereas
the odd-ramp key family has Omega(n^(3/2)) support. This distinguishes the
gap-only control from the full mixed objective. See [the proof](GAP_CORE_IDENTITY.md).
The 84 binary searches are diagnostic; only the proved gap bounds support an
asymptotic claim.

The search preceding that proof evaluates 145,155 fixed-mass candidates over
72 starts, plus 120 explicit patterns through 4096 keys. The proof audit checks
42,748 deletion formulas, 17,688 densities against independent subsequence DP,
and every one of the 1,896 proved cells at n=1024 against the original layer.
All counts and exact source hashes are recorded. No asymptotic result is
inferred from the search measurements.

The manuscript now gives the straight and bent rotation depth changes in full,
a boundary-counting lemma for arbitrary n, and the published product theorem's
exact statement and interface. It states one certificate pattern, groups its
family corollaries, consolidates negative results, and puts verification in
appendices. Python timing passages have been removed from the paper; historical
raw records remain in the repository. The title asterisk refers to the sponsor's
verbatim dedication at the end. The bundled Hebrew font includes its OFL license.

A further exact family identifies a limit of local charging. With just one
unit-weight key and n=2^(h+1), one accepted tile has h-3 nonzero densities,
each equal to one. The entire completed layer nevertheless has exactly
2n+2^h-2h-1 entries, and every one-key input has at most 3n entries per
layer. Thus the height factor cannot simply be dropped from individual tile
charges; a stronger global charging argument remains possible. The formula
audit checks every interval and density through 1024 keys, with additional
all-position one-key controls. See [the proof](LOCAL_TILE_OBSTRUCTION.md).

The full mixed objective also has an exact ruler-slot representation, with
adjacent-gap rewards given by minima of neighboring slot valuations. For a
prescribed height h and capacity deficit r=2^h-1-n>=0, a new implementation
constructs the exact height-limited optimum in O(n(r+1)) arithmetic operations,
including conversion from arbitrary selected slots to a valid tree. The
operation bound is independent of weight amplitudes. Above the terminal
layer's capacity, gap weights contribute only an additive term, so ordinary
densities there depend only on key weights. See [the representation and
proof](MIXED_SLOTS.md). The unrestricted height choice remains part of the
full problem; the existing Monge construction bound is unchanged.

## Earlier certificate results

The latest certificate partitions trees according to whether the largest
residual key is the root. The root case forces an alphabetic split at that
key's position; the nonroot case pays the extra capacity cost of putting a
lighter key at the root. At most three alphabetic constructions, one key sort,
and linear scans give a complete O(n log n)-work, O(n)-space certificate.
Original mixed weights remain the objective and rejection uses Knuth.
See [the case-partition proof and separation family](ROOT_PARTITION.md).

It closes the preceding four-key transfer obstruction and certifies an infinite
positive family that defeats **every** admissible additive reweighting of the
old separable K+A bound. At 262,143 keys, the family has 262,141 distinct key
weights and 262,144 distinct gap weights. Its full optimum is 92,530,765,201,355;
the preceding class's maximum is 91,912,294,498,251, a gap of 618,470,703,104.
The new construction uses three alphabetic calls and no interval-DP cells.

The independent harness checks 246,480 literal conditioned inequalities on
840 mixed instances. All 1,040 full solves match cubic/Knuth/direct costs,
including 720 literal controls. The route certifies 505 (240 are tiny base
cases) and falls back on 535. It exceeds the completed transfer maximum on
84 cases and rescues 11 price rejections, while losing 47 price certificates.
The fixed endpoint choice does not replace full price optimization.

The 88-trial benchmark retains 352 complete constructions. At 511 keys,
median paired new/Knuth ratios are 0.25899 on the new family, 1.21721 random,
1.31079 near-uniform, and 1.18771 geometric. Old specialized routes can be
much faster: profile, four-signature, and affine cases cost 15.47, 51.74,
and 43.04 times the previous portfolio. The M4 load and four same-process
observations per case limit timing precision. All regressions remain.

A separate one-key marked-merge probe matches 17,769 finite controls but
remains an unproved candidate family, with invalid reconstructions rejected.
Greedy activation fails on a strict positive example, and the activation
objective is not unimodal. The proved certificate does not rely on this probe.

The preceding endpoint-price certificate optimizes two endpoint prices after a
maximal interior shift. A rotation argument proves that these three
parameters exhaust all additive outcome-weight changes preserving relative
tree costs; a monotonicity argument removes the interior parameter from
the maximization. Exact supporting planes and rational LP vertices search
the remaining two-dimensional box. A logarithmic call budget keeps full
screening and candidate construction within O(n log^2 n) arithmetic work,
with O(n) space; rejection still uses Knuth. The finite uncapped optimizer
has no proved small iteration bound. See [the full proof](ENDPOINT_PRICES.md).

The new positive family has 262,143 keys, 262,142 distinct key weights,
262,144 distinct gap weights, and exact full cost 4,569,830,391,807.
One alphabetic call constructs the entire tree without interval-DP cells
or LP vertices. The previous shifted bound is lower by 8,590,000,165.
The family's O(n log n) proof includes all original mixed weights.

The approach has a sharp limitation: p=(1,1,2,1), q=(1,2,1,1,1) has full
optimum 24, but every nonnegative cost-preserving additive reweighting gives
K+A at most 23. The failure persists on an open box and with all nine
weights distinct. It is a barrier to this separable certificate class,
not to general subquadratic construction.

Independent checks include 60 complete arrangement maxima, 5,111 rational
points, 1,712 cubic-checked oracle calls, and 600 full mixed solves against
cubic/Knuth: 220 bounded certificates, including 152 previous rejections,
and 380 exact fallbacks. The 80-trial benchmark retains all 320 full
constructions and regressions. At 511 keys, median paired priced/Knuth
ratios are 0.12608 on the new family, 1.30491 random, 1.15055 near-uniform,
and 1.08209 geometric. The previous portfolio remains unchanged because
its old shortcuts can be much faster. The M4 was under substantial load;
the proof and counters, rather than precise timing claims, establish scaling.

The preceding standalone constructor subtracts the smallest key weight m and
adds it to every gap. An exact alphabetic optimum for q+m supplies a candidate
and the lower bound K(p-m)+A(q+m)-mn. This is the strongest bound of this form
over all admissible uniform transfers. Equality with the original full tree
cost certifies global mixed optimality in O(n log(n+1)) arithmetic work and
O(n) space. A positive nonuniform family has an original key-capacity deficit
of (n+1)/7, so it strictly extends the previous equality families. Full
construction reaches 229,375 keys, 196,608 distinct key weights, and cost
2,029,411,090,432 without interval-DP cells. See [the proof](SHIFTED_ALPHABETIC.md).

The independent probe checks 960 cubic cases, 3,629 scalar shifts, and 37,500
literal inequalities. The optimized constructor matches independent oracles
on 9,840 alphabetic cases and 960 mixed solves, including 560 exhaustive
controls, with 336 certificates and 624 exact Knuth fallbacks. Hu--Tucker
merging, its heap implementation, explicit tie handling, reconstruction, and
all full-cost checks are included. The general worst case remains quadratic.

Across 84 matched trials (252 full constructions), the new family has median
paired shifted/Knuth ratio 0.07629 at 895 keys. Random, near-uniform, and
geometric ratios are 1.02507, 1.14523, and 1.04554. The standalone route is
213.67 times slower than the previous portfolio on its old profile family,
and 12.57 times slower on its 639-key multilevel family. The previous portfolio
is unchanged. All raw timings and operation counts are retained; the M4 was
under substantial load, so these are qualified observations rather than
precise speedup claims. Mathematical priority is not established.

A separate mixed extension of compatible merging is rejected by a positive,
strict-choice six-key counterexample: even with freely permutable key weights
it returns 214, while the full ordered optimum is 213. The failure survives
an open perturbation box and extends to every n>=6. This is an obstruction
to the specified rule, not a general lower bound. The shifted alphabetic
certificate correctly obtains 213 on that same example.

The preceding constructor tests a max-Cartesian candidate against independent
global key and gap lower bounds. For arbitrary gap weights, the new bound
integrates exact binary-indicator optima, each equal to a unit-leaf depth
minimum plus the number of zero runs. Its order-sensitive term is a variation
scan; its ranked term uses dyadic linear selection, avoiding a complete sort.
Candidate construction, certification, and successful reconstruction take
O(n) arithmetic work and O(n) space. A proved positive family has Theta(n)
distinct key and gap weights, nonalternating gaps, and no common large baseline.
All n keys are constructed; both types of weights remain in the objective.

Independent checks include 862,118 binary-indicator/tree inequalities,
20,560 weighted-tree inequalities, 1,200 preliminary cubic controls,
3,000 complete constructor and 3,000 portfolio comparisons with cubic/Knuth,
21,844 gap formula checks, and 20 selection scaling controls through 100,000
gaps. Full construction reaches 327,679 keys with that many distinct key
weights and 65,538 gap levels, using 655,322 Cartesian comparisons and no
interval-DP cells. Exact full cost: 253,331,707,448,885,247. The implementation
also handles a certified 20,000-key chain iteratively. See
`results/threshold_probe.json`, `results/threshold_complete.json`, and
[the full proof and limitations](THRESHOLD_CERTIFICATE.md).

The bound is not always attained: p=(2,1,1), q=(100,10,1,10) gives lower
bound 158 and full optimum 160. Ties may hide an attaining tree from the
chosen Cartesian candidate. Exact Knuth fallback remains in the standalone
solver; the portfolio preserves the old profile shortcut before testing
the new candidate, then retains earlier signature/affine routes. The general
worst case remains quadratic and mathematical priority is not established.

The final matched benchmark checks 400 full constructions across 80 trials.
The positive multilevel family has a median paired portfolio/Knuth ratio
0.00601 at n=1279, while ordinary random and geometric controls are 1.03464
and 1.02515. The final run occurred under high M4 load and has substantial
same-kernel variation; these are qualified observations, not precise speedup
claims. All regressions, routing counters, and raw measurements are in
`results/threshold_complete_matched.json`. Operation counts are the scaling
evidence. The old profile shortcut runs first to avoid an extra candidate
construction on its successes.

The preceding constructor removes the large-baseline requirement on a new
recognized family. For alternating nonnegative gap weights, deleting one
parity of zero-weight leaves proves a global gap-cost lower bound attained
by every minimum-internal-path-length shape. A legal tree attaining the
independent key-depth profile lower bound is therefore fully optimal.
For two-level keys, four interval endpoints recognize and reconstruct
attaining patterns in O(n) arithmetic work and O(n) auxiliary space.
This includes arbitrary relative key/gap magnitudes, zeros, and nonperiodic
patterns. Strictly alternating keys and gaps always qualify when n+1 is
not a power of two. Perfect sizes require separate checks; p=(100,1,100)
with zero gaps has class cost 401 but full optimum 303.

The full solver validates 3,157 inputs against Knuth, including 2,847 cubic
controls, and another 3,157 portfolio solves agree. Separate exhaustive
checks cover 13,834 parity/tree and 69,170 mixed-weight/tree inequalities.
No-baseline construction reaches 393,216 keys: strict alternation has
393,216 joint-signature runs but only 196,608 interval transitions,
262,144 membership queries, and linear reconstruction, with no residual
Huffman work. Full counters and source hashes are in
`results/profile_complete.json` and `results/gap_parity.json`.

Eighty matched M4 trials compare five complete constructors (400 total).
At 1536 keys, the no-baseline nonperiodic and alternating families have
median paired portfolio/Knuth ratios 0.0022 and 0.0033. Five observations
per row and visible variation between identical kernels limit the timing
precision; operation counts are the scaling evidence. Unsupported inputs
preserve the previous portfolio, with measured overhead on some old fast
routes. Ordinary random and geometric portfolio/Knuth ratios are 1.0690
and 1.0375. The standalone solver instead falls directly to Knuth and can
lose earlier speedups. The general worst case remains quadratic; arbitrary
gap sequences and nonattaining patterns remain outside the linear theorem.
See `results/profile_complete_matched.json` for all positive and negative
controls. Mathematical priority and broad practical superiority are unproved.

The preceding representation groups consecutive equal pairs (p_i,q_i+q_(i+1)).
With k such blocks, the standalone minimum-path-length optimizer takes O(nk)
arithmetic work and O(n) auxiliary space, including full reconstruction.
An exact block reward telescopes in skeleton rank; four sliding maxima and
Hirschberg-style forward/backward recomputation replace the individual steps.
The full mixed certificate also uses O(k) weighted multiplicity records,
even when gap weights alternate at every position inside a block.
For arbitrary 0<=u_i,v_i<=M, M>=1, B=4(n+1)^2M, p_i=B+u_i, q_i=B+v_i,
the gate always passes. Thus the full standalone construction is O(nk)
time and O(n) space on this non-affine family. Both weight types can vary;
the large baseline and small signature count are substantive restrictions.

The portfolio scans the block count and uses this kernel only when
k<=max(16,floor(n/32)); otherwise it uses the preceding affine solver and
its exact fallback. This avoids expensive fragmented-input behavior found
in the retained standalone control. The portfolio retains O(nk) time on
the explicit family, but its alternate route may use more than linear space.
The standalone kernel is available separately. Neither solves unrestricted
weights subquadratically; all fallback results remain exact.

The new exact suite checks 1,023 cases with both standalone and routed
construction, including 778 cubic controls, 1,023 full shape-DP comparisons,
and 1,000 independently enumerated transfer vectors. Certified construction
reaches 98,304 keys with four and sixteen joint blocks. Sixty matched M4
trials compare five full constructors. At 1536 keys the portfolio/Knuth
median paired ratios are 0.0259 and 0.0961 for those two families; the old
full shape-DP ratios are 0.0893 and 0.3958. The standalone kernel is roughly
ten times slower than Knuth on fragmented controls, and the old full shape
DP still beats the routed solver on irregular large-baseline inputs. Those
negative results, all operation counts, and source hashes are retained in
`results/run_complete*.json`. The linear-space theorem belongs to the
standalone accepted path; routing and fallback have explicit qualifications.

A complementary exact constructor prunes a minimum-path-length shape DP using an
affine slot potential and a signed residual-profile bound. For n>=32,
B=4(n+1)^3, p_i=B+i+u_i, q_i=B+i+v_i, arbitrary signed integer perturbations
of total magnitude at most n give O(n log^2(n+1)) full construction; independent
unit perturbations at every key and gap give O(n log(n+1)) construction.
Both guarantees include slope inference, a global optimality certificate, and
reconstruction. The input weights need not stay monotone, and the optimum
need not keep the reference shape. A preflight test skips shape work when
the sufficient certificate cannot succeed. Other inputs retain exact Knuth
fallback; these are restricted-family results, not an unrestricted solution.

The new solver passes 1,166 exact full solves, including 802 cubic controls,
and reaches 98,304 keys with 410,752 shape states on alternating perturbations.
Its tree improves on the affine reference by 13 cost units. A four-constructor,
four-order M4 Python benchmark includes all preprocessing and reconstruction.
At 1536 keys the three certified families have median paired time ratios
0.0284--0.0364 versus Knuth and 0.0818--0.1091 versus the full shape DP.
Ordinary random/geometric inputs fall back; at 768 keys their ratios versus
Knuth are 1.1247 and 1.0110. These small matched measurements accompany proved
state bounds; they are not evidence of unrestricted or optimized-library
superiority. Full counters and timings are in `results/ramp_complete*.json`.

A complementary mathematical reduction uses penalized partial trees and a published
core-sparse Monge multiplication primitive. It gives exact
O(n^(3/2) log^(3/2)(n+1)) construction for arbitrary nonnegative integer mixed
weights of total mass O(n), including zeros. The intermediate-core bound,
finite completion, and witness reconstruction are proved in the note and
manuscript. **Condensed Python and C++ constructors are now implemented and
checked against dense products and independent BST oracles. No practical
speedup is claimed for this backend.** Ordinary witness arrays can use an
extra logarithmic factor in storage relative to the published succinct maps.
A centered extension bounds work by deviation R above the minimum key and gap
weights: for polynomial R, O(n(1+sqrt(R)) log^3(n+1)) arithmetic construction,
independent of baseline magnitudes in the operation count. R=O(n) yields
O(n^(3/2) log^3(n+1)); bit costs still depend on input length. The actual
normalized-height Python constructor and independent baseline/tile audits
are included. Neither result settles unrestricted weights or establishes
priority or practical superiority.

The input has weights on **both keys and gaps**. A complementary constructor retains
the constant-size search-path skeleton of the first possible two-gap core
violation, and bounds its remaining cost with mixed forests. It certifies a
family with a linear number of nonuniform keys at arbitrary middle positions
and two gaps of weight 3n; exact construction is O(n^alpha), alpha<1.59024,
using the existing mass-frontier theorem on the remaining interval. The
family's total weight O(n) also gives the global frontier this same exponent; the
advance is a tighter certificate and measured work reduction within that
regime, not a new subquadratic regime. Constant key-weight examples alone
reduce to alphabetic trees and are not evidence of
the full mixed-weight advance. The earlier residual certificate remains a
fallback, solving intervening intervals on local mass frontiers. Single-outcome
separators remain available as fallback. An interior-gap certificate retains both neighboring key
weights and gives an exact two-orientation cost identity. Static range indexes
avoid repeatedly scanning shrinking components. Earlier contraction and
bounded-shape methods remain available as controlled comparisons. The general
worst case remains quadratic; no unrestricted subquadratic solution or
impossibility proof is claimed. Priority of the sufficient conditions has
not been established.

The latest representation audit gives two positive mixed intervals with
identical endpoint-response functions, mass, and endpoint weights but different
optima in the same surrounding context (101 versus 100). Thus that value
function alone is not an exact composition interface. A separate construction
requires quadratically many explicit affine pieces but has a linear-size
factorization; polynomial endpoint mass ratios give only O(log^2 n) pieces.
These are scoped representation results, not a general complexity lower bound.

A further positive mixed family, p_r=q_r=4(n+1)^3+r, has quadratically many
nonzero Monge densities and mixed fourth differences, yet admits O(log n)
exact interval queries and O(n) exact tree construction. Its core follows a
dyadic ruler pattern. Thus listing either difference support is a quadratic
representation choice even on this easy family. The centered deviation is
R=n^2; the result does not contradict the earlier subquadratic deviation bounds.
The new exchange certificate also optimizes a wide last level directly when
its checkable local condition holds. The existing residual-Huffman gate then
certifies full optimality or triggers Knuth fallback. Accepted inputs take
O(n log n) time, or O(n) when both weight lists are monotone, including full
reconstruction and the bound. The general worst case remains quadratic.

The exact saturated-layer identity expresses its nonseparable part as a
weighted subsequence with coefficients 0,1,0,2,0,1,0,... . It passed 70,100
interval checks. The ramp formula passed 221,284 interval checks; the full
exchange/gate/fallback solver passed 1,210 solves and 826 cubic controls.
At 98,304 keys a certified ramp solve uses linear scans, construction, and
residual-bound work without an interval table. See RULER_REPRESENTATION.md for
the complete proofs, rejection controls, operation categories, and limitations.

```sh
python3 obst/code/ruler_layers.py --max-n 512
python3 obst/code/ruler_barrier.py --max-n 512
python3 obst/code/ordered_complete.py --max-n 768
python3 obst/code/check_ramp_complete.py --max-n 768 --scale-n 98304
python3 obst/code/benchmark_ramp_complete.py
python3 obst/code/check_run_complete.py --max-n 768 --scale-n 98304
python3 obst/code/benchmark_run_complete.py
```

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
python3 obst/code/check_pair_skeleton.py
python3 obst/code/pair_skeleton_family.py
python3 obst/code/pair_skeleton_crossover.py
python3 obst/code/boundary_response.py
python3 obst/code/penalty_layers.py
python3 obst/code/check_core_monge.py
python3 obst/code/check_compact_obst.py --max-n 512
python3 obst/code/centered_layers.py
python3 obst/code/centered_geometry.py
python3 obst/code/check_centered_obst.py
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


The condensed product implementation credits Gawrychowski, Gorbachev, and
Kociumaka (ESA 2025). The new OBST layer construction uses exact whole-table
fixed-point stopping and full witness reconstruction. `MONGE_PENALTY.md`
describes the implementation, the ordinary-map storage overhead, and its
independent tests. Source-hashed raw results are in `core_monge.json`,
`compact_obst.json`, and `compact_cpp_{sanitize,release}.json`.

Reproduce the compiled audit locally with an available Clang C++20 compiler:

```sh
clang++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra obst/code/compact_obst.cpp -o /tmp/obst-compact-release
python3 obst/code/check_compact_cpp.py /tmp/obst-compact-release --max-n 2048 --trials 3
```

The root AGENTS.md gives the M4 sanitizer and release commands. Both constructors
in the benchmark use exact signed-128 arithmetic and construct all keys. The
C++ driver rejects out-of-range weights before either solve; Python retains
arbitrary-precision arithmetic. The compact constructor itself does not allocate
the quadratic interval table, although the separate Knuth oracle does.

The release audit passed 1,362 complete solves through 2,048 keys. All 90
scaling trials were slower than the matched C++ Knuth constructor. At 2,048
keys, median compact/Knuth time ratios range from 44.3 to 185.1. The maximum
completed core is much smaller than the interval table, but 55.7--306.9 million
core visits and retained witness maps dominate these implementations. The
note and manuscript report these negative results, full counter categories,
and the distinction between instrumented work and machine instructions.


Root/nonroot coupling and retained marked-boundary diagnostics:

```sh
python3 obst/code/root_partition_probe.py
python3 obst/code/check_root_partition.py
python3 obst/code/root_partition_family.py
python3 obst/code/benchmark_root_partition.py
python3 obst/code/check_marked_event.py
```

Use the M4 wrappers in the root AGENTS.md for substantial runs. The standalone
root certificate and its fallback are in `code/root_partition.py`; the event
probe is explicitly experimental and is not called by that solver.

## Reproducing the current audit

From the repository root, use the M4 commands in `AGENTS.md` for the search,
explicit patterns, rotation/tiling checks, and `ramp_core_tightness.py`.
Build the manuscript **from `obst/manuscript/`** with
`tectonic --keep-logs main.tex`; the root repository has a different TeX project.
