from http.client import HTTPException
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from app.models import Traffic
from app.db import SessionLocal

load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_repos():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return [repo['name'] for repo in response.json()]

def fetch_repo_traffic(repo):
    base_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/traffic"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    views = requests.get(f"{base_url}/views", headers=headers).json()
    clones = requests.get(f"{base_url}/clones", headers=headers).json()
    return {"repo": repo, "views": views, "clones": clones, "timestamp": datetime.utcnow()}

def fetch_and_store_all_repo_traffic(db: Session):
    for repo in get_repos():
        fetch_and_store_repo_traffic(repo, db)

def fetch_and_store_repo_traffic(repo_name: str, db: Session):
    traffic_data = fetch_repo_traffic(repo_name)

    new_entries = []
    for day_data in traffic_data["views"]["views"]:  # GitHub gives daily breakdown
        date = datetime.strptime(day_data["timestamp"], "%Y-%m-%dT%H:%M:%SZ").date()
        views = day_data["count"]
        uniques = day_data["uniques"]

        # Only store if this date hasn't been stored before
        existing = db.query(Traffic).filter(
            Traffic.repo == repo_name,
            Traffic.date == date
        ).first()

        if not existing:
            new_entry = Traffic(
                repo=repo_name,
                date=date,
                views=views,
                uniques=uniques,
                last_updated=datetime.utcnow()
            )
            db.add(new_entry)
            new_entries.append(new_entry)

    db.commit()

    # Return current 14-day summary
    total_views = sum(e.views for e in new_entries)
    total_uniques = sum(e.uniques for e in new_entries)

    return {
        "status": "success",
        "data": {
            "repo": repo_name,
            "new_days_stored": len(new_entries),
            "views_fetched_now": total_views,
            "uniques_fetched_now": total_uniques
        }
    }