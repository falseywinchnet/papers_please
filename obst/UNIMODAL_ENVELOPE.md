# A near-linear above-capacity construction for unimodal keys

**Theorem.** Suppose the nonnegative key weights are unimodal in their fixed
key order: they are nondecreasing up to some peak and nonincreasing thereafter.
Gap weights may be arbitrary nonnegative reals. Use a valid terminal penalty.
At capacity c=2^h-1, the
entire ordinary core strictly above capacity has at most max(0,n-c-1)
positive entries. Every side-s square wholly above capacity has at most
2s-1 positive entries. All these cores, including their values, over every
layer with c<=n can be constructed in O(n log(n+1)) arithmetic work and
space. After the same preprocessing, any interval of length at least c
has an exact layer-value query and a contiguous optimal selected-block
witness in O(log(n+1)) time.

This covers unequal real key weights and every endpoint position. The leading
coefficient one in the global support bound is asymptotically sharp. The
construction handles the above-capacity portion; the below-capacity mixed
region and unrestricted full-tree construction require further work.

## Contiguous domination

**Lemma.** For any unimodal sequence x_0,...,x_(k-1), every t-element
subsequence is componentwise dominated by a contiguous t-element block.
Consequently, for any nonnegative coefficient vector v_1,...,v_t,

    max_(i_1<...<i_t) sum_r v_r x_(i_r)
      = max_(0<=a<=k-t) sum_r v_r x_(a+r-1).              (1)

To prove it, choose a peak position z and let b of the selected indices be
at most z. Compress these b indices to z-b+1,...,z, and compress the remaining
t-b indices to z+1,...,z+t-b. The compressed positions stay in the sequence:
there were at least b positions on the left and t-b on the right. Each left
index moves right within a nondecreasing part; each right index moves left
within a nonincreasing part. Every selected value weakly increases, in the
same selected order. This gives a contiguous block and proves (1). The cases
b=0 or b=t use only one side. The empty subsequence is immediate.

Unimodality here describes the weight sequence in the original key order;
no sorting or permutation of keys is performed.

## The window envelope

For any key weights, define the fixed-length ruler windows

    B_h(a)=sum_(r=1)^c p_(a+r-1) nu_2(r),  0<=a<=n-c.     (2)

For an interval [i,j) of length at least c, put

    S_hat_h(i,j)=max_(i<=a<=j-c) B_h(a),
    A_hat_h(i,j)=M(j-i-c)+h W(i,j)-S_hat_h(i,j).           (3)

A contiguous selected block is a valid subsequence, so A_hat_h>=A_h for
arbitrary inputs. If p[i:j] is unimodal, (1) proves equality. Arbitrary gap
weights contribute through W(i,j) exactly as in the original saturated-layer
identity; these terms cancel from ordinary densities strictly above capacity.

For a density cell (i,j) with j-i>c, let a=i, b=j-c+1, and
Q=max_(a<t<b) B_h(t). Four range maxima in (3) give

    D_(A_hat)(i,j)=max(0,min(B_h(a),B_h(b))-Q).             (4)

Thus the envelope core is exactly the nonadjacent strict horizontal
visibility pairs of the N=n-c+1 window values, with mapping

    (a,b) -> (i,j)=(a,c+b-1).                             (5)

Such pairs are noncrossing: a<b<c<d cannot support both (a,c) and (b,d),
since that would require both B(c)>B(b) and B(b)>B(c). The polygon-diagonal
argument gives at most max(0,N-2) pairs. The same decreasing-neighbor-span
argument as in PLATEAU_CORE.md gives at most 2s-1 pairs between two ordered,
disjoint endpoint ranges of at most s positions. An above-capacity s-square
maps to precisely such ranges. The established horizontal-visibility geometry
is used here; the additional result is the unimodal subsequence reduction.

When the whole input is unimodal, (4)--(5) construct the entire original
above-capacity core. Monotone key weights are included; in that case B_h is
monotone and has no nonadjacent strict visibility pair.

For sharpness, take C=2^h, n=2C and one unit key at zero-based position C+1.
The already proved one-key formula gives exactly C-2h above-capacity entries.
The new upper bound is n-c-1=C. Their ratio tends to one.

## Constructing all layers without scanning interval pairs

Let c_h=2^h-1, d=2^(h-1), and initialize B_0(a)=0 for 0<=a<=n. The ruler
word consists of two copies of the preceding word around its central reward:

    B_h(a)=B_(h-1)(a)+B_(h-1)(a+d)+(h-1)p_(a+d-1).        (6)

There are O(n) window entries per layer and O(log(n+1)) layers with c_h<=n.
Equation (6) constructs all their values in O(n log(n+1)) arithmetic work.
For each layer, the strict monotone-stack algorithm enumerates (4), including
its density values, in O(n) work. Each index is pushed once and popped at
most once. The construction uses no dense interval table and no population-
count primitive.

Build a maximum segment tree for each B_h, retaining the earliest maximizing
window start. Its preprocessing is O(n) per layer. An interval query in (3)
then uses O(log(n+1)) work, and its returned start identifies an optimal block
of c selected keys. Emitting those keys or their perfect partial skeleton
costs O(c) additional output work. Prefix sums give W(i,j) in constant time.
Keeping all window arrays, query trees and output cores uses O(n log(n+1))
space; generation of the window arrays themselves needs only two successive
layers.

## Certified exact pieces for arbitrary key inputs

The same preprocessing is useful without global unimodality. For each
adjacent difference Delta_t=p_(t+1)-p_t, let

    V_t=max {a: a<b<=t, Delta_a<0, Delta_b>0},             (7)

with value -1 if the set is empty. A scan maintains the last negative-difference
index and updates V whenever a positive difference occurs. An interval [i,j)
is unimodal exactly when j-i<=1 or V_(j-2)<i. This gives an O(1) exact
certificate after O(n) preprocessing, including flat valleys and plateaus.

Construct the envelope cores (4) for arbitrary nonnegative input weights.
Keep a core cell (i,j) exactly when [i,j+1) is certified unimodal. The result
is the complete set of positive original above-capacity densities with such
outer spans: all four corner intervals are then unimodal and their envelope
values equal their original values. Filtering the O(n) envelope entries per
layer takes O(n log(n+1)) total work. No original positive cell with a
certified outer span is missed.

More locally, if the key span [a,b+s) of an above-capacity tile
[a,a+s) x [b,b+s) is unimodal, that tile has at most 2s-1 original positive
densities. This supplies a constant-time certificate for the boundary term
of the open local hypothesis on arbitrary inputs. Any positive density
outside the constructed certified part has a nonunimodal outer key span.
It does not supply the missing bound for those interactions or for the
below-capacity mixed region.

## The correction has both density signs

Let E_h=S_h-S_hat_h=A_hat_h-A_h>=0. Nonnegative values do not make this
correction Monge. Already at h=3, c=7, use these two binary key words:

    p+ = (0,0,0,1,0,0,0,1,0),      cell (0,8),
    p- = (0,0,0,1,0,0,1,0,0,0),    cell (0,9).

For each cell list corners as (i,j),(i,j+1),(i+1,j),(i+1,j+1):

    input    S             S_hat        E             D_E
    p+       (2,3,0,2)     (2,2,0,2)    (0,1,0,0)      1
    p-       (3,3,1,3)     (2,2,1,2)    (1,1,0,1)     -1

These tables follow directly from the length-seven reward word
(0,1,0,2,0,1,0). Two unit keys have score at most three. For p+, the full
nine-key interval attains three at selected ranks (4,6). The seven-key
middle interval forces ranks (3,7), giving zero; the two eight-key intervals
have maxima two. For p-, the two left intervals attain three at (4,6), and
the right nine-key interval attains three at (2,4). In its right eight-key
interval, one deletion can leave the two positive ranks only in the patterns
(2,5),(3,5),(3,6), or delete one positive key, so the maximum is one.
Direct contiguous-window evaluation gives the displayed S_hat values.

Concatenate the two words to obtain a single binary input with correction
densities of both signs at cells (0,8) and (9,18). Interval locality preserves
both tables. Gap weights cancel throughout, so they can be arbitrary.
Thus the remaining correction is neither a universally Monge nor a universally
anti-Monge object; the published Monge product cannot be applied to it solely
because its entries are nonnegative.

## Verification

The implementation is `code/unimodal_above.py`; the independent audit is
`code/unimodal_above_audit.py`. The JSON record preserves the final executed-
source hashes and separates original all-root controls from larger sparse
constructions and sampled literal windows. The theorem and the signed
correction examples follow from the proofs above, independently of the audit.

The final record exhausts 920 unimodal ternary words through eight keys and
checks 136802 nonempty subsequences for componentwise domination. It also
checks 1589 arbitrary nonnegative reward templates from 12864 literal
subsequences. Original all-root controls on 236 mixed inputs through 32 keys
check 31438 interval values and contiguous witnesses, 560 complete support
sets, 24032 densities, and 99398 local squares. They use 565705 root
candidates and 65081 states.

The arbitrary-input envelope audit checks 1636 inputs: every binary word at
nine and ten keys, and 100 random mixed inputs through 32 keys. It checks
101300 interval-unimodality decisions independently, 200892 upper-cost
inequalities, 91143 certified exact interval values, 130408 envelope
densities, 38221 certified original densities, and 4988 certified support
sets. These original recurrences use 2345440 candidates and 435040 states.
The signed-correction tables have eight literal controls from 253 choices.

Fourteen larger constructions reach 65536 keys, with 1168 sampled literal
window controls, 2780 constructed square checks, and five sharp single-key
counts. They have no large original all-root reference. Both largest rows
perform 917538 ruler-window updates and 983026 range-tree build-node
operations. The isolated peak outputs 65294 core entries across all layers;
the irregular rational mountain outputs 1201. These finite outputs do not
replace the proved O(n log(n+1)) work and size bounds.
