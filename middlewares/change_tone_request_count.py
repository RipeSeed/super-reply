from flask import request, make_response
from firebase_admin import firestore, auth
from google.cloud.firestore_v1 import Increment
from .time_utils import get_dd_mm_yy, get_mm_yy

db = firestore.client()


def change_tone_request_count_middleware(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        user = auth.verify_id_token(token)

        user_id = user['user_id']
        date = get_dd_mm_yy()
        month = get_mm_yy()

        try:
            user_doc_ref = db.collection(
                'change_tone_request_count').document(user_id)

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
