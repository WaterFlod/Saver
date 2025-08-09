from pydantic import BaseModel

class Expense(BaseModel):
    amount: int
    description: str

class ExpenseDTO(Expense):
    id: int