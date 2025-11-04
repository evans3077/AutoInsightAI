from fastapi import APIRouter, Depends, HTTPException
from backend.ml.pipeline import pipeline
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/process-text/")
def process_text(text: str, token: str = Depends(oauth2_scheme)):
    features = pipeline.process_text(text)
    return {"features": features}

@router.get("/process-image/")
def process_image(image_path: str, token: str = Depends(oauth2_scheme)):
    features = pipeline.process_image(image_path)
    return {"features": features}
