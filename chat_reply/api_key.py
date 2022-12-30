import os
from firebase_admin import firestore
import requests
from datetime import datetime

db = firestore.client()
batch = db.batch()

api_key_ref = db.collection("api-keys")

KEY_REMOVE_THRESHOLD = os.environ.get("KEY_REMOVE_THRESHOLD", 17.7)
DEFAULT_OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")


def __get_usd(key):
    date = datetime.now()
    return requests.request("GET", f"https://api.openai.com/v1/usage?date={date.strftime('%Y-%m-%d')}",
                            headers={'Authorization': f'Bearer {key}'}).json().get('current_usage_usd')


def load_keys():
    # load api keys from firestore
    doc_snapshots = [item for item in api_key_ref.get()]

    try:
     # remove api keys with usage more than THRESHOLD
        [batch.delete(item.reference) for item in doc_snapshots if item.get(
            'usd_used') >= KEY_REMOVE_THRESHOLD]  # removes from firebase

        doc_snapshots = [item for item in doc_snapshots if item.get(
            'usd_used') < KEY_REMOVE_THRESHOLD]
    except Exception:
        pass

    # update usage on firestore
    [batch.update(item.reference, {"usd_used": __get_usd(item.get('key'))})
     for item in doc_snapshots]

    OPEN_AI_API_KEY = [item.to_dict() for item in doc_snapshots]

    batch.commit()

    return OPEN_AI_API_KEY


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
