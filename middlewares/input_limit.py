from flask import request, make_response
import os

BYPASS_PAYMENTS = os.environ.get('BYPASS_PAYMENTS', False)


def input_limit_middleware(func):
    if BYPASS_PAYMENTS:
        return func

    def wrapper(*args, **kwargs):
        body = request.get_json()
        messages = body['messages']

        user_type = body['user_type']

        total_words = sum([len(message['message'].split(' '))
                          for message in messages])

        if user_type == 'free' and total_words > 1000:
            return make_response({
                'error': 'Unlock access to super long email threads with our unlimited plan.'
            }, 403)

        elif user_type == 'unlimited' and total_words > 5000:
            return make_response({
                'error': 'Unfortunately, superReply is unable to process super long email threads at this time.'
            }, 403)

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
