import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Mapped


class UserSchemaCreate(BaseModel):
    name: str
    email: str


class UserSchemaFlat(UserSchemaCreate):
    id: int
    uuid: str
    registration_date: datetime.datetime


class UserSchema(UserSchemaFlat):
    groups: List["GroupSchema"]


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserTokenData(BaseModel):
    email_or_phone: str | None = None


class GroupSchemaCreate(BaseModel):
    slug: str
    name: str
    creator_id: int
    users_ids: Optional[List[int]] = None


class GroupSchema(GroupSchemaCreate):
    id: int
    created_at: datetime.datetime
    creator_id: int
    creator: UserSchemaFlat
    users: Optional[List[UserSchemaFlat]]
    # spendings: Optional[List[Spending]]
