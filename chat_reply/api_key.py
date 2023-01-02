import os
from firebase_admin import firestore
import requests
from datetime import datetime

db = firestore.client()

api_key_ref = db.collection("api-keys")

DEFAULT_OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")


def load_keys():
    # load api keys from firestore
    doc_snapshots = [item for item in api_key_ref.get()]

    OPEN_AI_API_KEY = [item.to_dict() for item in doc_snapshots]

    return OPEN_AI_API_KEY


def remove_key(key):
    result = api_key_ref.where('key', '==', key).get()
    for item in result:
        item.reference.delete()


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
