#!/usr/bin/env python3
"""Independent exact checks of the proposed whole-interval contraction."""
import json
from pathlib import Path
import random
from research import cubic


def verify():
    rng = random.Random(0xB10CC)
    checked = 0
    cases = 0
    for n in range(2, 17):
        for trial in range(300):
            p = [1 << rng.randrange(15) for _ in range(n)]
            q = [rng.randrange(3) if trial%2 else 1 << rng.randrange(10)
                 for _ in range(n+1)]
            opt, _ = cubic(p, q)
            cases += 1
            for i in range(n):
                for j in range(i+1, n+1):
                    if i == 0 and j == n:
                        continue
                    cp, cq = p[i:j], q[i:j+1]
                    c, _ = cubic(cp, cq)
                    w = sum(cp) + sum(cq)
                    threshold = c if i == 0 or j == n else w+c
                    if ((i == 0 or p[i-1] >= threshold)
                            and (j == n or p[j] >= threshold)):
                        pp = p[:i] + p[j:]
                        qq = q[:i] + [w] + q[j+1:]
                        reduced, _ = cubic(pp, qq)
                        assert opt == reduced+c, (p,q,i,j,opt,reduced+c)
                        checked += 1
    result = dict(input_instances=cases, valid_block_checks=checked,
                  seed=0xB10CC)
    target = Path(__file__).resolve().parents[1] / 'results/block_check.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    verify()
