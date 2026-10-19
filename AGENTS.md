# Research workspace

The authoritative copy is this local checkout. Use the user's M4 host selector.
For CPU-heavy builds and experiments, from this repository run:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/research.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/sparse.py --max-n 128
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/contract.py --max-n 512
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/block_check.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/block_contract.py --max-n 512
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/depth_dual.py --max-n 64 --iterations 300
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/depth_dual.py --max-n 256 --iterations 300
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/depth_dual.py --max-n 256 --iterations 300 --unique-root
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/recursive_contract.py --max-n 1024
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_recursive.py
```

Add specific compiled experiment commands here as they are introduced. Do not
edit the mirrored Mini checkout as the primary copy.

## Optimal BST research

The objective is the full static optimal binary search tree problem with
nonnegative weights on both keys and gaps. Preserve this scope. Alphabetic
leaf-only algorithms, dynamic optimality, and unproved heuristics do not resolve
the objective. Distinguish proved results, computational evidence, conjectures,
and known prior work. Keep counterexamples and failed experiments.

Use exact integer arithmetic for correctness experiments. Compare optimized
solvers with an independent cubic recurrence and exhaustive enumeration on
small instances. Benchmark full construction including preprocessing and tree
reconstruction. Never infer a worst-case bound from timings.

The user authorizes uploading resulting TeX and PDF to this repository. Mark
research drafts honestly; do not claim novelty before checking prior work.
