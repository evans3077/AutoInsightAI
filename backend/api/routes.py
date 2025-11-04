from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from fastapi.security import HTTPBearer
from core.security.auth import verify_token, create_access_token, verify_password, get_password_hash
from backend.db.database import get_db
from backend.db.models import User, VideoJob
from backend.services.video_processor import process_video_upload
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from typing import List, Optional

router = APIRouter()
security = HTTPBearer()

# ... (previous auth endpoints remain the same) ...

@router.post("/analyze/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Video file to analyze"),
    title: str = Form(..., description="Video title"),
    description: Optional[str] = Form(None, description="Video description"),
    tags: Optional[str] = Form(None, description="Comma-separated tags"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file.content_type} not supported. Use: {', '.join(allowed_types)}"
        )
    
    # Validate file size (50MB max)
    max_size = 50 * 1024 * 1024
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > max_size:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 50MB")
    
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
    db.refresh(job)
    
    # Process video in background
    background_tasks.add_task(process_video_upload, file, job_id, current_user.id)
    
    return {
        "job_id": job_id, 
        "status": "queued", 
        "message": "Video uploaded for analysis",
        "estimated_time": "30-60 seconds"
    }

@router.get("/analyze/jobs")
def get_user_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """Get user's analysis jobs"""
    jobs = db.query(VideoJob).filter(
        VideoJob.user_id == current_user.id
    ).order_by(
        VideoJob.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "jobs": [
            {
                "job_id": job.job_id,
                "status": job.status,
                "created_at": job.created_at,
                "completed_at": job.completed_at,
                "has_results": job.results is not None
            }
            for job in jobs
        ],
        "total": db.query(VideoJob).filter(VideoJob.user_id == current_user.id).count()
    }

@router.delete("/analyze/jobs/{job_id}")
def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific job"""
    job = db.query(VideoJob).filter(
        VideoJob.job_id == job_id,
        VideoJob.user_id == current_user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job deleted successfully"}