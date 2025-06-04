from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Traffic  # Import Base from models.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'traffic.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def store_traffic_data(data):
    db = SessionLocal()
    traffic = Traffic(**data)
    db.add(traffic)
    db.commit()
    db.close()