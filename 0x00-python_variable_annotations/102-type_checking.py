#!/usr/bin/env python3
"""
Module provides a type-annotated function to zoom in an array.
"""


from typing import Tuple, List, Any


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Zooms into an array by repeating each item according to the factor.
    """
    zoomed_in = [item for item in lst for _ in range(factor)]
    return zoomed_in
