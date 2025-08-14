from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from api.config import config

Base_Analytics_Datastore = declarative_base(metadata=MetaData(schema="public_mart"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
analytics_engine = create_engine(config.ANALYTICS_DATABASE_URL)

def get_analytics_datastore_db():
    db = SessionLocal(bind=analytics_engine)

    try:
        yield db
    finally:
        db.close()
