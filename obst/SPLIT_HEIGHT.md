# Split-height construction with a certificate against taller trees

The full input has nonnegative weights on every key and gap. This checkpoint
implements a known height-restricted optimization mechanism, then tests a
separate sufficient condition for unrestricted optimality. It does not assume
the unknown optimum is shallow. Failed certificates invoke full Knuth DP.

## Prior work and the change in scope

Karpinski, Larmore, and Rytter already describe splitting a height limit into
two halves, computing small height-restricted interval costs, and composing
them using Monge structure. Section 5, "Short height limited trees," of their
longer preprint explicitly states the fixed-height Monge property and this
construction. The six-page SODA version has different section contents.

- Longer preprint: https://www.researchgate.net/publication/2710579_Sequential_and_Parallel_Subquadratic_Work_Algorithms_for_Constructing_Approximately_Optimal_Binary_Search_Trees
- Conference version: https://theory.cs.uni-bonn.de/marek/publications/seq_and_par_subquadr.pdf

We do not claim to invent that algorithm or the Monge property. Our explicit
dyadic implementation, exact taller-tree exclusion test, and measured behavior
are the present experiment. The previous excess-budget representation could
have quadratic width even at zero excess, and skipped such sizes. A height
budget gives subquadratic attempted work at every size, although the new
attempt is more expensive on the narrow shape classes handled earlier.

## Exact class optimizer

Let H be the maximum external depth; the root has depth zero. Split H=L+U.
The implementation uses L=min(H,floor(H/2)+1). Set K=2^L and B=2^U.
Represent the tree by aligned dyadic leaf intervals in [0,1]. The top grid
has B blocks. A leaf above depth U occupies several grid blocks. Otherwise,
a grid block contains a complete lower subtree of height at most L.

First compute C_h(i,j), the optimal relative cost for keys [i,j) and their
endpoint gaps, with height at most h, for h=0..L and j-i<=2^h-1. Empty trees
have cost zero. The recurrence is

    C_h(i,j)=W(i,j)+min_r(C_(h-1)(i,r)+C_(h-1)(r+1,j)).

Only roots whose children fit the preceding height are feasible. Fixed-height
Monge inequalities give monotone minimizing roots as either endpoint moves;
choosing the leftmost tie permits the usual adjacent-interval bounds. For
each length, the root-search ranges telescope to O(n) work. Summing over
lengths and heights costs O(n*2^L), including all tables and backpointers.

At a top-grid boundary b, define D_b(i) to be the minimum cost of a partial
tiling that has consumed i gaps. It has already charged keys 0..i-2. For b>0
the boundary key i-1 has comparison length U-v2(b); charge its weight before
the following transition. At b=0 there is no boundary key. Write this charged
prefix value as R_b(i).

There are exactly two transition types:

1. A complete lower subtree, from (b,i) to (b+1,j), where i<j<=i+K, costs
   R_b(i)+C_L(i,j-1)+U*W(i,j-1).
2. A coarse gap, from (b,i) to (b+w,i+1), where w>=2 is a power of two,
   b is divisible by w, and b+w<=B, costs
   R_b(i)+q_i*(U-log2(w)).

The zero-key lower subtree covers width-one gaps. These transitions cover
every tree of height at most H and only such trees. The complete state is
D_B(n+1). Following backpointers recovers each lower tree and every boundary
key; its comparison length is U-v2(b). All key weights retain their fixed
inorder positions.

For fixed b, lower-subtree transitions form a banded Monge matrix in i,j.
Adding R_b(i) and the separable interval mass preserves the inequality.
SMAWK finds its column minima in linear queries. Reachable counts i form an
interval: the coarsest dyadic tiling of the prefix uses popcount(b) leaves,
and repeated leaf refinement realizes every count through b*K. Truncating
to at most n consumed gaps preserves this interval. Thus the searched output
columns j=first_i+1 through min(n+1,last_i+K) each have a feasible entry.

### Padding the band correctly

Tied infinity padding can destroy total monotonicity. Let
S=(H+1)*(sum(p)+sum(q))+1, strictly larger than every feasible prefix cost.
For matrix row j and candidate column i use

    S+j-K-i       if i<j-K,
    S+i-j+1       if i>=j,
    true cost    otherwise.

For fixed j, left-invalid entries improve toward the band and right-invalid
entries worsen away from it. As j increases the band moves right. For two
candidates i1<i2, once i2 strictly improves on i1 it cannot lose that strict
preference: while both are feasible this follows from Monge; outside the
band the distance penalties and the dominance of finite entries preserve
it. The same non-strict implication holds for ties. This is total monotonicity
in the orientation used by SMAWK. All output minima are feasible. Padding
queries are counted separately from genuine interval-cost queries.

Across b there are B-1 aligned choices of coarse width, so their work is
O(nB), including scans of possible prefix counts. Total work and stored
backpointers are

    O(n*(2^L+2^U)) = O(n*2^(H/2)).

For H=ceil(log2(n+1))+c with fixed nonnegative c, this is O(n^(3/2)). The
certificate adds O(n log n) weight sorting and linear residual-bound work.
The Python prototype uses dictionaries for reachable states; the finite
integer ranges also permit direct array indexing. These are arithmetic
operation bounds, excluding arbitrary-precision bit costs. The retained
divide-and-conquer search has an extra logarithmic factor in matrix queries.

## Exact minimum path length outside the height class

Let J(n,R) be the minimum unweighted internal path length among n-key trees
with external height at least R. If R>n the class is empty. Otherwise force
a root-to-leaf path containing R internal nodes, contributing R(R-1)/2.
The remaining nodes belong to the free forest beside this path: one free
root at each depth 1..R-1 and two at depth R. Fill the shallowest available
positions until n nodes have been placed.

Every tree in the class contains such a path. Its remaining nodes form an
ancestor-closed subset of that forest. The first n-R shallowest positions
are ancestor-closed and minimize their depth sum among all subsets of that
size. Hence the greedy value is exactly J(n,R), regardless of the direction
of the forced path. A level-count recurrence computes it without materializing
the tree. It takes O(R+log(n+1)) arithmetic work.

Set a=min(p), b=min(q), and let Q be the existing order-free mixed-node Huffman
bound on p-a,q-b. Every tree taller than H costs at least

    B_H=(a+b)*J(n,H+1)+(a+2*b)*n+Q.

This follows from external path length = internal path length + 2n. If the
computed height-restricted optimum is at most B_H, it is globally optimal.
If H>=n there is no excluded tree and certification is automatic. Otherwise
a failed test is inconclusive and solve() runs Knuth. With fixed c, the full
constructor retains O(n^2) worst-case work. No restriction is put on either
the key weights or the gap weights for correctness.

## Independent verification

The final SMAWK harness passed:

- 450 weighted height-class optima against exhaustive shapes through n=8;
- 44 exact tall-tree minimum-IPL comparisons against all shapes;
- 2,000 full mixed-weight inputs checked against cubic DP and direct cost,
  including successful certificates and complete fallback (917 certificates);
- 520 independent all-root height-DP comparisons, also comparing SMAWK
  against the divide-and-conquer implementation;
- 261,482 stored short-table entries against the independent height DP;
- 104 additional adversarial-family checks, including zeros, geometric
  weights, spikes, key-only and gap-only controls.

The larger sweep contains 36 fixtures at three height budgets each. All
near-uniform fixtures, including n=384,768,1000,1536, certified at every
tested budget. Random, geometric and gap-spike fixtures failed certification,
sometimes despite an optimal candidate. This is a lower-bound limitation,
not evidence that their true optimum must exceed the height limit.

At n=1000, the minimum-height near-uniform candidate and full optimum both
cost 18,973,413, below the exclusion bound 18,974,193. It uses 117,453 short
states, 220,483 short root candidates, 84,937 genuine top matrix queries,
10,268 padding queries, 16,016 top row scans, and 5,630 coarse transitions.
The bound adds 10,648 sorting and 1,335 merge comparisons and 1,000 contractions;
all 1,000 keys are reconstructed. Knuth uses 500,500 states and 1,002,162 root
candidates. Different operation types are reported separately, not equated.

Raw correctness/sweep evidence is results/split_height.json. The earlier
divide-search sweep is retained separately as split_height_divide.json; its
split and random fixture sequence differ, so those files are not a matched
performance comparison. Matched timing is a separate experiment with all
six solver orderings per fixture, timing preprocessing and reconstruction.

## Matched timing and limits

The 48 matched trials compare Knuth, minimum feasible height (c=0), and
one extra level (c=1), with every output directly evaluated and checked
against Knuth. Inputs are identical within each trial and vary between
trials except the repeated periodic fixture. Hardware is the sponsor's
Apple M4; Python is 3.9.6. Ratios are medians of per-trial solver/Knuth time.

| Fixture | c=0 ratio | c=0 certified | c=1 ratio | c=1 certified |
| --- | ---: | ---: | ---: | ---: |
| n=384, near-uniform | 1.22484 | 6/6 | 2.29965 | 6/6 |
| n=768, near-uniform | 0.94444 | 6/6 | 1.40863 | 6/6 |
| n=1000, near-uniform | 0.71530 | 6/6 | 1.03015 | 6/6 |
| n=1536, near-uniform | 0.65826 | 6/6 | 1.03916 | 6/6 |
| n=3072, near-uniform | 1.46288 | 0/6 | 0.70837 | 6/6 |
| n=1536, amplitude4 | 1.67333 | 0/6 | 1.18924 | 6/6 |
| n=1536, ordinary random | 1.55378 | 0/6 | 1.93841 | 0/6 |
| n=1023, periodic A=16 | 1.69541 | 0/6 | 1.06171 | 6/6 |

These results are mixed. Fewer arithmetic operations do not imply a faster
Python implementation at these sizes; small successful cases can still be
slower. An extra level strengthens the exclusion bound but increases work.
At n=3072 the c=0 candidate is already optimal in all six trials, but its
certificate fails; c=1 certifies. At the periodic fixture c=0 actually misses
the unrestricted optimum, while c=1 includes it. Ordinary random data still
pays substantial overhead and then the full quadratic fallback. The earlier
bounded-excess solver is preferable on its tested narrow periodic shape class.
All observations and counters are retained in results/split_height_matched.json.

The next unresolved algorithmic issue is avoiding this failed-attempt cost
and obtaining stronger unrestricted guarantees for nonuniform inputs. A
proper implemented comparison with the known width-limited Larmore/KLR
construction is also still missing; height-only measurements do not establish
an improvement over that prior full-OBST algorithm.
