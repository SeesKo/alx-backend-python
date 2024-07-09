#!/usr/bin/env python3
"""
Module defines an asynchronous generator that yields random numbers.
"""

import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """
    Asynchronous generator that yields random
    numbers after 1 second delay.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
