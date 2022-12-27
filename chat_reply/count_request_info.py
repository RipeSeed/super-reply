from firebase_admin import firestore
from google.cloud.firestore import Increment

db = firestore.client()


def __update_users(email, updates):
    doc = db.collection(
        "users").where('email', "==", email).get()

    user_ref = doc[0].reference
    user_ref.update(updates)


def update_request_info(email, email_count_update: int, words_sent=0, words_recieved=0, change_of_tone=0):
    __update_users(email, {
        "email_count": Increment(email_count_update),
        "words_sent": Increment(words_sent),
        "words_recieved": Increment(words_recieved),
        "change_of_tone": Increment(change_of_tone)
    })
