from sqlalchemy import Column, String, Integer, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Traffic(Base):
    __tablename__ = "traffic"

    id = Column(Integer, primary_key=True, index=True)
    repo = Column(String, index=True)
    date = Column(Date, index=True)
    views = Column(Integer)
    uniques = Column(Integer)
    last_updated = Column(DateTime)