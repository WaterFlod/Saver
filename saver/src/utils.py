from sqlalchemy import select

from models import ExpenseModel
from schemas import ExpenseDTO

async def get_expenses(session) -> list: #return all appointments in DB
    result = await session.execute(select(ExpenseModel))
    appointments = result.scalars().all()
    result_dto = [ExpenseDTO.model_validate(row, from_attributes=True) for row in appointments]
    return result_dto