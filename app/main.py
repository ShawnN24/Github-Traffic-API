from app.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Header, HTTPException
import os
from app.models import Traffic
from app.github import fetch_and_store_all_repo_traffic
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for testing with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_api_key(github_traffic_api_key: str = Header(...)):
    PROJECT_KEY = os.getenv("PROJECT_KEY")
    if github_traffic_api_key != PROJECT_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

def handle_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cron/fetch-all")
def scheduled_fetch_all(db: Session = Depends(handle_db), _: str = Depends(verify_api_key)):
    fetch_and_store_all_repo_traffic(db)
    return {"message": "Successful /cron/fetch-all"}

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