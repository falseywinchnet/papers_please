# Scalar-carry forward construction for arbitrary mixed OBST weights

The skyline restriction supports the forward step, not only traceback.
For an actual prefix function F=f_k represented by a D-node additive diagram
of height h, one arbitrary nonnegative key/gap update can be constructed in
O(h^2 D) arithmetic and dictionary operations. This removes the unbounded
generic-minimum context parameter X from the previous per-update theorem.
It does not bound D over all n updates, and hence does not by itself establish
a general subquadratic OBST algorithm.

The subsequent [punctured representation](SLOT_PUNCTURED.md) removes the
first-address replacement factor by storing each midpoint directly. It gives
O(h(D+1)) per update and O(h(n+sum_k D_k)) complete construction, with its
own diagram size D. The ordinary-diagram result below remains valid.

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

For a normalized parent node R=L||U, put C=min(min(L),U(0)).
The right child receives min(p,C). Classify that edge as a reset if C<=p,
including ties and infinite ties. If its child expands, its relative carry
C-min(U) depends only on the parent input node. Thus there is at most one
reset seed per input node. Infinity is kept separately; no infinity-minus-
infinity operation occurs.

The left edge always inherits p. If the right edge also inherits p, then
p<C<=min(L), so the left child is pruned. Each expanded state therefore
has at most one inherited expanded child. Start paths from the root and
from every reset seed, following inherited edges. They cover every state;
each step decreases the remaining depth by one. Memoization can merge
paths but cannot introduce uncovered states.

Writing d(u) for each reachable input node's depth, this proves

    Z <= h + sum_u max(d(u)-1,0) = O(hD)
    sum_expanded d <= h(h+1)/2 + sum_u d(u)(d(u)-1)/2.

An expanded depth-d state makes exactly d node-assembly calls and d
first-address replacement visits including the leaf. Shared templates
contribute at most h(h+1)/2 of either. Each total is consequently bounded by

    h(h+1) + sum_u d(u)(d(u)-1)/2 = O(h^2 D).

There are exactly 2Z+1 build calls, at most D summary expansions, and at
most 2D+Z summary calls. These counts include memo hits and intermediate
work. The counting argument holds for arbitrary signed/infinite inputs;
correctness as an OBST transition still uses endpoint dominance. A feasible
prefix has D>=1; an all-infinite input is handled in constant work.
Exact operand bit costs and dictionary implementation costs are additional
to this operation model.

## Sharpness for the general recursion

For m>=1 set N=2^m, h=2m, A(X)=2X-popcount(X), and

    F(NX+Y) = -A(X)/(m+1) - Y,  0<=X,Y<N.

The input has D=2m+1 additive nodes because it is a weighted sum of bits.
At each low-bit depth d=1,...,m, the expanded relative carries are
2^d-1 and (s+1)/(m+1) for s=0,...,m-1. At upper depth m+r there are
m-r valuation-indexed contexts and one initial-block context. Summing these exact level counts gives

    Z = 3m(m+1)/2 = Theta(hD).

Their depth sum is m(m+1)(7m+5)/6. Templates of depths 1,...,m-1
contribute m(m-1)/2 additional calls, so both the node-assembly count
and first-address replacement visits are exactly

    M = m(7m^2+15m+2)/6 = Theta(h^2 D).

These are operation counts, including node-interning hits. The manuscript
proves every level count. The family violates endpoint dominance:
F(N)=-1/(m+1)>F(N-1)=-(N-1), despite v(N)>v(N-1). It cannot be an
actual mixed OBST prefix. Thus it makes the general accounting sharp
while leaving stronger actual-prefix bounds open.

## Complete construction and remaining issue

Apply the recurrence successively to the normalized mixed weights. Store
all prefix roots and use the previous one-path skyline queries for O(nh)
selected-slot traceback, followed by sparse ancestor repair. The output is
an exact complete optimum at the prescribed height. Height n always
suffices, and the existing height certificate may select a smaller value.

For incoming sizes D_0,...,D_(n-1), forward construction takes
O(h^2 sum_k D_k) arithmetic/dictionary operations. The implementation
records actual expanded contexts and persistent replacements separately.
This polynomial per-update guarantee is stronger than the previous bound
with an unrestricted generic merge parameter. The still-open question is
a useful all-stage bound, or a construction that avoids large D_k entirely.

The harness compares all small prefix entries with direct predecessor
minimization, checks both the earlier node-pair injection and the sharper
reset-path cover explicitly, verifies original all-root optima and complete output trees, and reuses both kinds
of adversarial size-search winners. Separate necessary-height controls
retain all original weights and exact counts. Measurements are confined
to the manuscript's verification appendix and the source-hashed records.
