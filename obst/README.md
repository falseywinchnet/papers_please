# Full optimal binary search trees: research checkpoint

Research and exposition by OpenAI Codex Sydney, with sponsorship and problem
selection by the repository owner. The general research objective is ongoing.

- [Manuscript (PDF)](manuscript/main.pdf)
- [Manuscript (TeX)](manuscript/main.tex)
- [Research record and prior-work map](RESEARCH.md)
- [Contraction argument](CONTRACTION.md)
- [Relaxation, counterexamples, and failed sparse search](RELAXATION.md)

The input has weights on **both keys and gaps**. The checkpoint gives exact
sufficient conditions for collapsing keys or blocks, plus a linear pass that
chooses a block-size threshold minimizing subsequent interval-DP states.
The resulting bound is O(n + m² + sum k_t²). It remains quadratic in the
worst case; no general subquadratic solution or impossibility proof is claimed.
Novelty of the sufficient conditions has not been established.

At 512 keys, a positive-weight instance with 22 randomly located heavy keys
needed 10,344 total DP states rather than 131,328. This includes the tables
inside collapsed blocks. Ordinary random mixed weights benefited little.
These are state counts, not wall-clock speedup claims.

## Reproduce

Python 3, standard library only. From the repository root:

```
python3 obst/code/research.py
python3 obst/code/sparse.py --max-n 128 --trials 2
python3 obst/code/contract.py --max-n 512
python3 obst/code/block_check.py
python3 obst/code/block_contract.py --max-n 512
```

The sponsor's host-specific remote commands are in the root AGENTS.md.
Exact integer correctness checks use an independent cubic oracle, Knuth DP,
and direct tree-cost evaluation. The basic harness also enumerates shapes.
Seeds and counts are in the code and JSON results. The sparse solver is
preserved as a failed performance experiment, not recommended as a fast solver.
`block_contraction.json` preserves the earlier fixed-cap experiment;
`block_contraction_adaptive.json` records the current adaptive implementation.

Compile `manuscript/main.tex` with Tectonic or a compatible LaTeX installation.
