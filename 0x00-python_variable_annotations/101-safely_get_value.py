#!/usr/bin/env python3
"""TypeVar"""


from typing import Mapping, Any, TypeVar, Union


T = TypeVar('T')


def safely_get_value(dct: Mapping,
                     key: Any,
                     default: Union[T, None] = None
                     ) -> Union[Any, T]:
    """TypeVar wierd stuff"""
    if key in dct:
        return dct[key]
    else:
        return defaul
