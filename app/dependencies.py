from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.services.chat_service import ChatService
from app.auth.jwt_handler import verify_token


chat_service = ChatService()


def get_chat_service():
    return chat_service


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    username = verify_token(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return username