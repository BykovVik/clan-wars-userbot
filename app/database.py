from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://admin:admin@localhost/tg_game')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_all_tables():
    Base.metadata.create_all(engine)