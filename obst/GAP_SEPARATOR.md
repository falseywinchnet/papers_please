# Exact separators for dominant keys and gaps

This extends the full mixed-weight constructor with inexpensive certificates
that split the original ordered input into independent contiguous intervals.
The terminal intervals use the variable mass-frontier solver, with their own
local total masses. The purpose is to prevent one heavy outcome from inflating
the admissible interval domain in unrelated regions. The general worst case
remains quadratic. Priority of the sufficient separator conditions is not
established; no claim of inventing dominant-weight tree arguments is made.

## Restricting a tree to an interval

For a contiguous key interval and its endpoint gaps, delete comparisons at
keys outside the interval and follow the branch containing all retained
outcomes. Keep the remaining comparisons. This gives a valid search tree
on exactly the retained keys/gaps, without increasing any retained depth.
If the original root was outside the retained interval, every retained depth
decreases by at least one. This observation includes endpoint gaps, not only
successful-search weights.

## Interior-gap certificate

In a current component, let gap g have weight q, with adjacent keys a=g-1
and b=g of weights p_a,p_b. Let L be the interval strictly left of a and R
the interval strictly right of b, including their endpoint gaps. Write
W_L,W_R for their total masses, and W for the whole component mass:

    W = W_L + p_a + q + p_b + W_R.

If

    q + min(p_a,p_b) >= W_L + W_R,

there exists an optimal tree with g at depth two. Its top keys are exactly
a,b, in one of their two orientations. This is an existence certificate;
at equality other optimal shapes may also exist.

Proof: take any tree where g has depth at least three. Restrict it to L and R.
If its root lies in L, make a the root, attach the restricted L as its left
child, and make b its right child, with g on b's left and restricted R on
b's right. Every L outcome deepens by at most one. Every R outcome lost at
least its old root comparison, then gains two comparisons, so also deepens
by at most one. Key a becomes at least one level shallower; b does not
deepen. Gap g becomes at least one level shallower. Total cost change is
at most W_L+W_R-p_a-q. If the original root is in R, use the mirror image,
with change at most W_L+W_R-p_b-q.

If the old root is a, keep it as root and promote b to its right child.
The L depths do not increase, and R depths increase by at most one.
Since a,b are adjacent and g was deeper than two, b was at depth at least
two and saves at least one comparison. The change is at most W_R-p_b-q.
The case with old root b is symmetric. The stated condition makes every
case nonpositive. Apply the exchange to an optimum. An interior gap cannot
have depth below two, and at depth two its two bounding keys must be the
adjacent keys a,b, proving the structural claim.

Both key weights matter. Replacing min by max is false: with
p=[100,1,50],q=[1,1,1,1], the max-based test accepts gap 1, but forcing it to
depth two costs 261 while the full optimum is 212. This positive counterexample
is preserved in the harness.

## Solve the outside intervals once, then choose the orientation

Let C_L,C_R be the exact relative costs for L,R. Once the certificate passes,

    OPT = C_L+C_R+W+q+min(p_a+W_L, p_b+W_R).

With a at the root, the extra term is p_b+W_R; with b at the root, it is
p_a+W_L. Both orientations have the same two outside optimization problems.
Thus the solver does not branch into two recursive solves of each side.
Key weights, gap weights, and all depth offsets remain in the formula.

## Endpoint and key certificates

For a left endpoint gap and its adjacent key, if q_left+p_first is at least
the mass of every other outcome, there is an optimum with the first key as
root. The right endpoint is symmetric. If the adjacent key has original
depth h>=1, the endpoint gap has depth h+1. Promoting the key to root saves
h*(p+q), while restricting the other interval and attaching it below the
new root increases its cost by at most its mass. The condition makes the
exchange nonpositive. These endpoint tests are O(1) per component.

For any key r, 2*p_r>=W also suffices to place it at the root: restrict the
two sides and attach them beneath r. Other outcomes deepen by at most one,
whereas r saves at least one comparison if it was not already the root.
Its exact cost is W+C_left+C_right. These elementary dominance arguments
are used as certificates, not as a general rule for picking the largest key.

## Static range indexes prevent quadratic separator scanning

The recursive components are contiguous intervals of the ORIGINAL input;
no weight aggregation or relabeling changes the score of a surviving outcome.
For each original internal gap j define

    G_j = 2*q_j + p_(j-1) + p_j + min(p_(j-1),p_j),

and for each key define K_j=2*p_j. The gap certificate in component [i,k)
is exactly G_j>=W(i,k) for i<j<k. A range maximum query finds a qualifying
gap, if any. Another index finds qualifying keys. Prefix sums give W(i,k).
Both segment-tree indexes take O(n) build work and O(log(n+1)) per query.

The implementation checks endpoint certificates first. Index construction
is lazy: if endpoint rules exhaust the whole input, no range index is built.
All-zero components are returned as balanced trees directly. If no certificate
passes, the component is solved exactly by the existing mass-frontier method
or by Knuth in the controlled `terminal='knuth'` variant. Empty components
cost zero relative to their root and require no terminal optimization.

Each separator removes one or two keys from further subproblems. Terminal
intervals are disjoint and their total number of keys is at most n. No
whole-component array is copied during separator recursion; terminal slices
are disjoint. Therefore even a chain of n splits pays only O(n log(n+1))
separator work, not a quadratic rescan of shrinking components. Recursion
is a Python prototype and the harness raises the stack limit for deep trees.

If terminal component t has m_t keys and local contour counts S_(t,d), total
arithmetic work is

    O(n log(n+1) + sum_t min_d [S_(t,d)+m_t*2^d]).

Local parameter-selection costs are included because
sum m_t*log(m_t+1)<=n*log(n+1). The method remains O(n^2) in the worst case.
If all terminal sizes are bounded by b, the work is O(n log(n+1)+n*b), since
each terminal can choose its full Knuth table. Sequential scratch reuse gives
O(n+max_t[S_(t,d_t)+m_t*2^d_t]) storage including output and separator stack.
These are arithmetic bounds, not bit-complexity bounds for large integers.

## A linear arithmetic regime with full mixed weights

Set p_i=2^i and q_i=2^i for i=0..n-1, and q_n=2^n. The rightmost key and
gap have combined mass 3*2^(n-1), while the entire component has mass
3*2^n-2. Hence the right endpoint certificate passes, and the remaining
prefix has exactly the same form. Repeating yields the optimal rightmost-root
chain with n endpoint decisions, no range index, and no terminal DP: O(n)
arithmetic work and space. Reverse the input for the mirrored result.
The weights have O(n) bits, so this statement does not assert linear bit work.

Hierarchical dominant gaps give a different regime: recursively planted
central heavy gaps separate mixed random background intervals of bounded
size. The separator hierarchy then has O(n log n) total work by the terminal
bound above. The tests include varying positive weights on both keys and gaps.
This is a structured-family guarantee, not a general subquadratic solution.

## Verification

The harness exhaustively checks 22,140 inputs with weights in {0,1,2} through
four keys against every tree shape. It verifies 3,211 qualifying interior-gap
certificates (including the two-orientation cost formula), 2,036 endpoint
certificates, and 380 heavy-key certificates. All equality and zero-weight
cases are included. Another 3,280 full solves use both terminal strategies
on 1,640 inputs through 40 keys, including the empty input, geometric variants,
spikes, zeros, key-only and gap-only controls, and independent random mixtures.
Each matches an independent cubic recurrence and direct tree evaluation.

A 40-fixture larger sweep compares both terminal strategies against Knuth
and direct mass-frontier construction through 2,048 keys. Counter categories
include endpoint checks, range-index construction/query comparisons, separator
counts, terminal interval work, local matrix queries, and reconstruction.
The initial gap-first implementation was also correct; the final endpoint-first
version avoids index work on a fully certified endpoint chain.


## Operation counts at 2,048 keys

| Fixture | Direct frontier interval cells | Local frontier interval cells | Terminal components |
|---|---:|---:|---:|
| Random | 308,115 | 308,115 | 1 |
| Near-uniform | 309,290 | 309,290 | 1 |
| Geometric | 2,098,176 | 0 | 0 |
| Heavy key | 1,048,576 | 153,660 | 2 |
| Heavy gap | 1,047,552 | 153,582 | 2 |
| Random background, heavy gap | 1,047,552 | 153,362 | 2 |
| Hierarchical gaps | 522,242 | 22,333 | 64 |

Knuth has 2,098,176 interval cells in every row. Cells are only one category
of work. The hierarchical-gap case uses 63 separators, 254 endpoint checks,
6,142 range-index build comparisons and 1,476 range-query comparisons. Local
solves use 42,885 root candidates, 39,284 genuine top-matrix queries, 6,261
padding queries, 8,122 contour mass checks, 6,952 scans each for rows and
columns, and 1,792 coarse transitions. The heavy-gap case still requires
305,118 root candidates and 1,214,092 genuine top queries. Raw counts are
in `results/gap_separator.json`.

Terminal solver counters are added over components. Metadata such as
`terminal_actual_height`, `terminal_selected_depth`, and
`terminal_selected_width` are therefore sums of local values, not the
height/depth/width of the combined tree. `max_separator_depth` counts
separator recursion levels; a gap separator may contribute two BST levels.
The exact terminal sizes are retained separately.

## Matched timings

Ten balanced orders per fixture compare five solvers: five cyclic rotations
and their reversals, not all 120 permutations. The 70 trials contain 350
full timed solves, including preprocessing and reconstruction. Every tree's
cost is independently evaluated and all five answers agree. The platform is
Apple M4, Python 3.9.6. Inputs vary between trials except deterministic spike
and geometric families. Each entry is a median paired runtime ratio to Knuth;
smaller is better. SF uses frontier terminals, SK uses Knuth terminals, and
RC is the earlier recursive contraction solver.

| n / Fixture | Direct frontier | SF | SK | RC |
|---|---:|---:|---:|---:|
| 2,048 / Random | 0.87985 | 0.87172 | 1.03209 | 1.00381 |
| 2,048 / Near-uniform | 0.87747 | 0.90863 | 1.06833 | 1.06450 |
| 2,048 / Heavy key | 0.99362 | 0.74038 | 0.52307 | 0.01605 |
| 2,048 / Heavy gap | 0.99617 | 0.77197 | 0.51357 | 1.03871 |
| 2,048 / Random background, heavy gap | 0.90780 | 0.75211 | 0.49766 | 0.97692 |
| 2,048 / Hierarchical gaps | 1.06953 | 0.04608 | 0.01843 | 0.99421 |
| 1,024 / Geometric | 1.05318 | 0.00781 | 0.00548 | 0.04206 |

The gap certificate adds substantial coverage where RC does little, especially
hierarchical gaps. RC remains much faster on the heavy-key fixture. The local
frontier terminal implementation is slower than plain Knuth on these smaller
components despite reduced cell counts. SF and SK follow the same endpoint
path on geometric inputs, so their timing difference is not algorithmic.
Random and near-uniform controls do not split. These instrumented Python
measurements do not establish broad or production-language superiority.
Raw per-trial values and counters are in `results/gap_separator_matched.json`.

## A positive obstruction to this architecture

For every n>=5, set every key weight and every ordinary gap weight to one,
except q_1=q_(n-1)=M=n^3. The total mass is W=2M+2n-1. Both endpoint scores
are four, every key score is two, and the largest interior-gap score is
2M+3<W. No separator fires, so the entire input reaches the frontier planner.

In fact the planner chooses depth zero, not merely a quadratic-size contour.
Write tau(k)=k(k+1)/2 and h=floor((n-1)/2). At depth one all tau(n) cells
are admitted. At depth two the cutoff is W/2=M+n-1/2: an interval containing
one heavy gap has mass M+2*length, so it is admitted exactly when its length
is at most h. There are four disjoint such sets of h intervals, while the
intervals excluding both heavy gaps are exactly those on the middle n-4
keys. Hence S_2=tau(n-4)+4h, and S_2+4n=tau(n)+6+4h>tau(n).

For d>=3 with 2^d<=n, F_(d+1)>=3 and F_(d+1)<=2^d<=n. Thus the cutoff
is below M but above every all-unit interval mass. Exactly tau(n-4) cells
are admitted, and S_d+n*2^d>=tau(n-4)+8n=tau(n)+4n+6>tau(n).
If 2^d>n, the top term alone exceeds n^2>=tau(n). Every positive depth is
therefore worse than the depth-zero direct Knuth plan, which stores tau(n)
cells. This is a Theta(n^2) obstruction to this particular constructor;
it is not a lower bound for full OBST or for all combinations of shortcuts.

The independent contour checker caught an initial counting error: not every
interval containing only one heavy gap is admitted at depth two. The correct
length cutoff and four sets of h intervals above are now checked explicitly.
`separator_obstruction.py` checks all potentially competitive depth contours,
uses full solves only at small sizes, and marks larger rows as plan counts.
The obstruction points toward handling several comparable heavy outcomes
together rather than relying only on a single dominant outcome.

The obstruction harness checked eight full instances through 256 keys against
Knuth and reconstructed costs, including cubic checks through 32 keys. Four
larger instances through 65,536 keys count plans only. At 65,536 keys the
selected plan has 2,147,516,416 interval cells; that full solve was not run.
Raw results are in `results/separator_obstruction.json`.
