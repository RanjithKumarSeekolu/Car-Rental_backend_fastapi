import json

import firebase_admin
from firebase_admin import auth, credentials, firestore

from app.core.config import settings


def _load_credentials() -> credentials.Certificate:
    # Cloud (Railway etc.): full service-account JSON in one env var
    if settings.firebase_service_account_json:
        return credentials.Certificate(json.loads(settings.firebase_service_account_json))
    # Local dev: read from file
    return credentials.Certificate(settings.firebase_credentials_path)


if not firebase_admin._apps:
    bucket = settings.firebase_storage_bucket.removeprefix("gs://")
    options = {"storageBucket": bucket} if bucket else None
    firebase_admin.initialize_app(_load_credentials(), options)

db = firestore.client()
fb_auth = auth