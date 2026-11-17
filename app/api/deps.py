from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.firebase import db
from app.core.security import InvalidTokenError, decode_firebase_token
from app.schemas.auth import TokenUser

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> TokenUser:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No token provided")
    try:
        decoded = decode_firebase_token(credentials.credentials)
    except InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    return TokenUser(
        uid=decoded["uid"],
        email=decoded.get("email"),
        role=decoded.get("role", "renter"),
    )


def require_admin(
    user: Annotated[TokenUser, Depends(get_current_user)],
) -> TokenUser:
    doc = db.collection("users").document(user.uid).get()
    role = (doc.to_dict() or {}).get("role") if doc.exists else user.role
    if role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required")
    return user.model_copy(update={"role": role})


CurrentUser = Annotated[TokenUser, Depends(get_current_user)]
AdminUser = Annotated[TokenUser, Depends(require_admin)]