"""Exact mixed OBST at prescribed height: run vectors and gap transitions.

Uses prior-work SMAWK, never a product of full transfer matrices. The common
internal gap baseline is absorbed by an exact tree-cost identity. Remaining
gaps are handled by a linear ruler-valuation sweep. No unrestricted height
certificate is assumed.
"""
from collections import Counter
from concave_lws import row_minima
from mixed_slots import repair


def normalize(p,q):
    assert p and len(q)==len(p)+1 and all(x>=0 for x in (*p,*q))
    n=len(p)
    if n==1:return [p[0]+q[0]+q[1]],[0,0],0
    b=min(q[1:n]);w=[x+b for x in p]
    w[0]=p[0]+q[0];w[-1]=p[-1]+q[-1]
    g=[0]+[x-b for x in q[1:n]]+[0]
    return w,g,b*n


def operations(w,g):
    out=[];i=0
    while i<len(w):
        if i and g[i]>0:
            out.append((i,1,w[i],g[i]));i+=1
        else:
            j=i+1
            while j<len(w) and w[j]==w[i] and g[j]==0:j+=1
            out.append((i,j-i,w[i],0));i=j
    return out


def gap_pass(old,k,w,g,v,h,stats):
    """Append one key, retaining the best predecessor for each ending slot."""
    c=len(v)-1;new=[None]*(c+1);back=[-1]*(c+1)
    exact=[None]*h;suffix=[None]*h
    # k=0 has the unique empty predecessor at slot zero, of valuation zero.
    for b in range(k+1,c+1):
        a=b-1
        if old[a] is not None:
            d=v[a];cand=(old[a],a)
            if exact[d] is None or cand<exact[d]:exact[d]=cand
            for e in range(d+1):
                if suffix[e] is None or cand<suffix[e]:suffix[e]=cand
                stats['vector_gap_suffix_updates']+=1
            stats['vector_gap_insertions']+=1
        e=v[b];winner=None
        for d in range(e):
            if exact[d] is not None:
                val,a=exact[d];cand=(val-g*d,a)
                if winner is None or cand<winner:winner=cand
            stats['vector_gap_lower_scans']+=1
        if suffix[e] is not None:
            val,a=suffix[e];cand=(val-g*e,a)
            if winner is None or cand<winner:winner=cand
        assert winner is not None
        new[b]=winner[0]-w*e;back[b]=winner[1]
        stats['vector_gap_states']+=1
    return new,back


def run_pass(old,k,w,m,v,h,K,stats):
    """Append an equal-key run and force its final key to occupy column b."""
    c=len(v)-1;rows=range(k+m,c+1);cols=[0] if k==0 else range(k,c-m+1)
    def entry(b,a):
        stats['vector_run_entry_queries']+=1
        reward=v[b]
        for t in range(1,h):
            d=1<<t;reward+=min(m-1,(b-1)//d-a//d)
            stats['vector_run_threshold_terms']+=1
        return old[a]+K*max(m-b+a,0)-w*reward
    arg=row_minima(rows,cols,entry,stats)
    new=[None]*(c+1);back=[-1]*(c+1)
    for b in rows:
        a=arg[b];assert b-a>=m
        new[b]=entry(b,a);back[b]=a;stats['vector_run_states']+=1
    return new,back


def select_run(a,b,m,v,h,stats):
    assert b-a>=m
    if m==1:return [b]
    counts=[0]*h
    for t in range(a+1,b):counts[v[t]]+=1;stats['vector_trace_bucket_visits']+=1
    need=m-1;cut=h-1
    while need>counts[cut]:need-=counts[cut];cut-=1;stats['vector_trace_level_scans']+=1
    slots=[]
    for t in range(a+1,b):
        if v[t]>cut:slots.append(t)
        elif v[t]==cut and need:slots.append(t);need-=1
        stats['vector_trace_output_visits']+=1
    assert need==0
    return slots+[b]


def solve(p,q,h,stats=None,observer=None):
    assert h>=1
    stats=Counter() if stats is None else stats
    w,g,constant=normalize(p,q);n=len(w);c=(1<<h)-1
    if n>c:return None
    v=[0]*(c+1)
    for t in range(1,c+1):v[t]=0 if t%2 else v[t//2]+1;stats['vector_ruler_entries']+=1
    ops=operations(w,g);K=1+(h-1)*(sum(w)+sum(g));old=[None]*(c+1);old[0]=0;backs=[]
    stats['vector_normalized_keys']+=n
    for k,m,weight,gap in ops:
        if m==1:
            new,back=gap_pass(old,k,weight,gap,v,h,stats);stats['vector_singleton_passes']+=1
        else:
            assert gap==0
            new,back=run_pass(old,k,weight,m,v,h,K,stats);stats['vector_run_passes']+=1
        if observer is not None:observer(k,m,old,new,back,w,g,v,K)
        backs.append(back);old=new;stats['vector_predecessor_slots']+=len(back)
    value,b=min((old[t],t) for t in range(n,c+1));pieces=[]
    for (k,m,weight,gap),back in zip(reversed(ops),reversed(backs)):
        a=back[b];pieces.append(select_run(a,b,m,v,h,stats));b=a;stats['vector_trace_stages']+=1
    assert b==0
    slots=[t for piece in reversed(pieces) for t in piece]
    assert len(slots)==n and all(a<b for a,b in zip(slots,slots[1:]))
    reward=sum(x*v[t] for x,t in zip(w,slots))+sum(g[i]*min(v[slots[i-1]],v[slots[i]]) for i in range(1,n))
    assert value==-reward
    tree=repair(slots,h,stats)
    r=1+sum(w[i]!=w[i-1] for i in range(1,n));exceptions=sum(x>0 for x in g)
    assert len(ops)<=r+2*exceptions
    return dict(cost=h*(sum(w)+sum(g))+value+constant,tree=tree,slots=slots,
                runs=r,gap_exceptions=exceptions,stages=len(ops),height=h)
