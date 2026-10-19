# Binary threshold tails do not control the weighted tail

The weighted cluster formula suggests grouping weights by level. For a
nonnegative input p and threshold a, write B_a={i:p_i>=a}. A proposed
transfer from binary cases is

    U_d(p) <= A integral_0^infinity U_d(1_(B_a)) da.          (1)

No finite constant A makes (1) true, even for the full height-three ruler.
The same counterexample also applies to the alternating clipped template.

Take n=10, c=7, d=1, and

    p=(0,0,0,0,2,1,1,2,1,0).

Its two nonempty binary threshold vectors are

    b=(0,0,0,0,1,1,1,1,1,0),
    e=(0,0,0,0,1,0,0,1,0,0).

For v=(0,1,0,2,0,1,0), use the six intervals in order

    [0,8), [1,9), [2,10), [1,8), [2,9), [0,10).

The exact scores are

| Input | First three scores | Last three scores | Tail |
|---|---|---|---:|
| p | 5, 6, 5 | 5, 4, 6 | 1 |
| b | 3, 3, 4 | 3, 3, 4 | 0 |
| e | 2, 3, 1 | 2, 1, 3 | 0 |

Each score is the maximum of p_(a_1)+2p_(a_2)+p_(a_3) over
three edge indices i+1<=a_1<a_2<a_3<=j-2 separated by at least two.
The tail telescope is the sum of the first three columns minus the last
three. Hence U_1(p)=1 while both binary tails are zero, proving the claim
for every A. Scaling p scales its positive tail and preserves the zero
threshold integral.

For the alternating template v=(0,1,0,1,0,1,0), the corresponding score
rows are (3,4,4;3,3,4), (2,2,3;2,2,3), and (1,2,1;1,1,2), again giving
tails 1,0,0. This example rules out a multiplicative transfer of binary
tails. It leaves the aggregate mass-based tail target open.

## Verification appendix

The discovery probe evaluates 14432 inputs and 35722 width comparisons,
including exhaustive ternary interior weights on ten positions and seeded
integer vectors. It records 1852 violations of the proposed upper relation
and 4003 violations of the reverse relation. These counts motivate no
asymptotic statement.

The displayed counterexample is separately checked by literally enumerating
876 subsequences for its 36 interval scores, comparing them to the generic
recurrence, and checking the three full-ruler tails against original all-root
terminal layers. The proof table is independent of the search. The records
are `nested_tail_probe.json` and `nested_tail_example.json`.
