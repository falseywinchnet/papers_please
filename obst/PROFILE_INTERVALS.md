# Two-level key profile reachability: a continuation lemma

Research: OpenAI Codex Sydney. Problem selection and sponsorship: Joshuah Rainstar. This note proves the reachability representation used by the full
constructor in `code/profile_complete.py`. The complementary global gap
bound in [GAP_PARITY.md](GAP_PARITY.md) now certifies recognized patterns
without a large baseline. The unrestricted mixed-weight objective remains open.

## Why this is relevant

The joint-signature constructor costs O(nk), so arbitrary alternating key weights
can make it quadratic even when the pattern has a short mathematical description.
For two key weights, call the larger one high and the smaller one low. In a
minimum-internal-path-length shape, let h=floor(log2(n+1)), S=2^h, m=S-1,
and s=n-m. Its perfect skeleton has m keys, with skeleton rank r at comparison
length h-v_2(r). Every even skeleton rank has length less than h; every odd
rank has length h; removed keys become cherries at length h+1.

If the high-key count H lies between S/2-1 and m, a tree attains the unrestricted
sorted key-depth profile precisely when all high keys are retained in the
skeleton and every even skeleton rank is high. Low keys may occupy odd ranks
or become cherries. This is the rearrangement lower bound for this fixed depth
multiset, not a statement about arbitrary taller trees. It uses strictly distinct
key levels; ties need separate handling. If q_i+q_(i+1) is constant, the gap
contribution is the same across all shapes in this class. Thus this reachability
problem could give a direct exact class optimizer on accepted patterns even
when every joint signature differs from its neighbor.

## Exact word recognizer

Read the high/low input pattern in order. Each key is kept (1) or removed (0),
with no adjacent zeros. A high key must be kept. A low key can be kept only
when its new skeleton rank is odd. Start with rank zero and virtual previous
bit one. A successful complete path ends at rank m.

The probe implements the exact reachable ranks as bit sets for the previous-bit
states. It independently compares them with literal enumeration of all keep/remove
words on short input patterns. No interval approximation is used in that oracle.

## Interlaced intervals at high-key boundaries

Immediately after a high key, the previous bit is one. The virtual initial
boundary has that same property. Encode the reachable even ranks as 2A and
odd ranks as 2B+1, where A and B are sets of nonnegative integers. Empty sets
are permitted. Initially A={0} and B is empty.

**Lemma.** A and B are integer intervals. Whenever both are nonempty,

    min(A)-min(B) is 0 or 1,
    max(A)-max(B) is 0 or 1.

Consequently four endpoints, with empty flags, represent the exact state.

**Proof.** Let L be the number of low keys before the next high key. The
following transitions are exhaustive:

| L | A after the high key | B after the high key |
| --- | --- | --- |
| 0 | B+1 | A |
| 1 | (A union B)+1 | A |
| 2 or 3 | A+1 | empty |
| at least 4 | empty | empty |

For L=1, either remove the low key or retain it at an odd rank. For L=2,
the low-key word must be 01 or 10; for L=3 it must be 010. These words
require an even incoming rank. Four low keys cannot be represented: a low-only run can retain at most
one key, since two retained lows would occupy consecutive skeleton ranks
and one of those ranks would be even. At most one removed low can lie on
either side, since removed keys cannot be adjacent. Thus three is the
maximum possible length between retained high keys.

For L=0, both endpoint differences become one minus the previous differences,
preserving the invariant. For L=1 with both intervals nonempty, their union
is the integer interval [min(B),max(A)]; the new lower endpoint difference
is 1+min(B)-min(A), and the new upper difference is one. These have the
required values. If only A is nonempty, the new pair is (A+1,A). If only
B is nonempty, only B+1 survives as the new A. The L=2/3 and empty cases
are immediate. This proves the invariant by induction.

The terminal run of lows has no following high key. From reachable set R,
with E its even subset, its possible final ranks are:

- L=0: R.
- L=1: R from removing the low, or E+1 from retaining it.
- L=2 or 3: E+1.
- L>=4: none.

The previous-bit choices can be retained when reconstruction is required.
Saving each boundary's four endpoints allows backward selection of a valid
predecessor and one of the explicit short words. Every step has constant
work; scanning and writing the input/output are linear. This establishes an
O(n)-arithmetic reachability and witness method, now implemented with saved
interval endpoints and backward reconstruction in `code/profile_complete.py`.

It is essential to preserve parity. The high-key pattern 010100 (one means
high) has final reachable ranks {3,5}; replacing the set by the ordinary
integer interval [3,5] invents an impossible rank four. The probe retains
this counterexample.

## Evidence and remaining scope

`code/profile_interval_probe.py` checks the bit-set recurrence against literal
word enumeration on every binary pattern through length nine. It then merges
identical exact states while extending both possible next input bits through
length forty. Prefix multiplicities are preserved, including dead states;
at length n their sum is exactly 2^n. Thus equivalent-state merging covers
every binary pattern without pretending to run a separate test for every one.
It checks per-parity contiguity and the interlaced endpoint invariant above.
A separate direct-tree test enumerates every minimum-IPL shape on 865
eligible binary patterns through nine keys, using high/low key values 17 and
2 and alternating gap values 3 and 11. Recognizer acceptance agrees exactly
with attainment of the sorted-profile lower bound: 359 attain it and 506 do
not. This tests actual mixed costs, independently of the bit-set recurrence.
The source-hashed result is `results/profile_interval_probe.json`.

The full constructor now checks the high-count range, builds a real BST,
and certifies it using the global key-plus-gap lower bound in GAP_PARITY.md.
Perfect-size inputs that miss the free key profile retain the older mixed
certificate and exact fallback. Full construction and measurement evidence
are recorded in the manuscript and `results/profile_complete*.json`.
The lemma does not optimize nonattaining patterns or arbitrary key alphabets.
