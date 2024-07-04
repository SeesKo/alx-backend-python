#!/usr/bin/env python3
"""
Module provides a duck-typed function to safely
return the first element of a sequence.
"""

from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence) -> Union[Any, None]:
    """
    Returns the first element of the sequence if it exists,
    otherwise returns None.
    """
    if lst:
        return lst[0]
    else:
        return None
