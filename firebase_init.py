import firebase_admin

cred = firebase_admin.credentials.Certificate(
    f"serviceAccountKey.json")
firebase_admin.initialize_app(cred)
