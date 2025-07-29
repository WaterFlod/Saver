from fastapi import APIRouter, HTTPException

from main import db

from .schemas import Expense

user = APIRouter("/")


@user.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    if expense_id in db:
        expense = db[expense_id]
        return expense
    raise HTTPException(status_code=404, detail="Expense not found")


@user.get("/expenses", response_model=Expense)
def get_all_expenses():
    return db


@user.post("/expenses", response_model=Expense)
def create_expense(data:Expense):
    db[data.id] = data
    return data