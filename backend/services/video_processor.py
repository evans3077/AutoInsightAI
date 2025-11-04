import logging
from backend.scheduler.tasks import process_video_task

async def process_video_upload(file, job_id: str, user_id: int):
    """
    Handle video upload and trigger background processing
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Prepare metadata
        metadata = {
            "filename": file.filename,
            "title": file.filename,  # In production, get from form data
            "user_id": user_id,
            "file_size": len(file_content)
        }
        
        # Trigger background task
        process_video_task.delay(
            file_content=file_content,
            filename=file.filename,
            job_id=job_id,
            user_id=user_id,
            metadata=metadata
        )
        
        logging.info(f"Video processing task queued: {job_id}")
        
    except Exception as e:
        logging.error(f"Failed to queue video processing: {e}")
        raise