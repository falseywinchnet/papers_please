# Linear run dependence and arbitrary mixed gaps at a prescribed height

The full slot-window product is useful when all transfer entries are wanted.
A complete tree needs only a vector of prefix costs. Processing that vector
avoids the quadratic run dependence and also accommodates the signed gap
transition without constructing its dense matrix.

**Theorem.** Let n>=2 and let p_0,...,p_(n-1), q_0,...,q_n be arbitrary
nonnegative weights. For prescribed height h with c=2^h-1>=n, put
b=min(q_1,...,q_(n-1)) and define

    w_0=p_0+q_0,  w_(n-1)=p_(n-1)+q_n,
    w_i=p_i+b                         (1<=i<=n-2),
    g_0=g_n=0,  g_i=q_i-b             (1<=i<=n-1).

Let r be the number of constant runs in w and let e=#{i:g_i>0}.
A complete optimal BST of height at most h can be constructed in

    O(n+(r+e)c log(c+1)) arithmetic work,
    O(n+(r+e)c) words, including all backpointers and output.

The algorithm allows every original input, with r<=n and e<=n-2. At the
minimum feasible height c<2(n+1), its bound is
O(n+(r+e)n log(n+1)). For equal internal gaps e=0, this replaces the
previous r^2 dependence for complete construction by r. The all-entry
product theorem and its core bound remain separate valid statements.
A prescribed height is still a constraint; no unrestricted certificate is
inferred, and the original interval-core size hypothesis is unchanged.

## Exact mixed normalization

For every tree, E=I+2n=sum_i ell_i+n. The endpoint gap depths are ell_0
and ell_(n-1). Hence, keeping the arbitrary residual internal gaps,

    C_(p,q)(T) = C_(w,g)(T)+bn.                              (1)

All transformed weights are nonnegative, including when q_0 or q_n is
smaller than b. For n=1 use w_0=p_0+q_0+q_1 and zero gaps directly.
The total transformed outcome mass is sum w+sum g=W-b for n>=2.
This normalization is an application of the established tree-cost identity.

The mixed slot theorem makes the transformed optimum h(sum w+sum g)
minus the maximum score

    sum_i w_i v(t_i)+sum_(i=1)^(n-1) g_i min(v(t_(i-1)),v(t_i)),
    1<=t_0<...<t_(n-1)<=c,  v(t)=nu_2(t).                    (2)

Let f_k(a) be the minimum negative score of the first k keys ending at
slot a. For k>0 it is finite exactly at k<=a<=c. Initially f_0(0)=0
and there is no other state. We retain only finite true prefix states.

## One constant run by finite Monge row minima

Consider m>=2 consecutive keys of common weight w, with zero residual
gaps preceding and inside this run. Their last slot must be b'. If the
preceding prefix ends at a, their other m-1 slots lie in (a,b'). Put
R=(h-1)(sum w_i+sum g_i), K=R+1, and define for all a and b'

    B_(w,m)(a,b') = K max(m-b'+a,0) - w v(b')
       - w sum_(t=1)^(h-1)
          min(m-1, floor((b'-1)/2^t)-floor(a/2^t)).            (3)

For b'-a>=m this is the negative optimal run score with its final key
forced to b'. For every other pair it is the specified finite completion.
It equals the previous window factor for m-1 keys, evaluated at
(a,b'-1), minus the column potential w v(b'). Its entire rectangle is
therefore Monge by that factor's explicit density proof, valid for any
positive K. No monotonicity of the arbitrary prefix vector is required.

Compute f_(k+m)(b') as the row minimum, with row b' and column a, of

    f_k(a)+B_(w,m)(a,b').                                    (4)

Rows are k+m,...,c; candidate columns are k,...,c-m for k>0, and only
column 0 for k=0. The transpose is Monge; adding f_k(a) is a column
potential and preserves it. Every searched row has a feasible candidate.
An infeasible candidate has penalty at least K. The prefix negative score
is at least minus its own (h-1)-weighted mass, and the reward in (3) is
at most wm(h-1), including reversed windows. Thus an infeasible candidate
costs at least K-R=1. A feasible candidate costs at most zero. Consequently
(4)'s finite row minima give exactly the true prefix values and predecessors.

The SMAWK algorithm of Aggarwal, Klawe, Moran, Shor and Wilber (1987)
finds these leftmost minima with O(c) entry evaluations and O(c) additional
work and space. Formula (3) costs O(h) arithmetic operations per entry,
giving O(ch) work per run. We do not construct its full matrix, its core,
or a product matrix. The matrix-search primitive is prior work:
https://doi.org/10.1007/BF01840359 . IBM Research and the authors' institutional
record confirm its finite-real totally-monotone interface; here the stronger
Monge inequality supplies total monotonicity.

## One arbitrary gap by a linear valuation sweep

To append one key of weight w after a gap g>=0, compute

    f_(k+1)(b') = -w v(b')
                   +min_(k<=a<b') [f_k(a)-g min(v(a),v(b'))]. (5)

For k=0 only a=0 is available, v(0)=0, and g=0. In increasing b', insert
the newly eligible a=b'-1. Keep E_d, the minimum (f_k(a),a) among inserted
predecessors of exact valuation d, and S_d, the minimum among valuations
at least d. Pairs use lexicographic order, retaining the leftmost tie.
For t=v(b'), the query is

    min( min_(d<t) [E_d.value-gd], S_t.value-gt ),            (6)

with absent states omitted and their attaining predecessors retained.
Insertion of valuation d updates E_d and S_0,...,S_d. The query scans
only d<t and reads S_t once. Each slot is inserted or queried at most
once, and sum_(a=1)^c v(a)=c-h<c. Therefore all insertions, queries, array
initialization and witnesses take O(c+h)=O(c) work and O(c) words.
This includes g=0, so singleton runs use the same linear pass.
The dense signed checkerboard of the transition matrix is never stored.

## Stage count, full reconstruction, and complexity

Start a singleton stage at each key preceded by g_i>0. Otherwise collect
a maximal constant-weight segment with all its preceding/internal residual
gaps zero. The initial r key runs are split by at most e exceptional
gap positions, so there are at most r+e ordinary segments. Isolating the
first key after each exceptional gap creates at most one additional stage
per gap. Thus the total number of stages is at most r+2e.

More precisely, if R_2 stages have length at least two and S_1 are
singletons, the implementation takes

    O(n+c[1+h R_2+S_1]) work,
    O(n+c[1+R_2+S_1]) words.                               (7)

This implies the stated theorem since h=log2(c+1). In particular, when
every stage is a singleton the implementation takes O(nc), with no hidden
logarithmic factor on the gap transitions. Retain one predecessor array
per stage. Choose the smallest final slot attaining min_b f_n(b), then
trace the arrays backward. In a long run choose the m-1 largest valuations
in the recovered open window (a,b'), plus b', with earliest ties. Buckets
use h entries. Distinct stages have disjoint windows, so bucket and output
scans together cost O(c+(r+e)h+n). Singleton stages emit only their ending
slot. Traceback therefore fits (7).

Apply the established O(c+n) threaded slot-deletion repair to (2).
Nonnegative transformed weights ensure that repair cannot increase cost,
and equality of the minimum slot score and tree optimum makes its output
optimal. Add bn from (1). The full original mixed cost, inorder order and
height are independently checked in the harness.

## Reproducible evidence

`code/slot_vector_audit.py` checks literal tree-cost normalization and every
small prefix state/predecessor before comparing final trees with the
original all-root height recurrence. It also checks the entire forced-end
finite factor against the previous condensed factor and every four-corner
Monge inequality, including infeasible entries. Arbitrary mixed, rational,
geometric and long-run fixtures are separate from the exhaustive binary
inputs. Large constructions retain complete trees; only uniform rows have
a closed-form optimum reference. Exact operation counts and executed-source
hashes are recorded in `results/slot_vector_audit.json`. The proof, not the
finite audit or timing, supplies the complexity bound.
