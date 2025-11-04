from celery import Celery
from core.config.settings import settings
import logging
from backend.ml.pipeline import analyze_video_content
from backend.db.database import SessionLocal
from backend.db.models import VideoJob
from datetime import datetime

# Configure Celery
celery_app = Celery(
    'autoinsightai',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def process_video_task(self, file_content: bytes, filename: str, job_id: str, user_id: int, metadata: dict):
    """
    Background task to process video analysis
    """
    db = SessionLocal()
    
    try:
        # Update job status
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if job:
            job.status = "processing"
            job.started_at = datetime.utcnow()
            db.commit()
        
        # Save file temporarily (in production, use S3)
        file_path = f"/tmp/{job_id}_{filename}"
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Run analysis
        results = analyze_video_content(file_path, metadata)
        
        # Update job with results
        if job:
            job.status = "completed"
            job.results = results
            job.completed_at = datetime.utcnow()
            job.video_url = f"processed_{job_id}"
            db.commit()
        
        logging.info(f"Successfully processed job {job_id}")
        return {"status": "success", "job_id": job_id}
        
    except Exception as e:
        logging.error(f"Failed to process job {job_id}: {e}")
        
        # Update job with error
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()
        
        return {"status": "error", "job_id": job_id, "error": str(e)}
    
    finally:
        db.close()
        # Cleanup temporary file
        import os
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass