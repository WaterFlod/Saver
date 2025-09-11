from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from users.schemas import ExpenseSchema, UserRegisterSchema, UserAuthSchema
from models import ExpenseModel, UserModel
from users.dao import ExpenseDAO, UserDAO
from users.auth import get_hash_password, authenticate_user, create_access_token, check_current_user


router_auth = APIRouter(prefix="/auth", tags=["Auth"])

router_user = APIRouter(tags=["CRUD operations"])

check = Depends(check_current_user)


@router_auth.post("/register")
async def register_user(user_data:UserRegisterSchema):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user is already registered"
        )
    new_user = UserModel(
        username = user_data.username,
        email = user_data.email,
        password = get_hash_password(user_data.password)
    )
    await UserDAO.add(new_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content="You have successfully registered")


@router_auth.post("/login")
async def auth_user(response:Response, user_data:UserAuthSchema):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router_auth.post("/logout")
async def logout_user(response:Response):
    response.delete_cookie(key="user_access_token")
    return {"message": "The user has successfully logged out"}


@router_user.get("/info", summary="Get user info")
async def get_user_info(user_data: UserModel = check):
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "count expenses": user_data.count_expenses
        }
        
    return user


@router_user.get("/expenses/{expense_id}", response_model=ExpenseSchema, summary="Get expense by id")
async def read_expense(expense_id:int, user_data: UserModel = check):
    try:
        expense = await ExpenseDAO.find_by_id(expense_id=expense_id, user_id=user_data.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expense not found")
    else:
        return expense


@router_user.get("/expenses", summary="Get all expenses")
async def get_all_expenses(user_data: UserModel = check):
    expenses_data = await ExpenseDAO.find_all(user_id=user_data.id)
    expenses = dict()
    for expense in expenses_data:
        expenses[expense.id] = [{"expense_id": expense.expense_id, "amount": expense.amount, "description": expense.description}]
    return expenses


@router_user.post("/expenses", summary="Add expense")
async def add_expense(data:ExpenseSchema, user_data: UserModel = check):
    new_expense = ExpenseModel(
        expense_id = (user_data.count_expenses + 1),
        user_id = user_data.id,
        amount = data.amount,
        description = data.description,
    )
    
    try:
        await ExpenseDAO.create(new_expense)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=e)

    try:
        await UserDAO.update(user_id=user_data.id, new_count_expenses=(user_data.count_expenses + 1))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=e)
    
    return JSONResponse(content={"detail": "Expense added successfully"}, status_code=200)


@router_user.delete("/expenses", summary="Delete expense by id")
async def delete_expense(expense_id: int, user_data: UserModel = check):
    try:
        await ExpenseDAO.delete(expense_id=expense_id, user_id=user_data.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expense not found")
    else:
        return JSONResponse(content={"detail":"Expense deleted successfully"}, status_code=200)


@router_user.put("/expenses", summary="Update expense by id")
async def update_expense(expense_id: int, new_amount: Optional[int] = None, new_description: Optional[str] = None, user_data: UserModel = check):
    try:
        await ExpenseDAO.update_expense(expense_id=expense_id, user_id=user_data.id, new_amount=new_amount, new_description=new_description)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Expense not found")
    else:
        return JSONResponse(content={"detail":"Expense update successfully"}, status_code=200)
    
    