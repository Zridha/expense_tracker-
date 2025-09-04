import time 
from functools import wraps

def timeit(fn):
    @wraps(fn)
    async def _inner(*args, **kwargs):
        start = time.perf_counter()
        result = await fn(*args, **kwargs)
        dur = (time.perf_counter() - start) * 1000
        print(f"{fn.__name__} took {dur:.2f} ms")
        return result 
    return _inner
