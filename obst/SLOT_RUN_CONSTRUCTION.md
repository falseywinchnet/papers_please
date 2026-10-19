# Finite Monge slot windows and complete prescribed-height construction

Fix h>=1, c=2^h-1, and v(t)=nu_2(t) for 1<=t<=c. Partition an input
sequence of nonnegative key weights into r constant runs (w_l,m_l),
including zero-weight runs. Put P=sum_l w_l m_l and K=1+(h-1)P.
All assertions use exact arithmetic; weights may be nonnegative reals.

## A directly available finite factor

For slot boundaries 0<=a,b<=c define

    Q_l(a,b) = K max(m_l-b+a,0)
               - w_l sum_(t=1)^(h-1)
                    min(m_l, floor(b/2^t)-floor(a/2^t)).          (1)

The signed counts in (1) define the entire square, including a>b. If
b-a>=m_l, the penalty vanishes and the threshold identity for order
statistics shows that Q_l is the negative maximum reward of m_l equal
weights placed in slots (a,b]. A threshold contributes once for every
chosen slot whose valuation reaches it, up to the run length.

**Factor lemma.** Q_l is finite Monge. In the convention
D_Q(a,b)=Q(a,b+1)+Q(a+1,b)-Q(a,b)-Q(a+1,b+1), its nonzero densities are:

* K at b-a=m_l, for 0<=a<c-m_l;
* w_l at (a,b)=(kd-1,(k+m_l)d-1), where d=2^t, 1<=t<h,
  and 1<=k<=floor(c/d)-m_l, omitting zero weights.

The first assertion is the four-corner difference of a one-sided hinge.
For one threshold put x=floor(b/d)-floor(a/d). A mixed difference is zero
unless a+1 and b+1 are both multiples of d. When both are multiples, it is
w_l[2 min(m_l,x)-min(m_l,x-1)-min(m_l,x+1)], which equals w_l precisely
when x=m_l, and is zero otherwise. This proves the formula even in the
infeasible region. Different powers d cannot coincide because b-a=m_l d;
they cannot coincide with the hinge because d>=2 and m_l>=1. Thus

    delta(Q_l) <= max(0,c-m_l)
                    + sum_(t=1)^(h-1) max(0,floor(c/2^t)-m_l)
                < 2c.                                         (2)

Its condensed form is available in O(c) work and words. Let
F(a)=sum_(j=1)^a v(j). The left boundary is K(m_l+a)+w_l F(a).
For the top boundary, maintain sum_t min(m_l,floor(b/2^t)) as b increases.
Only thresholds t<=v(b) can change, and each changes by one precisely
when b/2^t<=m_l. The total threshold visits are sum_b v(b)=c-h<c.
The density coordinates above are generated directly; two bucket passes
order them in linear work. No dense matrix is constructed. This also
covers m_l>c, when the whole factor is a sum of row and column terms.

## Balanced composition, finite penalties, and witnesses

**Product theorem.** Let T=Q_1 tensor ... tensor Q_r, using min-plus
multiplication. For every b-a>=n=sum_l m_l,

    T(a,b) = -max_(a<t_1<...<t_n<=b) sum_i w_i v(t_i).             (3)

The product is finite Monge, has at most
2 r 2^ceil(log2 r) c <= 4r^2 c core entries, and has a condensed
construction in O(n+r^2 c log(c+1)) arithmetic operations.

A feasible product path has b_l-a_l>=m_l at every factor. It partitions
(a,b] into consecutive windows and assigns all m_l keys of a run to that
window. Conversely any increasing all-key selection can be partitioned
between runs: put each internal cut at the last selected slot of the
preceding run, and let the final run absorb the unused suffix. Thus the
feasible product paths give exactly the optimization in (3).

Every infeasible path incurs at least K penalty, since all boundaries
are integers and some deficit is at least one. Each threshold minimum is
at most m_l, including when its argument is negative. Hence the total
negative reward is bounded below by -(h-1)P on every path, even one that
moves backward. Its cost is at least K-(h-1)P=1. Every feasible path has
cost at most zero. This proves strict exclusion, for zero weights and ties
as well as for positive weights. The product's other entries are its
specified finite completion; no selection meaning is needed there.

The published core-sparse Monge product of Gawrychowski, Gorbachev and
Kociumaka (ESA 2025, Theorems 1.1, 1.2 and 4.7 as audited in CORE_SIZE_AUDIT.md)
applies to these finite real matrices and gives

    delta(X tensor Y) <= 2(delta(X)+delta(Y)).

In a balanced product tree, each leaf's core is amplified by at most
2^ceil(log2 r), proving the bound. At depth j from the root there are
at most 2^j nodes, each with at most ceil(r/2^j) leaves; summing the
resulting quadratic bounds over j gives O(r^2 c) total core size. The
O(rc) matrix-boundary terms also fit. With dimension c+1, the published
multiplication logarithm is O(log(c+1)). Run extraction costs O(n).
This is an application of the published primitive, not a new multiplication
algorithm. Ordinary witness arrays in the implementation give the
conservative auxiliary-space bound O(r^2 c log(c+1)).

Retain the product witnesses. From a feasible queried entry, recursively
recover each factor's two boundaries; the penalty proof guarantees that
all resulting windows are feasible. In a leaf window choose the m_l
largest valuations, taking earliest positions at a tied cutoff. Bucketing
by valuations takes O(window length+h). Leaf windows are disjoint and
partition the outer window. Thus leaf selection takes O(c+rh), and the
r-1 witness queries take O(r log(c+1)); both fit the construction bound.
The existing slot-deletion repair constructs a height-at-most-h tree in
O(c+n) work. Equality of the slot minimum and tree minimum proves that
repair preserves the optimum.

## Arbitrary keys with equal internal gaps

**Full prescribed-height construction.** Suppose n>=2, the internal gaps
q_1,...,q_(n-1) have common weight b>=0, and q_0,q_n and all keys are
arbitrary nonnegative weights. Define

    w_0 = p_0+q_0,
    w_i = p_i+b,             1<=i<=n-2,
    w_(n-1) = p_(n-1)+q_n.                                   (4)

For every tree T, with key comparison lengths ell_i,

    C_(p,q)(T) = sum_i w_i ell_i + bn.                         (5)

Indeed the total external path length is E=I+2n=sum_i ell_i+n.
The two endpoint gaps have depths ell_0 and ell_(n-1). Subtracting their
contributions from bE and replacing them by q_0 ell_0 and q_n ell_(n-1)
gives (5). All transformed weights are nonnegative, including when an
endpoint gap is smaller than b. For n=1 the cost is p_0+q_0+q_1.

For prescribed h with c>=n, apply (3) to (4), trace its optimal slots,
and repair. Its original mixed cost is

    h sum_i w_i + T(0,c) + bn.

If r is the number of transformed constant runs, the complete construction,
including preprocessing and output, uses O(n+r^2 c log(c+1)) operations
and O(r^2 c log(c+1)) auxiliary words with the implemented witnesses.
If the original keys have r_0 runs, r<=r_0+2. In particular the minimum
feasible height h=ceil(log2(n+1)) has c<2(n+1), giving
O(n+r^2 n log(n+1)) construction at that prescribed height.

This theorem optimizes over trees obeying the given height limit.
Unrestricted optimality requires a separate height certificate. The
factor c=2^h-1 is explicit; substituting a much larger sufficient height
does not yield a general subquadratic bound. The main arbitrary mixed
integer-mass result and the open original interval-core size hypothesis
are unchanged.

## A single internal gap has a dense signed slot transition

For consecutive selected slots u<v, an internal gap of weight q>0 adds

    B_q(u,v) = -q min(v(u),v(v))

to the minimization objective. Let e(u)=u+(u mod 2), the even member of
{u,u+1}. On every density cell with u+1<v and v+1<=c,

    D_B(u,v) = (-1)^(u+v) q min(nu_2(e(u)),nu_2(e(v))).          (6)

Each adjacent pair has one odd slot of valuation zero and one even slot
of positive valuation. Precisely one of the four B entries is nonzero.
Its coefficient in the density expression is positive when u,v have the
same parity, negative otherwise, which proves (6).

For any power of two s>=2 choose c=4s-1 (h=log2 s+2), rows 1<=u<=s
and columns 2s+1<=v<=3s. Every cell and all its corners are feasible.
There are exactly s^2 nonzero densities, half positive and half negative,
already at q=1. Thus no Monge or anti-Monge completion preserving these
feasible entries exists. Adding row or column potentials cannot change
this conclusion. An explicit representation listing nonzero signed second
differences has quadratic size on these coordinates.

This is a barrier for the natural consecutive-slot transition, not for
original interval cores or for every possible representation. In particular,
the equal-internal-gap transformation (4) removes all such pair terms by
a global tree identity. The original single-gap interval core has its
separate sparse classification. The checkerboard does not conflict with it.

## Reproducible audit

`code/slot_run_audit.py` first compares every finite product entry with an
independently evaluated dense product, including the infeasible completion.
Feasible entries additionally have a separate subsequence DP and literal
subset enumeration. Fractional, overlong single runs check the factor
formula outside the feasible domain. The complete constructor is checked
against original all-root height layers and independently evaluated output
trees. A separate four-corner audit checks (6). Larger rows construct full
trees with uniform and three-run keys; only the uniform rows have an
independent closed-form optimum. Exact counts and executed-source SHA-256
hashes are in `results/slot_run_audit.json`; no elapsed times support a claim.
