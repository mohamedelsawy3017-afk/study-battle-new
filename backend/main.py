# main.py - FastAPI application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from core.config import settings
from database.session import create_tables
from routers import auth_router, users_router, tasks_router

from database.session import AsyncSessionLocal
from models.user import User
from models.task import Task
from sqlalchemy import delete


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup/shutdown lifecycle."""
    await create_tables()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} is ready!")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="🔥 A gamified study competition app — may the grinder win!",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")


@app.get("/api/nuke")
async def nuke_database():
    """COMPLETELY WIPE the database - Use with caution!"""
    import sqlite3
    import os
    
    db_paths = [
        "study_battle.db",
        "backend/study_battle.db", 
        "/app/backend/study_battle.db",
        os.path.join(os.path.dirname(__file__), "study_battle.db")
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                return {"message": f"✅ Database deleted at: {db_path}"}
            except Exception as e:
                return {"message": f"❌ Could not delete: {db_path} - {str(e)}"}
    
    return {"message": "No database file found to delete"}


@app.get("/api/init-db")
async def init_database():
    """Force create all tables"""
    await create_tables()
    return {"message": "✅ Database tables recreated!"}


@app.post("/api/reset")
async def reset_database():
    """Delete all users and tasks (for testing)"""
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Task))
        await db.execute(delete(User))
        await db.commit()
    return {"message": "✅ All data cleared! Database is now empty."}


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


# Serve frontend static files
backend_dir = os.path.dirname(__file__)
frontend_dir = os.path.join(os.path.dirname(backend_dir), "frontend")

if not os.path.exists(frontend_dir):
    frontend_dir = os.path.join(backend_dir, "frontend")

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)