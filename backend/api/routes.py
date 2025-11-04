from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.security import HTTPBearer
from core.security.auth import verify_token, create_access_token, verify_password, get_password_hash
from backend.db.database import get_db
from backend.db.models import User, VideoJob
from backend.services.video_processor import process_video_upload
from backend.ml.pipeline import analyze_video_content
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

router = APIRouter()
security = HTTPBearer()

# Dependency to get current user
async def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(token.credentials)
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/auth/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create user
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    
    return {"message": "User created successfully"}

@router.post("/auth/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/analyze/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create job record
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    job = VideoJob(
        job_id=job_id,
        user_id=current_user.id,
        video_url=f"pending_{job_id}",
        status="queued"
    )
    db.add(job)
    db.commit()
    
    # Process video in background
    background_tasks.add_task(process_video_upload, file, job_id, current_user.id)
    
    return {"job_id": job_id, "status": "queued", "message": "Video uploaded for analysis"}

@router.get("/analyze/status/{job_id}")
def get_analysis_status(job_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id, VideoJob.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job.job_id,
        "status": job.status,
        "results": job.results,
        "created_at": job.created_at,
        "completed_at": job.completed_at
    }

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }