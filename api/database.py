from contextlib import closing

from confs.config import configs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(configs.POSTGRES_DNS, echo=False, encoding="utf8")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    with closing(SessionLocal()) as db:
        yield db
