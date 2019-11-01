import datetime
import functools


def public_handler(func):
    @functools.wraps(func)
    def wrapper(**params):
        params["now"] = datetime.datetime.now()  # send current date to handler and HTML template
        return func(**params)

    return wrapper
