from flask import request, make_response
from .time_utils import get_dd_mm_yy, get_mm_yy
from firebase_admin import firestore
from .limits_const import suggestions_limits
import os

db = firestore.client()

FREE_USER_LIMIT_DAILY = suggestions_limits['FREE_USER_LIMIT_DAILY']
FREE_USER_LIMIT_MONTHLY = suggestions_limits['FREE_USER_LIMIT_MONTHLY']

BYPASS_PAYMENTS = os.environ.get('BYPASS_PAYMENTS', False)


def limit_suggestion_requests_middleware(func):
    if BYPASS_PAYMENTS:
        return func

    def wrapper(*args, **kwargs):
        user_id = request.json['user_id']
        user_type = request.json['user_type']

        date = get_dd_mm_yy()
        month = get_mm_yy()

        try:
            doc = db.collection(
                "suggestion_requests_count").document(user_id).get()

            doc = doc.to_dict()

            if doc != None and user_type == 'free':
                if doc.get(date) != None and (doc.get(date) >= FREE_USER_LIMIT_DAILY):
                    return make_response({
                        "error": f"Free user can get {FREE_USER_LIMIT_DAILY} reply suggestions daily",
                        'error_code': 'FREE_USER_SUGGESTION_LIMIT_DAILY'
                    }, 403)
                elif doc.get(month) != None and (doc.get(month) >= FREE_USER_LIMIT_MONTHLY):
                    return make_response({
                        "error": f"Free user can get {FREE_USER_LIMIT_MONTHLY} reply suggestions monthly",
                        'error_code': 'FREE_USER_SUGGESTION_LIMIT_MONTHLY'
                    }, 403)

        except Exception:
            return make_response("Internal Server Error", 500)

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
