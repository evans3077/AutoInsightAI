from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class VideoJob(Base):
    __tablename__ = "video_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    job_id = Column(String, unique=True, index=True)
    video_url = Column(String)
    status = Column(String, default="queued")  # queued, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    results = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

class TrendCluster(Base):
    __tablename__ = "trend_clusters"
    
    id = Column(Integer, primary_key=True, index=True)
    cluster_name = Column(String)
    keywords = Column(JSON)
    momentum = Column(Float)
    category = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)