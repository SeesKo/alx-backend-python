#!/usr/bin/env python3
"""
Module defines a coroutine that measures the total runtime of executing
async_comprehension four times in parallel using asyncio.gather.
"""

import asyncio
from typing import List
from time import perf_counter
from importlib import import_module as using


async_comprehension = using('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Measures the total runtime of executing async_comprehension
    four times in parallel.
    """
    start_time = perf_counter()

    # Execute async_comprehension four times in parallel using asyncio.gather
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    end_time = perf_counter()
    return end_time - start_time
