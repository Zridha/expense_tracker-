# app/api/v1/reports.py
from fastapi import APIRouter, Depends, Response, BackgroundTasks, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from pathlib import Path
from uuid import uuid4
from decimal import Decimal
from typing import Dict, Any, List

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.expense import Expense
from app.services.reporting import save_report_files

router = APIRouter(prefix="/reports", tags=["reports"])

REPORTS_DIR = Path("data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
_REPORTS_ROOT = REPORTS_DIR.resolve()  # for security checks


def _to_float(x):
    # SQLAlchemy Numeric -> Decimal; convert cleanly
    return float(x) if isinstance(x, (Decimal, int, float)) else float(str(x))


@router.get("/monthly-summary")
async def monthly_summary(
    year: int = Query(..., ge=1),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    date_col = cast(Expense.spent_on, Date)

    q = (
        select(
            Expense.category,
            func.sum(Expense.amount).label("total"),
        )
        .where(
            Expense.owner_id == user.id,
            func.extract("year", date_col) == year,
            func.extract("month", date_col) == month,
        )
        .group_by(Expense.category)
    )
    res = await session.execute(q)
    rows = res.all()

    by_category = {cat: _to_float(total) for cat, total in rows}
    return {"year": year, "month": month, "by_category": by_category}


@router.post("/generate-monthly-report-background")
async def generate_monthly_report_background(
    year: int = Query(..., ge=1),
    month: int = Query(..., ge=1, le=12),
    background_tasks: BackgroundTasks = None,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    date_col = cast(Expense.spent_on, Date)

    q = (
        select(
            Expense.spent_on,
            Expense.amount,
            Expense.currency,
            Expense.category,
            Expense.note,
        )
        .where(
            Expense.owner_id == user.id,
            func.extract("year", date_col) == year,
            func.extract("month", date_col) == month,
        )
        .order_by(date_col.asc())
    )
    res = await session.execute(q)
    rows = res.all()

    payload: List[Dict[str, Any]] = [
        {
            "spent_on": (r[0].isoformat() if hasattr(r[0], "isoformat") else str(r[0])),
            "amount": _to_float(r[1]),
            "currency": r[2],
            "category": r[3],
            "note": r[4],
        }
        for r in rows
    ]

    if not payload:
        raise HTTPException(404, detail="No expenses for the requested month")

    uid = uuid4().hex
    csv_path = REPORTS_DIR / f"{user.id}_{year}_{month:02d}_{uid}.csv"
    pdf_path = REPORTS_DIR / f"{user.id}_{year}_{month:02d}_{uid}.pdf"
    title = f"Expenses-{year}-{month:02d}-{user.id}"

    background_tasks.add_task(
        save_report_files,
        payload,
        title,
        str(csv_path),
        str(pdf_path),
    )

    return {
        "task_id": uid,
        "csv": str(csv_path),
        "pdf": str(pdf_path),
        "message": "Report generation scheduled",
    }


@router.get("/download-report")
async def download_report(path: str):
    """
    Very important: lock downloads to data/reports and prevent path traversal.
    """
    p = Path(path)
    # Resolve and ensure it's inside REPORTS_DIR
    try:
        resolved = p.resolve(strict=True)
    except FileNotFoundError:
        raise HTTPException(404, detail="File not found")

    if _REPORTS_ROOT not in resolved.parents and resolved != _REPORTS_ROOT:
        raise HTTPException(400, detail="Invalid path")

    data = resolved.read_bytes()
    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={resolved.name}"},
    )
