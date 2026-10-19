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

Fixed-mass adversarial core-size search and independent layer audit:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_size_search.cpp -o /tmp/obst-core-size-search && python3 obst/code/core_size_search.py /tmp/obst-core-size-search'
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_size_search.cpp -o /tmp/obst-core-size-search && python3 obst/code/check_core_size_lemmas.py && python3 obst/code/core_size_patterns.py /tmp/obst-core-size-search && python3 obst/code/core_size_search.py /tmp/obst-core-size-search --sizes 16,31,32,63,64,127,128,255,256,511,512,1024 --steps 4000'
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/ramp_core_tightness.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/aggregate_core_audit.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/dyadic_mass_probe.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/single_key_tile.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_mixed_slots.py
```

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

Ruler-pattern identities, dense-difference barrier, and exchange constructor:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/ruler_layers.py --max-n 512
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/ruler_barrier.py --max-n 512
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/ordered_complete.py --max-n 768
```

Affine-regret corridor, independent exact checks, and matched full constructors:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_ramp_complete.py --max-n 768 --scale-n 98304
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_ramp_complete.py
```

Joint key/adjacent-gap signature transfers and linear-space reconstruction:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_run_complete.py --max-n 768 --scale-n 98304
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_run_complete.py
```

Two-level key profile reachability probe (no full solver claim):

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/profile_interval_probe.py --max-n 40 --literal-n 9
```

Full two-level profile constructor, independent oracles, and matched routes:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_profile_complete.py --max-n 768 --scale-n 393216
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_profile_complete.py
```

Global alternating-gap lower bound and exhaustive mixed-tree controls:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_gap_parity.py
```

Arbitrary-gap threshold bounds, dyadic selection, and full Cartesian certificate:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/threshold_probe.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_threshold_complete.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_threshold_complete.py
```

Joint-profile obstruction and shifted alphabetic full certificates:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/joint_merge_probe.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/joint_merge_obstruction.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/joint_coupling_audit.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/shifted_gap_probe.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_shifted_alphabetic.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_shifted_alphabetic.py
```

Exact endpoint pricing, all-transfer obstruction, and full mixed scaling:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_endpoint_prices.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/endpoint_price_search.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/endpoint_price_box.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/endpoint_price_family.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_endpoint_prices.py
```

Single interior-key marked-boundary event probe (unproved candidate family):

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_marked_event.py
```

Root/nonroot coupling harness, before the optimized constructor:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/root_partition_probe.py
```

Full root/nonroot constructor, independent oracles, scaling, and matched runs:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_root_partition.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/root_partition_family.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/benchmark_root_partition.py
```

Binary-weight adversarial controls and exact gap-core mass audit:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/binary_core_search.cpp -o /tmp/obst-binary-core-search && python3 obst/code/binary_core_search.py /tmp/obst-binary-core-search'
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/gap_core_identity.py
```

Full mixed boundary identities and off-boundary falsification probe:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/mixed_boundary_mass.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/core_tail_probe.py
```

All-band tail diagnostics and exact capacity-band construction:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_tail_search.cpp -o /tmp/obst-core-tail-search && python3 obst/code/core_tail_search.py /tmp/obst-core-tail-search'
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/core_tail_extremes.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/core_tail_interaction.py
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/check_capacity_band.py
```

Capacity interaction identity and adversarial interaction search:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/capacity_interaction.py
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_interaction_search.cpp -o /tmp/obst-core-interaction-search && python3 obst/code/core_interaction_search.py /tmp/obst-core-interaction-search'
```

Sharp capacity-interaction families:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/capacity_interaction_sharp.py
```

One-sided tail interaction diagnostics:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/one_sided_interaction.py
```

Sparse-weight interaction falsification:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_interaction_search.cpp -o /tmp/obst-core-interaction-search && python3 obst/code/sparse_interaction_search.py /tmp/obst-core-interaction-search'
```

Explicit two-key interaction barrier:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/sparse_interaction_barrier.py
```

Original total-tail target on sparse and coupled phase patterns:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_tail_search.cpp -o /tmp/obst-core-tail-search && python3 obst/code/sparse_tail_search.py /tmp/obst-core-tail-search'
```

Rank-reward perturbation and periodic clipping audit:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/rank_reward_tail.py
```

Repeated sparse clusters across ruler scales:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/core_tail_search.cpp -o /tmp/obst-core-tail-search && python3 obst/code/cluster_tail_search.py /tmp/obst-core-tail-search'
```

Exact periodic-template barrier audit:
`/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/periodic_tail_barrier.py`

Clipped-ruler width-sensitive tail falsification:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/periodic_tail_probe.cpp -o /tmp/obst-periodic-tail-probe && python3 obst/code/periodic_tail_probe.py /tmp/obst-periodic-tail-probe'
```

Alternating-template matching, augmentation, and sharp-scale audit:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/alternating_tail_bound.py
```

Retained-rank accounting for endpoint matching repairs:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/rank_matching_repair.py
```

Rightmost-optimum endpoint repair control:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/rank_matching_repair.py --rightmost
```

Exact rank-repair barriers and canonical-witness audit:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/rank_repair_barrier.py
```

True upper-tail input-key sensitivity diagnostic:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/key_tail_sensitivity.py
```

Fixed-mass exact input-key sensitivity search:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/key_sensitivity_search.cpp -o /tmp/obst-key-sensitivity-search && python3 obst/code/key_sensitivity_search.py /tmp/obst-key-sensitivity-search'
```

Weighted alternating-cluster formula and sensitivity audit:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/weighted_cluster_tail.py
```

Nested-threshold tail charging falsification:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/nested_tail_probe.py
```

Boundary-plus-mass local core-support search:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/tile_boundary_probe.cpp -o /tmp/obst-tile-boundary-probe && python3 obst/code/tile_boundary_probe.py /tmp/obst-tile-boundary-probe'
```

Capacity-adjacent tile-support search avoiding small-tile plateaus:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/tile_capacity_support.cpp -o /tmp/obst-tile-capacity-support && python3 obst/code/tile_capacity_support.py /tmp/obst-tile-capacity-support'
```

Single-key logarithmic-square support audit:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/one_key_square.py
```

Literal zero-threshold-tail counterexample:

```
/Users/ultimussecundai/.local/bin/m4build -- python3 obst/code/nested_tail_example.py
```

Fixed-side, variable-mass local support falsification:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/tile_support_frontier.cpp -o /tmp/obst-tile-support-frontier && python3 obst/code/tile_support_frontier.py /tmp/obst-tile-support-frontier'
```

General-template tail probe and explicit spaced-rank family:

```
/Users/ultimussecundai/.local/bin/m4build -- sh -c 'clang++ -std=c++20 -O3 -Wall -Wextra obst/code/template_tail_probe.cpp -o /tmp/obst-template-tail-probe && python3 obst/code/template_tail_probe.py /tmp/obst-template-tail-probe && python3 obst/code/spaced_rank_tail.py /tmp/obst-template-tail-probe && python3 obst/code/ruler_clipping_sharp.py /tmp/obst-template-tail-probe'
```

The sharpness audit reads the spaced-rank result as an independently computed
control and records its hash. The two-key rank enumeration and original
all-root checks are distinct from the generic compiled subsequence recurrence.
