from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os

# ======================
# CONFIG (from .env)
# ======================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

# ======================
# CREATE TOKEN
# ======================
def create_token(data: dict, expires_minutes: int = None):
    """
    Create JWT token with expiration.
    """

    to_encode = data.copy()

    expire_minutes = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ======================
# VERIFY TOKEN
# ======================
def verify_token(token: str):
    """
    Verify JWT token safely.
    Returns payload if valid, otherwise None.
    """

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None


# ======================
# EXTRACT USER
# ======================
def get_current_user(token: str):
    """
    Convenience wrapper:
    returns user id / subject if token is valid.
    """

    payload = verify_token(token)

    if not payload:
        return None

    return payload.get("sub")