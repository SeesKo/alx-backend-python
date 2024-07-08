#!/usr/bin/env python3
import asyncio
import time
from typing import List


# Import wait_n using dynamic import
wait_n_module = __import__('1-concurrent_coroutines')
wait_n = wait_n_module.wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measure the total execution time for wait_n(n, max_delay)
    and return the average time per task.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.time()

    total_time = end_time - start_time
    average_time = total_time / n
    return average_time
