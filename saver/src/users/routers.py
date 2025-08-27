from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from users.schemas import Expense
from models import ExpenseModel
from users.dao import ExpenseDAO

router_user = APIRouter()


@router_user.get("/expenses/{expense_id}", response_model=Expense, summary="Get expense by id")
async def read_expense(expense_id: int):
    try:
        expense = await ExpenseDAO.find_expense_by_id(expense_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expense not found")
    else:
        return expense
    


@router_user.get("/expenses", summary="Get all expenses")
async def get_all_expenses():
    return await ExpenseDAO.find_all_expenses()


@router_user.post("/expenses", summary="Add expense")
async def add_expense(data:Expense):
    new_expense = ExpenseModel(
        amount = data.amount,
        description = data.description,
    )
    try:
        await ExpenseDAO.create_expense(new_expense)
    except Exception as e:
        raise HTTPException(status_code=501, detail=e)
    else:
        return JSONResponse(content={"detail": "Expense added successfully"}, status_code=200)


@router_user.delete("/expenses", summary="Delete expense by id")
async def remove_expense(id: int):
    try:
        await ExpenseDAO.delete_expense(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expense not found")
    else:
        return JSONResponse(content={"detail":"Expense deleted successfully"}, status_code=200)


@router_user.update("/expenses", summary="Update expense by id")
async def update_expense(id: int, new_amount: int = None, new_description: str = None):
    try:
        await ExpenseDAO.update_expense(id, new_amount=new_amount, new_description=new_description)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expense not found")
    else:
        return JSONResponse(content={"detail":"Expense update successfully"}, status_code=200)
    
    