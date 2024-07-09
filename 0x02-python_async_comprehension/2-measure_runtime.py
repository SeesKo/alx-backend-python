#!/usr/bin/env python3
"""
Module defines a coroutine that measures the total runtime of executing
async_comprehension four times in parallel using asyncio.gather.
"""

import asyncio
import time
from typing import List
from time import perf_counter
from importlib import import_module as async_import


async_comprehension = async_import('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Measures the total runtime of executing async_comprehension
    four times in parallel.
    """
    start_time = perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = time.perf_counter()
    return end_time - start_time
