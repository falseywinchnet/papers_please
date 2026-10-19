# Exact full mixed OBST by periodic phase

**Theorem.** Let n>=1. Suppose both the key weights and gap weights are
restrictions of nonnegative real sequences with common period b. A complete,
unrestricted-height optimal BST can be constructed in O(nb) arithmetic
operations and O(nb) space. The dynamic program examines exactly b(2n-1)
root candidates, including all synthetic starting phases. Reconstruction
visits n keys and n+1 gaps. The input length need not be a multiple of b.

This is a direct application of Knuth's monotone-root theorem to a cyclic
quotient of interval states. It is independent of the integer-mass theorem
and of the lower-bound certificate. It permits zeros, arbitrary relative
key/gap magnitudes, and arbitrary nonnegative real weights within the period.
Its worst case on arbitrary input remains quadratic: the shortest common
finite period can be n+1. No priority claim is made for the periodic quotient.

## Exact quotient and cyclic amortization

Extend the two period words indefinitely. For phase a in {0,...,b-1} and
length l>=0, write C_a(l) for the exact cost of the interval beginning at
phase a with l keys, and rho_a(l) for its leftmost optimal relative root.
Translation by b preserves every ordered tree's weighted cost. Thus these
states represent all translated intervals exactly, with C_a(0)=0 and

    C_a(l)=W_a(l)+min_(0<=r<l)
             [C_a(r)+C_((a+r+1) mod b)(l-r-1)].             (1)

Compute lengths in increasing order. Knuth's inequalities, using leftmost
roots consistently, restrict the search for l>=2 to

    rho_a(l-1) <= r <= 1+rho_((a+1) mod b)(l-1).          (2)

Both endpoints lie in [0,l-1]. The inequalities are applied in the infinite
periodic extension, so (2) is also valid when a=b-1. Its right neighbor starts
at absolute position b and is a translate of phase zero. Consequently the
number of tested roots, summed over all b phases at a fixed l>=2, is exactly

    sum_a [2+rho_((a+1) mod b)(l-1)-rho_a(l-1)] = 2b.     (3)

For l=1 there is one candidate per phase. Summing (3) gives b(2n-1).
Individual phases need not have a constant-size search range; the proof
uses cancellation around the entire phase cycle. Keeping only the phases
that occur as actual length-l intervals in the finite input would discard
that cancellation. The algorithm deliberately computes all b phases at
every length, including synthetic intervals extending past the input end.

Every candidate lookup in (1) uses a strictly shorter length. One prefix
sum of p_t+q_t on n+b consecutive positions gives

    W_a(l)=prefix[a+l]-prefix[a]+q_((a+l) mod b)           (4)

in constant work. Computing (4) and maintaining a leftmost minimizer adds
O(nb) work. Cost and relative-root tables have (n+1)b entries each.

For reconstruction, an interval [i,j) uses relative root rho_(i mod b)(j-i).
Emit its absolute key index i+rho, then process its two child intervals.
An explicit stack handles even an all-zero input whose leftmost optimum is
a chain; no bounded-height assumption enters. Each key and each empty gap
is visited once. Its directly evaluated weighted depth cost equals C_0(n).
This establishes the full construction bound, including preprocessing and
reconstruction, without computing the ordinary quadratic interval table.

## Detecting the joint period on arbitrary input

A common finite period b means p_i=p_(i-b) for b<=i<n and q_i=q_(i-b)
for b<=i<=n. Vacuous period n+1 always exists. Form the n-symbol signature
word

    (p_i,q_i,q_(i+1)),  i=0,...,n-1.                     (5)

The ordinary prefix-function algorithm finds its shortest finite period
d=n-pi[n-1] in O(n) exact equality comparisons. If d<n, (5) enforces every
required key and gap equality, including the final gap, so b=d. If d=n,
period n is valid precisely when q_n=q_0; otherwise set b=n+1. Conversely
every common period below n is a period of (5), proving minimality.
For b=n+1, use p_n=0 as an unobserved padding key and period words
(p_0,...,p_(n-1),0) and (q_0,...,q_n). The original interval is unchanged.
For n=0 the empty tree has cost zero and is handled separately.

The final gap matters. Checking periodic key weights and only q_0,...,q_(n-1)
can falsely accept a shorter period when q_n differs. Exact recognition
therefore uses both adjacent gaps in (5). No normalization, rounding, or
approximate equality is used.

For fixed b the theorem gives linear full construction; for b=O(n^alpha)
with alpha<1 it gives O(n^(1+alpha)) work. It says nothing subquadratic about
an arbitrary nonperiodic sequence with b=Theta(n).

## Verification and research context

The independent audit exhausts all mixed binary inputs through four keys,
checks every binary key/gap period through length three at several input
lengths, and includes geometric, zero, rational, and final-gap-defect inputs.
All original interval costs and leftmost roots are checked against a fresh
all-root recurrence. A separate extended all-root table checks every synthetic
phase interval used in (3). Literal period enumeration controls (5); small
ordered-tree enumeration is independent of both dynamic programs.

Matched larger instances use the ordinary uncompressed Knuth recurrence.
The largest rows construct complete trees through 262144 keys, traverse
those trees independently, and check the exact candidate identity (3).
Those rows do not claim a quadratic independent optimality reference.
All operation counts and executed-source hashes are retained in
`results/periodic_obst_audit.json`.

The investigation began with above-capacity core searches. A separately
checked 128-key integer input of total key mass 128 has 270 above-capacity
entries at h=5. It refutes coefficient one in K_above<=n+P, not an O(n+P)
claim with an arbitrary constant. Period-three binary probes suggest a
logarithmic number of density diagonals; no asymptotic lower-bound theorem
is inferred from those observations. The periodic full solver follows from
(1)--(3), independently of that unfinished density analysis.

The final audit has 1042 small inputs, 62376 original interval values,
54672 leftmost-root controls, and 38756 synthetic phase controls. Its
all-root references examine 1993994 candidates and 154391 states, and it
independently enumerates 7882 ordered shapes. Twenty matched ordinary
Knuth references through 512 keys examine 1744227 candidates. Sixteen
large complete constructions reach 262144 keys; the period-five mixed
instance examines exactly 2621435 candidates. The separate 128-key
above-core witness uses 1788800 all-root candidates and 41280 states.
