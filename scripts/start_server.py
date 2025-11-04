#!/usr/bin/env python3
import subprocess
import sys
import time

def start_services():
    """Start all required services"""
    print("🚀 Starting AutoInsightAI Services...")
    
    # Start Redis
    print("📦 Starting Redis...")
    subprocess.Popen(["redis-server", "--daemonize yes"])
    time.sleep(2)
    
    # Start Celery Worker
    print("👷 Starting Celery Worker...")
    worker_process = subprocess.Popen([
        sys.executable, "-m", "celery", 
        "-A", "backend.scheduler.tasks.celery_app", 
        "worker", "--loglevel=info"
    ])
    
    # Start FastAPI Server
    print("🌐 Starting FastAPI Server...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])

if __name__ == "__main__":
    start_services()