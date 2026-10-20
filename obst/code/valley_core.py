"""Enumerate valley above-capacity cores through top-c sum support.

For integer keys of mass P, each layer has at most P candidates. All layers
take O((n+P) log^2(n+1)) work and O((n+P) log(n+1)) storage. Arbitrary
nonnegative gap weights cancel from the enumerated ordinary densities.
"""
from collections import Counter
from valley_above import ValleyAbove,largest_end_split


class ValleyCores(ValleyAbove):
    def first_greater(self,start,stop,value):
        # This range is on the nondecreasing right wing.
        while start<stop:
            mid=(start+stop)//2;self.stats['valley_core_bisection_steps']+=1
            if self.p[mid]<=value:start=mid+1
            else:stop=mid
        return start

    def count_greater(self,i,j,value):
        split=max(i,min(self.bottom,j));lo=i;hi=split
        while lo<hi:
            mid=(lo+hi)//2;self.stats['valley_core_bisection_steps']+=1
            if self.p[mid]>value:lo=mid+1
            else:hi=mid
        return lo-i+j-self.first_greater(split,j,value)

    def cutoff(self,i,j,c):
        t=largest_end_split(self.p,i,j,c,self.bottom,self.stats)
        candidates=[]
        if t:candidates.append(self.p[i+t-1])
        if c-t:candidates.append(self.p[j-(c-t)])
        self.stats['valley_core_cutoff_queries']+=1
        return min(candidates)

    def top_candidates(self,c):
        """Every positive top-c-sum density, without scanning zero cells."""
        assert 1<=c<=self.n
        for i in range(max(0,self.n-c-1)):
            self.stats['valley_core_rows']+=1
            j=i+c+1
            while j<self.n:
                z=self.cutoff(i+1,j,c)
                if z>=self.p[i]:break
                multiplicity=c-self.count_greater(i+1,j,z)
                assert multiplicity>=1
                first=self.first_greater(max(j,self.bottom),self.n,z)
                event=first+multiplicity-1
                if event>=self.n:break
                raised=self.cutoff(i+1,event+1,c)
                density=min(self.p[i],raised)-z
                assert density>0
                self.stats['valley_top_core_outputs']+=1
                yield i,event,density
                j=event+1

    def construct(self):
        self.cores={};self.candidate_counts={}
        h=1;c=1
        while c<=self.n:
            core={};candidate_count=0
            if h>=2:
                for i,j,top_density in self.top_candidates(c):
                    corners=((i,j),(i,j+1),(i+1,j),(i+1,j+1))
                    values=[self.score(h,a,b)[0] for a,b in corners]
                    density=values[0]+values[3]-values[1]-values[2]
                    assert 0<=density<=(h-1)*top_density
                    if density:core[i,j]=density
                    candidate_count+=1
            self.stats['valley_core_outputs']+=len(core)
            self.cores[h]=core;self.candidate_counts[h]=candidate_count
            h+=1;c=2*c+1
        return self.cores
