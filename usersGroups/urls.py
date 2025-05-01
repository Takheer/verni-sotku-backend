from datetime import timedelta
import random
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from db import SessionDep
from . import User
from .crud import create_user, send_email, create_otp, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, validate_user, get_user_by_uuid
from .schema import UserSchemaFlat, UserSchemaCreate, UserToken, UserSchema

user_router = APIRouter(prefix="/user", tags=["user"])
group_router = APIRouter(prefix="/group", tags=["group"])


@user_router.post("", response_model=List[UserSchemaFlat])
async def create_user_url(email: str, name: str, session: SessionDep):
    user = create_user(UserSchemaCreate(email=email, full_name=name, phone="none"), session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user


@user_router.get("/send-email/{email}", response_model=UserSchemaFlat)
async def send_email_url(email: str, session_dep: SessionDep):
    code = random.randint(1000, 9999)
    await send_email(email, code)
    return create_otp(email, code, session_dep)


@user_router.post("/auth")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep
) -> UserToken:
    try:
        user = validate_user(form_data.username, form_data.password, session)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return UserToken(access_token=access_token, token_type="bearer")


@user_router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@user_router.get("/{user_uuid}", response_model=UserSchema)
async def get_user_url(user_uuid: str, session: SessionDep):
    user = get_user_by_uuid(user_uuid, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
