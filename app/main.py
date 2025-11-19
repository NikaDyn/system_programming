from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.db import Database
from app.core.models.base import BaseModel
from app.routers import user, category, place, favorite

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
db = Database(url=DATABASE_URL)


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    await db.connect()
    async with db.engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(category.router)
app.include_router(place.router)
app.include_router(favorite.router)


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/health", tags=["System"])
async def health():
    ok = await db.ping()
    return {"status": "ok" if ok else "error"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
