import sys 
sys.path.append("/saver")

from sqlalchemy import select

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
            except:
                await session.rollback()
            else:                
                await session.commit()