from __future__ import annotations

import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, DateTime, String, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from spendings import Spending

users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("group_id", ForeignKey("group.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped[User] = relationship("User", foreign_keys=[creator_id])
    users: Mapped[List[User]] = relationship(
        secondary=users_groups, back_populates="groups"
    )
    spendings: Mapped[List[Spending]] = relationship()

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, name={self.name!r}, slug={self.slug!r})"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    last_otp_password: Mapped[Optional[str]] = None
    groups: Mapped[List[Group]] = relationship(
        secondary=users_groups, back_populates="users"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"