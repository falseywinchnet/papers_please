# Ruler patterns, a dense-core barrier, and an exchange shortcut

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar. These are exact statements for the full mixed key/gap
model. The unrestricted subquadratic objective remains open. Priority of the
identities and sufficient conditions is not established.

## 1. Saturated penalty layers are weighted subsequence problems

Use the terminal-penalty recurrence from MONGE_PENALTY.md, with
A_0(i,j)=M(j-i), A_h(i,i)=0 and

    A_h(i,j) = W(i,j) + min_r { A_(h-1)(i,r) + A_(h-1)(r+1,j) }.

For layers h<=H, take M>HW. Write c_h=2^h-1. When k=j-i>=c_h,
the penalty forces exactly c_h exposed keys: a competing partial tree can
have ordinary weighted cost at most hW, so losing one exposure cannot pay.
All positions in the first h levels must therefore be occupied. The exposed
tree is perfect, with c_h selected keys in inorder. Every gap, and every
unexposed key, pays h comparisons. Inorder position t in the perfect skeleton
has key comparison length h-v_2(t). Consequently

    A_h(i,j) = M(k-c_h) + h W(i,j)
               - max_(i<=s_1<...<s_c_h<j) sum_t v_2(t) p_(s_t).       (1)

Here v_2(t) counts trailing zero bits for positive integer t. The coefficient
sequence is 0,1,0,2,0,1,0,3,... . The formula retains every gap's contribution;
it applies only to these saturated partial-tree intervals, not to arbitrary
full-tree optima. On shorter intervals the gap depths can differ.

At h=2, the maximum is max(p[i+1:j-1]). At h=3, greedily choosing the
largest eligible root is already wrong. With

    p = [0,9,0,9,10,9,0,0], q = [1,1,1,1,1,1,1,1,1],

root 3 permits score 36, while the larger key at root 4 permits only 29.
Adding one to every key weight makes all weights positive and adds the same
four to both scores. Thus the failure does not depend on zero weights.

For nondecreasing p, the rightmost c_h keys maximize (1) coordinatewise;
for nonincreasing p, the leftmost keys do. The score then depends only on
one endpoint. Since W is separable in the endpoints on nonempty intervals,
the Monge density is zero whenever all four intervals in its stencil are
saturated, namely j-i>=c_h+1. This statement allows arbitrary gap weights.
It explains the zero far-band cores in the monotone-key diagnostic, but does
not remove the quadratic short-interval band as h approaches log n.

The subsequence formulation suggests connections to weighted semi-local
alignment. The unit-Monge/permutation representations for unweighted LCS
cannot simply be applied to arbitrary weights v_2(t)*p_s. Existing general
weighted core-sparse multiplication is already used in our earlier reduction.
No new fast product or closure theorem is claimed here.

## 2. An adjacent exchange eliminates a wide shape DP

Let h=floor(log2(n+1)), c=2^h-1 and s=n-c. Every minimum internal-path-length
shape is a perfect c-key skeleton with s of its 2^h external slots expanded
to one-key cherries. Consider adjacent skeleton slots g and g+1, with one
expansion between them. If i is their first input index, swapping expansion
pattern 01 to 10 changes the cost by exactly

    (1+v_2(g+1)) (p_i-p_(i+1)) + q_i-q_(i+2).                       (2)

Only the intervening skeleton key, the one added key, and these three gaps
change their comparison lengths. The coefficient lies between 1 and h.
Thus the following O(n)-checkable sufficient condition makes every such
leftward swap nonincreasing in cost:

    max(p_i-p_(i+1), h(p_i-p_(i+1))) <= q_(i+2)-q_i
    for every 0<=i<n-1.                                            (3)

Repeated swaps move all s expansions to the left. The resulting left-filled
last level is therefore optimal within the minimum-path-length class. The
reflected condition yields a right-filled last level. If s=0, the class has
only one shape and needs no condition. In particular, nondecreasing key
weights and nondecreasing gap weights satisfy (3), while its reflected
version handles both sequences nonincreasing. Conditions (2)--(3) also allow
nonmonotone keys when the gap increments compensate for their decreases.

This is a class-optimality theorem, NOT a global-optimality theorem. Use the
existing full mixed-node residual-Huffman certificate from COMPLETE.md:
for a=min(p), b=min(q), residual lower bound H_res, and candidate value V,

    V <= (a+b)(I_min(n)+1) + (a+2b)n + H_res.                       (4)

Every tree outside the class has I>=I_min+1, so (4) proves the candidate
globally optimal. Otherwise the implementation falls back to Knuth.

`ordered_complete.py` implements both orientations, direct reconstruction,
the existing two-queue mixed residual bound, and exact fallback. Accepted
inputs take O(n log n) time and O(n) auxiliary space in general, including
sorting for the lower bound. When both weight lists are monotone, the bound
needs only reversal/scans and two queues, giving O(n) total time. There is
no dependence on the number of optional slots in the last level. Rejection
preserves the quadratic worst case; sorted geometric weights are explicit
controls showing that (3) alone does not imply global optimality.

## 3. A quadratic core with a logarithmic-time interval oracle

For n>=1 set

    B=4(n+1)^3, p_r=B+r (0<=r<n), q_r=B+r (0<=r<=n).                (5)

Every weight is positive and uses O(log n) bits. The deviation above the
minimum key/gap baselines is exactly R=n^2. Even though all weights are very
close relative to B, the final optimal-cost matrix has quadratically many
nonzero Monge densities, and its mixed fourth difference has quadratically
many nonzeros as well. Nevertheless the exact tree can be built in O(n),
and any interval value can be queried with O(log n) arithmetic operations.

### Force and optimize the shape class

For an interval of k keys starting at i, its constant baseline is B+i.
If I is the unweighted internal path length, the total comparison length of
all keys and gaps is D=2I+3k. Any tree has I<=k(k-1)/2, hence
D<=k^2+2k. Relative weights in the interval are between zero and k, so their
entire contribution is at most n(n^2+2n). One extra unit of I costs at least
2B, which exceeds this bound. Every optimum therefore has minimum I.
Equation (2) is -3-v_2(g+1)<0 for (5), so filling the last level from the
left is optimal (indeed unique within this class).

### Exact formula

For k=j-i>0 define h=floor(log2(k+1)), c=2^h-1, s=k-c, and

    I(k) = (h-2)2^h + 2 + hs,
    D(k) = 2I(k)+3k,
    J(c) = sum_(t=1)^c (t-1)v_2(t),
    T(c,s) = sum_(t=1)^c min(s,t)v_2(t),
    E(k) = h c^2 - J(c) + s(2hc+h+1) + (h+3)s(s-1) - T(c,s).

Then

    C(i,j) = (B+i)D(k)+E(k).                                      (6)

To derive E, the perfect skeleton has linear-weight cost h c^2-J(c).
If a set S of bottom slots is expanded, a base key at r shifts by the number
of selected slots <=r, and a base gap at g shifts by the number <g. Summing
their index changes and the added key/gap costs gives

    E(S) = h c^2-J(c)
           + sum_(g in S) [2hc+3g+h+1 - sum_(t=g+1)^c v_2(t)]
           + (2h+3)|S|(|S|-1)/2.

Substitute S={0,...,s-1}; the nested sum is T(c,s), giving (6).

The sums do not need enumeration. For each ell=1,...,h-1, let
d=2^ell, m=floor(c/d), u=min(m,floor(s/d)). Its contributions are

    J: d m(m+1)/2 - m,
    T: d u(u+1)/2 + (m-u)s.

There are O(log n) terms. Once the family is recognized by a linear input
scan, the oracle requires only n and B, without a quadratic table.
Recursive left-filled construction emits each key once; its root has
left-subtree size 2^(h-1)-1+min(s,2^(h-1)). This is also the shape constructed
by the checked general certificate, not an assumed heuristic for all inputs.

### Dense second and fourth differences

Define d(i,j)=C(i,j+1)+C(i+1,j)-C(i,j)-C(i+1,j+1), for i<j<n.
Within a fixed h band, for 1<=s<2^h,

    d(i,j)=3+v_2(s),   s=(j-i)-(2^h-1).                            (7)

Here D has slope 2h+3, and E has second difference 2h+6+v_2(s).
The formula extends through the endpoint needed for s=2^h-1 because filling
all the bottom slots produces the next perfect skeleton.

For 2<=s<=2^h-2, all three density diagonals stay in this band, so

    d(i,j+1)+d(i+1,j)-d(i,j)-d(i+1,j+1)
      = v_2(s+1)+v_2(s-1)-2v_2(s),                               (8)

which is strictly positive for odd s and strictly negative for even s.
For n=2^m>=32 take h=m-2 and 2<=s<=n/4-2. There are n/4-3 eligible
lengths and at least n/2+2 placements per length. Thus at least

    (n/4-3)(n/2+2) = Omega(n^2)

fourth-difference cells are nonzero; the second-difference support is also
Omega(n^2). The same band forces quadratically many rowwise density changes.

Any algorithm that explicitly lists either of these supports has quadratic
output work on this family. This is a lower bound on those representations,
not on exact OBST construction: (6) and the linear constructor solve the same
family compactly. It also shows that merely differencing a core again does
not repair the unrestricted core-size obstacle. The known dyadic baseline
should instead be represented symbolically; closure under min-plus products
with arbitrary residual weights remains unproved.

## 4. Evidence and next research consequence

All arithmetic in the harnesses is exact. No timing or universal speedup is
inferred from the following counts.

- `ruler_layers.py`: 921 layer solves, 70,100 ruler-identity interval checks,
  22,437 range-maximum checks, 20,432 all-root checks, and 2,168 all-shape
  layer checks. The diagnostic deliberately computes 5,708,220 layer states
  and 11,108,348 layer candidates. Separate full-table controls use
  1,422,592 states and 2,692,718 candidates, with 96 cubic comparisons.
- `ruler_barrier.py`: 68 family sizes through 512, 221,284 interval/formula
  checks, 202,127 density checks, 179,486 fourth-difference identity checks,
  2,974 enumerated shapes, and 13 cubic controls. At n=512 every one of
  130,816 ordinary core cells and 129,795 valid fourth-difference cells is
  nonzero. The proof above only needs the explicit quadratic subfamily of
  cells; it does not infer a theorem from these observed complete supports.
  Formula/tree controls continue through 65,536 keys without dense tables.
- `ordered_complete.py`: 1,210 full solves, 826 cubic controls, 658 comparisons
  with the prior shape DP, and 386 independent minimum-IPL enumeration checks
  over 950 shapes. The gate certifies 349 cases; 512 fail the exchange
  condition and 349 pass the shape condition but fail the global gate.
  All fallback results are checked. At 98,304 keys the positive-ramp case
  uses 98,303 exchange checks, 98,304 constructed keys, 196,607 order-scan
  pairs, 98,304 residual contractions, and 121,509 queue comparisons, with
  no interval DP or comparison sort. This size has a wide, roughly half-filled last
  level; the shortcut is not relying on a narrow optional-slot DP.

The next obstacle is representation algebra: the dense ruler baseline is
cheap to query, but subtracting it leaves a residual that need not be Monge.
We do not yet have a general efficient product or an exact adaptive partition
that exploits this baseline while handling arbitrary nonuniform weights.
The earlier compact implementation's measured regressions remain unchanged.
