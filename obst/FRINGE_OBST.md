# Exact boundary extension around a periodic middle

**Theorem.** Let [l,r) be a nonempty middle interval of m=r-l keys in a
full mixed OBST input of n keys. Suppose its keys p_l,...,p_(r-1) and its
inclusive gaps q_l,...,q_r are restrictions of two sequences with common
period b<=m. All weights, including the d=n-m fringe keys and their gaps,
may be arbitrary nonnegative reals. A complete unrestricted-height optimal
BST, and a constant-time oracle for every interval cost and an optimal root,
can be constructed in O(mb+nd) arithmetic work and space.

The linear concave least-weight-subsequence algorithm is Wilber's prior
work. The result here composes that primitive with the cyclic phase oracle
and proves the OBST boundary reduction explicitly. It has no small-mass or
bounded-height assumption. The general nonperiodic worst case remains
quadratic; a small number of arbitrary *interior* defects need not leave a
middle with d small.

## The published primitive and its interface

Robert Wilber, *The Concave Least-Weight Subsequence Problem Revisited*,
Journal of Algorithms 9 (1988), 418--425, states that
“the concave least weight subsequence problem can always be solved in O(n) time”.
[Primary paper, pp. 418, 420--424](https://gwern.net/doc/design/typography/tex/1988-wilber.pdf).
Its domain is finite real weights w(s,t), 0<=s<t<=N, satisfying

    w(s,t)+w(s',t') <= w(s,t')+w(s',t),   s<s'<t<t'.       (1)

With constant-time weight access, it computes every value
F(0)=0, F(t)=min_(s<t){F(s)+w(s,t)} and predecessor witnesses in linear
work and space. No difference-of-weight condition is needed. Figure 1
uses two SMAWK searches per batch. Our implementation follows that
algorithm, with leftmost predecessor ties. Invalid cells internal to SMAWK
compare above every finite cell using an ordered tag; they never reach the
weight oracle. This has the same comparison outcomes as a sufficiently
large finite sentinel in each batch. The valid triangular arc domain
contains only finite entries.

## One new boundary column

Suppose all exact costs C(i,r) with 0<=i<=r<J are already available in
constant time. Adding key J-1 and gap J requires the new column

    D(J)=0,
    D(i)=W(i,J)+min_(i<=r<J){C(i,r)+D(r+1)}.              (2)

The convention C(i,i)=0 includes empty subtrees. Put F(t)=D(J-t), and
identify a predecessor s<t with root r=J-s-1. Then (2) becomes the LWS
recurrence with

    w(s,t)=C(J-t,J-s-1)+W(J-t,J).                        (3)

Every old interval on the right has endpoint at most J-1. Thus (3) uses
only the previous oracle and a prefix mass query; there is no circular
oracle call to an unfinished entry in the new column.

For s<s'<t<t', set a=J-t', b=J-t, c=J-s'-1, e=J-s-1.
Then a<b<=c<e. The ordinary mixed OBST Monge inequality is

    C(a,c)+C(b,e) <= C(a,e)+C(b,c).                       (4)

The two mass terms in (3) appear once on each side of (1) and cancel.
The remaining terms are exactly (4). This checks the direction, including
the case b=c, where the empty interval cost is zero. Finite nonnegative
input weights make every valid arc finite. Wilber therefore computes all
J new values and roots in O(J) work and space. Its leftmost predecessor
corresponds to a rightmost original root; either tie convention reconstructs
an exact optimum. Reflection gives the same result for a left boundary row.

## Composition and the exact number of added states

Construct the periodic middle oracle by cyclic phase amortization. This
uses b(2m-1) root candidates and O(mb) cost/root storage. Append the right
fringe one key at a time, then prepend the left fringe by reflection. After
t extensions the active interval has m+t keys. The new boundary contains
m+t nonempty states, so the number computed outside the middle is exactly

    S_boundary = sum_(t=1..d)(m+t)
               = dm+d(d+1)/2
               = n(n+1)/2-m(m+1)/2 <= nd.               (5)

Store each completed boundary as an indexed array. At any later step an
old interval is either wholly central, ends in a stored right column, or
starts in a stored left row. These three cases give constant-time lookup.
Rows take precedence when both endpoints are outside the middle. During
left extension every requested old left endpoint is strictly larger than
the new one, so all requested rows already exist. Reflection reverses key
indices and the inclusive gap sequence together.

For clarity, in original coordinates a new left row at i uses reversed
endpoint N=n-i. Its old-cost call is C(n-r,n-a), and its new interval mass
is W(i,n-a), for reversed coordinates a<=r<N. A reversed root r maps to
original root n-r-1. These formulas also cover empty old subtrees.

Equation (5) and the linear boundary lemma give O(mb+nd) total work and
space, including input prefixes and complete tree reconstruction: mb+nd>=n
when n>=1. Each reconstructed subinterval uses an exact stored minimizer;
an explicit stack visits every original key and gap once. The core-free
central quotient and the stored fringe states together cover *every*
original interval, not only the intervals selected by the output tree.

The proof also gives a general composition lemma: any exact central
constant-time interval oracle with construction/storage cost T can be
extended to arbitrary fringes in O(T+nd), plus O(n) output work. Periodicity
is one way to supply that central oracle.

## Automatic recognition and selection

For a proposed b<n, scan the n signatures s_i=(p_i,q_i,q_(i+1)). A middle
[l,r) of length greater than b has common key/gap period b if and only if
s_i=s_(i-b) for every l+b<=i<r. A failed comparison at i requires the next
eligible left endpoint to exceed i-b; set it to i-b+1. Between failures,
the current longest suffix gives the longest such middle in O(n) work.
This includes q_r: checking keys alone would be unsound.

Scan b=1,...,B, with B=min(n-1,ceil(log2(n+1))) by default. For each b,
keep a longest middle; it minimizes mb+n(n-m) because b<n. Compare these
proxies with n*b0, where b0 is the shortest whole-input common period,
allowing b0=n+1. If b0<=B, the whole-input construction already costs
O(nB) and the scan can be skipped. Otherwise choose the least proxy.
Consequently, with an empty inner minimum omitted, automatic construction
costs

    O(n(B+1) + min{n*b0, min_(b<=B)[m_b*b+n*(n-m_b)]}). (6)

Space is O(n+the selected proxy). The O(n(B+1)) formulation includes B=0.
With supplied constant b,d the construction is linear; automatic recognition
adds O(n log(n+1)). A defect only in the last gap can be enclosed in a
one-key fringe. Arbitrarily large fringe weights do not change (5) or (6).
These are arithmetic-operation bounds with exact comparisons, not bit-cost
bounds or timing estimates.

## Independent verification

The audit first compares the LWS implementation against its full dense
recurrence with signed finite arc weights. It then checks every interval
of exhaustive small binary mixed inputs and seeded periodic-middle inputs,
including rational and very large boundary weights. Boundary columns are
also tested independently of the periodic oracle. Literal substring scans
check recognition; ordered-tree enumeration checks small optimal costs.
Matched larger inputs use ordinary Knuth DP. The largest rows reconstruct
and independently traverse every node but have no separate quadratic
optimality oracle. Exact operation counts, verification scopes, seed,
and executed-source hashes are in results/fringe_obst_audit.json and the
manuscript appendix. Neither a measured growth rate nor a timing is used
to prove (5) or (6).
