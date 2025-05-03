import uuid
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

import aiohttp

from db import SessionDep
from spendings.models import Spending
from usersGroups.models import User, Group
import sqlalchemy as sa

from usersGroups.schema import UserSchemaCreate, UserTokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth")

SECRET_KEY = os.getenv("AUTH_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*30


def create_user(user: UserSchemaCreate, session: SessionDep):
    print('user', user)
    try:
        db_user = User(
            email=user.email,
            name=user.name,
            uuid=str(uuid.uuid4()),
            registration_date=datetime.now()
        )
        session.add(db_user)
        session.commit()
        print('db_user', db_user)
        return db_user
    except:
        return None


def create_otp(email_or_password: str, code, session: SessionDep):
    user = find_user_by_email_or_phone(email_or_password, session)
    if user is None:
        raise Exception('User not found')

    user.last_otp_password = pwd_context.hash(str(code))
    session.commit()

    return user


def validate_user(email_or_phone: str, otp: str, session: SessionDep):
    user = find_user_by_email_or_phone(email_or_phone, session)

    if not user:
        raise Exception('User not found')

    if not pwd_context.verify(otp, user.last_otp_password):
        raise Exception('Invalid otp')

    return user


def find_user_by_email_or_phone(credential: str, session: SessionDep):
    return session.query(User).filter(User.email == credential).first()


def get_user_by_uuid(user_uuid: str, session: SessionDep):
    return session.query(User).filter(User.uuid == user_uuid).first()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_or_phone = payload.get("sub")
        if email_or_phone is None:
            raise credentials_exception
        token_data = UserTokenData(email_or_phone=email_or_phone)
    except InvalidTokenError:
        raise credentials_exception
    user = find_user_by_email_or_phone(token_data.email_or_phone, session)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print('to_encode', to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def send_email(email: str, code: int):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "X-API-KEY": os.environ['UNISENDER_API_TOKEN']
        }

        request_body = {
            "message": {
                "recipients": [
                    {
                        "email": email,
                        "substitutions": {
                            "code": code,
                        }
                    }
                ],
                "body": {
                    "plaintext": "Введите код {{code}} для входа в личный кабинет Verni Sotku",
                },
                "subject": "Insola.design — одноразовый код для входа",
                "from_email": "info@insola.tech",
                "from_name": "Insola.design"
            }
        }

        async with session.post('https://go1.unisender.ru/ru/transactional/api/v1/email/send.json', headers=headers, json=request_body) as response:
            html = await response.json()
            print(html)
            if html['status'] == 'error':
                raise Exception(html['message'])

            return html


def get_group(group_slug: str, session: SessionDep):
    return session.query(Group).join(Spending).order_by(Spending.created_at.desc()).filter(Group.slug == group_slug).one_or_none()


def add_user_to_group(user: User, slug: str, session: SessionDep):
    group = session.query(Group).join(Spending).filter(Group.slug == slug).one_or_none()
    group.users.append(user)
    session.commit()
    return group
