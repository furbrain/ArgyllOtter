import asyncio
import concurrent.futures
import functools
import logging

import numpy as np

pool = concurrent.futures.ProcessPoolExecutor(max_workers=8)


def logged(func):
    @functools.wraps(func)
    def log_this(*args, **kwargs):
        items = [str(x) for x in args]
        items += ["%s=%s" % (x, str(y)) for x, y in kwargs.items()]
        logging.info("Calling %s(%s)", func.__name__, ', '.join(items))
        return func(*args, **kwargs)

    return log_this


def start_task(coro):
    return asyncio.ensure_future(coro)


def spawn(func, *args):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(pool, func, *args)


def get_coeffs(bearing):
    radians = np.deg2rad(bearing)
    return np.array((np.sin(radians), np.cos(radians)))
