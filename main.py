from fastapi import FastAPI
from backend.api.routes import router as api_router
from backend.db.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoInsightAI")

app.include_router(api_router, prefix="/api")
