#!/usr/bin/env python3
"""
the floor utility
"""


def floor(n: float) -> int:
    if n >= 0:
        return int(n)
    else:
        return int(n) - 1
