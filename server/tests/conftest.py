import os

# use .env.test
os.environ["ENV_FILE"] = ".env.test"

from app.core.bootstrap import load_environment

# Load test environment before database.py is imported
load_environment()

import pytest
from sqlalchemy import text

from fastapi.testclient import TestClient

from app.main import app
from app.db.deps import get_db
from app.db.database import SessionLocal


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    db.execute(text("""
        TRUNCATE TABLE
            incidents,
            histories,
            endpoints,
            groups
        RESTART IDENTITY CASCADE;
    """))

    db.commit()
    db.close()

@pytest.fixture
def db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def group_payload():
    return {
        "name": "STMicroelectronics",
        "type": "customer",
        "description": "semiconductor manufacturing and design company"
    }


@pytest.fixture
def endpoint_payload():
    return {
        "name": "Main website",
        "type": "https",
        "url": "https://st.com",
        "description": None,
        "method": "GET"
    }