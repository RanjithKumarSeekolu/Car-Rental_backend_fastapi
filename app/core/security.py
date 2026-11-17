from app.core.firebase import fb_auth

class InvalidTokenError(Exception):
    """Raised when a Firebase ID token is missing, malformed or expired."""

def decode_firebase_token(token: str) -> dict:
    try:
        return fb_auth.verify_id_token(token)
    except Exception as e:
        raise InvalidTokenError(str(e)) from e