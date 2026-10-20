# Certified coarse optimal faces and arbitrary-weight refinement

A low-mass integer instance can serve as an exact structural certificate for
nearby arbitrary weights. The coarse optimum need not be unique. We retain
roots shared by all coarse optima and solve only the remaining ambiguous
intervals with the original key and gap weights.

For a certified coarse instance of total mass O(n), and largest ambiguous
interval b, full construction takes

    O(n^(3/2) log^(3/2)(n+1) + n b)

arithmetic operations. Every original key and gap participates. The bound is
subquadratic whenever b=o(n). Global ambiguity can give b=n, and the automatic
constructor retains a quadratic worst case. The general research goal remains
open. This is a stability reduction using the existing Monge theorem and
published witness primitive; no priority claim is made for perturbation theory.

Perturbation arguments preserving optimality already occur in search-tree
work: [Chrobak, Golin, Munro and Young](https://www.cs.ucr.edu/~neal/Chrobak22Simple.pdf)
use infinitesimal changes to resolve ties in two-way comparison trees. Here
the integer cost gap gives an explicit finite signed-error certificate, and
the common-root partition supplies the construction bound.

## A signed-error certificate that preserves every optimum

Let a=(a^p,a^q) be nonnegative integer weights on the same ordered keys and
gaps, and let x=(p,q) be arbitrary nonnegative real weights. For a scale delta>0,
write x=delta*a+e and E=sum_o |e_o| over all 2n+1 outcomes. The errors can have
either sign. For n>=1, every key comparison length and gap depth lies in [1,n].
Hence, for every two full trees T and U,

    |C_e(T)-C_e(U)| <= (n-1) E.                              (1)

Suppose

    (n-1) E < delta.                                        (2)

If U is coarse-optimal and T is not, their integer coarse costs differ by
at least one. Therefore

    C_x(T)-C_x(U)
       = delta [C_a(T)-C_a(U)] + C_e(T)-C_e(U)
       >= delta-(n-1)E > 0.

Every fine-weight optimum is consequently coarse-optimal. There is no
uniqueness assumption and no need to guess which tied coarse optimum the
fine weights prefer. For n=0 the sole empty tree is handled directly.

## Unrestricted minimum and maximum optimal roots

Compute the final unrestricted coarse interval-cost matrix C* in condensed
Monge form, using the main constructor. Its sufficient height ensures that
all interval costs are unrestricted optima. Make one further min-plus product
with child terms C*(i,r) and C*(r+1,j). The existing finite padding handles
invalid roots as before. The exact leftmost witness gives the smallest
unrestricted optimal root of every interval. Repeat on reversed key and gap
sequences to obtain the largest root by reflection.

That last product matters: a sufficient height guarantees some optimum, not
all of them. On 2^h-1 all-zero keys with all-zero gaps, the unique tree of
height at most h is perfect, while every full BST is unrestricted-optimal.
Comparing two height-limited reconstructions can therefore falsely suggest
uniqueness. The new witnesses use unrestricted children and are reused at
every subtree depth, without decreasing a height budget.

Let S be the aggregate core-size quantity of the existing Monge theorem,
including its linear boundary terms. The extra products cost O((n+K_H)log(n+1))
and have O(K_H) output cores by the cited primitive. They are covered by
O(S log(n+1)) total preprocessing. Each extreme-root query costs O(log(n+1)).
No dense interval table is constructed for the coarse instance.

## The common-root partition

Start with [0,n). On a nonempty interval I, query its smallest and largest
optimal roots. If they agree at r, every coarse-optimal tree uses r there;
retain that key and recurse on its left and right intervals. If they differ,
stop and mark I ambiguous. At most n nonempty intervals are visited, so
partition extraction costs O(n log(n+1)). The stopped intervals are disjoint
in keys, with sizes m_1,...,m_t satisfying sum m_j<=n. The partition is empty
of ambiguous intervals exactly when the coarse optimum is unique.

By induction down retained roots, every coarse-optimal tree contains the
retained skeleton. By (2), every fine-optimal tree contains it as well.
For each ambiguous interval, use ordinary Knuth with its original p and q,
including both endpoint gaps. Attach the resulting complete subtrees to the
skeleton. Above an attached subtree, the contribution is its fixed total
mass times its fixed attachment depth; it is independent of the subtree
shape. Thus the payloads minimize independently. The restricted family
contains a global fine optimum, so this construction is globally optimal.

Full work, including coarse preparation and reconstruction, is

    O(S log(n+1) + n + sum_j m_j^2).                         (3)

The n log n partition term is absorbed by the coarse preparation bound.
Let b=max_j m_j, or b=0 if there are no ambiguous intervals. Then
sum_j m_j^2<=nb. At integer coarse mass W_a=O(n), (3) becomes

    O(n^(3/2) log^(3/2)(n+1) + nb).                         (4)

The theorem imposes no run, period, monotonicity, or integrality requirement
on the original fine key and gap sequences. The certificate and the measured
partition size are explicit conditions, not guarantees for all inputs.

After extracting the partition, discard the Monge matrices and witnesses.
Only O(n) base weights, skeleton entries and interval endpoints remain.
For another input x satisfying (2) relative to the same base a and any
positive delta, certificate checking and full construction take
O(n+sum_j m_j^2). A unique coarse optimum gives O(n) per full fine tree after
preparation. The implementation exposes this through Prepared.refine.

Theoretical preprocessing space is O(S) with the published succinct witness
representation. The retained implementation uses ordinary maps and can use
O(S log(n+1)) peak space. Payload DPs are processed sequentially, with peak
O(b^2+n) additional space. Arithmetic bounds exclude operand bit costs.

## An automatic exact constructor

Let X be the largest original weight. For X>0 test delta=X/m for
m=1,...,16. Round each original weight to the nearest nonnegative multiple
of delta, breaking half ties upward, and check (2) exactly. Each resulting
coarse weight lies in {0,...,m}; hence its total mass is at most 16(2n+1).
Scale selection costs O(n), with the constant sixteen independent of n.
All-zero input uses delta=1. If every candidate fails, use ordinary Knuth.
If one succeeds, build its partition and refine as above. The resulting
algorithm is globally exact on every input and has O(n^2) worst-case
arithmetic work. Accepted instances have the sharper bound (4).

An explicitly supplied scale may produce larger coarse mass; then (3), with
that base's actual Monge bound, applies. The implementation accepts exact
integers and fractions. It never rounds a floating-point approximation or
infers correctness from a tolerance.

## A real limitation of this partition

For n=2^h, h>=1, uniform unit key and gap weights have at least two optimal
root positions. Begin with the perfect n-1-key tree and add one key in its
leftmost or rightmost bottom gap. Both trees minimize internal path length,
and their root ranks differ. The partition therefore stops at [0,n), so
its refinement uses the whole quadratic table even for perturbations as
small as desired. This is a limitation of the common-root partition; it
does not assert hardness of optimizing all such perturbations.

## Verification and operation counts

The primary audit checks every interval on 716 coarse inputs: all 680 binary
mixed inputs through four keys plus 36 seeded inputs at sizes 5,8,12. Its
7540 minimum/maximum root pairs agree with an independent all-root DP.
An independent optimal-tree count agrees with all uniqueness decisions;
311 coarse faces are unique. There are 1432 complete signed-rational
refinements, six automatic-scale controls, four certificate-rejection
controls, three zero-coarse-mass controls and twenty queries reusing a
prepared partition. Every output matches an independent original-weight
optimum and an independent tree-cost traversal. Fine interval-DP cell counts
match sum_j m_j(m_j+1)/2 exactly.

The scale audit retains eight unstructured lattice perturbations through
256 keys, with all 2n+1 original weights distinct. The largest ambiguous
intervals are 0,0,3,2,11,128,28,8. Thus one 128-key input retains the entire
table. The 256-key rows use 772 and 168 fine DP cells, but their coarse
preparation also performs 20,585,886 and 19,925,218 core visits, respectively.
These are separate operation categories; the payload savings are not claimed
as full-construction speedups. Four ordinary mixed controls reject all sixteen
scales and use Knuth. Three uniform global-ambiguity controls retain the full
payload table. Twelve further queries reuse four perfect-size uniform
preparations and need no fine DP cells or new Monge products; those uniform
bases already have a direct linear constructor.

Both result files retain all original scale inputs, exact counts, independent
reference counts and eight source hashes. Their finite measurements do not
prove a typical-case or worst-case bound on the ambiguous interval sizes.
