from db import get_db_connection, get_sa_connection
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User

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
        stmt = select(User).where(User.uuid == uuid)
        for row in session.execute(stmt):
            return row[0].to_json()
