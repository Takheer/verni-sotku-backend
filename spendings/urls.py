from typing import List

from fastapi import APIRouter

from db import SessionDep
from spendings import Spending
from spendings.crud import get_group_spendings, create_spending
from spendings.schema import SpendingSchema, SpendingSchemaCreate

router = APIRouter(prefix="/spendings", tags=["spendings"])


@router.get("/{group_slug}", response_model=List[SpendingSchema])
async def get_group_spendings_url(group_slug: str, session: SessionDep):
    return get_group_spendings(group_slug, session)


@router.post("", response_model=SpendingSchema)
async def add_group_spending_url(spending: SpendingSchemaCreate, session: SessionDep):
    return create_spending(spending, session)
