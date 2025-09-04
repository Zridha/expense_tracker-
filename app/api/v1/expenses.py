# app/api/v1/expenses.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.schemas.expense import ExpenseCreate, ExpenseOut
from app.models.expense import Expense
from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseOut)
async def create_expense(
    payload: ExpenseCreate,
    session: AsyncSession = Depends(get_session),  # Fixed: Use get_session instead of oauth2_scheme
    user: User = Depends(get_current_user)
):
    exp = Expense(**payload.model_dump(), owner_id=user.id)
    session.add(exp)
    await session.commit()
    await session.refresh(exp)
    return exp

@router.get("/", response_model=list[ExpenseOut])
async def list_expenses(
    session: AsyncSession = Depends(get_session),  # Fixed: Use get_session instead of oauth2_scheme
    user: User = Depends(get_current_user)
):
    q = select(Expense).where(Expense.owner_id == user.id).order_by(Expense.spent_on.desc())
    res = await session.execute(q)
    return list(res.scalars().all())

@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    session: AsyncSession = Depends(get_session),  # Fixed: Use get_session instead of oauth2_scheme
    user: User = Depends(get_current_user)
):
    q = delete(Expense).where(Expense.id == expense_id, Expense.owner_id == user.id)
    res = await session.execute(q)
    await session.commit()
    if res.rowcount == 0:
        raise HTTPException(404, detail="Not found")
    return {"ok": True}