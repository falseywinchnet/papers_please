# Full mixed boundary mass and why its magnitude can mislead

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. The full mixed-weight objective is retained throughout.

## Exact identity for arbitrary nonnegative weights

Use zero-based keys p_0,...,p_(n-1), gaps q_0,...,q_n, totals P=sum p,
Q=sum q, W=P+Q. Fix h>=1, c=2^h-1<=n, and M>hW. Let v(t)=nu_2(t).
For 0<=i<n-c define

    G_i=max_(0<=r<=(c-1)/2) [q_(i+2r+1)
             +sum_(l=1)^r v(2l)(p_(i+2l)-p_(i+2l-1))],
    B_tail=sum_(t=1)^c p_(n-c+t-1) v(t).

The ordinary density mass strictly below the capacity line is exactly

    S_h=(h-1)P+(h-2)Q+q_0+q_n+sum_i G_i-B_tail.            (1)

This includes h=1 and c=n and holds for arbitrary nonnegative real weights.
It reduces to the previous gap-only identity when p=0.

Proof: a c-key interval is forced to be perfect. In the slot formula for
its final c-1 keys, omitting slot t=1 leaves key reward
B_i=sum_(t=1)^c p_(i+t-1)v(t), since v(1)=0. Moving the omitted slot to t
changes that reward by

    sum_(k=1)^(t-1) p_(i+k)(v(k)-v(k+1)).

An even omitted slot cannot beat the preceding odd omitted slot: the added
term is nonpositive and the preceding odd choice also earns a nonnegative
gap reward. At odd t=2r+1 the key change groups into the sum defining G_i,
and its one gap reward is q_(i+2r+1). Thus

    A_h(i+1,i+c)=h W(i+1,i+c)-B_i-G_i.

For h=1 the interval is empty, B_i=0 and G_i=q_(i+1), so this holds directly.
Since A_h(i,i+c)=hW(i,i+c)-B_i, the sum of below-capacity densities in row i
is h(p_i+q_i)+G_i-(p_i+q_i+q_(i+1)). The remaining triangular corner has
mass A_h(n-c,n)-sum_(i=n-c)^(n-1)(p_i+q_i+q_(i+1)). Its perfect-tree reward
is B_tail. Addition proves (1). Every term has an explicit mathematical
definition; the identity does not depend on a particular implementation.

## Bounded positive weights give quadratic mass but a small core

Let n=2^s>=16, h=s-1, c=n/2-1. More generally take

    p_i=a+1 for even i, p_i=a for odd i; q_i=b,

where a,b are nonnegative integers. For even i the prefix walk in G_i is
increasing; for odd i it is decreasing. Because sum_(l=1)^((c-1)/2) v(2l)
=c-h, we get G_i=b+(c-h) for even i and G_i=b for odd i. The tail starts
at odd n-c, so B_tail=(a+1)(c-h). Substitution gives

    S_h=n^2/8+n(h-3)/4+(a+b)((h-1)n+h-c).                  (2)

In particular, a=b=1 gives strictly positive weights in {1,2} and
W=5n/2+1, yet S_h=Theta(n^2).

The quadratic term is concentrated. The ordinary densities on the immediately
lower diagonal are

    D_h(i,i+c-1)=c+1-h for even i, and zero for odd i.       (3)

There are n/4+1 nonzero entries there, of total mass

    J_h=(n/4+1)(n/2-h).

For (3), put m=2^(h-1). At lengths c-1 and c-2, alternating keys admit a
minimum-IPL tree assigning the high keys to the shortest available comparison
lengths, as in the proved alternating-profile corollary. The cost is the
uniform (a,b) baseline plus K(H), where K(H)=sum_(r=1)^H bitlength(r).
The baseline has zero density at the even length c-1. At length c, a high-first
perfect interval has incremental high-key cost hm; a low-first one has K(m-1). For an
even row the four-corner difference is

    hm+K(m-2)-2K(m-1)=2m-h=c+1-h,

using K(m-1)=(h-2)m+1 and K(m-2)=K(m-1)-(h-1). An odd row gives zero.

For intervals of length at least c+1, a contiguous c-key subsequence starting
with a low key puts every high key at an even skeleton rank. It attains the
maximum reward (a+1)(c-h). Thus above-capacity densities vanish except at
length c+1, where odd rows have density c-h and even rows have zero.

Subtracting (3)'s diagonal from (2) leaves exactly

    S_h-J_h=n(2h-5)/4+h+(a+b)((h-1)n+h-c).                 (4)

For a=b=1 this is O(nh). Integer densities off that diagonal therefore
have O(nh) support. The removed diagonal, the capacity line, the sole
above-capacity diagonal, and the completion each contribute O(n) entries.
The entire completed core in this layer is O(n log n), despite its
quadratic below-capacity mass. This is a barrier to replacing core support
by unrestricted global density mass. It is not a lower bound on core size
or on OBST running time.

## A more focused tail question

The explicit family suggests removing a narrow band around capacity before
using mass to bound support. Define

    T_(h,d)=sum D_h(i,j) over 0<=i<j<n with |j-i-c|>=d,
    L=ceil(log2(n+1)), d>=1.

A candidate bound is T_(h,d)=O(W(L+c/d)) for early layers c<n. This is
**unproved**. The probe evaluates exactly this ratio on mixed fixtures and
fixed-mass searches. It supplies direction only. If proved uniformly, charging
O(nd) entries to the excluded band and choosing d near sqrt(Wc/n) would give
per-layer support O(n+WL+sqrt(nWc)) in the relevant range, closing the current
sqrt(log n) loss after summing layers at W=O(n). Neither this consequence nor
the candidate bound is claimed as an achieved result.

A simplistic unit-by-unit subadditivity proof is already false away from the
boundary: at h=2, two adjacent unit keys create a length-one density of one,
where either key alone gives zero. The proposed WL term must account for
such interactions; independent one-outcome bounds alone do not suffice.

## Independent evidence

`code/mixed_boundary_mass.py` checks 308 inputs with its independent all-root
reference, including every mixed binary vector through three keys, seeded
arbitrary integer weights, and alternating families through n=128. It checks
756 mass identities, 6656 one-missing-slot formulas, 3376 lower-neighbor
densities, 136680 above-capacity densities, and 80 family mass formulas.
Reference work is 369396 states and 13048220 candidate roots. Executed-source
hashes and exact family rows are in `results/mixed_boundary_mass.json`.
The separate tail probe and its source-hashed results retain the unproved
candidate expression explicitly.

The retained tail probe uses 981 evaluations and 105 all-root controls. It
records 16327392 states, 32066815 root candidates, and 16062720 density checks.
Its largest tested ratio is 342/151, at n=255, W=1, h=7, c=127, d=3,
with outside mass 114. This finite maximum supplies no universal constant
and no asymptotic certification.
