import firebase_admin
from firebase_admin import auth, credentials
from flask import request

cred = credentials.Certificate(f"middlewares/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def firebase_auth_middleware(func):
    def wrapper(*args, **kwargs):
        # Get the ID token sent by the client
        id_token = request.headers.get('Authorization')
        # Verify the ID token and get the corresponding user
        try:
            decoded_token = auth.verify_id_token(id_token)
            auth.get_user(decoded_token['uid'])
        except Exception as e:
            # Respond with an error if the ID token is invalid or has expired
            return 'Unauthorized', 401
        # Call the original view function
        return func(*args, **kwargs)
    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
