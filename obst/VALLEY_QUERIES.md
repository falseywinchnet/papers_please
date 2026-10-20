# Exact valley queries despite quadratic original interval cores

For nonnegative key weights that are nonincreasing and then nondecreasing,
every above-capacity interval has an exact implicit representation with
O(n log(n+1)) preprocessing and storage and O(log(n+1)) query work. Gap
weights are arbitrary nonnegative reals. A query also returns two end blocks
whose concatenation is an optimal selected subsequence. This is an interval
oracle, not a construction of the full mixed optimal BST.

Unlike a single peak, a single valley can have a quadratic above-capacity
core in the **original interval coordinates**. The explicit positive-integer
family below has exactly s^2/2 core entries in a side-s square. Dividing all
its key weights by n preserves that support and makes its total mass Theta(n).
Thus the integrality assumption in mass-dependent core bounds cannot be
removed by normalizing real weights. Both versions still have the logarithmic
query representation just stated.

## Universal domination by the largest end keys

Call x[0:k] a valley if some split z makes x[0:z] nonincreasing and
x[z:k] nondecreasing, with the original sequence decreasing into and increasing
out of its minimum. A minimum position can be assigned to the right side.
Every subinterval is again a valley, including monotone subintervals.

**Lemma.** There is one c-element subsequence of a valley that componentwise
dominates every c-element subsequence. It consists of the c largest keys,
taking a prefix and suffix and resolving equal weights toward the left.
It simultaneously maximizes every nonnegative rank-reward vector.

For a subsequence with t selected keys left of z, move those keys to the
first t positions, and the remaining keys to the last c-t positions. Each
left key moves left in a nonincreasing segment; each right key moves right
in a nondecreasing segment. Every selected value increases weakly. The
possible end-block words X(t) have

    max(0,c-(k-z)) <= t <= min(c,z).

Consecutive words X(t), X(t+1) differ only at selected rank t+1, replacing
x[k-c+t] by x[t]. On this feasible range x[t] is nonincreasing and
x[k-c+t] is nondecreasing. Therefore x[t]-x[k-c+t] is nonincreasing.
Move through every nonnegative difference and stop before the first negative
one. Each move before that stopping point weakly increases one component;
each subsequent move weakly decreases one component. The stopping word
dominates all X(t), hence all original subsequences. Its two decreasing
end lists have selected exactly their largest c values. This proves the
lemma, including ties and zero rewards. Binary search finds the stopping
split in O(log(k+1)) comparisons.

Restricting to feasible splits is essential for that binary search. Over all
unrestricted t, comparisons within a flat part of one wing need not form
the same monotone Boolean predicate. The implementation clips the two wings
at the valley minimum before searching.

## Ruler-prefix queries

For arbitrary p define

    P(a,t)=sum_(r=1)^t p[a+r-1] nu_2(r),  P(a,0)=0.

Retain all perfect-ruler windows B_h from UNIMODAL_ENVELOPE.md, with B_0=0.
If 2^k<=t<2^(k+1), the ruler identity gives

    P(a,t)=B_k(a)+k p[a+2^k-1]+P(a+2^k,t-2^k).       (1)

The remaining length has a smaller highest power. Scanning decreasing powers
of two evaluates (1) in O(log(n+1)) arithmetic work, without assuming a
constant-time population-count operation. The B_h arrays take O(n log(n+1))
work and storage. Build them for both p and its reversal.

For c=2^h-1, the ruler is symmetric: nu_2(c+1-r)=nu_2(r). If a query on
[i,j) chooses t left keys and c-t right keys by the domination lemma, then

    S_h(i,j)=P_p(i,t)+P_reverse(p)(n-j,c-t),
    A_h(i,j)=M(j-i-c)+h W(i,j)-S_h(i,j).                (2)

The split search and two prefix queries each take O(log(n+1)) work. Prefix
mass sums give W in O(1), for arbitrary nonnegative gap weights. The witness
is [i,i+t) followed by [j-(c-t),j); it is stored in constant space per query.
Emitting its c selected keys or perfect partial skeleton costs O(c) output
work. The terminal penalty must be valid as in the main layer theorem.

The preprocessing constructs no interval table and does not enumerate a core.
It covers all layers c<=n in the stated bound. Intervals below capacity and
composition of these implicit matrices remain separate requirements for a
general full-tree algorithm.

## A quadratic above-capacity square with a closed density formula

Let s=2^t>=4, n=4s, m=2s, and c=m-1=2^h-1. Set

    p_k = 2(m-k)          for 0<=k<m,
          2(k-m)+1        for m<=k<2m.                 (3)

These are the distinct weights 1,...,n arranged in a single valley:
the left side is decreasing even weights, and the right side increasing odd
weights. On the square 0<=i<s, 3s<=j<4s, all four intervals are above or at
capacity (in fact strictly above), and

    D_Ah(i,j)=nu_2(3s-ceil((i+j)/2)).                  (4)

**Proof.** Consider the inner interval [i+1,j), and let

    d=j-i-m,      a=m-i-1-floor(d/2),      b=c-a.

Its c largest keys omit exactly the d globally smallest weights, namely
the contiguous positions [m-floor(d/2),m+ceil(d/2)). These positions and
the next two weights fit strictly inside all the queried intervals: the
chosen square puts every interval endpoint beyond their relevant wing
frontiers. In particular the two smallest retained weights are z=d+1 and
w=d+2, with at least one selected key on each wing even after both are
removed. The same largest-key rule applies to all four corners.

Write each score as a sum of a left-end prefix and a reversed right-end
prefix, using ruler symmetry. Let L_t,R_t denote these prefix scores on the
inner interval; primes denote prefixes after adding the corresponding new
endpoint. The scores are

    corner          d even             d odd
    inner           L_a+R_b            L_a+R_b
    left only       L'_(a+1)+R_(b-1)   L'_a+R_b
    right only      L_a+R'_b           L_(a-1)+R'_(b+1)
    both ends       L'_a+R'_b          L'_a+R'_b.

Here 'left only' is [i,j), 'right only' is [i+1,j+1), and 'both ends' is
[i,j+1). End-prefix weights shift when an endpoint is added; their unchanged
parts cancel in S_left+S_right-S_both-S_inner. If d is even, z is the first
retained right key and w the last retained left key. Their remaining
contribution is

    (L'_(a+1)-L'_a)+(R_(b-1)-R_b)
      =w nu_2(a+1)-z nu_2(b)=nu_2(a+1),

because b=m-(a+1). If d is odd, z is the last retained left key and w the
first retained right key. The contribution is

    (L_(a-1)-L_a)+(R'_(b+1)-R'_b)
      =w nu_2(b+1)-z nu_2(a)=nu_2(a),

because b+1=m-a. Every other selected weight has canceled. Substituting
a and the parity of d into these two expressions yields (4). The affine
penalty and mass terms in (2), including all gap weights, also cancel.

The integer r=3s-ceil((i+j)/2) lies between s/2+1 and 3s/2. It is even
exactly when i+j is 0 or 3 modulo 4, since s is divisible by four. Each
row has s columns and precisely s/2 such residues. Hence the square has
exactly s^2/2=n^2/32 positive densities.

Even the dense square has a succinct explicit density description. Since
1<=r<2s and s is a power of two,

    D_Ah(i,j)=sum_(ell=1)^log2(s)
        1[i+j is 6s or 6s-1 modulo 2^(ell+1)].         (5)

Thus its density is a sum of logarithmically many modular diagonal patterns.
This is an exact representation statement, not a fast product theorem for
such patterns.

With zero gap weights, (3) has W=n(n+1)/2. Dividing every key weight by n
gives W=(n+1)/2 and scales every density in (4) by 1/n while preserving its
support. All weights remain positive rationals with O(log n)-bit numerators
and denominators. This rules out a core bound depending only on normalized
real mass in the same way as the integral-mass theorem. It does not contradict
that theorem, whose weight unit is fixed by integrality, and it does not prove
a lower bound on computing an optimal BST.

## Verification scope

The implementation is `code/valley_above.py`; `code/valley_above_audit.py`
separates exhaustive domination, arbitrary nonnegative reward vectors,
independent original mixed layers, and larger sampled implicit queries.
The density theorem is checked on both its integer and normalized rational
versions against the original all-root recurrence. The JSON result records
operation counts and source hashes; no wall-clock times enter the claims.

The final audit exhausts 920 ternary valley words through eight keys, with
136802 literal domination checks and 6198 arbitrary reward controls. Its
independent definition rejects 8920 nonvalley words. On 256 mixed inputs
through 64 keys, original all-root layers check 56076 interval values and
56076 two-block witnesses, using 1396993 root candidates and 113799 states.
The integer and normalized rational dense families contribute 672 original
four-corner formula controls and six exact square-support counts.

Fourteen larger query constructions reach 65536 keys, with 896 sampled
literal largest-key controls, 896 literal prefix controls, and 640 sampled
density-formula controls. At 65536 keys both fixtures perform 1835076 window
updates and retain 1966150 window entries, counting both orientations and
zero bases. These rows construct no dense interval table and have no large
original all-root references. The proofs, rather than these finite counts,
establish the query complexity and quadratic support.
