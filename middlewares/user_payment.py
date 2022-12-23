from flask import request


def user_payment_middleware(func):
    def wrapper(*args, **kwargs):
        # set values of user type for next middlewares
        request.json['user_type'] = "free"

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
