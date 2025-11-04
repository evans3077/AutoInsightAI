from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from backend.api.routes import router as api_router
from backend.db.database import engine, SessionLocal
from backend.db.models import Base
import logging

# Create tables
Base.metadata.create_all(bind=engine)

# Security
security = HTTPBearer()

app = FastAPI(
    title="AutoInsightAI",
    description="AI-powered YouTube Content Optimization Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AutoInsightAI API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)