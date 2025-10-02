from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database name
DB_NAME = "weather.db"

# Database setup
db_url = f"sqlite:///{DB_NAME}"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
