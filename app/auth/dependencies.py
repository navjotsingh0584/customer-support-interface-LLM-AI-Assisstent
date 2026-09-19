from fastapi import Depends, HTTPException, Header
from app.auth.jwt_handler import verify_token


def get_token(authorization: str = Header(None)):
    if not authorization:
        return None

    if authorization.startswith("Bearer "):
        return authorization.split(" ")[1]

    return authorization


def get_current_user(token: str = Depends(get_token)):
    """
    NEVER crash request.
    If token invalid → fallback user.
    """

    user = verify_token(token)

    if user:
        return user

    # DEV MODE fallback (prevents 500 errors)
    return "dev-user"