from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file — backend ఫోల్డర్ లోపల phantomweave.db అనే ఫైల్ క్రియేట్ అవుతుంది
SQLALCHEMY_DATABASE_URL = "sqlite:///./phantomweave.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite కి FastAPI తో వాడటానికి అవసరం
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ప్రతి API request కి ఒక database session ఇచ్చి, పని అయ్యాక close చేసే function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()