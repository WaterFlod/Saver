from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from users.schemas import Expense
from models import ExpenseModel
from users.schemas import ExpenseDTO
from users.dao import ExpenseDAO

router_user = APIRouter()




@router_user.get("/expenses/{expense_id}", response_model=Expense)
async def read_expense(expense_id: int):
    expenses = await ExpenseDAO.find_all_expenses()
    result_dto = [ExpenseDTO.model_validate(row, from_attributes=True) for row in expenses]
    for expense in result_dto:
        if expense.id == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")


@router_user.get("/expenses", summary="Получить все расходы")
async def get_all_expenses():
    return await ExpenseDAO.find_all_expenses()


@router_user.post("/expenses")
async def add_expense(data:Expense):
    new_expense = ExpenseModel(
        amount = data.amount,
        description = data.description,
    )
    try:
        ExpenseDAO.create_expense(new_expense)
    except Exception as e:
        raise HTTPException(status_code=501, detail=e)
    else:
        return JSONResponse(content={"detail": "Expense added successfully"}, status_code=200)