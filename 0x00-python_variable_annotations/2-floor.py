#!/usr/bin/env python3
"""
the floor utility
"""


def floor(n: float) -> int:
    """Get the floor value of a float"""
    if n >= 0:
        return int(n)
    else:
        return int(n) - 1
