from fastapi import FastAPI

import uvicorn

from .routers import user 

app = FastAPI()

app.include_router(user)

db = {
    0: {"id": 0, "amount": 110, "description": "Cola"},
}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
