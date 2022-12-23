from flask import request, make_response


def request_count_middleware(func):
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
