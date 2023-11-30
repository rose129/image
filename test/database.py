import imp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "sqlite:///./image.sqlite"

Base = declarative_base()
engine = create_engine(DB_URL, connect_args = { "check_same_thread": False })
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
