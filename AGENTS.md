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
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/depth_order.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/complete.py --max-n 1024
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_complete.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/baseline_prices.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_baseline.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/ordered_certificate.py --max-n 512 --iterations 32
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/ordered_obstruction.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/excess.py --max-n 1024
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_excess.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/split_height.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_split_height.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/mass_frontier.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_mass_frontier.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/frontier_separation.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/gap_separator.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_gap_separator.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/separator_obstruction.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/heavy_core.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_heavy_core.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/heavy_core_scale.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_core_exclusion.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_core_exclusion.py --mixed-only
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_core_exclusion.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/core_exclusion_scale.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_pair_skeleton.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/pair_skeleton_family.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/pair_skeleton_crossover.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/boundary_response.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/penalty_layers.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_core_monge.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_compact_obst.py --max-n 512
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

Compiled condensed-Monge checks (binary outside the mirrored repository):

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer obst/code/compact_obst.cpp -o /tmp/obst-compact-sanitize && python3 obst/code/check_compact_cpp.py /tmp/obst-compact-sanitize --max-n 128 --trials 1 --label sanitize --flags="-std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer"'
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra obst/code/compact_obst.cpp -o /tmp/obst-compact-release && python3 obst/code/check_compact_cpp.py /tmp/obst-compact-release --max-n 2048 --trials 3'
```

Baseline-centered core and normalized-height diagnostic:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/centered_layers.py
```

Full condensed constructor with normalized height:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_centered_obst.py
```

Weight-independent baseline-diagonal packing audit:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/centered_geometry.py
```
