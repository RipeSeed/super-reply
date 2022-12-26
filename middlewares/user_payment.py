from flask import request
from firebase_admin import firestore

db = firestore.client()


def user_payment_middleware(func):
    def wrapper(*args, **kwargs):
        # set values of user type for next middlewares
        request.json['user_type'] = "free"
        user_email = request.json.get("user_email")

        doc = db.collection(
            "users").where("email", "==", user_email).get()

        if doc != None and len(doc) > 0:
            users = doc[0].to_dict()
            request.json['user_type'] = users.get('status', 'free')

        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
