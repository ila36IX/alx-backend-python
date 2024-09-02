#!/usr/bin/env python3
"""
Function `sum_list` which takes a list input_list of floats as argument and
returns their sum as a float.
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Calculating the sum of floats in a list"""
    s: float = 0
    for n in input_list:
        s += n
    return s
