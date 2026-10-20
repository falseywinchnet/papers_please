# Focused paper and claim audit

Checkpoint 72 separates the Monge paper from the broader research notebook.
The current paper is `manuscript/main.tex` and its compiled PDF. The independent
verification record is `manuscript/verification.tex` and its PDF. The exact
checkpoint-71 TeX/PDF are preserved as `research-notebook-71.tex/.pdf` beside
them, with their historical numbering and wording. That archive is not the
current paper.

## Argument retained

1. Model, fixed key/gap positions, cost convention and prior work.
2. Terminal-penalty Monge construction, mixed-weight height proof and finite completion.
3. Intermediate and aggregate core-size bounds.
4. Published condensed-product interface, full reconstruction and exact stopping.
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
| Empirical stopping behavior | A lemma proves that consecutive condensed equality identifies the full optimum and adds O(S) comparison work. |
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

The main paper has seven sections, 18 numbered results, 51 unique labels,
five cited bibliography entries, no legacy labels and no empirical appendix.
Its abstract has 166 whitespace-delimited words when each mathematical span
is counted as one word. The main PDF is 19 pages; the empirical supplement is
48 pages. Both compile without warnings, unresolved references, missing
characters or overfull/underfull boxes. All pages are rendered and visually
reviewed before publication. The title asterisk, Joshuah Rainstar attribution
and final dedication are preserved; the dedication text is byte-identical.
