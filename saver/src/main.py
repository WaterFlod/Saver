from fastapi import FastAPI, HTTPException

import uvicorn

from .schemas import Expense

app = FastAPI()

db = {
    0: {"id": 0, "amount": 110, "description": "Cola"},
}


@app.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    if expense_id in db:
        expense = db[expense_id]
        return expense
    raise HTTPException(status_code=404, detail="Expense not found")


@app.get("/expenses", response_model=Expense)
def get_all_expenses():
    return db


@app.post("/expenses", response_model=Expense)
def create_expense(data:Expense):
    db[data.id] = data
    return data


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
