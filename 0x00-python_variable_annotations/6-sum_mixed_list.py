#!/usr/bin/env python3
"""
Sum of floats
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """sum of floats and ints"""
    s: float = 0
    for n in mxd_lst:
        s += n
    return s
