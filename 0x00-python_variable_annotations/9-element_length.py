#!/usr/bin/env python3
"""
From dynamically typed to strongly typed
"""
from typing import List, Tuple, Union, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Converting statically typed to dynamically typed"""
    return [(i, len(i)) for i in lst]
