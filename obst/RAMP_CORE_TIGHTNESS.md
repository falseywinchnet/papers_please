# Linear-mass intermediate cores require n^(3/2) entries

Research and exposition: OpenAI Codex Sydney. Problem selection and sponsorship:
Joshuah Rainstar.

## Statement

Let m=2^t with t>=5, n=m^2, z=(n-m)/2, h=2t-1, and c=2^h-1=n/2-1.
All gap weights are zero. All key weights outside [z,z+m) are zero, and

    p_(z+r-1)=2r-1,  1<=r<=m.

The total mass is exactly W=m^2=n. Use the terminal-penalty layers in
MONGE_PENALTY.md, with any global height budget H>=h and penalty M>HW.
Layer h has at least

    n m/16 - 9n/64 - m/4 >= n m/32 = n^(3/2)/32

strictly positive interior densities. Every one of these densities has an
explicit formula below. Thus an O(n polylog n) bound for every intermediate
core at W=Theta(n) is impossible. This makes the exponent 3/2 necessary
for this explicit representation; the sqrt(log n) gap to the current upper
bound O(n sqrt(W L)) remains. It is not a lower bound on all OBST algorithms.

## Height-limited keys as a subsequence of the ruler word

For q=0 and k<=c, the layer exposes every key. It minimizes the key cost
over trees of height at most h. The perfect c-key tree has comparison
length h-nu_2(r) at inorder slot r, 1<=r<=c.

The minimum cost is exactly the minimum weighted comparison length over
all ordered k-slot subsets of that perfect tree. One direction holds because
every height-at-most-h tree is an ancestor-closed subset of the perfect
tree's slots. Conversely, delete every unselected key from the perfect tree
using ordinary BST deletion: with two children replace its key by its inorder
successor, then splice out that successor from its old position; with at most
one child splice out the node. Every remaining key keeps or decreases its
depth, and inorder order is preserved. Nonnegative key weights therefore
cannot increase cost. These two inequalities prove equality of the minima.
Zero gap weights are essential for this particular deletion argument.

Now consider an interval containing the whole positive ramp, with A leading
zero keys and B trailing zero keys. Its length is k=A+m+B<=c. The positive
keys can occupy any m slots in the zero-based slot window

    [a,b)=[A,c-B),     b-a=m+(c-k).

There are enough slots to accommodate the A preceding and B following zero
keys exactly when those positive slots lie in this window. Define

    f_m(a,b)=max sum_(r=1)^m (2r-1) nu_2(t_r+1),
             over a<=t_1<...<t_m<b.

For the original interval [i,j), with a=z-i and b=c-j+z+m,

    A_h(i,j)=hW-f_m(a,b).

## A closed-form optimal deletion rule

Let v_u=nu_2(u+1), so even zero-based positions have coefficient zero and
odd positions have coefficient at least one. Let D bound every coefficient
in the ambient ruler word. In any consecutive segment of length ell,

    sum v_u <= ell + D.

Indeed, v_u=sum_(d=1)^D [2^d divides u+1], and a length-ell segment contains
at most ell/2^d+1 multiples of 2^d. Sum the geometric series.

**Deletion lemma.** If b-a=m+s and m>2s+D, then f_m(a,b) is obtained by
deleting the rightmost s zero coefficients and keeping every other position.

Proof by peeling the right endpoint. If the last coefficient is zero and
s>0, some optimum omits it: replace it in any selected subsequence by an
earlier omitted position. The inserted coefficient is nonnegative and the
selected coefficients it passes move to larger, not smaller, odd weights.

If the last coefficient is positive, every optimum selects it. Suppose it
were omitted. There is a selected zero, because the window has fewer than m
positive coefficients. Let u be the last selected zero. All selected positions
after u are positive. Every zero after u is omitted; the final positive
coefficient also uses one of the s omissions. Since zeros alternate, the
distance from u to the last position is at most 2s-1. The sum of selected
coefficients after u is consequently at most 2s-1+D. Replace that selected
zero by the final positive coefficient v>=1. Its weight becomes 2m-1;
each previously selected coefficient after u loses two in its multiplier.
The gain is at least

    (2m-1) - 2(2s-1+D) > 0,

where m>2s+D suffices. This contradicts optimality.

Thus a final positive coefficient is kept, and the preceding zero is omitted
while omissions remain. Removing this pair changes (m,s) to (m-1,s-1),
which preserves the strict inequality. If the initial last coefficient is
zero, omitting it first only strengthens the inequality. Once s=0 every
remaining position is kept. This proves the rule.

## Density in closed form

Use zero-based ruler-window coordinates (a,b), with b-a=m+s, s>=1 and
m>2(s+1)+D. The deletion rule applies to all four windows in

    d_f(a,b)=f_m(a,b+1)+f_m(a+1,b)-f_m(a,b)-f_m(a+1,b+1).

If b is odd, the newly appended coefficient v_b is positive. Comparing
f_m(a,b+1) with f_m(a,b) deletes the additional zero at b-2s-1 and appends
b. The s retained positive coefficients between them each lose two in their
multiplier. Consequently

    f_m(a,b+1)-f_m(a,b)
      =(2m-1)v_b - 2 sum_(r=1)^s v_(b-2r).

After removing the left endpoint, the analogous sum has s-1 terms, so

    d_f(a,b)=-2 v_(b-2s)=-2 nu_2(b-2s+1) < 0.

The score-to-cost transformation reverses this sign. For the original cell
(i,j), set a=z-i, b=c-j+z+m and s=c-(j-i). If b is even, the formula is

    Delta_(A_h)(i,j)=2 nu_2(b-2s) >= 2.

The four original intervals correspond to the four score windows based at
(a-1,b-1). All contain the complete ramp in the range counted next.

## Counting explicit cells

Take s=1,...,m/4 and a=1,...,c-m-s-1 with b=a+m+s even, and put

    i=z-a,     j=c-b+z+m.

These are valid, distinct density cells; both external sides of each of the
four intervals have nonnegative numbers of zero keys. All coefficients
have D=h-1=2t-2. For t>=5,

    m > 2(m/4+1)+D,

so the deletion lemma applies throughout. For each s the number of allowed
a is floor((c-m-s)/2). With u=m/4 even, summing gives

    sum_(s=1)^u floor((c-m-s)/2)
      = u(c-m-1)/2-u^2/4
      = nm/16-9n/64-m/4.

For m>=32 this is at least nm/32. The density formula and this exact count,
not a regression on observed core sizes, establish the lower bound.

## Independent checks

`ramp_core_tightness.py` first compares the weighted-subsequence recurrence
with literal subset enumeration. It then checks the perfect-slot embedding
against an all-root interval recurrence on smaller full instances, compares
the deletion rule and density formula with independent subsequence DP,
and checks every counted cell at n=1024 against the original penalty layer.
Larger rows explicitly distinguish formula evaluation from independent DP.
All costs and checks use exact integers. Source hashes and counts are retained.
