import sys 
sys.path.append("/saver")

from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound
from pydantic import EmailStr
from typing import Optional

from src.models import ExpenseModel, UserModel
from src.database import connection


class UserDAO:
    @classmethod
    @connection
    async def find_one_or_none(cls, session, email: Optional[EmailStr] = None, id: Optional[int] = None):
        if email:
            query = select(UserModel).where(UserModel.email == email)
        
        if id:
            query = select(UserModel).where(UserModel.id == id)
        
        user = await session.execute(query)
        try:
            return user.scalars().one()
        except NoResultFound as e:
            return None
        
    
    @classmethod 
    @connection
    async def add(cls, user_data, session):
        try:
            session.add(user_data)
        except Exception as e:
            await session.rollback()
            raise e
        else:                
            await session.commit()
    

    @classmethod
    @connection
    async def update(cls, user_id, session, new_count_expenses: Optional[int] = None):
        if new_count_expenses:
            query = update(UserModel).where(UserModel.id == user_id).values(count_expenses = new_count_expenses)
        try:
            await session.execute(query)
        except Exception as e:
            await session.rollback()
            raise e
        else:
            await session.commit()
        
            
class ExpenseDAO:
    @classmethod
    @connection
    async def find_by_id(cls, expense_id, user_id, session) -> list: 
        query = select(ExpenseModel).where(ExpenseModel.expense_id == expense_id, ExpenseModel.user_id == user_id)
        expenses = await session.execute(query)
        return expenses.scalars().one()
    

    @classmethod
    @connection
    async def find_all(cls, user_id, session) -> list:
        query = select(ExpenseModel).where(ExpenseModel.user_id == user_id)
        expenses = await session.execute(query)
        return expenses.scalars().all()    
    
    
    @classmethod
    @connection
    async def create(cls, expense, session) -> None:
        try:
            session.add(expense)
        except Exception as e:
            await session.rollback()
            raise e
        else:                
            await session.commit()
    
    
    @classmethod
    @connection
    async def delete(cls, expense_id: int, user_id, session):
        query = delete(ExpenseModel).where(ExpenseModel.expense_id == expense_id, ExpenseModel.user_id == user_id)
        await session.execute(query)
        await session.commit()  
    
    
    @classmethod
    @connection
    async def update_expense(cls, expense_id: int, user_id: int, session, new_amount: Optional[int] = None, new_description: Optional[str] = None):
        if new_amount and new_description:
            query = update(ExpenseModel).where(ExpenseModel.expense_id == expense_id, ExpenseModel == user_id).values(amount = new_amount, description = new_description)
        elif new_amount:
            query = update(ExpenseModel).where(ExpenseModel.expense_id == expense_id, ExpenseModel == user_id).values(amount = new_amount)
        elif new_description:
            query = update(ExpenseModel).where(ExpenseModel.expense_id == expense_id, ExpenseModel == user_id).values(description = new_description)    
        
        try:
            await session.execute(query)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=e)
        else:
            await session.commit()
         
            