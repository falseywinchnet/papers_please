# An exact two-key full-ruler tail and sharp clipping scale

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar.

The remaining support-size hypothesis is unchanged. This result addresses the
alternative tail-mass route: the rank-clipping error really can have order
P C/d, even when the clipped tail vanishes. Density mass and core cardinality
remain distinct quantities.

## Exact full-ruler family

Let a>=0, b>=3, d=2^a, Q=2^b, C=dQ, h=a+b, c=C-1, and n=2C.
Use one-based positions x=C-3d and y=C. Give these two keys unit weight and
all other keys weight zero. Gaps may have arbitrary nonnegative weights:
they cancel from every above-capacity density. For v_r=nu_2(r), write U_d(v)
for the sum of above-capacity densities at lengths at least c+d. Then

    U_d(v) = 5Q/4 - 3b + 2,
    U_d(min(v,a)) = 0.                                      (1)

The removed reward in the existing clipping lemma is Q-b-1. Since P=2,

    [U_d(v)-U_d(min(v,a))] / [P(Q-b-1)] -> 5/8.              (2)

Thus that clipping allowance has the correct asymptotic order. In particular,
the C/d term cannot be omitted from a uniform full-ruler tail estimate.
Multiplying both key weights by any positive scalar multiplies both tails.
For example, multiplying by C makes total key mass W=n. This does not
multiply the number of positive density cells.

## Separating the low levels without separating the input keys

Put l_r=min(v_r,a) and z_r=(v_r-a)_+. The latter is zero away from multiples
of d, and z_(dt)=nu_2(t). We prove compatible optimization on the boundary
intervals used in the tail identity, rather than assuming that maxima add.

Take an interval with slack e=d or d-1, containing both positive keys. Let
r be the first key's relative one-based position. If both keys are selected,
their ranks have the form

    r-u, r+3d-w,  0<=u<=w<=e.                              (3)

Both ranks must lie in [1,C-1]. If r mod d is nonzero, each key's feasible
rank window contains at most one multiple of d. When both multiples are
valid, choosing u=w=r mod d attains both. Every other rank has low reward
less than a and high reward zero. Any choice using one of the two multiples
can therefore round the other rank to its multiple without losing reward
or violating (3). This simultaneously maximizes the low and high scores.

When r=dR and e=d, the feasible pairs of multiples, after division by d, are

    (R,R+3), (R-1,R+2), (R,R+2),                          (4)

with out-of-range pairs discarded. For the boundary starts with both keys
present, 1<=R<=Q-3, so the third pair is always valid. A pair with one rank
off the multiples can round that rank while preserving the rank already on
a multiple: the first two pairs in (4) are forced at the two extreme shifts,
and the third handles the two intermediate cases. A pair with neither rank
on a multiple is dominated in low reward by the third pair. Thus a high-score
maximizer in (4) also attains the maximal low score 2a. For slack d-1, only
the unique pair of multiples is available, as in the preceding case.

The remaining boundary case with both keys present is 1<=r<d. The first
key has no feasible multiple of d; its best low reward is attained at a
rank in [1,r]. The second key's unique multiple is 3d, with reward a and
high reward zero. These two choices are compatible because the first
omission count is less than r and the second is r. If only one key remains,
a rank window either contains a multiple of d, in which case its maximum
is a plus its maximal high reward, or contains none, in which case its
high reward is zero. This also handles the terminal boundary interval.

On the full interval, the low score is 2a. Two selected ranks are separated
by at most 3d, so at most one can be divisible by 4d. Their full reward is
at most (h-1)+(a+1)=h+a. Ranks C/2 and C/2+2d attain it and are feasible
at x,y, since Q>=8. Their high score is b. Consequently, on every interval
in the tail identity, including the full interval,

    S_v = S_l + S_z.                                      (5)

This is a family-specific compatibility statement; it is not a general
additivity assertion for optimized scores.

The low score is also the sum of the two separate one-key low scores on
these same intervals. A one-key capped-ruler maximum is a sum, over
1<=r<=a, of indicators that its feasible rank window meets a multiple of
2^r. The corresponding density cells lie at capacity distance 2^r-1<d,
by the consecutive-multiple classification. Hence each one-key low tail
is zero. Equation (5) therefore gives U_d(v)=U_d(z) and U_d(l)=0.

## Exact coarse boundary accounting

Let k=C+d-1. The tail identity is

    U_d = sum_(i=0)^(n-k) S(i,i+k)
           -sum_(i=0)^(n-k-1) S(i+1,i+k) - S(0,n).         (6)

For high rewards, divide selected multiple ranks by d. The coarse instance
has capacity Q-1, length 2Q, unit keys at Q-3,Q, and the ordinary ruler
template nu_2(t). If i=jd, its long boundary score maps to the coarse
interval [j,j+Q). If i=jd+r with 1<=r<d, that score maps to
[j+1,j+Q). Every short score with i in this same block maps to
[j+1,j+Q). These are precisely the unique-pair and three-pair alternatives
above. The terminal high score is zero, and the full score maps to the
coarse full interval. Cancelling within each block, including the zero
endpoint terms, proves

    U_d(z) = U_1(nu_2 on ranks 1,...,Q-1;
                  unit input keys at Q-3,Q).              (7)

## The remaining parity sum

Set V(r)=nu_2(r) for 1<=r<Q, and V(r)=0 otherwise. In the coarse instance,
put R=Q-3-i. The long interval has one omission and the short interval has
none. Their difference is exactly

    delta_R = max(V(R)+V(R+3), V(R)+V(R+2),
                  V(R-1)+V(R+2)) - V(R-1)-V(R+2).         (8)

The nonzero range is -2<=R<=Q-3. For even R, delta_R=V(R), giving

    sum_(R even) delta_R = Q-b-2.                         (9)

For odd R, delta_R=[V(R+3)-V(R-1)]_+. The boundary values R=-1 and
R=1 contribute 1 and 2. Values R=3 mod 4 contribute zero. Writing
R=4t+1 for the others reduces the positive differences to nu_2(t+1)
when t is odd; the final t=Q/4-1 contributes zero because V(Q)=0.
Thus

    sum_(R odd) delta_R
       =3+sum_(j=1)^(Q/4-1) nu_2(j)=Q/4-b+4.             (10)

The full coarse reward is b: two ranks within distance three cannot both
be divisible by four, and ranks Q/2,Q/2+2 attain (b-1)+1. Subtracting b
from (9)+(10) proves (1). Formula (2) follows directly.

## Why template reward mass alone cannot replace capacity

A broader proposed estimate U_d(v)<=A P(max v + sum v/d) is false for every
absolute A, even for periodic binary templates and two unit keys.

For integers d>=1 and m>=2, put C=2d(m+1), c=C-1, n=2C, x=C-3d, y=C,
and v_r=1 exactly at ranks 2d,4d,...,2dm. Then

    U_d(v)=m-1.                                          (11)

Here are the boundary counts, giving a self-contained proof. At slack d,
both keys get reward one precisely when the first relative rank is 2dt,
1<=t<=m-1: their input separation 3d requires all d omissions between
them to reach consecutive rewarding ranks. There are m-1 such starts.
At slack d-1, both rewards are impossible, because rewarding rank gaps
are either at most 2d or at least 4d, while the feasible gap lies in
[2d+1,3d].

For a key at position X, a long start giving it reward one lies in
[X-2dt-d,X-2dt] for some 1<=t<=m. Taking the union for x,y and intersecting
with the boundary start range gives [0,C-4d] union [C-3d,C-2d], containing
C-3d+2 starts. For short starts, the analogous union is [1,C-4d] union
[C-3d+1,C-2d], containing C-3d starts. Thus the two boundary sums in (6)
are C-3d+m+1 and C-3d. The full score is two, proving (11).

Taking m=d gives ratio (d-1)/4 to P(max v + sum v/d), which is unbounded.
This obstruction concerns a sparse auxiliary template. It does not refute
the full-ruler target O(P(h+C/d)), whose capacity term accommodates (11).

## Audit and scope

`ruler_clipping_sharp.py` independently enumerates the feasible ranks of
the two positive keys, checks score compatibility and the coarse mapping,
and compares small cases with generic subsequence optimization, literal
subsets, and original mixed-weight terminal layers. It also checks the three
boundary counts in (11), independently of the generic template diagnostic.
Larger formula-only rows are explicitly distinguished from those controls.

`template_tail_probe.py` retains the finite joint input/template search that
preceded the explicit sparse family. `tile_support_frontier.py` separately
attacks the still-open local support hypothesis with variable integer mass
at fixed tile sides; its observed maximum 136/149 supplies no upper bound.
All records retain source hashes and operation counts. The main full mixed
construction theorem and the remaining square-root logarithmic core gap
are unchanged.
