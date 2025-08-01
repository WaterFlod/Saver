from fastapi import FastAPI
import uvicorn
import asyncio

from routers import router_user 
from database import Base, engine

app = FastAPI()

app.include_router(router_user)


async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", reload=True, log_level="info", host="0.0.0.0")
