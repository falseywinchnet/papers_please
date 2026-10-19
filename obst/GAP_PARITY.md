# A global lower bound for alternating gap weights

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
the repository owner. This is a proved component bound for the full mixed-weight
OBST objective. Mathematical priority has not been established.

For n>=1, write h=floor(log2(n+1)), S=2^h, s=n+1-S. Let q_j alternate
between arbitrary nonnegative values a and b. Every minimum-internal-path-length
shape has exactly the same gap cost:

    G(q) = h sum(q) + s(a+b).

The new fact needed by the constructor is that G(q) is a lower bound for
**every** binary search tree, including taller trees.

## Deleting one parity of leaves

Fix one parity of the n+1 inorder gaps. Give these H leaves unit weight and
the other Z=n+1-H leaves zero weight. Delete a zero leaf and contract its
parent into its sibling. The sibling contains at least one selected leaf:
remaining zero leaves are separated in inorder by selected leaves, and a
subtree has a contiguous leaf interval. An all-zero sibling subtree would
contradict that separation. Deletion preserves separation because it removes
only zero leaves. Every contraction reduces the selected depth sum by at
least one. After all Z deletions, a full tree with H unit leaves remains.

Its external path length is at least E_min(H). Here S/2<=H<=S, so

    E_min(H) = (h+1)H-S,
    E_min(H)+Z = hH+s.

The formula is valid at both power-of-two endpoints. Thus the original
selected depth sum is at least hH+s. A minimum-IPL shape attains equality:
every gap is at depth h or h+1, and each of its s bottom cherries supplies
one deeper gap of each parity. Applying the argument separately to the two
parities and multiplying by a,b proves the full gap bound G(q).

The assumption a,b>=0 is needed when adding the inequalities. No large
baseline, relative-amplitude restriction, or positive lower bound is needed.
For n=0, the single gap is at depth zero and its contribution is zero.

## Combining the gap bound with the key bound

Let p_(1)>=...>=p_(n) be the key weights sorted by value, ignoring their
fixed inorder positions only for this lower bound. Every BST satisfies

    key_cost >= K(p) = sum_(r=1)^n p_(r) bitlength(r).

There are at most 2^(d-1) keys at comparison length d. Thus its sorted
comparison lengths dominate bitlength(1),...,bitlength(n) componentwise;
the rearrangement inequality pairs the largest nonnegative weights with
the shortest lengths. Consequently

    OPT(p,q) >= K(p) + G(q).

If a legal minimum-IPL tree attains K(p) on its keys, it attains this global
mixed lower bound exactly and is globally optimal. This certificate compares
with every taller tree. It does not assume that the optimum is nearly complete.
Finding an attaining tree for arbitrary key weights remains a separate task.

## Linear construction for recognized two-level patterns

Suppose key weights take two values l<u, with H high keys, and
S/2-1<=H<=S-1. The parity-interval recognizer in PROFILE_INTERVALS.md
finds a word with S-1 skeleton keys, no adjacent removed keys, every high
key retained, and every even skeleton rank high, or proves that this
specific profile is unattainable. Such a word assigns all high keys to the
shortest H comparison lengths and all low keys to the remaining lengths.
It therefore attains K(p), and the gap theorem proves full optimality.

The implementation takes O(n) arithmetic work and O(n) auxiliary space,
including validation, recognition, reconstruction, and the certificate.
Only two key multiplicity records are ordered; no general sort or residual
Huffman bound is required on this path. Arbitrary integer magnitudes retain
their bit costs. The recognized family includes nonperiodic patterns and
can have n distinct neighboring joint signatures.

One key level is handled directly. At perfect sizes s=0, the unique class
tree is evaluated: if it attains K(p), the new global bound certifies it;
otherwise the older mixed-Huffman gate may certify it, and failure invokes
exact fallback. An unsuccessful recognition also invokes exact fallback;
it does not prove that every minimum-IPL tree is suboptimal.

## Strict alternation without a baseline

For s>0, strictly alternating two-level keys always admit the profile.
Let A=1 when the first key is high and A=0 otherwise. If s mod 2=A,
remove the first s low keys. Otherwise remove the first s-1 low keys and
the last low key. All removed positions are nonadjacent and every high
key remains. Before the initially removed lows end, retained keys are high.
After removing t initial lows, a high key has skeleton-rank parity A-t.
Thus the unmodified suffix has high keys at even ranks when t mod 2=A.
In the second construction, deleting the final low affects at most one
subsequent high, which may occupy an odd rank. Every even rank is high.
There are enough lows because s<=S-1, and the high count is in the stated
range. The recognizer therefore succeeds.

Hence, for every n>=1 with n+1 not a power of two, arbitrary nonnegative
strictly alternating two-level key weights and arbitrary nonnegative
alternating gap weights admit a full exact O(n)-time, O(n)-space constructor.
The levels may have arbitrary relative magnitudes. Equal key levels are
covered by the direct uniform route. This is an explicit mixed-weight
family with k=n and no baseline restriction.

The perfect-size exception is essential. With p=(100,1,100) and all four
gap weights zero, the unique minimum-IPL tree costs 401, but the full optimum
is 303. Cubic DP and Knuth agree. Therefore the no-baseline alternating
corollary must not silently include every size/orientation.

## Independent evidence

`code/check_gap_parity.py` enumerates every BST through nine keys. It checks
13,834 parity/tree inequalities and 69,170 mixed-weight/tree inequalities
with seeded arbitrary key values and alternating gap values. For each size
and parity it verifies equality of the best tree and the formula. The perfect
counterexample is retained. Results and source hashes are in
`results/gap_parity.json`.

The full constructor, independent word/tree checks, scaling counts, and
matched comparisons are in `code/profile_complete.py`,
`code/check_profile_complete.py`, and `code/benchmark_profile_complete.py`.
The general unrestricted mixed-weight problem remains open: arbitrary gap
sequences, nonattaining key patterns, and taller optimal shapes can still
invoke quadratic fallback. This bound does not establish priority or a
universal subquadratic algorithm.
