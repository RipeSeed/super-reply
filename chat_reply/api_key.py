import os
from firebase_admin import firestore
import time

db = firestore.client()

api_key_ref = db.collection("api-keys")

DEFAULT_OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")


def __current_timestamp():
    return int(time.time())


def __timestamp_before_n_mins(n: int):
    return __current_timestamp()-(n*60)


def load_keys():
    doc_snapshots = [item for item in api_key_ref.get()]

    OPEN_AI_API_KEY = [item for item in [item.to_dict() for item in doc_snapshots] if item.get(
        'timestamp', 0) < __timestamp_before_n_mins(2)]

    return OPEN_AI_API_KEY


def remove_key(key):
    result = api_key_ref.where('key', '==', key).get()
    for item in result:
        item.reference.delete()


def add_timestamp(key):
    result = api_key_ref.where('key', '==', key).get()
    for item in result:
        item.reference.update({"timestamp": __current_timestamp()})


def get_usage():
    doc_snapshots = [item for item in api_key_ref.get()]
    response = [item.to_dict() for item in doc_snapshots]
    response = [
        {
            **item,
            "key": item['key'][:5]+'...'+item['key'][-5:],
        }
        for item in response
    ]
    return response
