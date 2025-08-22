import sys 
sys.path.append("/saver")

from sqlalchemy import select, delete

from src.models import ExpenseModel
from src.database import async_session_maker

class ExpenseDAO:
    @classmethod
    async def find_all_expenses(cls) -> list: #return all appointments in DB
        async with async_session_maker() as session:
            query = select(ExpenseModel)
            expenses = await session.execute(query)
            return expenses.scalars().all()
        
    @classmethod
    async def create_expense(cls, expense) -> None:
        async with async_session_maker() as session:
            try:
                session.add(expense)
            except Exception:
                await session.rollback()
                raise Exception
            else:                
                await session.commit()
    
    @classmethod
    async def delete_expense(cls, id: int):
        async with async_session_maker() as session:
            delete_expense = (delete(ExpenseModel).where(ExpenseModel.id == id))
            await session.execute(delete_expense)
            await session.commit()   
            