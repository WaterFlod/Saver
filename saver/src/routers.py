from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import uuid

from database import get_session
from schemas import Expense
from models import ExpenseModel
from schemas import ExpenseDTO

router_user = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_expenses(session) -> list: #return all appointments in DB
    result = await session.execute(select(ExpenseModel))
    expenses = result.scalars().all()
    return expenses


@router_user.get("/expenses/{expense_id}", response_model=Expense)
async def read_expense(session: SessionDep, expense_id: int):
    expenses = await get_expenses(session)
    result_dto = [ExpenseDTO.model_validate(row, from_attributes=True) for row in expenses]
    for expense in result_dto:
        if expense.id == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")


@router_user.get("/expenses", response_model=Expense)
async def read_all_expenses(session:SessionDep):
    expenses = await get_expenses(session)
    json = {}
    for expense in expenses:
        json[expense.id] = [expense.amount, expense.description]
    return JSONResponse(content=json, status_code=200)

@router_user.post("/expenses", response_model=Expense)
async def create_expense(session: SessionDep, data:Expense):
    new_expense = ExpenseModel(
        amount = data.amount,
        description = data.description,
    )
    session.add(new_expense)
    await session.commit()
    return JSONResponse(content={"detail": "Expense added successfully"}, status_code=200)