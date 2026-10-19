# Two weights disprove a logarithmic additive interaction allowance

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. The full mixed-weight tail bound remains the research target.

## The explicit counterexample

For h>=5, put C=2^h, c=C-1, n=2C. Give keys x=C-5 and y=C weight one
(zero-based indices); every other key and every gap has weight zero. Let
T_4 be ordinary density mass over |j-i-c|>=4. Then exactly

    T_4(e_x+e_y) = 21C/16 - 3h + 1,
    T_4(e_x)+T_4(e_y) = C - 4h + 4,
    T_4(e_x+e_y)-T_4(e_x)-T_4(e_y) = 5C/16 + h - 3.       (1)

Here W=2. The excess divided by hW tends to infinity. Therefore no absolute
constant K can make

    T_d(w) <= sum_z w_z T_d(e_z) + K hW

hold on all mixed-weight inputs and all widths. The obstruction already uses
two positive key weights and no positive gaps. Scaling both weights by C
makes W=n and preserves the ratio. It does not contradict the broader target
T_d=O(W(L+c/d)): at d=4 both sides of that target have order C in this family.
It shows that interactions can contribute at the scale of the c/d term,
not merely at the scale of the logarithmic allowance.

## Interaction of interval costs

Remove terminal penalties and write R_w(i,j) for the ordinary comparison
cost at height h. Define

    E(i,j)=R_(e_x+e_y)(i,j)-R_(e_x)(i,j)-R_(e_y)(i,j).

It is zero when an interval does not contain both keys. Its four-corner
difference is the difference between the combined density and the two unit
densities away from capacity. Singletons have E=0. On the full interval,
each key alone can occupy the root, giving reward h-1. Jointly, two selected
skeleton ranks are at distance at most five. At least one therefore has
valuation at most two, while the other has valuation at most h-1. Reward
h+1 is attainable by assigning the first key to rank C/2 and the second to
rank C/2+4. Thus

    E(0,n)=2(h-1)-(h+1)=h-3.                              (2)

For k let F_k=sum_(i=0)^(n-k) E(i,i+k), and let
b_k=E(0,k)+E(n-k,n). Summing a length-k density diagonal gives

    sum_i D_E(i,i+k)=F_(k+1)-2F_k+F_(k-1)+b_k-b_(k-1).

For the excluded lengths c-3,...,c+3, the edge terms telescope to
b_(c+3)-b_(c-4)=0. Indeed the short edge intervals do not contain both keys;
at the left long edge the maximizing rank choices are compatible, and the
right long edge omits the keys. Hence the desired interaction is

    E(0,n)+F_(c-3)-F_(c-4)+F_(c+3)-F_(c+4).              (3)

The same telescoping separates the excess into F_(c-3)-F_(c-4) below
capacity and E(0,n)+F_(c+3)-F_(c+4) above capacity. The formulas below give
C/8 and 3C/16+h-3 respectively. Thus each side separately defeats an O(hW)
interaction allowance.

It remains to compute four sums of local ruler formulas. This avoids any
asymptotic inference from the finite search.

## Exact rank formulas on the four diagonals

Write v(t)=nu_2(t) and r=x-i+1. For a length c-a interval containing both
keys, their selected perfect slots have the form

    s=r+u, t=r+5+z,       0<=u<=z<=a.

The inequality u<=z leaves room for the four intervening zero keys. Its
interaction is the sum of the independent maxima minus the joint maximum:

    e^-_a(r)=max_(0<=u<=a) v(r+u)+max_(0<=z<=a) v(r+5+z)
              -max_(0<=u<=z<=a) [v(r+u)+v(r+5+z)].        (4)

For a length c+a interval, selected ranks instead have the form
s=r-u, t=r+5-z with 0<=u<=z<=a, clipped to 1<=s<t<=c. Formula (4), with
these negative shifts and clipping, defines e^+_a(r). Because a<=4 is
smaller than the distance between the two keys, an optimum may expose both:
any selected positive key can be supplemented by the other at a feasible
rank without lowering its reward. Equivalently, every independent feasible
rank has a compatible rank for the other key. All such assignments extend
to c selected input keys by filling the remaining ranks with zero keys.

The actual starts give the ranges

    F_(c-a)=sum_(r=1)^(C-6-a) e^-_a(r),
    F_(c+a)=sum_(r=1)^(C-4) e^+_a(r),       a=3,4.        (5)

The other starts contain at most one positive key and contribute zero.

## Evaluating the finite ruler cases

For the two lower diagonals, (4) gives the following periodic lists, indexed
from r=1. The period for a=3 is eight and for a=4 is sixteen:

    e^-_3: 1,1,2,0,2,1,1,0.
    e^-_4: 1,1,1,1,1,1,0,0, 1,1,2,2,1,1,0,0.           (6)

These cases use only the valuations 0,1,2,3, and >=4. One takes the two
independent maxima in their four- or five-position windows, then enforces
u<=z. When their locations already satisfy that inequality the defect is
zero; otherwise maximizing the remaining finite rank pairs gives (6).
No value above four changes the displayed defect: its contribution cancels
or the competing lower-valued slot determines the loss. The first seven
entries of the first list sum to eight, and the first six entries of the
second sum to six. Applying the ranges in (5) gives

    F_(c-3)=C-8,        F_(c-4)=7C/8-8.                  (7)

For e^+_3, only residues r=3,7 modulo eight contribute. At r=8k+3 the two
independent maxima are at 8k and 8k+8. Away from the edges, their valuations
A,B have min(A,B)=3. They cannot both be selected, since their distance is
eight while the two input keys are only five positions apart. Keeping the
first high rank forces the other reward to zero, and keeping the second
forces the first to zero; using neither gives at most two. Thus the defect
is min(A,B)=3. At r=8k+7 the independent rewards are both two, while the
best compatible sum is two, giving defect two. Every other residue has
compatible independent maxima. The two clipped cells r=3,C-5 have defect
one instead of three. There are C/8 cells of residue three and C/8-1 of
residue seven, so

    F_(c+3)=3(C/8)+2(C/8-1)-4=5C/8-6.                   (8)

For e^+_4, only residues r=3,4 modulo eight contribute. Formally set
v(0)=v(C)=h and put A=v(8k), B=v(8k+8). Before the clipping corrections,

    e^+_4(8k+3)=min(A,B-2),
    e^+_4(8k+4)=min(A-2,B).                              (9)

For the first formula, the best compatible joint reward is max(A+2,B):
keeping the first high rank permits the intervening valuation-two slot,
while keeping the second high rank forces the first reward to zero.
The second formula follows from the joint reward max(A,B+2). Other choices
have smaller rewards. At r=4 and r=C-5 clipping changes the displayed value
from three to zero, for a total correction of six. The other edge values
already agree with (9).

Put m=C/8, a power of two at least four. For each k=0,...,m-1 one of the
adjacent integers k,k+1 is odd. The two expressions in (9) therefore sum
to three if the even neighbor has valuation one, and four if its valuation
is at least two. Exactly m/2 indices give each case, counting the endpoints
with the formal valuations above. Consequently

    F_(c+4)=3m/2+4m/2-6=7C/16-6.                        (10)

Substituting (2), (7), (8), and (10) into (3) proves the excess formula (1).
For each of the two unit keys, the consecutive-power classification places
outside-band densities at distances 2^t-1, 3<=t<h. All these pairs fit
inside this input. There are C/2^t below and C/2^t-2 above for each key.
Summing gives C/2-2h+2 per key. This proves the unit-tail formula in (1),
and addition gives the combined-tail formula.

## A separate small failure above capacity

The stronger claim that above-capacity interaction is bounded by full-interval
interaction also fails. At n=10,h=3,c=7,d=2, put unit weights at keys 3 and 6.
Only the density cell (0,9) is in this upper tail. The perfect-subsequence
rewards for intervals [0,10), [0,9), [1,10), [1,9) are respectively 3,3,3,1.
Their difference is 3+3-3-1=2. Each unit tail is zero, and full-interval
interaction is 2+2-3=1. Thus the excess is two while the proposed controlling
quantity is one. The large family above disproves the more generous hW
allowance as well.

## Verification and provenance

The one-sided all-root diagnostic checked 2,956 vectors and 91,370 inequalities,
using 1,770,275 states and 28,876,151 root candidates. It found the ten-key
example. A sparse search then evaluated 19,614 inputs: all unit pairs on
keys and gaps through n=64, structured unequal-weight pairs, and sparse
random inputs through n=512. Its growing winners suggested the family in (1).
The sparse search uses the existing optimized recurrence, with independent
all-root controls for retained winners through n=64. Its search output is
historical evidence of falsification, not the proof of growth.

The explicit-family audit checks all original-layer tail cells and every
needed band value against three independent all-root recurrences (combined
input and both unit inputs) through h=7. Literal feasible rank choices check
(6)-(10) through h=12. Larger rows through h=128 evaluate the proved formulas
only and are labeled separately. Exact operation counts and executed-source
hashes are in results/one_sided_interaction.json,
results/sparse_interaction_search.json, and results/sparse_interaction_barrier.json.
