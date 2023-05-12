from __future__ import annotations

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, DateTime, String, func, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base
from .spending import Spending

users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(350))
    name: Mapped[str] = mapped_column(String(350))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped[User] = relationship("User", foreign_keys=[creator_id])
    users: Mapped[List[User]] = relationship(
        secondary=users_groups, back_populates="groups"
    )
    spendings: Mapped[List[Spending]] = relationship()

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, name={self.name!r}, slug={self.slug!r})"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(350))
    email: Mapped[str] = mapped_column(String(350))
    registration_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    groups: Mapped[List[Group]] = relationship(
        secondary=users_groups, back_populates="users"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"