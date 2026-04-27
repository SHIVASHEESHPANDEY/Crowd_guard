import time
from collections.abc import Awaitable, Callable


async def enforce_max_response_time(
    operation: Callable[[], Awaitable[object]],
    seconds: float = 5.0,
) -> object:
    start = time.perf_counter()
    result = await operation()
    elapsed = time.perf_counter() - start
    if elapsed > seconds:
        raise TimeoutError(f"Response exceeded {seconds} seconds")
    return result
