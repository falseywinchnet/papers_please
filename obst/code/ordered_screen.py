#!/usr/bin/env python3
"""Exact arbitrary-fine-weight screening with a dense-core-free coarse oracle."""
from collections import Counter
from coarse_screen import Prepared as GenericPrepared
from ordered_ranges import OrderedRanges


class Prepared(GenericPrepared):
    def __init__(self,p,q,stats=None):
        stats=Counter() if stats is None else stats
        self.ranges=OrderedRanges(p,q,stats)
        self.n=len(p);self.p=tuple(p);self.q=tuple(q);self.mass=sum(p)+sum(q)
        self.coarse_height=self.n.bit_length();self.core=None
        self.value=self.ranges.query(0,self.n,stats)
        self.prefix=[0]
        for a,b in zip(p,q[1:]):self.prefix.append(self.prefix[-1]+a+b)
        stats['screen_coarse_prefix_items']+=self.n
        stats['screen_stored_base_items']+=2*self.n+1
