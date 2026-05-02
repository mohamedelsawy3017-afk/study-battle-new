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

# ADD THIS IMPORT for the reset endpoint
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


# Initialize FastAPI app - THIS MUST COME FIRST
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="🔥 A gamified study competition app — may the grinder win!",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")


# ADD THE RESET ENDPOINT HERE - AFTER app is created
@app.post("/api/reset")
async def reset_database():
    """Delete all users and tasks (for testing)"""
    async with AsyncSessionLocal() as db:
        # Delete all tasks first (due to foreign key)
        await db.execute(delete(Task))
        # Delete all users
        await db.execute(delete(User))
        await db.commit()
    return {"message": "✅ All data cleared! Database is now empty."}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
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