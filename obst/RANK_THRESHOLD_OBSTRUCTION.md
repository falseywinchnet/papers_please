# Ruler rank thresholds need incompatible subsequences

The identity nu_2(r)=sum_(a=1)^(h-1) 1[2^a divides r] does not permit
optimizing each level separately and adding the optima. Already with
binary input keys, the separate optima can sum to almost twice the
actual ruler reward.

This concerns thresholds of the **rank reward**, with the binary input
held fixed. It differs from the earlier input-weight threshold-tail
counterexample in NESTED_TAIL_OBSTRUCTION.md.

## An explicit family

Fix h>=5, C=2^h, c=C-1, and n=C. Set m=h-1. Give weight one to the
one-based key positions

    X=C/2+1,
    Y_r=C/2+4r+2,     0<=r<m,

and weight zero to every other key. These positions lie strictly below
C. Let S be the optimal reward from selecting c keys with ruler rewards
nu_2(1),...,nu_2(c). Let T_a be the optimal reward when the rank reward
is instead the binary indicator 1[nu_2(r)>=a]. Then

    S=h-1,
    T_1=h-1,  T_a=1 for 2<=a<=h-1,
    sum_a T_a=2h-3.                                     (1)

In particular (sum T_a)/S=2-1/(h-1) tends to two. No constant smaller
than two can universally bound this separate-level upper estimate by
that constant times S. This is a lower obstruction on such a comparison;
it does not establish a universal factor-two upper bound.

**Proof.** Every c-subsequence deletes exactly one input key t.
If t<X, key X shifts to selected rank C/2, of valuation h-1, and every
Y_r shifts to an odd rank, of valuation zero. Thus the full reward is
h-1 and every binary threshold reward is one.

If t=X, that key disappears and every Y_r shifts to an odd rank, so
all rewards are zero. If t>X, key X stays at an odd rank. Each Y_r<t
stays at its original rank, congruent to two modulo four, and contributes
exactly one to the ruler reward and the first threshold. A key Y_r=t
is deleted; each Y_r>t shifts to an odd rank and contributes zero.
The full and first-threshold rewards are therefore exactly the number
of Y_r<t, at most m, and every higher threshold reward is zero.
Deleting a key after the last Y_r attains m. These exhaustive cases
prove (1).

Arbitrary gap weights do not alter the above-capacity ruler optimization:
their contribution to the layer value is additive. The obstruction is
to independent rank-level optimization, not to the OBST objective or
the main core-size theorem.

## A smaller exact example

At h=4, n=16, and c=15, unit keys at one-based positions 9,12,14 give
S=3 and threshold optima (2,1,1), summing to four. Deleting a key before
9 gives valuation profile (3,0,0). Deleting key 9 gives zero. Deleting
10 or 11 gives zero; deleting 12 also gives zero. Deleting 13 or 14
gives the single positive rank reward two from key 12. Deleting 15 or
16 gives rewards two and one from keys 12 and 14. Hence the full maximum
is three, the first threshold maximum is two, and the other two maxima
are one. No minimality assertion is needed.

## Verification appendix

The discovery probe checks 65454 inputs using 15176940 subsequence
transitions. Its first counterexample has 22 keys, full reward seven,
and binary-level optima (5,2,1). Independent literal enumeration checks
all 170544 length-15 subsequences of that input.

The explicit family and the smaller example are checked by all 32752
single deletions through n=16384, evaluating 425838 retained positive
ranks and making 5176333 threshold comparisons. At n<=128, 22 independent generic subsequence controls use
145386 transitions and 66 score entries. Four original all-root controls
with nonzero gap weights use 2812064 root candidates and 73456 states.
The larger rows enumerate all deletions; they are not original all-root
runs. The closed-form proof applies to all h>=5 independently of the audit.

Sources and manifests are in `code/rank_threshold_probe.cpp`,
`code/rank_threshold_obstruction.py`, `results/rank_threshold_probe_raw.json`,
and `results/rank_threshold_obstruction.json`.
