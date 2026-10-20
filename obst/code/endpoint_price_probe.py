#!/usr/bin/env python3
"""Independent tree, arrangement, and transformation oracles before pricing."""
from fractions import Fraction
from itertools import combinations
from joint_merge_probe import enumerated
from threshold_probe import key_bound


def transformed(p,q,a,x,y):
    assert len(p)>=3
    return [x]+[v-a for v in p[1:-1]]+[y], [p[0]+q[0]-x]+[v+a for v in q[1:-1]]+[p[-1]+q[-1]-y]


def literal(p,q,a,x,y):
    pp,qq=transformed(p,q,a,x,y)
    gap=min(sum(v*d for v,d in zip(qq,qd)) for _,_,qd in enumerated(len(p)))
    return key_bound(pp)+gap-a*len(p)


def arrangement_max(p,q):
    """Independent exhaustive arrangement of every gap-tree and key-rank break."""
    n=len(p);a=min(p[1:-1]);L=p[0]+q[0];R=p[-1]+q[-1]
    planes=set()
    for _,_,qd in enumerated(n):
        c=L*qd[0]+R*qd[-1]+sum((v+a)*d for v,d in zip(q[1:-1],qd[1:-1]))
        planes.add((-qd[0],-qd[-1],c))
    lines={(1,0,0),(1,0,L),(0,1,0),(0,1,R),(1,-1,0)}
    for v in p[1:-1]:lines.update(((1,0,v-a),(0,1,v-a)))
    for u,v in combinations(planes,2):
        A=u[0]-v[0];B=u[1]-v[1];C=v[2]-u[2]
        if A or B:lines.add((A,B,C))
    points={(Fraction(0),Fraction(0)),(Fraction(L),Fraction(R))}
    for (A,B,C),(D,E,F) in combinations(lines,2):
        det=A*E-B*D
        if det:
            x=Fraction(C*E-B*F,det);y=Fraction(A*F-C*D,det)
            if 0<=x<=L and 0<=y<=R:points.add((x,y))
    best=max((literal(p,q,a,x,y),x,y) for x,y in points)
    return best,len(points)


def rank(rows):
    basis={}
    for row in rows:
        row=list(map(Fraction,row))
        for pivot,v in sorted(basis.items()):
            z=row[pivot]
            if z:row=[x-z*y for x,y in zip(row,v)]
        pivot=next((i for i,x in enumerate(row) if x),None)
        if pivot is not None:
            z=row[pivot];basis[pivot]=[x/z for x in row]
    return len(basis)
