# Full optimal binary search trees: research record

Started 2026-10-18, America/Chicago. Research and exposition by OpenAI Codex
Sydney, with sponsorship and problem selection by the repository owner.

## Objective and status

Find a substantively useful improvement for the full optimal binary search tree
problem, or prove an appropriate barrier to subquadratic construction. The
general exact subquadratic problem remains unresolved by this project.
The current checkpoint gives exact sufficient contraction rules and an
adaptive linear preprocessing pass. Its bound is O(n+m^2+sum k_t^2), where
m is the surviving core size and k_t are independently solved block sizes.
This improves state counts substantially on a seeded heavy-separator input,
but little on ordinary random mixed weights. Novelty is unestablished;
no general subquadratic bound or complexity lower bound is claimed.

Input: ordered keys 1..n, key weights p[1..n], gap weights q[0..n], all
nonnegative. No normalization is required. Use comparison cost with root key
cost one and gap cost equal to the number of internal ancestors. In half-open
key intervals [i,j),

    C(i,i) = 0
    W(i,j) = sum(p[i:j]) + sum(q[i:j+1])
    C(i,j) = W(i,j) + min_r(C(i,r) + C(r+1,j)), i <= r < j.

The common convention charging one additional unit at every gap differs by
sum(q), independent of tree shape.

## Prior-art map (initial)

- Knuth (1971), Optimum binary search trees: quadratic dynamic programming
  using monotone roots. DOI 10.1007/BF00264289. Need inspect original proof.
- Larmore (1987), A subquadratic algorithm for constructing approximately
  optimal binary search trees, Journal of Algorithms 8:579-591.
  DOI 10.1016/0196-6774(87)90052-6. Exact subquadratic under weight restrictions;
  also approximation. Author's 1986 report:
  https://escholarship.org/content/qt4v7249bv/qt4v7249bv.pdf
- Karpinski, Larmore, Rytter (1996), Sequential and Parallel Subquadratic Work
  Algorithms for Constructing Approximately Optimal Binary Search Trees.
  https://theory.cs.uni-bonn.de/marek/publications/seq_and_par_subquadr.pdf
- Nagaraj (1997), Optimal binary search trees, TCS 188:1-44.
  https://community.wvu.edu/~krsubramani/courses/fa16/Aaoa/lecnotes/obst.pdf
  Crucial: Section 2.3 corrects subtree-weight claims when gaps have weight.
  Section 5.1 asks about subquadratic construction and verification.
- Nipkow and Somogyi (2025), Isabelle/AFP formalization of Knuth/Yao/Mehlhorn:
  https://www.isa-afp.org/browser_info/current/AFP/Optimal_BST/document.pdf
- Becker (2010), Optimal Binary Search Trees with Near Minimal Height.
  https://arxiv.org/abs/1011.1337. Full mixed weights; O(n^2) for a fixed
  additive height excess. Sequential key placement uses a bit-vector state
  for the occupied right-fringe levels. Relevant to near-uniform inputs;
  this representation is existing work, not a novel proposal here.

## Research directions to discriminate

User steering: primary measurements are visited interval states, candidate
roots, and all preprocessing/bound work. Include geometric, reversed geometric,
folded geometric, near-uniform, random, zeros/ties, and mixed key/gap inputs.
An improvement must avoid most of the interval table in its claimed regime.

1. Sparse optimality certificates / demand-driven exact DP: can many interval
   states be excluded by certified lower bounds without losing exactness?
2. A representation of mixed key/gap cost that permits an efficient relaxation
   with a verifiable gap. Preserve key termination; do not silently convert to
   the alphabetic special case.
3. Rotation-based or stronger local certificates: find exact small
   counterexamples before investing in claims of sufficiency.
4. Compressed interval DP and structural parameterization: identify which
   parameters actually bound work, and compare with Larmore's existing method.

## Second checkpoint: depth prices and recursive decomposition

The previous goal turn was progress: it produced a committed, pushed,
compiled, visually checked manuscript and an exact contraction implementation.
The full research objective is still unresolved.

The new depth-chain relaxation retains fixed key and gap positions and prices
the necessary level-flow equations. An affine-tail projection lemma makes
each full-problem bound evaluation O(n log n), without assuming a bound on
the unknown optimal BST height. A unique-root version obtains all forced-root
marginals in two passes. See DEPTH_DUAL.md for the proof and exact checks.

Crucial negative evidence: a positive five-key input has an invalid depth
sequence satisfying all these constraints with cost 470, versus true OPT 472.
No multipliers can close this gap. At n=256 the root marginals also leave
254 roots on the ordinary random mixed instance. This lower bound has not
yet supplied an efficient exact construction method.

`recursive_contract.py` combines the existing exact single-key reductions,
whole-instance Huffman equality certificates, and block decomposition. A
decomposition is accepted only when its table-state estimate drops by at
least one quarter. This bounds recursion depth and avoids repeated scans
after tiny reductions. It passed 3,000 independent cubic checks and 20
nested 383-key checks against Knuth, exercising two decomposition levels.
Matched five-trial measurements at n=1024 gave median runtime ratio 0.134
on positive heavy-separator inputs, but essentially no gain on random or
near-uniform mixed weights. Several n=512 controls were slower. No broad
practical superiority is claimed.

## Completion requirements

- A fully stated, proved result or substantively validated algorithm for the
  requested mixed-weight problem, with honest scope and prior-art comparison.
- Reproducible correctness and adversarial evidence; practical claims require
  appropriate matched benchmarks against Knuth and relevant alternatives.
- TeX manuscript and compiled, visually checked PDF uploaded to papers_please.
- Continued pursuit of the full objective; intermediate notes are not completion.
