from fastapi import APIRouter
from backend.ml.pipeline import generate_insights
from backend.auth.login import login_user
from backend.auth.register import register_user

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/login")
def login(username: str, password: str):
    success = login_user(username, password)
    return {"success": success}

@router.post("/register")
def register(username: str, password: str):
    register_user(username, password)
    return {"status": "registered"}

@router.post("/insights")
def create_insights(data: list):
    result = generate_insights(data)
    return result
