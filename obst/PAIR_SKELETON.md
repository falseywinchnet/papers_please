# Coupled two-gap skeleton certificates

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. This is an exact sufficient certificate for the **full
mixed-weight** problem. It does not give a general subquadratic algorithm, and
priority of the certificate has not been established.

## Why retain a skeleton?

The earlier residual certificate adds two separate minima: the cost of heavy
outcomes and an unordered lower bound for all residual weights. The same tree
need not attain both. We retain the geometry of the first possible violation,
and place residual weights in forests attached to that geometry.

Choose two internal gaps a<b. Let A be the distinct neighboring keys
{a-1,a,b-1,b}, with m=|A| (three for adjacent gaps, four otherwise).
A tree is closed with respect to A if no outside key is an ancestor of an
A-key. Write M1=q[a], M2=q[b], theta=min(M1,M2). All weights are nonnegative.

Every A-key is on one of the two selected search paths. In a nonclosed tree,
their union also contains an outside key. If the selected gap depths sum to D,
the union contains at most D-1 keys, since the root is shared. Consequently
D>=m+2. When equality holds, the paths share exactly the root and their union
has exactly m+1 keys: A and one outside **bridge**. This is a skeleton with at
most five keys, so at most 42 binary-tree shapes per bridge region suffice.

Let B0 be the unordered mixed-tree optimum with selected gap weights replaced
by zero, retaining all other key and gap weights. Each internal gap has depth
at least two. Thus the basic and deeper-violation lower bounds are

    Bbasic = 2(M1+M2) + (m-2)theta + B0,
    Btail  = 2(M1+M2) + (m-1)theta + B0.

The second applies when D>=m+3. The first applies to every nonclosed tree.

## Equal-depth mixed forests

For multisets P of internal weights and Q of leaf weights, with
|Q|=|P|+k, define F_k(P,Q) as the minimum mixed cost over k rooted binary
trees whose roots all start at depth zero. Empty trees (single leaves) are
allowed, and weights may be permuted within each type.

Sort P and Q ascending. For each internal weight in ascending order, remove
the two smallest current leaf weights, add their sum plus the internal weight
to the answer, and insert that total as a new leaf weight. Stop after |P|
merges, leaving k roots. This computes F_k exactly.

Proof: in an optimal forest take a deepest internal node. It is a cherry.
Exchange weights within each type to put a smallest internal weight there and
the two smallest leaf weights at its children. These exchanges do not increase
cost. Contracting that cherry contributes its total weight once; the contracted
forest is the smaller unrestricted problem. Conversely, expanding that leaf
in any smaller forest is feasible and has exactly that added cost. Induction
proves the rule. Nonnegative weights make generated merge weights nondecreasing,
so two sorted queues perform linear work after sorting. Total O(n log n).

The independent checker enumerates forests and assigns sorted weights to sorted
depth slots; it does not use this greedy recurrence as its reference.

## Cost of a first-violation skeleton

Delete A from key order to obtain its m+1 intervening intervals. The two
selected gaps occupy empty intervals; all other intervals are light regions.
In any first-violation skeleton the bridge lies in one nonempty light region t.

Retain the exact key comparison lengths for A and exact selected gap depths.
An ordinary light region s, attached at hole depth h_s, contributes the bound

    h_s W_s + F_1(P_s,Q_s).

The bridge region has two holes. Lower both hole depths to their minimum h.
If the bridge comparison length is ell, both holes descend from the bridge,
so h>=ell. Every other internal key in the two-root forest then has comparison
length at least h+1, strictly greater than ell. In this relaxed problem, a
largest regional key weight x can therefore occupy the bridge by exchange.
The contribution becomes

    ell*x + h*(W_t-x) + F_2(P_t minus one occurrence of x, Q_t).

This exchange is justified **after** equalizing hole depths; it is not a claim
about which key is the bridge in the original ordered tree. All original
weights survive the relaxation. Only regional order and the larger of the
two hole depths are forgotten.

Minimize over all admissible constant-size skeletons and bridge regions to
obtain Bfirst. Every nonclosed tree costs at least

    B = max(Bbasic, min(Bfirst, Btail)).

If the first class is empty, use Btail. A closed witness of cost U<=B proves
that some global optimum is closed. Optimize that closed class by solving
the intervening intervals exactly and then a constant-size full-weight core.
Equality is safe: the closed witness is no worse than any excluded tree.

The implementation tries a midpoint payload witness first. Optional refinement
computes the exact closed candidate even if the witness fails. Failure falls
back to the earlier exact constructor. Screening takes O(n log n); the general
worst case remains quadratic. Adjacent selected gaps and zero weights are
included in the exhaustive checks.

## A family with arbitrary placements of nonuniform keys

Constant key weights alone do not establish progress on genuinely mixed input:
for p_i=c, internal/external path-length identity E=I+2n gives

    C(T;c,q) = sum_g (q_g+c) depth_T(g) - cn.

Thus that family is equivalent to an alphabetic gap-only problem. The following
family has a linear number of nonconstant key weights.

Let n=2^h, h>=5, r=n/16, s=r-1. All ordinary gaps have weight one; gaps
1 and n-1 have weight M=3n. All keys have weight one except **any s middle
keys** among positions 2 through n-3, which have weight two. The four core
keys retain weight one. No regularity of the chosen positions is assumed.

For unit keys define U0=(2h+3)n-6h-3. The optimal closed cost is 5M+U0.
Indeed, the middle payload has n-4 keys and cost
(2h-1)n-6h-2. Its mass is 2n-7. Of the 14 four-key core shapes, the minimum
has selected depth sum five, payload hole depth two, and other cost thirteen,
giving core cost 5M+4n-1. The alternatives have (selected sum, middle depth,
other cost) among (5,3,12), (6,3,13), (6,3,15), (6,4,14), and (7,4,13),
which are no cheaper. This also proves the baseline closed minimum used below.

A midpoint middle payload has maximum comparison length h relative to its
own root. Every extra unit of key weight therefore costs at most h+2 in the
full closed witness:

    U <= 5M+U0+(h+2)s.

Let G_k(t) be the minimum sum of comparison lengths of t marked internal
nodes in a k-root forest. Filling capacities k*2^(ell-1) at lengths ell gives

    G_1(s)   = (h-5)r+1,
    G_2(s-1) = (h-6)r+2.

For the unit background, the two-root forest has n-5 internal nodes, with

    F_2 = (2h-3)n-6h+5.

To see this, its balanced leaf profile has three leaves at depth h-2 and
n-6 at depth h-1. The forest identity E=I+2(n-5) gives mixed cost 2E-(n-5).
The minimum over first-violation skeletons is

    Bfirst(unit) = 6M+(2h+1)n-6h+5.

There are ten admissible five-key profiles. With middle hole minimum d,
bridge length ell, and fixed core/endpoint contribution c, the distinct
(d,ell,c) triples are (2,2,16), (2,2,15), (3,3,13), (2,1,15),
(3,1,14), and (2,1,16). Substituting 2d(n-4)+ell+c+F_2 shows that
(2,1,15) minimizes the expression for n>=8.

Removing the largest key at the bridge leaves s-1 extra unit weights. Each
remaining extra receives the depth shift at least two, plus forest comparison
lengths summing to at least G_2(s-1). The bridge receives at least one extra
unit of cost. Therefore

    Bfirst >= Bfirst(unit) + 2s-1 + G_2(s-1).

The residual unordered bound is exactly

    B0 = 2nh-n+2+G_1(s).

For the base term, absorb unit key weights into gaps: there are two leaf
weights one and n-1 leaf weights two. Their Huffman tree is a perfect h-level
tree with one bottom leaf expanded into the two unit leaves. Subtract n to
recover mixed cost. The first h-4 internal levels are full; assigning the
s extra key units there simultaneously attains G_1(s), proving equality.

After substituting M=3n the two certificate margins are

    Bfirst-U >= 5n/8+h+9 > 0,
    Btail-U  >= 25n/16+7h+8 > 0.

Hence the inexpensive witness certifies **every placement** in this family.
The middle payload has all key weights in [1,2] and all gap weights one.
The existing bounded-positive-weight mass-frontier theorem gives exact total
construction O(n^alpha), alpha=1+log_(2 phi)(2)<1.59024, including the new
O(n log n) screening and complete reconstruction. The exponent comes from
the previously documented frontier architecture. Crucially, this family's
total weight is still O(n), and every key weight is at least one. The earlier
global frontier already guarantees the same exponent on the whole instance.
This is a stronger certificate and a measured work reduction within that
regime, **not a new subquadratic input regime**.

For h>=6 this strictly strengthens the earlier **fixed-pair** certificate,
even if the latter computes the exact closed optimum first. Every closed
tree costs at least its unit-background closed optimum plus G_1(s), while
Bbasic=6M+B0. Their difference is at least n-6h-5>0. This claim is about
that pair's residual certificate, not every core another selector could try.

## Evidence and limitations

`check_pair_skeleton.py` passed 11,880 independent forest checks, 24,188
exhaustive weight inputs, 51,654 pair-exclusion checks (with separate first
and tail checks), and 6,560 complete solves against cubic DP. The exhaustive
pair cases include 3,288 exact closed candidates certified by the coupled
bound but not by Bbasic. Larger adversarial checks use n=128,512,2048 and
both payload kernels. Random and near-uniform controls often fail this
certificate and pay its overhead before the exact fallback.

`pair_skeleton_family.py` checks the family formulas and placement variants,
scales nonuniform construction through n=16,384, checks uniform 2n gaps
through n=65,536, and records balanced matched full-construction timings
with raw operation counts. Results are in `results/pair_skeleton*.json`.

The 31 nonuniform placement/size combinations all pass; 28 additionally match
Knuth and eight match cubic DP. Fourteen unit-background formulas pass through
n=65,536. At n=2,048 and unit background with selected gaps 2n, the new bound
is 71,619 and exact cost 71,611, closing the old bound's 67,586 deficit.
At n=16,384 with 1,023 randomly placed doubled key weights, exact construction
uses 11,681,397 DP states (short + top + both tiny core solves), versus a
134,225,920-cell full table. It also uses 42,351,013 top-matrix queries and
15,502,473 short-root candidates. State reduction is not a runtime ratio.
The cost is 767,240, witness 768,946, and excluded bound 780,208; full
construction took 54.59 seconds once. No full quadratic reference was run
at that largest size.

The 224 matched complete constructions at n=512 retain all trial orders,
times, counts, and exact cost checks. For spread/random nonuniform placements,
the new frontier route takes median 1.48227/1.39273 times Knuth, but
0.48126/0.47931 times the previous residual constructor. With a Knuth payload
kernel the ratios to Knuth are 0.93990/0.86098. The unit 2n-gap case gives
0.04285/0.03927 for the frontier/Knuth kernels. Random and near-uniform
controls fail the new certificate and remain slower than plain Knuth.
The varying-background benchmark uses ordinary weights in [1,1000] and
selected gaps 1000n; all eight attempts fail this certificate. The geometric
control also fails, so its favorable ratio is not credited to the new bound.

The separate larger matched check uses four alternating orders per size and
fresh random placements. All 16 complete constructions agree with exact Knuth
and direct tree evaluation. At n=2,048 and 4,096, median new/Knuth time ratios
are 0.65948 and 0.56309 respectively (about 1.52x and 1.78x faster). These are
instrumented Python measurements on the sponsor's M4, not comparisons with
optimized compiled implementations. Raw trials and source hashes are in
`pair_skeleton_crossover.json`.

The central limitation is the constant-size selected-path skeleton. Arbitrary
mixed inputs need not have a cheaply certified four-key core. Extending the
representation to larger path unions requires controlling both the number
of boundary states and their update cost; the current theorem does neither.
JesseSort's compact-boundary and deferred-materialization principles suggest
this question, but do not supply its missing bound. No result here is attributed
to JesseSort, and no novelty or broad practical superiority is claimed.
