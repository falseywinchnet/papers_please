# Exact full mixed OBST under positive affine translation

**Theorem.** Let n>=1 and let all original key and gap weights be
nonnegative. Suppose 1<=b<=n, lambda>0, and alpha satisfy

    p_(i+b)=lambda*p_i+alpha       (0<=i<n-b),
    q_(j+b)=lambda*q_j-alpha      (0<=j<=n-b).             (1)

A full unrestricted optimal BST, and constant-time access to every interval
cost and its leftmost optimal root, can be constructed in O(nb) arithmetic
operations and space. The smallest admissible b and a witness lambda,alpha
can be found within the same O(nb) bound. No positivity of a hypothetical
infinite continuation is required.

The original periodic theorem is lambda=1,alpha=0. Pure geometric block
scaling has alpha=0; opposing arithmetic drifts have lambda=1. Both key and
gap weights may vary at every position. The construction uses Knuth's
established root inequalities, with a cost transformation that preserves
all minimizing shapes. It does not claim a new monotone-root theorem or
priority for special geometric cases. Arbitrary inputs admit b=n, which
recovers a quadratic worst-case bound.

## Shape-independent cost transformation

For a tree on ell keys, let I be its internal path length. The sum of key
comparison lengths is I+ell and the sum of gap depths is I+2ell. The second
identity follows by induction: joining two subtrees increases internal path
length by ell-1 and external path length by ell+1. Their difference is 2ell.
Therefore replacing every key weight by lambda*p+alpha and every gap weight
by lambda*q-alpha changes every shape cost by the same affine rule:

    cost_new(T)=lambda*cost_old(T)-alpha*ell.              (2)

Positive lambda preserves the complete set of minimizing shapes, including
leftmost root ties. Thus translation by b in (1) gives

    C(i+b,j+b)=lambda*C(i,j)-alpha*(j-i).                 (3)

Define P_k=lambda^k and G_k=sum_(t=0..k-1)lambda^t, including P_0=1,G_0=0.
Tabulate these in linear work by multiplication and addition; no division
by lambda-1 is used. For i=a+kb, 0<=a<b,

    C(i,i+ell)=P_k*C(a,a+ell)-alpha*ell*G_k,              (4)

whenever both intervals lie in the input. Their leftmost relative roots
are equal. All intermediate translations also lie inside the input.

## Finite phase cycles and the terminal lengths

Put m=n-b+1. For every 1<=ell<=m, all b phase intervals [a,a+ell),
0<=a<b, are genuine input intervals. Store their exact costs C_a(ell)
and leftmost relative roots rho_a(ell), starting with C_a(0)=0.
At length ell, evaluate the ordinary root recurrence, retrieving child
values through (4). Each child is shorter, so its phase state already exists.
Actual prefix masses provide W(a,a+ell) in constant time.

For ell>=2, Knuth bounds the relative root by

    rho_a(ell-1) <= r <= 1+rho_((a+1) mod b)(ell-1).       (5)

When a=b-1, the right neighbor begins at b. Its cost is an affine transform
of phase zero, so its relative minimizer is exactly rho_0(ell-1). This
neighbor ends at b+ell-1<=n. Every use of Knuth is consequently on actual
nonnegative input weights. The inclusive widths telescope around the cycle:

    sum_a [2+rho_((a+1) mod b)(ell-1)-rho_a(ell-1)] = 2b.

Including the first length, phase computation examines exactly b(2m-1)
root candidates.

For ell=m+1,...,n, only t=n-ell+1<b input intervals exist. Compute these
last b-1 diagonals directly using ordinary Knuth bounds. If rho_i denotes
the relative root of [i,i+ell-1), their total candidate count is

    2t+rho_t-rho_0 <= 2t+ell-2 = 2n-ell.                 (6)

Here rho_0,rho_t are both in [0,ell-2]. Summing (6) bounds all terminal
candidates by

    (b-1)n+(b-1)(b-2)/2.                                (7)

They store exactly b(b-1)/2 nonempty states. Child lookups use (4) for
lengths at most m and the stored terminal diagonal otherwise. The total
number of nonempty stored states is exactly

    bm+b(b-1)/2 = nb-b(b-1)/2 <= nb.                     (8)

Equations (5)--(8) prove the O(nb) work and space bounds. Prefix sums,
power/geometric-sum tables, and an explicit-stack reconstruction add O(n).
An original interval of length at most m uses its phase's relative root;
a longer interval uses its stored absolute root. Every original key and
gap is emitted once. Zeros and height-n optimal chains are included.

The terminal treatment matters. For example, b=2, lambda=1, alpha=1,
p=(1,2,2,3,3), q=(2,2,1,1,0,0) is a valid nonnegative input. Continuing
the pattern would create a negative gap. The proof computes complete phase
cycles only through m=4, then computes the single remaining length from
the actual input. It never imports nonnegative-weight monotonicity from
an invalid continuation.

## Exact recognition without asymptotic overhead

For a proposed b<n define X_i=p_i+q_i and Y_i=p_i+q_(i+1). Condition (1)
implies X_(i+b)=lambda*X_i and Y_(i+b)=lambda*Y_i. Conversely, these
proportionality equations imply (1): write e_j=q_(j+b)-lambda*q_j. The two
sums imply p_(i+b)-lambda*p_i=-e_i=-e_(i+1), so all e_j are equal and
alpha=-e_0. The final gap is part of Y_(n-1).

A positive source component fixes lambda by its target/source ratio. A zero
source requires a zero target; a positive source with zero target rejects
positive lambda. Check all components and then both original sequences.
If all paired components are zero, choose lambda=1; nonnegativity makes
all constrained weights zero, so alpha=0 works. This is a complete O(n)
feasibility test for each b. Exact integer/rational inputs use exact ratios.

For b=n there are no key comparisons and only q_n=lambda*q_0-alpha;
lambda=1,alpha=q_0-q_n always works. Test b=1,2,... until the first success
b_*. At most b_* linear scans are performed. The smallest affine period and
full construction therefore take O(nb_*) work together, with no logarithmic
recognition overhead. An optional capped scan may fall back to b=n, but the
default implementation performs the complete search.

For b=1, the solver uses exactly 2n-1 root candidates and no terminal
diagonals. In particular, p_i=i+1 and q_j=n+1-j are strictly positive,
nonconstant mixed weights with lambda=1,alpha=1. Their total mass is
(n+1)^2. The complete optimum is constructed in O(n) operations on
O(log n)-bit words. Pure geometric inputs also have linear arithmetic
work when b is constant, but their exact input and output bit lengths may
grow with n; no linear bit-complexity claim follows.

The general central-oracle composition lemma also applies: an affine-period
middle of length m and parameter b, with d arbitrary fringe keys, gives
O(mb+nd+n) full construction. The implementation audited here is the global
affine-period constructor; this last statement follows from the established
boundary extension theorem. Arbitrary interior changes remain unresolved.

## Independent verification and research context

The harness first enumerates tree shapes to test (2), independently of the
solver. It then checks every original interval and leftmost root against a
fresh all-root recurrence, including every finite phase and terminal state.
An independent two-variable linear-system solver checks period feasibility;
this uses the original p/q equations rather than the adjacent-sum detector.
Negative hypothetical continuations have explicit controls. Larger matched
cases use ordinary Knuth; the largest rows reconstruct and independently
traverse complete trees, with their reference scope labeled separately.

The result record is results/affine_period_audit.json. It retains the seed,
operation counts, costs, scope of each row, and executed-source hashes.
Targeted literature searches did not locate a directly applicable primary
statement for this finite affine mixed-weight quotient; that is not a claim
of priority or an exhaustive literature result. The proof uses the standard
external/internal path-length identity and Knuth's root theorem explicitly.
The general core-size gap and arbitrary-input subquadratic objective remain
open.
