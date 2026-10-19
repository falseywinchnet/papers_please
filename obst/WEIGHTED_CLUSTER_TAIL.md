# Exact weighted cluster tails and the limit of pointwise charging

The alternating-template theorem bounds the true upper tail by
P min((c-1)/2, 2+(c-3)/d). Its growing-width lower family extends to
arbitrary nonnegative real weights, with an exact formula. That formula
also distinguishes aggregate weight charging from uniform bounds on the
sensitivity to each individual key.

## Weighted cluster theorem

Let C=2^h, K>=3, C>=4K, c=C-1, n=2C, and x=C-3(K-1).
Put arbitrary nonnegative weights w_0,...,w_(K-1) at

    x, x+3, ..., x+3(K-1)=C,

and zero at other positions. For the alternating rank template v_r=1 at
even ranks and zero at odd ranks, put mu=min_r w_r and P=sum_r w_r. Then

    U_K = N mu,     N=ceil(x/2)-1.                         (1)

Consequently, for fixed total cluster mass P,

    max U_K = (N/K) P,                                    (2)

attained by equal weights. Since N>0, equality in (2) requires equal weights.

### Endpoint proof, including arbitrary unequal weights

Set k=c+K and b=n-k=C-K+1. The exact upper-tail telescope is

    U_K = sum_(i=0)^(b-1) [S(i,i+k)-S(i+1,i+k)]
          +S(b,n)-S(0,n).

For every i<x, the old interval rewards all K positive positions. Let
R=x-i+1 be the first position's local index. Omit u=0 positions before
it if R is even, or u=1 if odd, and one position in each spacing-three
gap. This uses K-1+u<=K omissions. The last rewarded rank is
C-K+2-i-u, even and at most C-2. The only apparent endpoint exception,
K=3 and i=0, forces u=1 and also fits. Put any remaining omission after
the last positive key. Thus the old score is P.

In the shortened interval the omission budget is K-1 and the first local
index is r=x-i. If r is even, all K keys can again receive reward one.
If r is odd and r>=3, rewarding all K would need one omission before the
first key and at least one in each of K-1 odd gaps: K omissions, too many.
At least one weight is therefore lost, giving score at most P-mu.

Every choice of the unrewarded key attains that bound when it is a minimum:

- Leave the first key unrewarded. The next key has even local index r+3.
  The remaining K-2 odd gaps use K-2 omissions.
- Leave an interior key unrewarded. Use one omission before the first
  rewarded key and one in each of K-3 remaining odd gaps. The single gap
  across the unrewarded key has length six and requires no omission.
  Total omissions are K-2.
- Leave the last key unrewarded. Use one initial omission and one in
  each of K-2 odd gaps, totaling K-1.

In the first two cases the final rewarded rank is C-K+2-i. It is even
and at most C-2: the possible K=3,i=0 exception has even r and is outside
this case. In the third it is C-K-2-i. The unrewarded key can occupy an
odd rank, so it need not consume an extra omission. All remaining omissions
fit after the final rewarded key. Thus the shortened optimum is P-mu.

At i=x-1, the first key is the shortened interval's left endpoint, where
it can only occupy odd rank one. Its loss is w_0; all other keys can be
rewarded. For i>=x, at most K-1 eligible positive positions remain. Their
first local index is at most four; the initial parity correction and
inter-key omissions fit the K-1 budget, and their last rewarded rank is
at most 2K<=C-2. Both intervals reward every eligible key. Their difference
is therefore p_(i+1).

There are exactly N starts i<x-1 with x-i odd. The later endpoint losses,
plus S(b,n), equal P-w_0, while S(0,n)=P. Hence

    U_K = N mu + w_0 + (P-w_0)-P = N mu.

Finally mu<=P/K, with equality exactly at equal weights, proves (2).

## Exact directional behavior

Let I={r:w_r=mu}. For any direction z preserving nonnegative weights for
sufficiently small positive epsilon, the right directional derivative is

    D_z U_K = N min_(r in I) z_r.                          (3)

This follows directly from (1): keys outside I remain above the minimum
for a sufficiently small perturbation. In particular:

- If the minimum is unique, increasing that key has derivative N.
- If two or more keys tie for the minimum, increasing any one key alone
  has derivative zero.
- Increasing all cluster weights together by epsilon increases the tail
  by exactly N epsilon, including at ties.

The directional derivatives at a tie need not form an additive linear
functional. The aggregate bound survives these large or coupled local changes.

## A linear-mass obstruction to uniform pointwise sensitivity

Take K=2^r>=4, C=K^2, h=2r, n=2C, and d=K. Give the cluster weights

    (K, 3K, 2K, ..., 2K).

Their total is exactly n and the first key is the unique minimum. Here

    N=(K^2-3K+2)/2,
    U_K=N K,
    partial_+ U_K / partial w_0 = N.

The alternating template has maximum reward t=1. Therefore

    N / (t+(c+1)/d) = (K^2-3K+2)/(2(K+1)) -> infinity.     (4)

The ratio still diverges if the denominator is enlarged to h+C/K.
This disproves every uniform constant bound on the individual key derivative
by t+(c+1)/d, already in the alternating subproblem. The known aggregate
bound U_d=O(P(1+c/d)) is fully consistent with the family. Its sharp charge
on this cluster is N min(w), which is bounded using all K participating
weights. Equation (4) does not disprove the analogous derivative estimate
for the *full* ruler template; the alternating template is an auxiliary
periodic problem with its own rewards.

## Diagnostic method and verification appendix

For integer input weights and an integer template in [0,t], exact right
key derivatives can be evaluated without floating point. For each interval,
maximize the pair (ordinary score, reward at the perturbed key)
lexicographically. Its second coordinate is the right derivative. Equivalently,
if T is the entire tail function,

    D_x T(p) = T((t+1)p+e_x) - (t+1)T(p).

A primary-score gap is at least one; after scaling by t+1, no reward change
of at most t can close it. Among primary maximizers the increment selects
the maximum slope. The same exact identity holds after taking the signed
tail telescope. The diagnostic compares these two implementations.

The weighted-family audit compares independent generic subsequence and
cardinality-matching tables on 81 inputs. It checks 3652 endpoint formulas,
162 terminal scores, 169 coordinate derivatives, and 47 joint increments.
This includes all ternary weight vectors on a three-key cluster, unequal
weights, zero minima, and ties. Larger formula-only rows are marked.

The separate full-ruler search examines 21020 fixed-mass inputs through
256 positions, including 29 independent scaled-perturbation controls. Its
largest derivative ratio to h-1+2^h/d is 416/129 on 128 positions. This
finite value implies no asymptotic bound. A preliminary canonical-witness
probe checks 5616 Euler identities on 608 inputs, then checks right derivatives
at improving candidate positions. Canonical coefficients need not equal
right derivatives at ties; the records retain that distinction.

Exact counts, inputs, and executed-source hashes are in
`weighted_cluster_tail.json`, `key_sensitivity_search.json`, and
`key_tail_sensitivity.json`. The search suggested the pointwise question;
only the explicit weighted family proves the obstruction.
