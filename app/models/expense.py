from sqlalchemy import ForeignKey, Numeric, String, Date 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Expense(Base):
    __tablename__ = "expenses"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8), default="INR")
    category: Mapped[str] = mapped_column(String(50))
    spent_on: Mapped[Date] = mapped_column(Date, nullable=False)  # ← Date, not str

    note: Mapped[str | None] = mapped_column(String(255), nullable=True)  # ← add this

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="expenses")
    
    