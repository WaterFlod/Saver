from pydantic import BaseModel

class Expense(BaseModel):
    id: int
    amount: int
    description: str
    pass

class ExpenseDTO(Expense):
    pass