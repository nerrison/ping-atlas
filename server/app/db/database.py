import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
from app.core import env_config


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=env_config.DB_USER,
    password=env_config.DB_PASSWORD,
    host=env_config.DB_HOST,
    port=env_config.DB_PORT,
    database=env_config.DB_NAME,
)

engine = create_engine(DATABASE_URL,connect_args={"options": "-csearch_path=public"}, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()