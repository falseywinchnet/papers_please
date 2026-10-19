#!/usr/bin/env python3
"""Exact robust-box controls for the entire additive-transfer obstruction."""
import hashlib,itertools,json
from pathlib import Path
from endpoint_prices import attempt
from research import cubic,knuth


def main():
    p=[1,1,2,1];q=[1,2,1,1,1];minimum=None;maxcalls=0
    for signs in itertools.product((-1,1),repeat=9):
        ws=[100*z+e for z,e in zip(p+q,signs)];pp,qq=ws[:4],ws[4:]
        _,_,s,d=attempt(pp,qq,budget=100,stop_on_certificate=False)
        assert d['max_complete'];opt=cubic(pp,qq)[0];assert opt==knuth(pp,qq)[0]
        gap=opt-d['lower'];assert gap>=56
        minimum=gap if minimum is None else min(minimum,gap);maxcalls=max(maxcalls,s['oracle_calls'])
    ws=[1000*z+i-4 for i,z in enumerate(p+q)];pp,qq=ws[:4],ws[4:]
    _,_,s,d=attempt(pp,qq,budget=100,stop_on_certificate=False)
    opt=cubic(pp,qq)[0];assert opt==knuth(pp,qq)[0]
    assert len(set(ws))==9 and d['max_complete'] and opt-d['lower']>=824
    result=dict(corners=512,min_corner_gap=str(minimum),max_calls=maxcalls,
                distinct=dict(p=pp,q=qq,optimum=opt,lower=str(d['lower']),history=d['history']),
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('endpoint_price_box.py','endpoint_prices.py','shifted_alphabetic.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'endpoint_price_box.json').write_text(json.dumps(result,default=str,indent=2)+'\n')
    print(json.dumps(result,default=str,indent=2),flush=True)


if __name__=='__main__':main()
