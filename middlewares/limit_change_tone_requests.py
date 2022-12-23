from flask import request, make_response
from .time_utils import get_dd_mm_yy
from firebase_admin import firestore

db = firestore.client()

FREE_USER_LIMIT_DAILY = 1


def limit_change_tone_requests_middleware(func):
    def wrapper(*args, **kwargs):
        user_id = request.json['user_id']

        date = get_dd_mm_yy()

        try:
            doc = db.collection(
                "change_tone_requests_count").document(user_id).get()

            doc = doc.to_dict()

            if (doc and doc.get(date) >= FREE_USER_LIMIT_DAILY):
                return make_response({
                    'error': f"Free user can get {FREE_USER_LIMIT_DAILY} change of tone daily"
                }, 403)

        except Exception:
            return make_response("Internal Server Error ", 500)

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
