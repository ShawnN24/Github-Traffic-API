from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from app.db import SessionLocal
from app.db import db_fetch_traffic, db_fetch_timeline
from app.github import fetch_and_store_all_repo_traffic, sync_db_from_github, commit_updated_db_to_github

app = FastAPI()

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

@app.put("/cron/update-db")
def scheduled_fetch_all(db: Session = Depends(handle_db), _: str = Depends(verify_api_key)):
    sync_db_from_github()
    fetch_and_store_all_repo_traffic(db)
    commit_updated_db_to_github()
    return {"message": "Successful /cron/update-db"}

@app.get("/traffic/{repo_name}")
def fetch_traffic(repo_name: str, db: Session = Depends(handle_db), _: str = Depends(verify_api_key)):
    return db_fetch_traffic(repo_name, db)

@app.get("/timeline/{repo_name}")
def fetch_traffic(repo_name: str, db: Session = Depends(handle_db), _: str = Depends(verify_api_key)):
    return db_fetch_timeline(repo_name, db)