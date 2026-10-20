#!/usr/bin/env python3
"""Complete unstructured lattice perturbations, face reuse and negative controls."""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from coarse_face import solve,Prepared
from trimmed_height import knuth_fallback
from slot_records_audit import check_tree


def main():
    rng=random.Random(663019);rows=[];reuse=[]
    for n in (32,64,128,256):
        for trial in range(2):
            bp=[rng.randrange(8) for _ in range(n)];bq=[rng.randrange(8) for _ in range(n+1)];D=64*(n+1)**4
            fine=[D*x+i+1 for i,x in enumerate(bp+bq)];p,q=fine[:n],fine[n:]
            counts=Counter();ans=solve(p,q,counts);refs=Counter();value,_=knuth_fallback(p,q,refs)
            assert ans['method']=='face' and ans['cost']==value==check_tree(ans['tree'],p,q,n,Counter())
            assert len(set(p+q))==2*n+1
            rows.append(dict(n=n,trial=trial,kind='unstructured_lattice',p=p,q=q,coarse_mass=ans['coarse_mass'],delta=str(ans['delta']),error=str(ans['error']),blocks=ans['blocks'],counts=counts,reference_counts=refs))
            print('lattice',n,trial,'forced',counts['face_forced_keys'],'largest',max([b-a for a,b in ans['blocks']]+[0]),'payload cells',counts['height_fallback_states'],'core visits',counts['core_visits'],flush=True)
        p=[rng.randrange(1,1000) for _ in range(n)];q=[rng.randrange(1,1000) for _ in range(n+1)]
        counts=Counter();ans=solve(p,q,counts);refs=Counter();value,_=knuth_fallback(p,q,refs)
        assert ans['cost']==value==check_tree(ans['tree'],p,q,n,Counter())
        rows.append(dict(n=n,kind='ordinary_mixed',p=p,q=q,method=ans['method'],blocks=ans['blocks'],counts=counts,reference_counts=refs))
    for n in (31,63,127,255):
        # Every perfect-size uniform coarse tree is uniquely balanced.
        prep_counts=Counter();prepared=Prepared([1]*n,[1]*(n+1),prep_counts);assert prepared.plan['unique']
        D=64*(n+1)**4;trials=[]
        for trial in range(3):
            p=[D+rng.randrange(-n,n+1) for _ in range(n)];q=[D+rng.randrange(-n,n+1) for _ in range(n+1)]
            counts=Counter();ans=prepared.refine(p,q,D,counts);refs=Counter();value,_=knuth_fallback(p,q,refs)
            assert ans['cost']==value==check_tree(ans['tree'],p,q,n,Counter())
            assert not counts['height_fallback_states'] and not counts['product_calls']
            trials.append(dict(p=p,q=q,counts=counts,reference_counts=refs))
        reuse.append(dict(n=n,preparation_counts=prep_counts,trials=trials));print('reuse',n,flush=True)
    # Non-perfect uniform coarse inputs have global root ambiguity. Small
    # perturbations are valid but this partition can retain the entire table.
    for n in (32,64,128):
        D=64*(n+1)**4;p=[D+i+1 for i in range(n)];q=[D+n+i+1 for i in range(n+1)]
        counts=Counter();ans=solve(p,q,counts,delta=D);refs=Counter();value,_=knuth_fallback(p,q,refs)
        assert ans['cost']==value==check_tree(ans['tree'],p,q,n,Counter()) and ans['blocks']==[(0,n)]
        rows.append(dict(n=n,kind='uniform_global_ambiguity',p=p,q=q,blocks=ans['blocks'],counts=counts,reference_counts=refs))
    root=Path(__file__).resolve().parents[1]
    files=['coarse_face_scale.py','coarse_face.py','compact_obst.py','core_monge.py','penalty_layers.py','research.py','trimmed_height.py','slot_records_audit.py']
    out=dict(scope='Complete exact original-weight construction with coarse preparation included, reused-face queries separated, and global ambiguity/rejection controls retained',seed=663019,rows=rows,reuse=reuse,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/coarse_face_scale.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
