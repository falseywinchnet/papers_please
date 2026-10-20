# Implicit ordered references and nonlinear exchange corridors

The full problem retains arbitrary nonnegative weights on keys and gaps at
fixed input positions. This checkpoint proves two further exact constructions
and a maximum-support core example. The general arbitrary-weight subquadratic
objective remains open. Bounds below count arithmetic and comparison
operations; operand bit costs are additional.

## One global shape certificate

Set a=min p, b=min q, and E0=sum(p-a)+sum(q-b). If

    a+b > (n-1)E0,

every interval optimum has minimum internal path length (IPL). The uniform
part costs (a+b)I+(a+2b)m on m keys. A unit IPL increase costs a+b, whereas
the residual-cost difference between two trees is at most (m-1)E0(I).
This also orders fixed-root classes with distinct least IPLs. Uniform inputs
have a direct linear construction, including the all-zero case.

## Interval and root-range oracle without explicit cores

Add the leftward exchange condition, or its reflection, with
h=floor(log2(n+1)):

    max(p_i-p_(i+1), h*(p_i-p_(i+1))) <= q_(i+2)-q_i.

Every interval then has a left-filled minimum-IPL optimum. Its skeleton keys
have comparison lengths h_m-v2(t); expansion changes their positions to
i+t-1+min(s,t). The manuscript gives the full exact interval formula. Expanding
1+v2(t) as a sum of divisibility indicators reduces its evaluation to dyadic
residue-class sums. All stride-prefix arrays take O(nL) preparation and
storage, and an interval query takes O(L), L=ceil(log2(n+1)).

The forced-root child cost is unimodal. Outside the minimum-IPL root plateau,
the baseline certificate orders the costs strictly. Inside the plateau,
moving an expansion from the right child to the next empty left slot is a
sequence of nonincreasing leftward exchanges. Clamping the known left-filled
root to a requested range therefore gives its minimum in O(L). Binary search
finds both endpoints of a threshold set in O(L^2); enumeration adds O(t).

Substitution into the general coarse-regret screen gives O(nL) preparation
and O(nL+V L^2+A L) deterministic additional work for arbitrary original
weights, any positive scale, V reached intervals and A retained root rules.
Balanced endpoint dictionaries account for the A L term. A counted 4nL
budget and exact Knuth fallback include interrupted work. The coarse index
can be reused for unrelated originals. No Monge product or core is built.

## Nonlinear reference corridor

A separate construction fits a strict reference in linear time:

    qbar_j = min q
    pbar_0 = p_0
    pbar_i = max(p_i, pbar_(i-1)+1).

Fit both orientations and choose the smaller error allowance. Let Ep and Eq
be total absolute key and gap errors from the fitted reference. Every
leftward bottom-slot exchange improves reference cost by at least one.
Sorting a shape's expansion word takes exactly its inversion count. Across
minimum-IPL shapes, key comparison lengths vary by at most h and gap lengths
by at most one. Every original class optimum thus has at most

    D = floor(h Ep+Eq)

inversions. A prefix with a used zeros and b remaining ones already commits
to at least ab inversions. Retain precisely the feasible states with ab<=D.
For S=2^h, s=n-S+1 and z=S-s, their number is at most

    S+1+min(s*z, D*ceil(log2(z+1))).

The bound follows by summing min(s,floor(D/a)) over a=1,...,z. Compact
per-layer arrays and a monotone lower-endpoint pointer give constant work
per state, including transition tests; predecessor bytes support full
traceback. Original key and gap costs are used throughout. The shape
certificate makes this class optimum globally optimal. Rejected inputs use
full Knuth after linear checks, preserving O(n^2) worst-case work and space.

For a concrete proved family, take any f_0=0 with increments at least one,
F=sum f, p_i=B+f_i+u_i, q_j=B+v_j, and |u_i|,|v_j|<=U. If

    2B-2U > (n-1)*(F+2U*(2n+1)),

the constructor takes O(n+U*n*log^2(n+1)) work and space, including fitting,
certification and full output. Indeed Ep<=2Un and Eq<=2U(n+1). Independent
errors may occur at every key and gap. The profile can be nonlinear, such as
f_i=i+floor(i^2/n); the implementation requires none of f, B or U as input.
This extends the earlier affine corridor to arbitrary increasing references.

## Exact dense final core

For p_i=B+i, q_j=B, B>=n^3+1, put m=j-i, h=floor(log2(m+1)), c=2^h-1,
s=m-c. Every interior density equals

    2B+i-c+h       when s=0,
    1+v2(s)       when s>0.

All are positive, giving exactly n(n+1)/2 entries in the finite completed
core. Every interval optimum has minimum IPL. Scaling by 1/B puts all weights
arbitrarily close to one while preserving support. The prior ruler theorem
already supplies the qualitative dense-core obstruction; this variant gives
maximum support and exact densities inside the implicit-oracle class.

## Reproduction and independent checks

Run the three commands in the root AGENTS.md. The implementation and audits
are `code/ordered_ranges.py`, `code/ordered_screen.py`,
`code/ordered_range_audit.py`, `code/exchange_corridor.py`,
`code/exchange_corridor_audit.py` and `code/final_core_probe.py`. Completed
records are the three correspondingly named JSON files in `results/`.

The ordered audit checks 7,344 independent root-cost sequences, 17,424
indexed interval values, 44,064 range minima and 44,064 threshold sets.
It checks 144 full arbitrary-original queries and 144 zero-budget fallbacks,
plus 24 larger full Knuth comparisons through n=767. Sparse perturbations
that fail both ordered conditions still complete exact screening.

The corridor audit checks 1,638 literal exchange-regret inequalities, 530
optimal-prefix inclusions, 128 literal class optima, 108 independent cubic
full controls, 84 literal full-tree controls, eighteen rational cases and
forty-two independent Knuth comparisons through n=1,535. Larger complete
runs at 6,143, 24,575 and 98,303 keys use the proved certificate and independent
original-cost traversal, without a quadratic reference run. The largest
retains 5,295,604 states and admits 10,525,670 transitions under a proved
10,026,753-state cap. All fitting, rejected transitions and output work are
counted separately in the record; these are operational counts, not timings.

The dense diagnostic covers 136 instances through n=512. It rejects the
height-only sparse-core proposal and motivates the exact formula above.
All 22 source-hash entries across the three records match the executed
sources. The manuscript keeps measurements in its verification appendix and
the theoretical bounds in the main argument. No priority claim is made.
