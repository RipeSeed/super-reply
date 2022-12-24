from firebase_admin import auth
from flask import request, make_response


def firebase_auth_middleware(func):
    def wrapper(*args, **kwargs):
        # Get the ID token sent by the client
        id_token = request.headers.get('Authorization')
        # Verify the ID token and get the corresponding user
        try:
            user = auth.verify_id_token(id_token)
            user_id = user['user_id']
            request.json['user_id'] = user_id
            auth.get_user(user['uid'])
        except Exception:
            # Respond with an error if the ID token is invalid or has expired
            return make_response('Unauthorized', 401)
        # Call the original view function
        return func(*args, **kwargs)
    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
