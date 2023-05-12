from db import get_sa_connection
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Group, User, users_groups, Spending

import uuid

def create_group(name, created_user_uuid):
    with Session(get_sa_connection()) as session:
        user_stmt = select(User).where(User.uuid == created_user_uuid)
        user = session.scalars(user_stmt).all()[0]

        group = Group(
            name=name,
            slug=str(uuid.uuid4()).split('-')[0],
        )
        group.creator = user
        group.users.append(user)
        session.add(group)
        session.commit()

    return []


def get_all_groups():
    with Session(get_sa_connection()) as session:
        stmt = select(Group)

        groups = []
        for g in session.scalars(stmt):
            groups.append(g.to_json())

        return groups


def get_all_user_groups(uuid):
    with Session(get_sa_connection()) as session:
        stmt = select(Group).join(users_groups).join(User).where(User.uuid == uuid)
        all = session.scalars(stmt).all()
        print(all)

        groups = []
        for g in session.scalars(stmt):
            groups.append(g.to_json())

        return groups


def get_group_by_slug(slug):
    with Session(get_sa_connection()) as session:
        stmt = select(Group) \
            .join(users_groups) \
            .join(User) \
            .outerjoin(Spending, Spending.group_id == Group.id) \
            .where(Group.slug == slug)
        group = session.scalars(stmt).all()[0]
        print(group)

        serialized_group = group.to_json()
        serialized_group['spendings'] = [s.to_json() for s in group.spendings]
        serialized_group['creator'] = group.creator.to_json()
        serialized_group['users'] = [u.to_json() for u in group.users]

        return serialized_group
