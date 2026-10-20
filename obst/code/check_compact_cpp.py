#!/usr/bin/env python3
"""Independent tree/cost checks and paired full-constructor C++ measurements."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import subprocess
from research import cubic,knuth
from compact_obst import solve
from check_compact_obst import fixture


def tree_cost(parent,p,q):
    n=len(p)
    assert len(parent)==n
    if not n:return 0
    roots=[i for i,x in enumerate(parent) if x==-1]
    assert len(roots)==1
    children=[[] for _ in p]
    for i,x in enumerate(parent):
        if x!=-1:
            assert 0<=x<n and x!=i
            children[x].append(i)
    seen=set();total=0;stack=[(roots[0],0,n,0)]
    while stack:
        r,lo,hi,depth=stack.pop()
        assert lo<=r<hi and r not in seen
        seen.add(r);total+=p[r]*(depth+1)
        left=[x for x in children[r] if x<r];right=[x for x in children[r] if x>r]
        assert len(left)==int(lo<r) and len(right)==int(r+1<hi)
        if left:stack.append((left[0],lo,r,depth+1))
        else:total+=q[lo]*(depth+1)
        if right:stack.append((right[0],r+1,hi,depth+1))
        else:total+=q[hi]*(depth+1)
    assert len(seen)==n
    return total


def main():
    ap=argparse.ArgumentParser();ap.add_argument('binary');ap.add_argument('--max-n',type=int,default=2048)
    ap.add_argument('--trials',type=int,default=3);ap.add_argument('--label',default='release')
    ap.add_argument('--flags',default='-std=c++20 -O3 -DNDEBUG -Wall -Wextra')
    args=ap.parse_args();rng=random.Random(613579);checks=Counter();rows=[]
    proc=subprocess.Popen([args.binary],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
    def check(p,q,oracle=False,python=False):
        proc.stdin.write(' '.join(map(str,[len(p),*p,*q]))+'\n');proc.stdin.flush()
        line=proc.stdout.readline()
        if not line:raise RuntimeError('C++ stopped with code '+str(proc.poll()))
        row=json.loads(line);value=int(row['cost'])
        assert tree_cost(row['parent'],p,q)==value
        assert row['counts']['constructed_keys']==len(p)
        if oracle:
            ref=knuth(p,q)[0]
            assert value==ref;checks['independent_knuth']+=1
            if len(p)<=12:assert value==cubic(p,q)[0];checks['independent_cubic']+=1
        if python:assert solve(p,q)[0]==value;checks['python_compact']+=1
        checks['solves']+=1;checks['keys_checked']+=len(p)
        row.pop('parent');return row
    for n in range(5):
        for v in itertools.product((0,1),repeat=2*n+1):check(list(v[:n]),list(v[n:]),True)
        print('binary exhaustive',n,flush=True)
    for n in range(1,49):
        for t in range(12):
            p=[rng.randrange(31) for _ in range(n)];q=[rng.randrange(31) for _ in range(n+1)]
            check(p,q,True,python=(n<=12 and t==0))
    for n in (16,32,64):
        for name in ('geometric','folded'):
            p,q=fixture(n,name,rng);row=check(p,q,True);row.update(n=n,family=name,trial=0);rows.append(row)
    for n in (32,128):
        check([0]*n,[0]*(n+1),True)
        for at in (0,n//2,n):
            q=[0]*(n+1);q[at]=1;check([0]*n,q,True)
    n=128
    while n<=args.max_n:
        for name in ('uniform','binary','near_uniform','random_16','sparse','alternating'):
            for trial in range(args.trials):
                p,q=fixture(n,name,rng);row=check(p,q,oracle=(trial==0));row.update(n=n,family=name,trial=trial,mass=sum(p)+sum(q));rows.append(row)
            print(name,n,'C/K seconds',row['compact_seconds'],row['knuth_seconds'],'core visits',row['counts']['core_visits'],flush=True)
        n*=2
    proc.stdin.close();assert proc.wait()==0
    # Invalid integers and the documented arithmetic domain fail explicitly.
    for bad in ('1 -1 0 0\n','1 0 0\n','1 '+str(1<<120)+' 0 0\n'):
        rejected=subprocess.run([args.binary],input=bad,text=True,capture_output=True)
        assert rejected.returncode!=0 and not rejected.stdout
        checks['invalid_inputs_rejected']+=1
    root=Path(__file__).resolve().parents[1]
    files=('compact_obst.cpp','check_compact_cpp.py','research.py','compact_obst.py','core_monge.py','check_compact_obst.py')
    result=dict(seed=613579,label=args.label,max_n=args.max_n,trials=args.trials,flags=args.flags,
                compiler=subprocess.check_output(['clang++','--version'],text=True),host=platform.platform(),
                checks=dict(checks),rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files},
                timing_scope='Both full constructors, including preprocessing and tree reconstruction; order alternates per case. Exact signed-128 arithmetic. Independent Python audits are outside timings.',
                counter_scope='Instrumented core visits, allocations in slots, candidate evaluations, and witness work; categories are not equivalent machine instructions and do not count every arithmetic operation.')
    (root/'results'/('compact_cpp_'+args.label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(dict(checks),flush=True)

if __name__=='__main__':main()
