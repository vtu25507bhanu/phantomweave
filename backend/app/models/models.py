from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.database.database import Base


class User(Base):
    """
    Dashboard లోకి login అయ్యే admin users కోసం.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VisitorLog(Base):
    """
    Honeypot pages ని ఎవరైనా visit చేసినప్పుడు, ఆ attempt వివరాలు ఇక్కడ save అవుతాయి.
    """
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    user_agent = Column(String)
    page_visited = Column(String)          # e.g. "fake_login", "fake_admin"
    session_duration = Column(Float, default=0.0)   # seconds
    risk_score = Column(Float, default=0.0)         # AI model output (0-1)
    is_threat = Column(Integer, default=0)          # 0 = safe, 1 = threat (AI classification)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    """
    Blockchain-style tamper-evident audit trail.
    ప్రతి entry, దాని ముందున్న entry హాష్‌ని కలిగి ఉంటుంది (Step 11 లో వివరిస్తాను).
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_data = Column(Text)
    previous_hash = Column(String)
    current_hash = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())