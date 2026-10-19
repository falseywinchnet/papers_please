# Exact capacity bands for full mixed-weight penalty layers

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. This is an exact component of the full mixed OBST construction.

Let c_h=2^h-1 and fix a nonnegative integer width d. For h=0,...,H, retain
all intervals whose key length k satisfies |k-c_h|<=d, within 0<=k<=n.
With M>HW, every retained terminal-penalty value and a minimizing root can
be computed in O(n(d+1)(H+1)) arithmetic operations and words. For H=O(log n)
this is O(n(d+1) log n). Weights may have arbitrary nonnegative magnitudes.
Array storage is used, so the bound does not assume hashing.

For d>=1, the same data give all ordinary densities with
|j-i-c_h|<=d-1 by four table lookups. In particular, d=1 computes all
capacity-line densities in O(n log n) work over the early layers. This
computes the boundary directly; it does not assume a bound on the remaining
core. The general mixed construction bound is unchanged.

## Closure of the band

At layer h, put a=c_(h-1). A parent has k keys and root split lengths u,v,
where u+v=k-1. Since M>hW, an optimum exposes min(k,c_h) keys: sacrificing
one exposed key adds M and can save at most hW in weighted comparison cost.

If k<=c_h, full exposure requires u,v<=a. Thus

    max(0,k-1-a)<=u<=min(a,k-1).

The two deficits a-u,a-v are nonnegative and sum to c_h-k<=d. Both child
lengths are in the preceding band. If k>=c_h, maximum exposure requires
u,v>=a, so

    a<=u<=k-1-a.

The two excesses u-a,v-a sum to k-c_h<=d, again keeping both children in
the preceding band. Every split in these ranges attains maximum exposure.
Consequently the restricted recurrence equals the full terminal-penalty
recurrence on every retained state. At h=0, initialize A_0(i,i+k)=Mk for
k<=d. Empty intervals always have value zero.

## Monotone roots and total candidate work

For each h, compute lengths increasingly from k_min=max(1,c_h-d) to
k_max=min(n,c_h+d). On the first diagonal, examine every maximum-exposure
split. Its range has at most d+1 roots, so all first-diagonal states cost
O(n(d+1)). No values just outside the band are required.

On every later diagonal, restrict to the intersection of the feasible split
range and

    R_h(i,j-1)<=r<=R_h(i+1,j),

where R_h is the leftmost minimizing root. These roots are already stored
on the preceding length diagonal.

For completeness, this monotonicity follows from the Monge property of
A_(h-1). For r<s, increasing j increases the cost difference between root r
and root s, by the Monge inequality on rows r+1,s+1. Increasing i also
increases that difference, by the inequality on columns r,s. Thus a leftmost
minimizer cannot move left when either interval endpoint increases. The
interval-weight term is common to all roots and does not affect the choice.
The roots of the restricted maximum-exposure recurrence are the same roots
as in the unrestricted penalty recurrence.

At a fixed length k, write b_i=R_h(i,i+k-1). The total width of the
unclamped candidate ranges is

    sum_i (b_(i+1)-b_i+1) <=2n.

Intersecting with feasibility only decreases the work. There are at most
2d further length diagonals. Hence the entire layer takes O(n(d+1)) work.
The concrete audit checks the bound n(d+1)+2n(k_max-k_min) on root candidates
for every computed layer. Prefix sums, base entries, and all allocations fit
the same asymptotic bound.

The implementation retains all layer values and roots in arrays, using
O(n(d+1)(H+1)) words. For a retained fully exposed interval, following its
roots reconstructs every original key in O(k) work. Closure guarantees that
every needed child state is stored. A prescribed height is still a constraint:
the component reconstructs its exact height-limited optimum, and unrestricted
optimality requires an adequate height bound or a separate certificate.

## Relation to the existing slot constructor

The slot constructor solves one full height-limited instance in O(n(r+1))
work for its capacity deficit r. The band computation instead shares work
across every start position, every retained length, and every layer. Its
O(n(d+1)H) bound computes an entire family of interval values and densities;
it is not a faster replacement for the single-instance slot bound.

## Independent evidence

`code/check_capacity_band.py` compares every retained entry against an
independent all-root recurrence on exhaustive mixed binary inputs through
three keys, seeded integer inputs, and geometric inputs through 32 keys.
It verifies reconstructed original-weight costs, including nonperfect sizes.
Scale rows use near-uniform strictly positive mixed weights and record states,
root candidates, initialization, and output separately. Their independent-
reference flags are false: the large rows check reconstruction and counters,
while the proof establishes optimality. Results and executed-source hashes
are in `results/capacity_band.json`.
