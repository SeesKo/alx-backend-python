#!/usr/bin/env python3
"""
Module defines a coroutine that collects random numbers
using async comprehension over async_generator.
"""

import asyncio
from typing import List
from importlib import import_module as async_import


async_generator = async_import('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Asynchronously collects 10 random numbers using async comprehension.
    """
    return [num async for num in async_generator()]
