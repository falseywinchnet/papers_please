# Core-size proof audit and fixed-mass adversarial search

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar.

## The mixed mass lemma, outcome by outcome

All depths here are edge depths. A depth change of one changes an outcome's
cost by its weight, for keys as well as gaps. A subtree's mass includes all
its keys and external gaps, even when the subtree is a single external gap.

Use `v(L,R)` for a key with its left and right subtrees. Up to reflection,
the straight configuration and rotation are

    v(y(X,B),D) -> y(X,v(B,D)).

Key y and every outcome of X rise one level; key v and every outcome of D
fall one level; every outcome of B keeps its depth. With
O=p_v+mass(D), the change is O-p_y-mass(X). Optimality implies
O>=p_y+mass(X)>=mass(X).

For the bent configuration the grandchild X is internal, with key x:

    v(y(A,x(B,C)),D) -> x(y(A,B),v(C,D)).

Key x rises TWO levels. Every outcome of B and C rises one level. Key v
and every outcome of D fall one level. Key y and every outcome of A keep
their depths. The total change is

    p_v+mass(D)-2p_x-mass(B)-mass(C)
      = O-p_x-mass(X).

Again O>=mass(X). These are legal inorder-preserving full-tree rotations;
no unfinished terminal interval is rotated. Along the ancestor path of any
internal S, masses therefore obey m_1>=m_0 and m_i>=m_(i-1)+m_(i-2).
Induction gives W>=F_(d+1) mass(S). The proof covers zero weights and ties.

## Explicit dyadic boundary lemma, including arbitrary n

Density indices are integer pairs (i,j) in [0,n)^2. Remove i>=j and m
additional diagonals j-i=d_t. Set N to the least power of two >=n.
Recursively subdivide [0,N)^2 into four equal aligned dyadic squares.
Discard squares without any allowed cell; accept a square when all its cells
are allowed; otherwise split until unit cells. The accepted squares partition
the allowed cells and are maximal within this quadtree.

Every accepted side-s square has a parent of side 2s. The root is never
accepted because it contains diagonal cells. That parent is not allowed in
full. As it contains the accepted child, it cannot be wholly outside the
domain. Consequently it crosses x=n or y=n, contains a cell of i=j, or
contains a cell on one of the removed diagonals. These are the only possible
reasons the parent was split. This statement does not require n to be a
power of two; the extra area is handled by the two boundaries at n.

At a fixed parent side t, a diagonal j-i=d meets at most two aligned
parent squares in each row of squares: its integer column indices over a
row of t integer row indices form t consecutive integers. Thus it meets
at most 2N/t parents. Each boundary x=n or y=n crosses at most N/t parents
(if grid-aligned it crosses none). There are at most four accepted children
per such parent. Hence there are at most

    4 [2(m+1)+2] N/(2s) <= 8(m+2)n/s

accepted side-s squares. The looser constant 64(m+1)n/s also suffices.
Touching a boundary without straddling it causes no difficulty: charge only
parents actually containing a forbidden cell. Unit cells on removed lines
are accounted for separately, not accepted tiles.

For the uncentered early layer m=1. On each accepted tile of side s,
the penalty density is zero and the nonnegative integer density sum is
at most 2hW. Thus at most min(s^2,2hW) core entries occur. Summing the
explicit bound gives, conservatively,

    delta(E_h) <= 2n + 96 n sqrt(2hW),  1<=h<L, W>0.

The geometric inequality used is sum_(s dyadic) min(s,t^2/s)<=4t for t>=1.
For W=0 the ordinary tiles contribute zero. The two O(n) contributions are
the removed penalty diagonal and the finite-completion diagonal. The final
layers obey delta(E_h)<=n+LW by global telescoping, and every layer also
obeys the elementary bound n(n+1)/2. This supplies a concrete, deliberately
loose constant as well as the asymptotic estimate.

## Published primitive: precise interface

Primary source: Gawrychowski, Gorbachev, Kociumaka, ESA 2025, article 74,
https://doi.org/10.4230/LIPIcs.ESA.2025.74 (CC BY 4.0).

Definition 2.5 uses exactly our density sign and a core of triples (i,j,value),
not a sum of density magnitudes. Definition 3.2 uses exactly the topmost row,
leftmost column, and those triples. The introductory discussion mentions a
different sufficient boundary convention; the formal definition matches ours.

Theorem 1.2 takes condensed p-by-q and q-by-r Monge matrices and computes
the condensed product deterministically in
O(p+q+r+(delta(A)+delta(B)) log(1+delta(A)+delta(B))).
Theorem 1.1 gives delta(A product B)<=2(delta(A)+delta(B)).
Theorem 4.7 adds, within the same construction time, a witness structure of
O(p+q+r+delta(A)+delta(B)) space with query time
O(log(2+delta(A)+delta(B))). Definition 2.3 specifies the smallest minimizing
index, including ties. Fact 4.1 supplies entry queries with logarithmic time.

In our call the dimensions are (n+1)-by-n and n-by-(n+1). Both operands
are contiguous submatrices of E_(h-1), hence their core triples are obtained
by filtering/reindexing, with boundary extraction. The lower triangle is
P(i-j), P=4nM+4W+1. Every entry is an ordinary finite integer; no infinity
or extended-real arithmetic is passed to the primitive. An invalid root
costs at least P, while a valid root pair costs at most nM. All intermediate
core magnitudes may be large; the primitive counts triples rather than mass.
The product core has at most four times the completed input core size.

## Search protocol and what it establishes

`code/core_size_search.cpp` evaluates every partial-tree layer using dense
exact-integer recurrence and counts nonzero densities, including the n
finite-completion entries. A whole-table fixed point allows repeating the
same counts for remaining layers. `code/core_size_search.py` first checks
complete layer vectors against an independent Python implementation, with
exhaustive all-root and all-shape controls on small inputs.

Every search candidate has integer nonnegative weights and total W=n.
Single-unit transfers, larger transfers, swaps, and reversals preserve this
constraint. Simulated annealing explores score plateaus; acceptance uses
floating point only for the search policy, never for cost or density
arithmetic. Seeds, vectors, all layer counts, and operation counters are saved.

The objective is max_h delta(E_h)/(n sqrt(W ceil(log2(n+1)))). A finite
search cannot prove an asymptotic upper bound or its tightness. A pattern
extracted from the winners needs a separate closed-form density proof.
Raw timings are not used.

## Result of the search-directed proof work

The clustered ramp led to the exact W=n odd-ramp family in
[RAMP_CORE_TIGHTNESS.md](RAMP_CORE_TIGHTNESS.md). Its explicit density
2 nu_2(b-2s), on a counted set of nm/16-9n/64-m/4 cells, proves an
Omega(n^(3/2)) intermediate core. Thus a universal n polylog n core bound
is ruled out; the sqrt(log n) gap remains. This conclusion uses the proof,
not a fit to the search's scores.
