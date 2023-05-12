from db import get_db_connection, get_sa_connection
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User, users_groups, Group

def create_user(uuid, name, email):
    with Session(get_sa_connection()) as session:
        user = User(
            uuid=uuid,
            name=name,
            email=email,
        )
        session.add(user)
        session.commit()

    return []

def get_users():
    session = Session(get_sa_connection())
    stmt = select(User)

    users = []
    for u in session.scalars(stmt):
        users.append(u.to_json())

    return users

def get_user_by_uuid(uuid):
    with Session(get_sa_connection()) as session:
        stmt = select(User).join(users_groups).join(Group).where(User.uuid == uuid)
        groups_stmt = select(Group).join(users_groups).join(User).where(User.uuid == uuid)
        all_groups = session.scalars(groups_stmt).all()
        user = session.scalars(stmt).all()[0]
        print(user.groups)

        serialized_user = user.to_json()
        serialized_user['groups'] = [g.to_json() for g in user.groups]

        return serialized_user
