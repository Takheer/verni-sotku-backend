import datetime
from typing import List, Optional

from pydantic import BaseModel


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
    users: Optional[List[UserSchemaFlat]] = None


class GroupSchemaFlat(GroupSchemaCreate):
    id: int
    created_at: datetime.datetime
    creator_id: int
    creator: UserSchemaFlat


class GroupSchema(GroupSchemaFlat):
    users: Optional[List[UserSchemaFlat]]
