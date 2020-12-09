from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.flex.core.config import get_settings

engine = create_engine(get_settings().SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
