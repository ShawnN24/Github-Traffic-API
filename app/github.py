from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from git import Repo, GitCommandError
from app.models import Traffic

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
    repo = Repo(".")
    db_file = "traffic.db"
    branch = "traffic-db-storage"

    # Checkout traffic-db-storage branch
    try:
        repo.git.fetch()
        repo.git.checkout(branch)
    except GitCommandError:
        print(f"Branch '{branch}' not found locally. Fetching from origin...")
        repo.git.fetch("origin", branch)
        repo.git.checkout(branch)

    # Stage traffic.db
    repo.git.add(db_file)
    if not repo.is_dirty(untracked_files=False):
        print("No changes to traffic.db. Nothing to commit.")
        return

    # Commit traffic.db updates
    print("Committing traffic.db...")
    repo.index.commit("Update traffic.db with latest traffic data")

    # Set remote url for push
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/Github-Traffic-API.git"
    if "origin" not in [remote.name for remote in repo.remotes]:
        repo.create_remote("origin", remote_url)
    else:
        repo.git.remote("set-url", "origin", remote_url)

    # Push branch changes
    repo.git.push("origin", branch)
    print("Push successful.")

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