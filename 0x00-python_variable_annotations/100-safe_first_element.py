#!/usr/bin/env python3
"""
list or a dict as an argument only need their argument to be somehow
“list-like” or “dict-like”. A specific meaning of “list-like” or “dict-like”
(or something-else-like) is called a “duck type”
"""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """duck type"""
    if lst:
        return lst[0]
    else:
        return None
