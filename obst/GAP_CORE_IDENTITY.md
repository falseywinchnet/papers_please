# Gap-only density mass and the sharp binary leading term

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. This is a control theorem for the full mixed-weight core
investigation; the full mixed-weight construction and its bounds remain the
main result. No new alphabetic-tree construction claim is made.

## Exact mass identity

Let all key weights be zero. Fix a penalty layer h>=1, capacity c=2^h-1,
and penalty M>hW. Write A(i,j) for its interval cost, and

    D(i,j)=A(i,j+1)+A(i+1,j)-A(i,j)-A(i+1,j+1).

Suppose c<=n. For 0<=i<n-c define

    Q_i=max(q_(i+1),q_(i+3),...,q_(i+c)).

Then all densities strictly above the capacity line vanish, the n-c densities
on it equal M-Q_i>0, and the total density mass strictly below it is exactly

    S_h=(h-2)W+q_0+q_n+sum_(i=0)^(n-c-1) Q_i.                 (1)

An empty sum is zero. These identities hold for arbitrary nonnegative real
gap weights, including c=1 and c=n.

**One missing slot.** At length c the perfect tree is forced, so A(i,i+c)
is h times the interval gap mass. At length c-1, the slot representation
selects all but one of the c perfect slots. Removing an even slot leaves
all gap rewards zero. Removing an odd slot produces exactly one reward,
equal to the weight of the corresponding even-indexed gap of this interval:
its two neighboring valuations have minimum one, or its single endpoint
neighbor has valuation one. Thus

    A(a,a+c-1)=h sum_(t=a)^(a+c-1) q_t
               -max(q_a,q_(a+2),...,q_(a+c-1)).             (2)

For h=1 the interval is empty and (2) reads q_a-q_a=0, so it remains valid
without a neighboring selected slot. Above capacity, the exposed perfect
skeleton sends every gap to depth h; its cost is M(k-c)+h times gap mass.
Four-corner subtraction therefore gives zero strictly above capacity and
M-Q_i on the capacity line.

**Telescoping below capacity.** For each i<n-c, sum the densities over
j=i+1,...,i+c-1. The sum is

    A(i,i+c)-A(i+1,i+c)-A(i,i+1)
      =h q_i+Q_i-(q_i+q_(i+1)).

The remaining triangular corner starts at n-c and has total density mass
A(n-c,n)-sum_(i=n-c)^(n-1) A(i,i+1). Its full interval has length c and
hence perfect-tree cost. Adding cancels all internal boundary terms and
gives (1). This is also valid when the row sums are empty.

For nonnegative integer gaps, write
X_h=sum_(j-i<c) max(D(i,j)-1,0). The completed core includes n diagonal
entries, so its exact size is

    delta(E_h)=2n-c+S_h-X_h.                                 (3)

Here E_h denotes the completed matrix. In particular,
for binary gaps, Q_i<=1 gives

    delta(E_h)<=3n-2c+(h-2)W+q_0+q_n.                       (4)

For c>n, ordinary whole-triangle telescoping instead gives total density
mass A(0,n)-sum_(i=0)^(n-1)(q_i+q_(i+1)).

## Sharp leading term at fixed binary mass

Let n=2^s, s>=4, and let q be binary with W=n/2. For every layer, including
layer zero,

    delta(E_h) <= (s+1)n/2+4.                               (5)

For 1<=h<=s, insert c=2^h-1 into (4) and use q_0+q_n<=2. The resulting
bound U(h) has difference U(h+1)-U(h)=n/2-2^(h+1). Its maximum occurs at
h=s-2 and h=s-1, giving (5). Layer zero has core n. For h>=s+1, a
minimum-internal-path-length tree has n-1 keys in a perfect skeleton and
one bottom cherry. All gaps have depth s except the two cherry gaps, which
have depth s+1. Thus A(0,n)<=sW+2. Whole-triangle telescoping gives a
completed core of at most sn/2+4, smaller than (5).

The leading term is attained by an explicit fixed-mass family: q_i=1 for
even i<n, q_i=0 for odd i and for i=n. Choose h=s+1. Every interval not
containing the last gap has strictly alternating gap weights. If it has k
keys and Q positive gaps, its unrestricted optimum is

    F(i,k)=t Q+(k+1-2^t),  t=floor(log2(k+1)).

The parity contraction lemma in GAP_PARITY.md proves this lower bound and
minimum-IPL trees attain it. Their height is at most h, so it is also the
penalty-layer value on these intervals. For 1<=k and i+k+1<=n-1,
substitution into the four-corner difference gives

    D(i,i+k)=1 if i is even and k=2^d-1 for some d>=1,
             0 otherwise.                                (6)

To see the cancellation explicitly: away from k=2^d-2 or 2^d-1 all four
logarithms equal the same t and both gap mass and the linear residual cancel.
At k=2^d-2, only the longest interval changes logarithm, and its k+2=2^d
gaps have exactly 2^(d-1) ones; the jump cancels. At k=2^d-1, the shortest
interval uses d-1 and the other three use d; the difference is
2^(d-1)-Q_short, which is one for even i and zero for odd i. For d=1 the
shortest interval is empty with cost zero, and the same formula holds.

For each d=1,...,s-1, (6) supplies (n-2^d)/2 positive densities. Their sum
is (s-2)n/2+1. Adding the n completion entries proves

    max_h delta(E_h) >= sn/2+1.                             (7)

Consequently the maximum over fixed-mass binary gap inputs and all layers
is (1/2)n log2 n+O(n). This asymptotic statement follows from (5)--(7),
not from the search. It does not extend to arbitrary key weights: the
linear-mass odd-ramp key family already has Omega(n^(3/2)) support.

## Search and independent checks

The binary search preserves total mass in each of 84 runs: seven sizes,
three placements (keys, gaps, both), four initial patterns. It evaluates
all layers and counts completed core entries. The maximum masses are n
for mixed runs and n/2 for key-only and gap-only runs. The existing Python
reference independently checks 81 vectors, with all-root and all-shape
controls on the small cases. Exact inputs, seeds, operation counts, and
source hashes are retained in results/binary_core_search.json.

The new all-root harness independently checks (1)--(4), the one-missing-slot
formula, the binary upper bound, and every claimed density in (6). It uses
exhaustive small binary and ternary gap vectors, seeded nonbinary vectors,
search winners, and explicit family members. Its counts and hashes are in
results/gap_core_identity.json. Search winners are finite evidence only;
(5) and (7) supply the upper and lower proofs.
