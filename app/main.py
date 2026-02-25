import uvicorn
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi.security import OAuth2PasswordBearer

# Ваші імпорти
from app.db import init_db, engine
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(category_router.router, prefix="/categories", tags=["Categories"])
app.include_router(place_router.router, prefix="/places", tags=["Places"])
app.include_router(favorite_router.router, prefix="/favorites", tags=["Favorites"])

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE_PATH = BASE_DIR / "static" / "index.html"


@app.get("/", tags=["UI"])
async def read_index():
    if INDEX_FILE_PATH.exists():
        return FileResponse(INDEX_FILE_PATH)

    return HTMLResponse(content=f"""
        <html>
            <body style="font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: #f8fafc;">
                <h1 style="color: #ef4444;">Файл інтерфейсу не знайдено ⚠️</h1>
                <p>Я шукав файл за цим шляхом:</p>
                <code style="background: #e2e8f0; padding: 10px; border-radius: 5px;">{INDEX_FILE_PATH}</code>
                <p>Будь ласка, переконайтеся, що файл <b>index.html</b> лежить саме там!</p>
                <a href="/docs" style="margin-top: 20px; color: #3b82f6;">Перейти до API документації (Swagger)</a>
            </body>
        </html>
    """, status_code=404)


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