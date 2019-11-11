import functools
import logging
def logged(func):
    @functools.wraps(func)
    def log_this(*args, **kwargs):
        items = [str(x) for x in args]
        items += ["%s=%s" % (x, str(y)) for x, y in kwargs.items()]
        logging.debug("Calling %s(%s)",func.__name__, ', '.join(items))
        return func(*args, **kwargs)
    return log_this
