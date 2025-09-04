# app/schemas/expense.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float = Field(gt=0)
    currency: str = "INR"
    category: str
    spent_on: date
    note: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id: int
    owner_id: int  # Add this field

    class Config:
        from_attributes = True