#!/usr/bin/env python3
"""Weight-independent packing audit for the baseline dyadic tiling."""
from collections import Counter,defaultdict
import hashlib,json,random
from pathlib import Path


def check(n):
    N=1<<(n-1).bit_length();lines=[(1<<t)-1 for t in range(1,n.bit_length()+1) if (1<<t)-1<n]
    tiles=defaultdict(list);exceptional=0;covered=0
    def visit(a,b,s):
        nonlocal exceptional,covered
        if a>=n or b>=n or b+s-1<a:return
        inside=a+s<=n and b+s<=n
        lo,hi=b-a-s+1,b+s-1-a
        hit=lo<=0<=hi or any(lo<=d<=hi for d in lines)
        if s>1 and (not inside or hit):
            t=s//2
            for x,y in ((a,b),(a+t,b),(a,b+t),(a+t,b+t)):visit(x,y,t)
        elif inside and hit:
            if a<b:exceptional+=1;covered+=1
        elif inside:
            assert a+s<=b
            tiles[s].append((a,b+s));covered+=s*s
    visit(0,0,N);assert covered==n*(n-1)//2
    rows=[]
    for s,intervals in sorted(tiles.items()):
        delta=[0]*(n+2)
        for a,b in intervals:delta[a]+=1;delta[b+1]-=1
        current=maximum=0
        for v in delta:current+=v;maximum=max(maximum,current)
        # Every nonnegative residual-weight vector is bounded by this maximum.
        assert maximum*s<=64*n
        assert len(intervals)*s<=64*n*(1+(n//s).bit_length())
        rows.append(dict(side=s,tiles=len(intervals),maximum_gap_overlap=maximum))
    return dict(n=n,exceptional_cells=exceptional,scales=rows)


def main():
    rng=random.Random(81739)
    sizes=sorted(set(range(1,130))|{255,256,257,511,512,513,1023,1024,1025,2047,2048,2049,4095,4096}|{rng.randrange(130,4097) for _ in range(20)})
    rows=[]
    for n in sizes:
        rows.append(check(n))
        if n>=255:print('geometry',n,flush=True)
    root=Path(__file__).resolve().parents[1]
    out=dict(seed=81739,checked_sizes=len(sizes),checked_scales=sum(len(r['scales']) for r in rows),rows=rows,source_sha256={'centered_geometry.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (root/'results'/'centered_geometry.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['checked_sizes'],out['checked_scales'],flush=True)
if __name__=='__main__':main()
