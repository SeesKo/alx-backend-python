#!/usr/bin/env python3
"""
Module provides a type-annotated function to
safely retrieve a value from a dictionary.
"""

from typing import Mapping, Any, TypeVar, Union

# Define a generic type variable ~T
T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[T, Any]:
    """
    Safely retrieves a value from a dictionary.
    """
    if key in dct:
        return dct[key]
    else:
        return default
