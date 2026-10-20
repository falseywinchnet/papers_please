"""Wilber's 1988 linear concave least-weight subsequence algorithm.

The algorithm is prior work. This implementation uses two SMAWK searches
per speculative batch, and symbolic ordered completion for invalid cells.
All actual arc weights are finite. Returned predecessors use leftmost ties.
"""
from collections import Counter


def row_minima(rows,columns,entry,stats):
    answer={}
    def visit(rr,cc):
        if not rr:return
        stats['lws_smawk_index_visits']+=len(rr)+len(cc)
        reduced=[]
        for col in cc:
            while reduced:
                row=rr[len(reduced)-1]
                stats['lws_smawk_comparisons']+=1
                if entry(row,col)<entry(row,reduced[-1]):reduced.pop()
                else:break
            if len(reduced)<len(rr):reduced.append(col)
        visit(rr[1::2],reduced)
        indices={col:k for k,col in enumerate(reduced)};low=0
        for pos in range(0,len(rr),2):
            high=indices[answer[rr[pos+1]]] if pos+1<len(rr) else len(reduced)-1
            row=rr[pos];best=reduced[low];value=entry(row,best)
            for k in range(low+1,high+1):
                col=reduced[k];other=entry(row,col);stats['lws_smawk_comparisons']+=1
                if other<value:best=col;value=other
            answer[row]=best;low=high
    visit(list(rows),list(columns))
    return answer


def concave_lws(n,weight,stats=None):
    stats=Counter() if stats is None else stats
    F=[None]*(n+1);pred=[-1]*(n+1);F[0]=0;r=c=0;charge=0
    def entry(j,i):
        stats['lws_entry_queries']+=1
        if i>=j:
            stats['lws_completion_queries']+=1
            return (1,0)
        assert F[i] is not None
        stats['lws_weight_queries']+=1
        return (0,F[i]+weight(i,j))
    while c<n:
        end=min(2*c-r+1,n);charge+=c-r+1
        stats['lws_batches']+=1
        selected=row_minima(range(c+1,end+1),range(r,c+1),entry,stats)
        for j in range(c+1,end+1):
            pred[j]=selected[j];F[j]=entry(j,pred[j])[1]
        newer=row_minima(range(c+2,end+1),range(c+1,end),entry,stats)
        first=None
        for j in range(c+2,end+1):
            candidate=entry(j,newer[j])[1];stats['lws_correction_checks']+=1
            if candidate<F[j]:first=j;value=candidate;break
        if first is None:c=end;stats['lws_accepted_batches']+=1
        else:
            F[first]=value;pred[first]=newer[first]
            r=c+1;c=first;stats['lws_corrected_batches']+=1
    assert charge<=3*n if n else charge==0
    stats['lws_span_charge']+=charge;stats['lws_vertices']+=n
    return F,pred
