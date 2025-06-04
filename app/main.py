from app.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Header, HTTPException
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import os
from app.models import Traffic
from app.github import fetch_and_store_all_repo_traffic
from sqlalchemy import func

app = FastAPI()

def verify_api_key(github_traffic_api_key: str = Header(...)):
    PROJECT_KEY = os.getenv("PROJECT_KEY")
    if github_traffic_api_key != PROJECT_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

def scheduled_fetch_all():
    db = SessionLocal()
    try:
        fetch_and_store_all_repo_traffic(db)
    finally:
        db.close()
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_fetch_all, 'cron', hour=1, minute=0)
scheduler.start()

def handle_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/traffic/{repo_name}")
def fetch_traffic(repo_name: str, db: Session = Depends(handle_db), _: str = Depends(verify_api_key)):
    total_views = (
        db.query(func.sum(Traffic.views))
        .filter(Traffic.repo == repo_name)
        .scalar()
    )
    total_uniques = (
        db.query(func.sum(Traffic.uniques))
        .filter(Traffic.repo == repo_name)
        .scalar()
    )
    last_updated = (
        db.query(func.max(Traffic.last_updated))
        .filter(Traffic.repo == repo_name)
        .scalar()
    )

    return {
        "repo": repo_name,
        "total_views": total_views or 0,
        "total_uniques": total_uniques or 0,
        "last_updated": last_updated.isoformat() if last_updated else None
    }