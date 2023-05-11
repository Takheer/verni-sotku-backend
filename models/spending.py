from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, DateTime, String, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base

class Spending(Base):
    __tablename__ = "spendings"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    who_bought_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    who_bought = relationship("User", foreign_keys=[who_bought_id])
    whom_bought_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    whom_bought = relationship("User", foreign_keys=[whom_bought_id])
    sum: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(500))
    calculation_breakdown: Mapped[str] = mapped_column(String(350))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())