#!/usr/bin/env python3
"""
Module provides a type-annotated function
to sum a list of integers and floats.
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Returns the sum of a list containing integers and floats.
    """
    return sum(mxd_lst)
