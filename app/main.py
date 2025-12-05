import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi.security import OAuth2PasswordBearer
from app.db import init_db, engine

from app.core.models import user as user_model
from app.core.models import category, place, favorite

from app.routers import user, category as category_router, place as place_router, favorite as favorite_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(
    title="Location Explorer API",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(category_router.router, prefix="/categories", tags=["Categories"])
app.include_router(place_router.router, prefix="/places", tags=["Places"])
app.include_router(favorite_router.router, prefix="/favorites", tags=["Favorites"])


@app.get("/", tags=["System"])
def root():
    return {"message": "Welcome to the Location Explorer API"}


@app.get("/health", tags=["System"])
async def health():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "db_status": "connected"}
    except Exception as e:
        return {"status": "error", "db_status": str(e)}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)