from flask import request, make_response
from .time_utils import get_dd_mm_yy, get_mm_yy
from firebase_admin import firestore
from .limits_const import suggestions_limits, word_limits
import os

db = firestore.client()

BYPASS_PAYMENTS = os.environ.get('BYPASS_PAYMENTS', False)


FREE_USER_LIMIT_DAILY = suggestions_limits['FREE_USER_LIMIT_DAILY']
FREE_USER_LIMIT_MONTHLY = suggestions_limits['FREE_USER_LIMIT_MONTHLY']

FREE_USER_WORD_LIMIT = word_limits['FREE_USER_WORD_LIMIT']
PAYED_USER_WORD_LIMIT = word_limits['PAYED_USER_WORD_LIMIT']


def input_limit_middleware(func):
    if BYPASS_PAYMENTS:
        return func

    def wrapper(*args, **kwargs):
        body = request.get_json()
        user_id = body['user_id']
        messages = body['messages']
        user_type = body['user_type']

        body['remaining_suggestions_daily'] = FREE_USER_LIMIT_DAILY
        body['remaining_suggestions_monthly'] = FREE_USER_LIMIT_MONTHLY

        date = get_dd_mm_yy()
        month = get_mm_yy()

        # query usage from firebase
        suggestion_requests_count_doc = db.collection(
            "suggestion_requests_count").document(user_id).get()
        suggestion_requests_count_doc = suggestion_requests_count_doc.to_dict()

        change_tone_requests_count_doc = db.collection(
            "change_tone_requests_count").document(user_id).get()

        change_tone_requests_count_doc = change_tone_requests_count_doc.to_dict()

        # set input limits in request body
        body['suggestion_requests_count_doc'] = suggestion_requests_count_doc
        body['change_tone_requests_count_doc'] = change_tone_requests_count_doc

        if suggestion_requests_count_doc != None and user_type == 'free':
            # set remaining emails
            request.json['remaining_suggestions_daily'] = FREE_USER_LIMIT_DAILY - \
                suggestion_requests_count_doc.get(date, 0)
            request.json['remaining_suggestions_monthly'] = FREE_USER_LIMIT_MONTHLY - \
                suggestion_requests_count_doc.get(month, 0)

        total_words = sum([len(message['message'].split(' '))
                          for message in messages])

        if user_type == 'free' and total_words > FREE_USER_WORD_LIMIT:
            return make_response({
                'error': 'Unlock access to super long email threads with our unlimited plan.',
                'error_code': 'FREE_USER_INPUT_LIMIT'
            }, 403)

        elif user_type == 'unlimited' and total_words > PAYED_USER_WORD_LIMIT:
            return make_response({
                'error': 'Unfortunately, superReply doesn\'t support super long email threads at this time.',
                'error_code': 'INPUT_LIMIT'
            }, 403)

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
