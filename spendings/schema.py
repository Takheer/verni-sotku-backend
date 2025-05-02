from datetime import datetime

from pydantic import BaseModel


class UserSchemaFlat(BaseModel):
    name: str
    email: str
    id: int
    uuid: str
    registration_date: datetime


class SpendingSchemaCreate(BaseModel):
    group_id: int
    who_bought_id: int
    whom_bought_id: int
    sum: int
    comment: str
    calculation_breakdown: str


class SpendingSchema(SpendingSchemaCreate):
    id: int
    who_bought: UserSchemaFlat
    whom_bought: UserSchemaFlat
    created_at: datetime
