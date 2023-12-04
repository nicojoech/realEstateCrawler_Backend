from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models import User
from app.schemas import Token
from app.services.auth import login, get_current_user

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return login(form_data)


# test route to see if a user is logged in
@router.get("/test")
async def test_for_logged_users(current_user: User = Depends(get_current_user)):
    return {"message": "You are authenticated!", "username": current_user.username}
