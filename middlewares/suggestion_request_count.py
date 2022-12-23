from flask import request, make_response
from firebase_admin import firestore
from google.cloud.firestore_v1 import Increment
from .time_utils import get_dd_mm_yy, get_mm_yy

db = firestore.client()


def suggestion_request_count_middleware(func):
    def wrapper(*args, **kwargs):
        user_id = request.json['user_id']

        date = get_dd_mm_yy()
        month = get_mm_yy()

        try:
            user_doc_ref = db.collection(
                'suggestion_requests_count').document(user_id)

            user_doc_ref.set({
                date: Increment(1),
                month: Increment(1)
            }, merge=True)
        except Exception:
            return make_response("Internal Server Error ", 500)

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
