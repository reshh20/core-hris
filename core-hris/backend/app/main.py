
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from app.database import init_db, SessionLocal
from app.routes import employees, departments, positions, organization
from app.utils.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()
    print("[OK] Database tables created.")

    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    yield
    print("Application shutting down.")


app = FastAPI(
    title="Core HRIS API",
    description=(
        "Simplified Core Human Resource Information System API. "
        "Provides employee directory, organizational chart, "
        "and HR management capabilities."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(positions.router)
app.include_router(organization.router)


@app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check():
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred. Please try again later.",
        },
    )
