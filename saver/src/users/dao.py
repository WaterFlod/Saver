import sys 
sys.path.append("/saver")

from sqlalchemy import select, delete, update

from src.models import ExpenseModel, UserModel
from src.database import connection


class UserDAO:
    @classmethod
    @connection
    async def find_one_or_none(cls, email: str, session):
        try:
            query = select(UserModel).where(UserModel.email == email)
            user = await session.execute(query)
        except Exception:
            return None
        else:
            return user.scalars().one()

            
class ExpenseDAO:
    @classmethod
    @connection
    async def find_expense_by_id(cls, id, session) -> list: 
        query = select(ExpenseModel).where(ExpenseModel.id == id)
        expenses = await session.execute(query)
        return expenses.scalars().one()
    
    @classmethod
    @connection
    async def find_all_expenses(cls, session) -> list:
        query = select(ExpenseModel)
        expenses = await session.execute(query)
        return expenses.scalars().all()    
    
    
    @classmethod
    @connection
    async def create_expense(cls, expense, session) -> None:
        try:
            session.add(expense)
        except Exception as e:
            await session.rollback()
            raise e
        else:                
            await session.commit()
    
    
    @classmethod
    @connection
    async def delete_expense(cls, id: int, session):
        query = delete(ExpenseModel).where(ExpenseModel.id == id)
        await session.execute(query)
        await session.commit()  
    
    
    @classmethod
    @connection
    async def update_expense(cls, id: int, session, new_amount: int = None, new_description: str = None):
        if new_amount and new_description:
            query = update(ExpenseModel).where(ExpenseModel.id == id).values(amount = new_amount, description = new_description)
        elif new_amount:
            query = update(ExpenseModel).where(ExpenseModel.id == id).values(amount = new_amount)
        elif new_description:
            query = update(ExpenseModel).where(ExpenseModel.id == id).values(description = new_description)    
        await session.execute(query)
        await session.commit()
         
            