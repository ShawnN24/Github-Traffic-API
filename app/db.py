from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Traffic  # Import Base from models.py

DATABASE_URL = "sqlite:///./traffic.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def store_traffic_data(data):
    db = SessionLocal()
    traffic = Traffic(**data)
    db.add(traffic)
    db.commit()
    db.close()