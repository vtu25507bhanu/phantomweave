import json
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.models import VisitorLog, AuditLog
from app.ai_engine.detector import predict_threat
from app.blockchain.blockchain import calculate_hash, create_genesis_hash

router = APIRouter(prefix="/detect", tags=["Threat Detection"])


class BehaviorData(BaseModel):
    page_visited: str
    request_count: int
    session_duration: float
    failed_login_attempts: int
    typing_speed: float
    mouse_movement: int


@router.post("/analyze")
def analyze_visitor(data: BehaviorData, request: Request, db: Session = Depends(get_db)):
    result = predict_threat(
        request_count=data.request_count,
        session_duration=data.session_duration,
        failed_login_attempts=data.failed_login_attempts,
        typing_speed=data.typing_speed,
        mouse_movement=data.mouse_movement
    )

    visitor_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    log_entry = VisitorLog(
        ip_address=visitor_ip,
        user_agent=user_agent,
        page_visited=data.page_visited,
        session_duration=data.session_duration,
        risk_score=result["risk_score"],
        is_threat=int(result["is_threat"])
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    # ===== Blockchain-style Audit Log Entry =====
    last_block = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    previous_hash = last_block.current_hash if last_block else create_genesis_hash()

    event_data = json.dumps({
        "visitor_log_id": log_entry.id,
        "ip_address": visitor_ip,
        "page_visited": data.page_visited,
        "is_threat": result["is_threat"],
        "risk_score": result["risk_score"]
    })

    timestamp_now = datetime.utcnow()
    current_hash = calculate_hash(event_data, previous_hash, timestamp_now.isoformat())

    audit_entry = AuditLog(
        event_data=event_data,
        previous_hash=previous_hash,
        current_hash=current_hash,
        timestamp=timestamp_now
    )
    db.add(audit_entry)
    db.commit()

    return {
        "log_id": log_entry.id,
        "is_threat": result["is_threat"],
        "risk_score": result["risk_score"],
        "confidence": result["confidence"]
    }


@router.get("/logs")
def get_visitor_logs(db: Session = Depends(get_db)):
    logs = db.query(VisitorLog).order_by(VisitorLog.timestamp.desc()).limit(100).all()
    return logs