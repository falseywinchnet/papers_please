# Scalar-carry forward construction for arbitrary mixed OBST weights

The skyline restriction supports the forward step, not only traceback.
For an actual prefix function F=f_k represented by a D-node additive diagram
of height h, one arbitrary nonnegative key/gap update can be constructed in
O(h^2 D^2) arithmetic and dictionary operations. This removes the unbounded
generic-minimum context parameter X from the previous per-update theorem.
It does not bound D over all n updates, and hence does not by itself establish
a general subquadratic OBST algorithm.

## Block recurrence

Let F be a nonempty mixed prefix function. Its endpoint dominance says
F(c)<=F(a) when 1<=a<=c and v(a)<=v(c). Consider a dyadic block
[B,B+2^d), and define p_B=min_{a<=B} F(a). For B>0, v(B)>=d.
Every predecessor a<=B of valuation below d is dominated by B. Thus the
minimum defining p_B can be attained at valuation at least d. At any
interior destination b of this block, v(b)<d, so the entire outside
contribution to the gap-adjusted predecessor value is

    p_B - g v(b).

For B=0, p_B is infinity for every nonempty prefix. The empty prefix is
handled by its initial g=0 transition, where the same formula is valid.
This exception is essential: slot zero has valuation zero, not height h.

For a local block function R of length 2^d, define

    E_g(R) = min_{0<t<2^d} [R(t)-g v(t)].

The first local address is excluded because its global valuation can be
larger than the block height. If R=L||U and m is U's first value, then

    E_g(R) = min(E_g(L), E_g(U), m-g(d-1)).

A singleton has E=infinity. The summary commutes with additive offsets,
so all summaries of a D-node input take O(D) arithmetic/dictionary work.

A recursive construction emits infinity at the first local output address;
its parent supplies the correct boundary value. At the midpoint M of a
block, the new output is exactly

    min(p_B-g(d-1), E_g(L)) - w(d-1).

The right child's carry is

    p_M = min(p_B, min(L), F(M)).

Recurse on both children with their respective carries and replace the
right output's first address with the displayed boundary value. Replacing
one first address takes O(d) persistent node constructions. All formulas
remain valid with infeasible input positions represented by infinity.

If p_B<=min(R), the outside predecessor dominates every internal one.
The entire block interior is simply p_B-(g+w)v(t), with infinity at t=0.
All such template functions are shared by depth; constructing every
required template takes O(h^2) work. An all-infinite input block is handled
by the same rule. No pointwise diagram minimum or addition is needed.

## Bounding the scalar carries

Normalize the input block by its minimum finite value m. A recursive state
is determined by its input-node identity and the relative carry p_B-m,
with infinity represented separately. Only states with p_B>m are expanded;
the other states use the preceding template rule.

Let Q(b)=min_{a<=b}F(a) be the inclusive prefix-minimum function on the
entire input domain. The standard two-half recurrence is

    Q(L||U) = Q(L) || min(min(L), Q(U)).

The same monotone-cap proof as for exclusive prefix minima constructs Q
with O(hD) nodes and operations. Within an expanded block, Q's first
value is p_B and its minimum is m. Consequently the normalized Q-node's
first-address value is exactly p_B-m (including infinity). The pair
(input-node identity, normalized Q-node identity) therefore determines
the recursive state. There are at most D*|Q|=O(hD^2) expanded states.
This is an injection argument, not an empirical estimate of carry diversity.

Each expanded state makes two recursive calls, a constant number of scalar
comparisons, and O(h) work to replace a first address and assemble the node.
Including summaries and templates gives O(h^2D^2) arithmetic and dictionary
operations and at most that many newly created nodes. The algorithm need
not construct Q: Q certifies the bound only. Exact operand bit costs and
dictionary implementation costs are additional to this operation model.

## Complete construction and remaining issue

Apply the recurrence successively to the normalized mixed weights. Store
all prefix roots and use the previous one-path skyline queries for O(nh)
selected-slot traceback, followed by sparse ancestor repair. The output is
an exact complete optimum at the prescribed height. Height n always
suffices, and the existing height certificate may select a smaller value.

For incoming sizes D_0,...,D_(n-1), forward construction takes
O(h^2 sum_k D_k^2) arithmetic/dictionary operations. The implementation
records actual expanded contexts and persistent replacements separately.
This polynomial per-update guarantee is stronger than the previous bound
with an unrestricted generic merge parameter. The still-open question is
a useful all-stage bound, or a construction that avoids large D_k entirely.

The harness compares all small prefix entries with direct predecessor
minimization, checks the carry-to-node-pair injection explicitly, verifies
original all-root optima and complete output trees, and reuses both kinds
of adversarial size-search winners. Separate necessary-height controls
retain all original weights and exact counts. Measurements are confined
to the manuscript's verification appendix and the source-hashed records.
