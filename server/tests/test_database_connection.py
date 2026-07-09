from sqlalchemy import text
from app.db.database import SessionLocal


def test_database_is_test_db():
    db = SessionLocal()

    result = db.execute(text("SELECT current_database();"))

    database_name = result.scalar()

    db.close()

    assert database_name == "test_pingatlasdb"