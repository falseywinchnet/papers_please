# Full mixed construction with block interiors

Separating a block's first entry from its interior removes the persistent
boundary-replacement factor in the scalar-carry constructor. One arbitrary
mixed update now takes O(h(D+1)) arithmetic and dictionary operations on a
D-node input of height h. The complete optimal height-h tree, including all
forward work, traceback and ancestor repair, takes

    O(h (n + sum_k D_k)).

Here D_k counts the interior diagram before update k, and D_0=0. Choosing a
proved sufficient height makes this an unrestricted full mixed-OBST solver.
An [explicit positive mixed family](SLOT_PUNCTURED_BARRIER.md) forces
Omega(n^3) final nodes and Omega(n^4) distinct nodes in shared prefix history.
Thus this representation has no universally small size guarantee. No run
restriction is imposed on either the key weights or the gaps.

## Representation

A punctured node of depth d represents the positions 1,...,2^d-1 of a block.
Its tuple is (left interior, midpoint scalar, right interior). The first
position of each full block is outside that tuple. Depth zero has no
interior, and an all-infinite interior is a null reference.

Subtract the minimum finite entry from the child references and midpoint,
then intern that normalized tuple and its depth. This is canonical up to
additive translation: induction on depth reduces equality to the two child
interiors and the midpoint. Assembling a node takes constant work.

An ordinary additive node L||R converts to (puncture(L),R(0),puncture(R)).
First values and conversion are memoized by source node. Conversion takes
O(D_standard) work and creates at most one punctured node per ordinary
nonterminal. It may merge further nodes whose only difference was the
omitted first entry.

## Exact recurrence and charge

The inclusive carry p_B=min_(a<=B) F(a) already satisfies p_B<=F(B).
Consequently the omitted first input entry cannot improve the carry.
Endpoint dominance supplies the outside-predecessor formula used by the
previous scalar-carry constructor. For P=(L,c,R) at depth d, update with
normalized key weight w and preceding residual gap g as follows:

    E_g(P) = min(E_g(L), c-g(d-1), E_g(R))
    left carry = p
    right carry = min(p, min L, c)
    output midpoint = min(p-g(d-1), E_g(L)) - w(d-1).

Recurse on the two interiors and assemble their outputs with that midpoint.
The E summary excludes each block's first address by definition. Memoized
summaries take O(D) work. Infinite alternatives are omitted from minima.

When p<=min(P), or P is all infinite, output the valuation template
p-(g+w)v(t) for t>0. Each template is assembled from two references to the
preceding template and one midpoint scalar. All templates cost at most h
assembly calls. The empty initial prefix has no interior, carry zero, and
g=0; subsequent prefix roots have an infinite carry.

Normalize an expanded state's carry by its input interior minimum. Put
C=min(min L,c). If C<=p, the right child resets to C, with normalized state
determined solely by its parent input node. Otherwise p<C<=min L prunes
the left child. Hence each expanded state has at most one inherited child.
The reset paths from the root and at most one seed per input node cover
all expanded states. With d(u) the input node depths,

    Z <= h + sum_u (d(u)-1)
    assembly calls = Z + T <= 2h + sum_u (d(u)-1),  T<=h.

There are exactly 2Z+1 recursive build calls, at most D summary expansions,
and at most 2D+Z summary calls. Thus the bound counts intermediate work,
including interning hits, rather than only final graph size.

## Complete tree and memory

The skyline predecessor walk follows the bits of b-1. Entering a right
half exposes the required candidate directly as the midpoint scalar.
It takes O(h) work per query and makes no new diagram nodes. Retaining
prefix roots therefore supports O(nh) selected-slot traceback.

Collect the chosen slots and their perfect-tree ancestors, at most nh
vertices. This set is ancestor-closed. Starting at the perfect-tree root,
visit only collected children in inorder to enumerate their labels in
increasing order. This costs O(nh), replacing comparison sorting. The
existing sparse deletion repair then uses parent/child and inorder-neighbor
links to delete every unwanted ancestor in constant work. Its complete
output is identical to the sorting-based repair. This gives O(nh) full
reconstruction work. The bound on all created diagram nodes plus this
ancestor set also bounds stored words by O(h(n+sum_k D_k)).

## Exact general-diagram sharpness

The previous weighted-bit family F(2^m X+Y)=-(2X-popcount(X))/(m+1)-Y
has h=2m and D=2m punctured nodes. Its expanded state count remains
Z=3m(m+1)/2. Exactly m-1 templates are built, so the new assembly count is

    3m(m+1)/2 + m-1 = Theta(hD).

The proof enumerates every carry level; the audit checks the formulas.
F(2^m)>F(2^m-1) explicitly violates endpoint dominance, so this family
cannot arise as an actual mixed OBST prefix. It proves sharpness of the
general recursion's accounting and leaves stronger actual-prefix bounds
open. The former Theta(h^2 D_standard) replacement cost is avoided by
changing what a node represents.

## Verification

The audit uses direct all-predecessor prefix values and queries, original
all-root tree optima, independent Knuth controls, and complete output-tree
checks. Conversion is checked against dense canonicalization and exact
values including rational, signed and infeasible entries. Every small slot
subset is repaired by both the new traversal-based and retained sorting-based
constructors. Actual size-search winners are compared at every prefix by
canonical equality with conversion of the previous constructor.

The separate scale audit reuses the exact earlier necessary-height chain
inputs and adds arbitrary mixed integer inputs at certified sufficient
height. Results retain original weights, all operation counts, source hashes
and consumed-input hashes. Finite verification counts are in the manuscript
appendix and the JSON records. The proof, not measured scaling, supplies the
per-update and complete-construction bounds. Exact integer/rational operand
bit costs remain additional to the arithmetic/dictionary operation model.
