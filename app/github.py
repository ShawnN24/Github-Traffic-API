from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import json
import requests
from datetime import datetime
from git import Repo, GitCommandError
from tempfile import TemporaryDirectory
import shutil
from app.models import Traffic
from app.db import db_fetch_traffic, db_fetch_timeline

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

def sync_db_from_github():
    db_path = "./cloned-repo/traffic.db"
    url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/Github-Traffic-API/traffic-db-storage/traffic.db"

    print("Downloading latest traffic.db from GitHub...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(db_path, "wb") as f:
            f.write(response.content)
        print("traffic.db updated from GitHub")
    else:
        print(f"Failed to download traffic.db (status {response.status_code})")

def commit_updated_db_to_github():
    db_path = os.path.abspath("cloned-repo/traffic.db")
    branch = "traffic-db-storage"

    with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        print(f"Cloning fresh copy into {tmpdir}...")
        repo = Repo.clone_from(
            f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/Github-Traffic-API.git",
            tmpdir,
            branch=branch
        )

        target_db = os.path.join(tmpdir, "traffic.db")
        shutil.copy2(db_path, target_db)

        repo.index.add(["traffic.db"])

        if repo.is_dirty(untracked_files=False):
            print("Committing updated traffic.db...")
            repo.index.commit("Update traffic.db with latest traffic data")
            repo.git.push("origin", branch)
            print("Push successful.")
        else:
            print("No changes to traffic.db. Nothing to commit.")

def commit_updated_cache_to_github():
    metrics_path = os.path.abspath("metrics.json")
    branch = "cache"

    with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        print(f"Cloning fresh copy into {tmpdir}...")
        repo = Repo.clone_from(
            f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/Github-Traffic-API.git",
            tmpdir,
            branch=branch
        )

        target_metrics_path = os.path.join(tmpdir, "metrics.json")
        shutil.copy2(metrics_path, target_metrics_path)

        repo.git.add("metrics.json")

        if repo.is_dirty(untracked_files=False):
            print("Committing updated metrics.json...")
            repo.index.commit("Update metrics.json cache")
            repo.git.push("origin", branch)
            print("Push successful.")
        else:
            print("No changes to metrics.json. Nothing to commit.")

def fetch_and_store_all_metrics(db: Session):
    metrics = {}
    for repo in get_repos():
        metrics[repo] = {
            "traffic": db_fetch_traffic(repo, db),
            "timeline": db_fetch_timeline(repo, db)
        }
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    commit_updated_cache_to_github()
    

def fetch_and_store_all_repo_traffic(db: Session):
    sync_db_from_github()
    for repo in get_repos():
        fetch_and_store_repo_traffic(repo, db)
    commit_updated_db_to_github()

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