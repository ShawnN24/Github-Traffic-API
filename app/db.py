from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, Traffic
import os


DATABASE_URL = "sqlite:///traffic.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def db_fetch_traffic(repo_name: str, db: Session):
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

def db_fetch_timeline(repo_name: str, db: Session):
    records = (
        db.query(Traffic)
        .filter(Traffic.repo == repo_name)
        .order_by(Traffic.date)
        .all()
    )

    return [
        {
            "date": record.date.isoformat(),
            "views": record.views,
            "uniques": record.uniques
        }
        for record in records
    ]