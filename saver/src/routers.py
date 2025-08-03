from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from database import get_session
from schemas import Expense
from models import ExpenseModel
from utils import get_expenses

router_user = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]

db = {
    0: {"id": 0, "amount": 110, "description": "Cola"},
}

@router_user.get("/expenses/{expense_id}", response_model=Expense)
async def read_expense(session: SessionDep, expense_id: int):
    expenses = await get_expenses(session)
    for expense in expenses:
        if expense.id == id:
            return expenses
    raise HTTPException(status_code=404, detail="Expense not found")


@router_user.get("/expenses", response_model=Expense)
async def read_all_expenses(session:SessionDep):
    expenses = await get_expenses(session)
    return expenses

@router_user.post("/expenses", response_model=Expense)
async def create_expense(session: SessionDep, data:Expense):
    new_expense = ExpenseModel(
        id = 0,
        amount = data.amount,
        description = data.description,
    )
    session.add(new_expense)
    await session.commit()
    return {"access": "True", "detail": "Expense added successfully"}