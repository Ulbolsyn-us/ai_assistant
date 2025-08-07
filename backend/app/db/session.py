# import os 
# from dotenv import load_dotenv
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.api.models import Base

# load_dotenv()

# DB_URL = os.getenv("DATABASE_URL")

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()