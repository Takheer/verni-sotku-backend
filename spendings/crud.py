from db import SessionDep
from spendings import Spending
from spendings.schema import SpendingSchemaCreate
from usersGroups import Group


def create_spending(spending: SpendingSchemaCreate, session: SessionDep):
    db_spending = Spending(**spending.model_dump())
    session.add(db_spending)
    session.commit()

    return db_spending


def get_group_spendings(group_slug: str, session: SessionDep):
    return session.query(Spending).order_by(Spending.created_at.desc()).join(Group).filter_by(slug=group_slug).all()
