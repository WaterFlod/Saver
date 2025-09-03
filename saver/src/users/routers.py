from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from users.schemas import ExpenseSchema, UserRegisterSchema
from models import ExpenseModel
from users.dao import ExpenseDAO, UserDAO
from users.auth import get_hash_password

router_auth = APIRouter(prefix="/auth", tags=["Auth"])

router_user = APIRouter()


@router_auth.post("/register")
async def register_user(user_data:UserRegisterSchema):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user is already registered"
        )
    user_dict = user_data.dict()
    user_dict["password"] = get_hash_password(user_data.password)
    await UserDAO.add(**user_dict)
    return JSONResponse(status_code=status.HTTP_200_OK, content="You have successfully registered")
    pass


@router_user.get("/expenses/{expense_id}", response_model=ExpenseSchema, summary="Get expense by id")
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
async def add_expense(data:ExpenseSchema):
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
    
    