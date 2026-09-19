from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.user_service import UserService
from app.auth.jwt_handler import create_token

router = APIRouter()

service = UserService()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    valid = service.authenticate(
        form_data.username,
        form_data.password
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Create JWT payload
    token = create_token(
        {
            "sub": form_data.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }