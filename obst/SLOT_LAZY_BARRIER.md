# An exact lazy prefix search and its exponential obstruction

Evaluating only requested prefix states avoids materializing the entire slot
vector or diagram. The resulting recurrence is exact, but a natural
rearrangement bound cannot keep its search small: an explicit positive mixed
family forces at least 2^(n-2)-2 distinct evaluated states.
This is a lower bound for the specified search and pruning rule. The same
family has a directly certified linear arithmetic-work OBST construction.

## The bound, including arbitrary residual gaps

Fix height h and normalized nonnegative key weights w_0,...,w_(n-1) and
residual gaps g_0,...,g_n, with g_0=g_n=0. Write v(s)=nu_2(s). For increasing
slots s_0<...<s_(k-1)=b, the reward is

    R = sum_(i=0)^(k-1) w_i v(s_i)
        + sum_(i=1)^(k-1) g_i min(v(s_(i-1)),v(s_i)).

The exact prefix cost f_k(b) is minus the maximum reward. Its feasible
domain is k<=b<2^h. Put a_i=2w_i+g_i+g_(i+1), and let T_t(r) be the sum
of the t largest coefficients among a_0,...,a_(r-1), with T_0(r)=0. Then

    U_2(k,b) = (2w_(k-1)+g_(k-1))v(b)
               + sum_(d=1)^(h-1) T_min(k-1,floor((b-1)/2^d))(k-1),
    2 f_k(b) >= -U_2(k,b).                                  (1)

Indeed, 2 min(x,y)<=x+y distributes each residual gap to its two endpoints.
The last key is fixed at b; its coefficient excludes the absent next gap.
Ignore order among the remaining k-1 keys, choose slots in [1,b-1], and
pair the largest coefficients with the largest valuations. An exchange
argument proves this pairing maximizes the relaxed dot product. Exactly
floor((b-1)/2^d) available slots have valuation at least d. Summing those
threshold contributions gives (1). All arithmetic is exact, including for
rational inputs; doubling avoids rounding in the pruning comparisons.

A persistent count-and-sum tree over sorted coefficient values stores all
coefficient prefixes in O(n log(n+1)) work and space. Each top-t query takes
O(log(n+1)) work, so each bound costs O(h log(n+1)).

## Complete mechanical search

For b-1 with set bits d_1>...>d_t, let S(b) contain its successive leading
bit sums. Endpoint dominance proves that these are sufficient predecessors:

    f_k(b) = -w_(k-1)v(b)
             + min_(a in S(b), a>=k-1)
               [f_(k-1)(a)-g_(k-1)min(v(a),v(b))].             (2)

The base is f_1(b)=-w_0 v(b). Add the sentinel state (n+1,2^h), with zero
key and gap reward, to obtain the minimum of f_n over all final slots.
For each candidate, combine half the bound in (1) with its transition cost.
Evaluate candidates in increasing bound order and memoize exact states.
Once a feasible incumbent is no larger than every remaining lower bound,
stop that state. Store an attaining predecessor with each exact value.
An explicit stack implements the recurrence; k strictly decreases along
its calls. Trace the chosen slots and apply ancestor closure and sparse
repair to construct the full original-weight tree.

Let V count expanded states, including the sentinel, and Q distinct bound
states. Candidate enumeration costs O(Vh), sorting costs O(Vh log(h+1)),
and computing the bounds costs O(Qh log(n+1)). Full work is

    O(n log(n+1) + Qh log(n+1) + Vh log(h+1) + nh),            (3)

with O(n log(n+1)+Q+V+nh) storage. At most h candidates are generated per
expanded state, so Q<=Vh. These are output-dependent bounds, not a bound
on V. Choose a certified sufficient h<=n for unrestricted construction.
Stopping counted search work at 8n^2 and falling back to ordinary Knuth
keeps total arithmetic/dictionary work O(n^2), including unsuccessful
search, height selection, normalization, traceback and full repair.
Exact operand bit costs are additional. A larger explicitly requested
experiment budget is not covered by this particular quadratic safeguard.

## Exponentially many candidates that cannot be pruned

For n>=6 put A=n+1, w_i=A^(n-i), p_i=w_i-1, and q_j=1 for every gap.
Common-gap normalization gives precisely w, zero residual gaps, and cost
shift n. The unique optimum is the right chain of necessary height h=n:
for every suffix, n sum_(t>i)w_t=w_i-A<w_i, so making its first key a
nonroot costs more than the right-chain competitor. The input has
O(n^2 log(n+1)) bits in total.

The same inequality ensures strict lexicographic dominance of valuation
vectors with entries in [0,n-1]. Consider a candidate f_m(a) with

    m>=4,  a>3*2^(n-2).                                    (4)

Its first three keys are free in the relaxation. The three highest slot
valuations before a are (n-1,n-2,n-2), at positions 2^(n-1), 2^(n-2),
and 3*2^(n-2). The bound assigns these valuations, in that order, to its
three largest weights w_0,w_1,w_2.

No increasing sequence of selected slots has this initial valuation triple.
If its first valuation is n-1, its first slot must be 2^(n-1). A following
slot of valuation n-2 must then be 3*2^(n-2), and no further such slot
exists. Every feasible valuation vector is therefore lexicographically
smaller within its first three coordinates. At its first differing index r,
the lost w_r exceeds every possible gain from later coordinates, since
w_r>(n-1)sum_(i>r)w_i.

This comparison also holds after adjoining the parent's fixed final key:
all coordinates after the first difference, including that key, remain in
[0,n-1]. Thus the child's relaxed bound plus its transition cost is strictly
less than the *true optimum of the parent*, not just less than this child's
exact value. At the root sentinel the same reasoning applies without an
additional key. Every feasible incumbent is at least the true optimum, so
no candidate satisfying (4) can be pruned by the specified bound, whatever
the candidate processing order.

For every nonempty proper subset S of {0,...,n-3}, start at
(k,b)=(n+1,2^n) and process its elements d in descending order, taking

    (k,b) -> (k-1,b-2^d).                                  (5)

Previously selected bits are larger than d, so b is divisible by 2^(d+1).
Consequently b-2^d is exactly the skyline prefix of b-1 ending at bit d.
The accumulated subtraction x is less than 2^(n-2); every child endpoint
is therefore greater than 3*2^(n-2). Its key count is at least four,
and its endpoint is large enough to be feasible. Every edge in (5) is
unprunable by the preceding argument. Distinct subsets yield distinct states

    (n-|S|+1, 2^n-sum_(d in S)2^d).

Memoization cannot identify them. The completed unbudgeted search therefore
expands at least

    sum_(r=1)^(n-3) binomial(n-2,r) = 2^(n-2)-2 = Omega(2^n)                     (6)

distinct actual-prefix states. The counted fallback bounds the implemented
full solver, but does not turn (1) into a strong pruning rule. A stronger
rule must preserve more information about the order of attainable valuations.

## Independent verification

The bound audit checks 55,744 entries against dense exact prefix values and
literal sorted dot products; it checks 14,245 evaluated states against fresh
all-predecessor recurrences and 1456 height-constrained optima against the
original all-root DP. Its 2184 full constructions include zero, small and
default budgets, and all match unrestricted Knuth and original tree costs.

The scale audit retains 22 complete constructions and their independent
Knuth controls. Uniform rows through 512 keys finish the lazy search; all
ten bounded/binary mixed rows reach their default budgets. The explicit
chain finishes through 12 keys and reaches its larger diagnostic budget at
14,16,18. Exact operation categories, original inputs and fallback work are
retained. These counts do not estimate an asymptotic exponent.

A separate unbudgeted audit at n=6,8,10,12 checks every state in (6), every
edge in its canonical paths, and strict comparison with exact parent optima.
It finds 14,62,254,1022 distinct forced states, respectively. Larger rows are
formula evaluations only. The three result files each retain eight source
hashes. The manuscript places all finite counts in its verification appendix.
