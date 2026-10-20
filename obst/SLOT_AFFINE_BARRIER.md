# Cubic prefix diagrams survive positive affine normalization

Allowing a block to rescale as well as shift does not remove the preceding
actual-prefix size obstruction. An explicit positive mixed family requires
Omega(n^3) distinct final blocks, and Omega(n^4) distinct blocks across
prefix history, even when same-depth functions f and g can share whenever
f=alpha*g+beta for arbitrary alpha>0 and beta. The proof uses three entries
per block. It applies to fixed dyadic blocks; it does not constrain other
representations or unrestricted OBST algorithms.

## A polynomially encoded separating family

For n>=2 put

    A=16n^2+1, e_t=t+2n t^2 (1<=t<=n),
    w_i=A^(e_(n-i)), p_i=w_i-1, q_j=1.

The largest weight has O(n^3 log(n+1)) bits, and the complete binary input
has O(n^4 log(n+1)) bits. The construction uses ordinary finite integers.
As before, common-gap normalization gives w, zero residual gaps, and cost
shift n. Consecutive weights differ by a factor at least A, so
n sum_(j>i)w_j<w_i. The unique optimum is the right chain of necessary
height n. Its cost is n+sum_i(i+1)w_i and it has a linear arithmetic-work
construction and certificate. Bit-operation costs remain separate.

## Quadratic scalar equality implies polynomial equality

All unordered sums e_a+e_b are different. Indeed, equality implies

    a+b-c-d = -2n(a^2+b^2-c^2-d^2).

The left side has absolute value at most 2n-2, hence it is zero. The sums
and sums of squares coincide, so ab=cd and the unordered pairs coincide.

Let u,v,u',v' be integer vectors with coordinates in [-(n-1),n-1].
Consider the homogeneous quadratic polynomial

    P(X)=(u.X)(v'.X)-(u'.X)(v.X).

Every coefficient has magnitude at most 4(n-1)^2: a cross term has four
products, a square term two. After substituting X_i=w_i, distinct monomials
become distinct powers of A. A nonzero coefficient at the highest exponent
has magnitude at least that power, while all lower terms have total
magnitude strictly smaller, because 4(n-1)^2<A-1. Therefore

    P(w)=0  implies  P(X) is identically zero.                 (1)

This is a signed-digit argument; it does not assume transcendental weights
or infer independence from numerical precision.

Suppose additionally u and v are nonzero and linearly independent. Their
linear forms U and V are coprime in Q[X_0,...,X_(n-1)]. If
U V'=U' V, then U divides U'. For nonzero linear U', this forces
U'=lambda U, and substitution gives V'=lambda V. Thus

    (u'.w)/(v'.w)=(u.w)/(v.w)
       implies (u',v')=lambda (u,v),                         (2)

whenever these denominators are nonzero. The same conclusion follows with
numerator and denominator exchanged. Both linear independence and the
bounded-coefficient substitution in (1) are needed for this inference.

## Affine invariants of actual prefix blocks

Use exactly the three addresses and index ranges from
[SLOT_PUNCTURED_BARRIER.md](SLOT_PUNCTURED_BARRIER.md):

    Q=2 ceil(n/2), d0=ceil(log2(Q+1))+2, N=max(0,n-d0),
    d0<=d<=s<n, 1<=r<=min(n-s,k-3),
    t*=1, t-=2^(d-2)+Q, t+=2^(d-1)+Q.

The boundary has r high one bits with its lowest at s. The greedy valuation
vectors v(t) depend only on lexicographic dominance, so all preceding
feasibility arguments still hold for these new weights. Zero-pad them to n
coordinates, and put

    u=v(t+)-v(t-), v=v(t*)-v(t-).

The first nonzero coordinate of u is r and equals one. Also u_(k-1)=0,
while the last nonzero coordinate of v is k-1 and equals -nu_2(Q), which
is nonzero. In particular u and v are linearly independent. Finally
v_r=s-d. All their coordinates have magnitude at most n-1.

For the actual block function f, the three-entry quantity

    R(f)=[f(t*)-f(t-)]/[f(t+)-f(t-)] = (v.w)/(u.w)

is well-defined and invariant under every positive affine transformation.
The denominator is nonzero by lexicographic dominance. If two same-depth
witness blocks have the same R, (1) and (2) imply u'=lambda u and v'=lambda v.
The first nonzero coordinate of each u is one, forcing equal r and lambda=1.
The last nonzero coordinate of v then recovers k; its rth coordinate recovers
s. Thus every (d,s,r,k) witness is different even under affine equivalence.
Depths are part of the fixed-block representation and are counted separately.

## Exact lower bounds and consequence

Let D_k^aff count the nonnull equivalence classes of depth-tagged dyadic
interior blocks in prefix k, allowing arbitrary positive scale and shift.
Let H^aff count their union over all prefixes, also with cross-stage sharing.
The same witness count gives

    D_k^aff >= sum_(t=1)^N (N-t+1) min(t,max(0,k-3)),
    D_n^aff >= binomial(N+2,3) = Omega(n^3),
    H^aff >= (n-2) binomial(N+2,3)-binomial(N+3,4) = Omega(n^4).

These inequalities concern the coarsest exact affine equivalence, whether
or not a particular implementation achieves it. They do not rely on the
cost of canonicalization or on enumerating intermediate representations.
Consequently adding a scalar multiplier to normalized references cannot
supply a universally small diagram for this full mixed-prefix recurrence.
A useful replacement must share more than affine copies of fixed dyadic
blocks, avoid these prefix functions, or exploit additional input structure.

The same lower bounds apply if each block also includes its first address:
affine equivalence of whole blocks would imply affine equivalence of the
three strictly interior test entries. The witnesses are therefore independent
of the earlier first-address representation change.

## Verification

The audit checks distinct quadratic exponents through n=256, then verifies
all small greedy values against the independent dense subsequence recurrence.
Complete original-weight constructions check exact three-entry rational
invariants at every witness, including distinctness across prefix stages.
They also check the coefficient identities, nontrivial affine transformations,
independent Knuth optima and full original-weight trees. No affine solver is
introduced: the existing additive solver supplies exact function values,
while the new invariants test the more permissive equivalence relation.
Finite counts and input bit lengths are retained separately from the proof.
