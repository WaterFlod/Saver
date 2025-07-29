from fastapi import FastAPI

import uvicorn

from routers import router_user 

app = FastAPI()

app.include_router(router_user)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, log_level="info", host="0.0.0.0")
