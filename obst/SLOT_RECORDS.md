# Valuation-class records without expanding the perfect tree

At prescribed height h, put c=2^h-1. Normalize arbitrary nonnegative key and
gap weights as in SLOT_VECTOR_CONSTRUCTION.md, obtaining keys w, residual
gaps g with zero endpoints, and a tree-independent additive cost. Let M be
the total normalized mass. Split into s<=r+2e stages: constant-key runs with
zero preceding/internal residual gaps, and single keys after exceptional
gaps. The following algorithm never allocates c slots.

## Records and exact domination

Let f_k(b) be the minimum negative reward for k keys whose last slot is b.
For each valuation d=nu_2(b), f_k(b) is nonincreasing as b increases among
slots of valuation d. Indeed, move only the last selected slot to a later
slot of the same valuation. Its key reward and preceding gap reward remain
unchanged, and order is preserved.

Store the first feasible slot of each class and every strict value decrease,
with an attaining predecessor. Call their number B_k (at stage boundaries).
If an unrecorded state b has the same value as an earlier record a in its
class, a dominates it for every subsequent stage. For a singleton, the
preceding-gap reward is identical and the earlier position preserves
feasibility. For a zero-gap run, the earlier position leaves a superset of
available inner slots. Thus all predecessor minima can be restricted to the
records. Ties need not retain every predecessor.

If weights are nonnegative integers, every f_k(b) is an integer between
-(h-1)M and zero. Therefore

    B_k <= min(c, h[1+(h-1)M]).                            (1)

This is a proof from a finite score range, not an empirical observation.
For arbitrary nonnegative exact weights, the representation and algorithm
remain exact; (1)'s score-range bound requires integrality (or scaling to
an integer lattice). The empty prefix has the sole record (0,0).

More generally, mark t outcomes of arbitrary nonnegative weights and let
V be the total of the remaining INTEGER weights. A marked outcome contributes
one of h possible reward coefficients, 0,...,h-1 (zero when outside the
prefix). Thus the marked coefficient vector has at most h^t possibilities.
The unmarked reward is an integer in [0,(h-1)V]. There are at most
h^t[1+(h-1)V] distinct prefix values, regardless of marked magnitudes.
Multiplying by h ending-slot classes gives

    B_k <= min(c, h^(t+1)[1+(h-1)V]).                      (1a)

The marked weights may be rational or real; only the unmarked weights need
be integers for this counting argument. An entire constant interval still
requires only one attaining predecessor.

## Finding records without scanning their gaps

For a singleton of key weight w and preceding gap g, process each destination
valuation d separately. Scan predecessor records (a,f_k(a)) in increasing a.
Its candidate value is f_k(a)-g min(nu_2(a),d)-wd. It becomes eligible at the
first slot of valuation d strictly greater than a. These eligibility positions
are nondecreasing. Maintain the running minimum, recording only decreases;
combine improvements at the same position. This costs O(h B_k) work plus
record organization, bounded by O(h(B_k+B_(k+1))).

For a long run of m>=2 keys of weight w, use the already proved FINITE Monge
factor, with P=1+(h-1)M:

 B(a,b) = P max(m-b+a,0) - w nu_2(b)
          - w sum_(t=1)^(h-1) min(m-1, floor((b-1)/2^t)-floor(a/2^t)).

Columns are predecessor records a<=c-m (only 0 for the empty prefix).
Rows are destination slots b>=k+m. Each row has a feasible candidate: a=k
is the first feasible slot in its valuation class, hence a record. Invalid
candidates cost at least one; feasible ones cost at most zero. Adding the
prefix value and restricting to record columns preserves finite Monge.
Any chosen batch of rows can therefore be evaluated by SMAWK in O(B_k+Q)
entry queries, where Q is the number of queried rows. Each entry costs O(h).

A valuation class is an arithmetic progression. Query its first and last
feasible positions. Equal endpoint values certify that the entire class
interval is constant. Otherwise bisect its index interval. Query all required
midpoints across all classes together in one sorted batch, and recurse only
on children whose endpoint values differ. Adjacent unequal endpoints reveal
exactly a strict-decrease record. Retain the first feasible record separately.

There are at most h bisection levels. At each level, every active interval
contains a distinct strict decrease; the intervals are disjoint within each
class. Thus at most O(B_(k+m)) rows are queried per level, and all levels
use O(h(B_k+B_(k+m))) entry queries and O(h^2(B_k+B_(k+m))) work. Sorting
rows and organizing records fit this bound because their positions lie in
[1,c] and log(c+1)=h. Store only active interval endpoints and discovered
records: O(B_k+B_(k+m)+h) working words, not a cache of every queried row.

A predecessor saved at the first position of a constant interval remains
attaining at every later position of that class in the interval. With that
predecessor fixed, the transition cost cannot increase; the global minimum
remains equal, so the candidate cannot decrease strictly either. This proves
that the compressed backpointer representation is sufficient for traceback.

## Full reconstruction without an exponential tree

For a recovered long-run window (a,b), choose m-1 slots of highest valuation,
then append b. For threshold t the number of eligible inner slots is

    N_t = floor((b-1)/2^t)-floor(a/2^t).

Find d such that N_(d+1)<m-1<=N_d. Take every multiple of 2^(d+1) in the
window, then the earliest required odd multiples of 2^d. These are two
sorted arithmetic progressions; merging them costs O(m), and finding d costs
O(h). Across all stages, traceback costs O(n+sh).

Construct only the union of ancestor paths of the n selected slots in the
height-h perfect tree. It has at most nh vertices. For x with d=nu_2(x)<h-1,
its parent is x-2^d if bit d+1 of x is set, and x+2^d otherwise. An ancestor
walk stops as soon as it meets an already retained vertex. Unrepresented
branches contain no selected key and can first be collapsed to empty trees.

On this ancestor-closed tree, delete every unselected key in increasing label
order. With two children, promote its inorder successor, which has no left
child, and splice that successor's possible right child upward. With at most
one child, splice that child upward directly. Threaded predecessor/successor
links make each deletion constant work after organization. No surviving
key's depth increases. Thus selected key i has comparison length at most
h-nu_2(t_i). An internal gap's depth is the maximum of its adjacent key
comparison lengths (an endpoint gap has its adjacent key's length). This
recovers the mixed slot cost upper bound. Combined with the converse slot
embedding theorem, the reconstructed tree is an exact height-h optimum.

Ancestor organization uses O(nh^2) work and O(nh) words with deterministic
ordered dictionaries or sorted arrays; no expected hash-table bound is needed
for the theorem. The prototype uses Python dictionaries. Final output is
built iteratively, so chain-shaped answers impose no recursion-depth limit.

## Complete bound and unrestricted corollary

Write B_0=1 and B_1,...,B_s for the stage record counts. Including input
normalization, all predecessors, traceback, and full tree reconstruction:

    work = O(h^2 [n + sum_(j=0)^s B_j]),
    words = O(nh + sum_(j=0)^s B_j).                         (2)

For integer weights this implies

    work = O(nh^2 + s(M+1)h^4),
    words = O(nh + s(M+1)h^2).                              (3)

All bounds count arithmetic operations on exact weights and h-bit slot
coordinates; unbounded operand bit costs are additional. The dependence on
2^h is gone from (3), including the cost of writing the whole output tree.

For original integer mass W=O(n), M<=W. The mixed mass lemma, or the stronger
trimmed height theorem with k=0, supplies h=O(log(n+1)): positive singleton
mass is at least one, and zero-weight intervals can be balanced in logarithmic
height. Hence constant r+e yields complete UNRESTRICTED construction in
O(n log^4(n+1)) arithmetic work and O(n log^2(n+1)) words, with zero keys
allowed. Choosing the sufficient height costs O(n log n), absorbed here.
For arbitrary s the guarantee is O(n log^2 n+s(W+1)log^4 n); choosing Knuth
when this a priori proxy is larger retains quadratic worst-case work. This
last choice is an algorithmic bound, not the default of the prescribed-height
prototype, which deliberately exposes all record counts.

There is also a magnitude-independent extension. Suppose all normalized
weights are integers, t outcomes are marked, the remaining mass V=O(n),
and s,t are fixed. The marked-outcome height theorem supplies
h=O(log(n+1)+t), because every positive singleton has mass at least one.
Using (1a) in (2) gives complete unrestricted construction in

    O(n log^(t+4)(n+1)) arithmetic work,
    O(n log^(t+2)(n+1)) words.

The constants do not depend on marked magnitudes. Zero runs are allowed.
This extends the near-linear bound to arbitrarily large exceptional integer
weights; the earlier n^(log_phi 2) result also covers nonlattice backgrounds.

This does not prove a general arbitrary-weight subquadratic algorithm. It
also does not alter the original interval-core lower bounds or close their
remaining square-root logarithmic gap. It is a separate exact construction
that computes only one prefix vector at each stage.

## Independent verification

The harness was written before the record kernel. It checks literal slot
subsets and repaired key depths, literal highest-valuation selections,
every prefix value and exact breakpoint against the dense vector solver,
and original mixed height optima against an all-root recurrence. Rational
and geometric inputs are included. Larger rows use an independent ordinary
Knuth optimum. The enormous-capacity rows construct full uniform trees and
use the closed minimum-internal-path-length cost. The source-hashed JSON
records exact operation types; it contains no timings.
