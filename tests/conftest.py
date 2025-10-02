import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from db import get_db

# Test database setup
test_url = "sqlite:///:memory:"
engine = create_engine(test_url, connect_args={"check_same_thread": False})
connection = engine.connect()  # <-- single connection
TestingSessionLocal = sessionmaker(bind=connection)

# Create the database tables
Base.metadata.create_all(bind=connection)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """
    Fixture to provide a TestClient for FastAPI app with an in-memory SQLite database.
    """
    return TestClient(app)