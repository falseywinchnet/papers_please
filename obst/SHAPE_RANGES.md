# Sharp shape stability from key and gap ranges

This result concerns full static OBST with arbitrary nonnegative weights on
both keys and gaps, at their fixed ordered positions. It supplies a linear
certificate for a globally optimal shape class and an exact worst-case
threshold for perfect sizes. It does not solve arbitrary-profile construction.

## Universal shortening capacities

Let L=ceil(log2(n+1)), K=2^L-L-1, and G=2^(L-1) for L>=2 (G=0 for n=1).
For every tree T, the total positive shortening of key comparison lengths
relative to L is at most K. At level t, there are at most 2^t-1 keys with
comparison length at most t; sum over t=1,...,L-1.

The corresponding gap shortening is at most G. For integer u>=1,
u<=2^(u-1), so each gap at depth d<L contributes at most
2^(L-1)*2^(-d). Kraft equality bounds the sum by G.

Set a=min p, b=min q, P=max p-a, Q=max q-b. Every minimum-IPL tree S has
all comparison lengths at most L. A competing tree T with integer excess
e=I(T)-I_min>=1 consequently satisfies

    C(T)-C(S) >= (a+b)*e - P*K - Q*G.

Thus a+b>=P*K+Q*G certifies that optimizing the minimum-IPL class yields a
full unrestricted optimum. Equality is sufficient. The certificate costs
O(n) and may be combined with previous sufficient certificates.

## Exact threshold at perfect sizes

For n=2^h-1, h>=2, the perfect tree is optimal for EVERY assignment in

    p_i in [a,a+P], q_j in [b,b+Q]

if and only if

    a+b >= (n-h)*P + Q.

This is a universal statement about the entire box, not a necessary
condition for any particular input to have a perfect optimum. At n=1
there is only one possible tree.

To prove the sharper gap coefficient, put k_j=d_j-h and write
A=sum(-k_j)_+, Z=sum(k_j)_+. Kraft equality implies

    sum_(k<0) (2^(-k)-1) = sum_(k>0) (1-2^(-k)).

The left side is at least A and the right side at most Z/2, hence Z>=2A.
External and internal path lengths differ by 2n, so the excess is
Z-A>=A. A competing tree's gap shortening is therefore at most its
excess e, while key shortening is at most n-h. Its cost relative to the
perfect tree is at least (a+b-Q)e-P(n-h), proving sufficiency.

For necessity, start with the perfect tree, delete its greatest leaf key,
and insert a new least key as the left child of its least surviving key.
Relabel in order. The deletion removes a key at internal depth h-1 and
the insertion adds one at depth h, giving exactly one unit of excess.
Its key comparison lengths are h+1 at index zero and h-v2(i) for i>=1.
Its first two gaps have depth h+1, its last has depth h-1, and all others h.

Give residual weight P to even key indices i>=2 and zero to other keys;
give residual weight Q only to the final gap. The selected keys shorten
by sum_(i=1)^(2^h-2) v2(i)=n-h, and the selected gap by one. The exact
cost difference is a+b-P(n-h)-Q. It is negative below the stated threshold.
This proves sharpness simultaneously in both key and gap ranges.

At perfect sizes, scanning the input and building the perfect tree is a
complete O(n) exact constructor whenever the certificate passes. A failed
certificate permits an exact fallback; it does not prove that this input's
perfect tree is suboptimal.

## Weaker baseline for nonlinear reference corridors

For p_i=B+f_i+u_i and q_j=B+v_j, assume f_0=0, f_(i+1)-f_i>=1,
|u_i|,|v_j|<=U, and nonnegative input weights. Write M=f_(n-1). The new
sufficient baseline condition is

    2B-2U >= (M+2U)*K + 2U*G.

For example, B=n*(M+4U)+U+1 suffices. The same automatic nonlinear
prefix-envelope fit from ORDERED_REFERENCE.md has Ep<=2Un and Eq<=2U(n+1).
Thus the complete construction still takes O(n+Un log^2(n+1)) arithmetic
work and space, including certification, fitting and reconstruction.
For f_i=i+floor(i^2/n) and fixed U, the sufficient baseline is now O(n^2),
whereas the preceding total-residual-mass condition requires order n^3.

The implementation is `code/range_exchange.py`. It scans the range and
mass thresholds, adds the sharp threshold at perfect sizes, constructs the
perfect tree directly when appropriate, and otherwise invokes the existing
original-cost corridor after acceptance. Rejection uses full Knuth.
The entire constructor has O(n^2) worst-case arithmetic work and space.
Operand bit costs are separate. The all-interval query oracle still uses
its own hypotheses; this new certificate concerns full shape optimization.

## Independent audit

`code/shape_range_audit.py` was authored and its independent claims run before
the optimized wrapper existed. It checks 6,917 literal tree capacity bounds,
435 perfect-size gap charges, and 33,304 box vertices through seven keys.
The sharp witness has 135 exact identity checks through 65,535 keys; 54
boundary cases also have independent Knuth controls and full solver checks.
Full construction has 576 cubic controls, including 96 rational cases,
144 literal full-tree controls and 28 larger Knuth comparisons through
1,535 keys. Fourteen curved/reflected cases fail the earlier mass gate
and pass the new range gate. Large runs through 98,303 keys use the proved
certificate and full original-cost traversal, not a quadratic reference.
The complete record is `results/shape_range_audit.json` with source hashes.

All state counts are operational evidence; asymptotic and threshold claims
follow from the proofs. The exact universal threshold is a shape-preservation
barrier, not an unrestricted computational lower bound. No priority claim
is made for Kraft equality, depth-capacity arguments or these derived bounds.
