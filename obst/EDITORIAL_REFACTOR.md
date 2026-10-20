# Focused paper and claim audit

Checkpoint 72 separated the Monge paper from the broader research notebook.
The current paper is `manuscript/main.tex` and its compiled PDF. The independent
verification record is `manuscript/verification.tex` and its PDF. The exact
checkpoint-71 TeX/PDF are preserved as `research-notebook-71.tex/.pdf` beside
them, with their historical numbering and wording. That archive is not the
current paper.

## Argument retained

1. Model, fixed key/gap positions, cost convention and prior work.
2. Terminal-penalty Monge construction, mixed-weight height proof and finite completion.
3. Intermediate and aggregate core-size bounds.
4. Published condensed-product interface and full reconstruction.
5. Centering around separate constant key and gap baselines.
6. Explicit lower bounds for the density representation: odd ramp, positive ruler and local charging obstruction.
7. The remaining logarithmic gap and a conditional improvement.

The full proof chain is in the paper. Its statements require no code files,
experimental counts, archived theorem numbers or external research-note definitions.
The shape-box threshold, periodic/affine constructors, refinement grammars,
slot diagrams, contraction certificates and unrelated barrier families remain
in the archived notebook and their existing research notes. They do not enter
the proof of this paper's main result.

## Claim decisions

| Issue | Final treatment |
| --- | --- |
| “The core exponent is necessary” | The polynomial exponent in the explicit-core size analysis is tight; the bounds retain a square-root-logarithmic gap. |
| Core support versus OBST complexity | The lower bounds explicitly concern density lists. The positive ruler has quadratic support and a proved linear tree constructor. |
| Single-layer versus aggregate size | Separate statements and proofs; the construction time uses the aggregate bound. |
| Arithmetic versus bit complexity | Operations count exact arithmetic/comparisons; the integer-mass theorem separately bounds operand bit lengths. Baseline-independent operation counts retain dependence on operand lengths in bit cost. |
| Sparse support versus density mass | Defined separately. Integrality turns a nonnegative density-mass bound into a support bound; rescaling does not shrink support. |
| Residual Monge property | Only actual completed layers are required to be Monge. Residual densities are used on tiles where baseline density vanishes. |
| Space bound versus implementation | The paper states the published succinct-witness bound. Ordinary-map implementation qualifications stay in the supplement. |
| Exact stopping | Removed from the focused paper in checkpoint 73 because it changes no stated bound; the implementation discussion remains in the supplement. |
| Remaining improved exponent/logarithm | The boundary-plus-mass hypothesis is explicitly open; its consequence is a conditional lemma. |
| Priority and repeated disclaimers | Unneeded priority caveats and notebook commentary are removed. Published ingredients retain precise attribution. |

The positive-ruler proof now includes the actual key-length and gap-depth
changes for its adjacent expansion exchange. The main theorem's original
rotation table, non-power-of-two boundary count, finite-entry completion,
published primitive quotation and witness interface remain explicit.

## Preservation and validation

The empirical appendix is preserved in a separate supplement with references
to removed results resolved to their checkpoint-71 numbers. The supplement
links the complete archived notebook so those references have an available
source. Raw experiments, code and source-hashed records are unchanged.

After checkpoint 73, the main paper has seven sections, 16 numbered results, 49 unique labels,
five cited bibliography entries, no legacy labels and no empirical appendix.
Its abstract has 158 whitespace-delimited words when each mathematical span
is counted as one word. The main PDF is 20 pages; the empirical supplement is
48 pages. Both compile without warnings, unresolved references, missing
characters or overfull/underfull boxes. All pages are rendered and visually
reviewed before publication. The title asterisk, Joshuah Rainstar attribution
and final dedication are preserved; the dedication text is byte-identical.

## Checkpoint 73: prior-work scope and explicit centered overlap

The introduction now states Larmore's exact interval-mass theorem and its
positive-frequency corollary, using Theorem 1.1 and Corollary 1.2 of his
accessible author report. It states Karpinski–Larmore–Rytter's structural
sequential bound (Lemma 3.2), local-mass parallel bound (Theorem 4.1), the
sequential exponent supplied by that proof, and the random-permutation scope
of Theorem 5.1. The report is linked in the existing Larmore bibliography entry.

The classes overlap: positive integer inputs with linear total mass can meet
the earlier local-frequency hypotheses. The unrestricted placement of zeros
can violate those hypotheses. The example p_0=n, all other outcomes zero,
forces Larmore's interval threshold to have ell at least n-1 and violates
KLR's positive-singleton hypothesis. This compares the stated frequency
guarantees, without claiming that KLR's structural lemma cannot apply to
other such inputs. On the positive-frequency overlap, the new stated bound
also improves the prior sequential exponent.

Access counts from O(n) sampled lookups motivate the regime directly. The
abstract now gives the result, regime, centered extension, representation
lower bounds and open general problem; proof mechanisms open Section 2.

The existing per-outcome overlap lemma now covers any subset of lines
j-i=2^t-1. At scale s, short distances share one strip and give at most
36 spans through a position. Long distances contribute less than 72n/s;
the non-power-of-two outer boundaries contribute at most 8n/s. Thus the
total is at most 116n/s, stated conservatively as 120n/s. The centered
section applies this lemma directly to obtain sum_T R(J_T) <= 120nR/s.
The former separate asymptotic packing lemma is removed.
