# Individual-weight charges and sparse construction for valley cores

The implicit valley representation also gives a direct integer-mass charge.
Let P=sum_i p_i, with nonnegative integer valley key weights and arbitrary
nonnegative real gap weights. At every capacity c=2^h-1, the entire strictly
above-capacity original core has at most P entries. More locally, a rectangle
with row set I and column set J, wholly above capacity, has at most

    min(sum_(i in I) p_i, sum_(j in J) p_j)              (1)

positive entries. This proves the open boundary-plus-mass support target on
valley above-capacity tiles, using only the endpoint masses and no side term.
All such cores over all layers can be constructed in
O((n+P) log^2(n+1)) arithmetic work and O((n+P) log(n+1)) space.
The below-capacity mixed region remains outside this construction.

## An auxiliary support envelope

Write T_c(i,j) for the sum of the c largest weights in p[i:j], defined for
j-i>=c. Put

    Gamma_c(i,j)=T_c(i,j)+T_c(i+1,j+1)
                  -T_c(i,j+1)-T_c(i+1,j),             (2)

for j-i>c. This sign matches the original layer density because its ruler
score is subtracted from its affine cost. For arbitrary input weights,
Gamma_c>=0. If c>=2, let x=p_i, y=p_j, and let z,w be the c-th and (c-1)-th
largest weights of the inner interval [i+1,j), respectively. Directly
inserting the two endpoints gives

    Gamma_c(i,j)=max(0,min(x,y,w)-z).                  (3)

Only the two smallest retained values can be displaced, which proves (3)
by comparing their replacements in the four sums. For c=1 the same formula
uses w=+infinity.

**Support lemma.** On a valley, for the perfect-ruler score and h>=1,

    0 <= D_Ah(i,j) <= (h-1) Gamma_c(i,j).              (4)

In particular a positive ruler density requires a positive top-c-sum density.
This holds for real weights as well as integers; integrality is used later.

For h=1 every ruler reward is zero. Suppose h>=2. The universal end-block
domination lemma makes a largest-c selection optimal for the ruler on all
four intervals. Moreover all largest-c selections have the same value word:
the dominating word has the same unweighted sum, so componentwise dominance
forces equality at every component.

If x<=z, adding x does not change the inner top-c sum or its value word.
After adding y the cutoff can only increase, so x remains ineffective there.
Both ruler-score changes are zero. The case y<=z is symmetric.

Suppose x,y>z but min(x,y)<w. If x<w, the left endpoint dominates every key
on its nonincreasing wing. Thus at most one selected inner value lies on
that wing, and every retained value except z is at least w>x. Adding x
replaces the first selected value z by x. Adding y raises the cutoff to
at least w, so x is then ineffective. The resulting four-corner difference
is (x-z) nu_2(1)=0. Reflection treats y<w. Both x and y cannot be below w,
since w lies on a wing dominated by its corresponding endpoint.

It remains that x,y>=w. Choose adjacent smallest selected values z<=w in
the valley word; if there is a tie, choose adjacent values within its trough.
Each one-end extension replaces z, and the two-end extension replaces z,w.
If z has selected rank r, cancellation gives

    D_Ah(i,j)=(w-z) nu_2(r).                          (5)

Here is explicit cancellation for the two left-minimum cases. Let L_a,R_b
be left and reversed-right prefix scores of the inner selected word, with
a+b=c; primes mean the corresponding new endpoint has been adjoined.
If both w,z lie on the left, z has rank a. The four scores in order
(inner,left,right,both) are

    L_a+R_b, L'_a+R_b, L_(a-1)+R'_(b+1),
    L'_(a-1)+R'_(b+1).

Their difference is (L'_a-L'_(a-1))+(L_(a-1)-L_a)
=w nu_2(a)-z nu_2(a). If z is left and w right, the four scores are

    L_a+R_b, L'_a+R_b, L_(a-1)+R'_(b+1), L'_a+R'_b,

giving w nu_2(b+1)-z nu_2(a)=(w-z)nu_2(a), since b+1=2^h-a.
Reflection handles the two right-minimum cases, using ruler symmetry.
The formulas also give zero when w=z. Finally nu_2(r)<=h-1 and (3) equals
w-z in this last case, proving (4). Arbitrary gaps cancel from these
above-capacity densities.

## Charging each endpoint weight

Fix row i and let z_i(j) be the c-th largest weight in p[i+1:j]. Then

    Delta_i(j)=T_c(i,j)-T_c(i+1,j)=max(0,p_i-z_i(j)).   (6)

As j increases, z_i(j) is nondecreasing. Equation (2) is exactly
Gamma_c(i,j)=Delta_i(j)-Delta_i(j+1). Thus

    sum_(j=i+c+1)^(n-1) Gamma_c(i,j) <= p_i.           (7)

Reversing the input gives the column bound sum_i Gamma_c(i,j)<=p_j.
These auxiliary mass bounds hold for arbitrary nonnegative input weights.
For integer keys, a positive Gamma_c is at least one. The support inclusion
(4), followed by (7), proves the total bound P and the rectangle bound (1).
There is no multiplication by h in the support charge.

The dependence on mass is necessary up to constants. The integer dense
valley family has P=n(n+1)/2 and at least n^2/32 entries in one layer.
Its side-s square has row-endpoint mass 3s^2+s and column-endpoint mass
3s^2, with exactly s^2/2 core entries. Thus the local endpoint-mass bound
is attained within a factor of six by an explicit proved family.

This does not extend to unrestricted real mass: the normalized dense valley
family has fractional Gamma_c=1/n on its square. It is fully consistent with
both (4) and (7). Nor does the argument give the same inclusion for arbitrary
nonvalley words; universal end-block domination is used essentially.

In fact the inclusion is false outside the valley class. The already used
binary word p+=(0,0,0,1,0,0,0,1,0), at h=3 and cell (0,8), has ruler scores
(2,3,0,2) in corner order (i,j),(i,j+1),(i+1,j),(i+1,j+1). Its original
density is one. Every corner has top-c sum two, so Gamma_c is zero. The
same direct rank calculation in UNIMODAL_ENVELOPE.md proves these scores.
Thus an auxiliary top-c support envelope alone misses actual two-peak
interactions even at integer mass two.

## Enumerating changes without scanning zero cells

The constructor first builds the O(n log(n+1)) valley interval-query
representation. Binary search in the two monotone wings also answers a
c-th-largest query, or counts values strictly above a threshold, in O(log n).

For row i begin at j=i+c+1. Compute z=z_i(j). If z>=p_i, the row has no
remaining auxiliary density. Otherwise let g count inner values strictly
greater than z. The retained top-c set has m=c-g copies of its minimum z.
Find the first future position k on the nondecreasing wing with p_k>z.
Every intervening value is at most z. After k, all values are greater than z.
The cutoff therefore remains z until exactly m such values have arrived:
its next strict increase occurs when position

    j'=k+m-1                                         (8)

is added. If j'>=n there is no further event. Otherwise query
z'=z_i(j'+1)>z and emit the auxiliary density

    Gamma_c(i,j')=min(p_i,z')-z>0.

Continue at j=j'+1. Equation (8) handles repeated weights; emitting an event
at every p_k>z would incorrectly count zero cells while the minimum still
has multiple copies. If j is still on the nonincreasing wing, all future
keys on that wing are at most the current cutoff, so the same right-wing
search remains valid.

Each emitted event and the final row termination use O(log(n+1)) work.
Every positive Gamma_c event is emitted exactly once. Evaluate the four
original ruler scores at each event in O(log(n+1)) work and retain a cell
exactly when its original density is positive. The support lemma proves
completeness. Height one has no ruler core and is skipped.

Let Delta be the total number of auxiliary positive cells across the
constructed layers and L=ceil(log2(n+1)). The real-weight bound is
O((nL+Delta)L) work and O(nL+K) space, where K is the total original output
size. For integer keys Delta<=PL and K<=Delta, giving the stated
O((n+P)L^2) work and O((n+P)L) space. This includes preprocessing and every
core value, but not a full-BST construction through the mixed lower region.

## Verification

`valley_core_audit.py` checks auxiliary supports against literal sorted sums,
the support inequality and two-threshold formula, original all-root mixed
layers, and every eligible small square's boundary-mass bound. Larger rows
construct complete sparse cores and use sampled literal selected-key scores.
The independent dense valley formula is checked on complete constructed
squares. The record `results/valley_core_audit.json` separates these scopes
and retains exact operation counts and executed-source hashes.

The final audit has 1513 small inputs: 1461 exhaustive ternary valleys through
nine keys, 48 varied mixed inputs, and four dense-family integer/rational
inputs. It checks 73082 literal auxiliary densities, 32810 two-threshold
formulas, 4267 auxiliary and 4267 ruler support sets, and 198321 local
boundary-mass controls. Original all-root mixed layers separately check
49278 densities and 2644 complete support sets on 972 inputs, using 1006805
root candidates and 163435 states. The nonvalley witness has its own 495
original root candidates and 135 states.

Twelve larger complete sparse constructions reach 16384 keys, with 3264
sampled literal density controls. At that size the binary-end input emits
4084 original core entries from 8178 auxiliary events, and the bounded
valley emits 16477 from 32995. Each preprocessing uses 393276 ruler-window
updates. Five complete dense-family constructions check 5456 formula cells
through side 64. Large rows have no original all-root reference, and their
finite counts do not replace the complexity or support proofs.
