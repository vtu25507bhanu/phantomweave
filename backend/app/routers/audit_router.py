from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import AuditLog
from app.blockchain.blockchain import verify_chain_integrity

router = APIRouter(prefix="/audit", tags=["Blockchain Audit Log"])


@router.get("/logs")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.id.asc()).all()
    return logs


@router.get("/verify")
def verify_audit_chain(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.id.asc()).all()
    result = verify_chain_integrity(logs)
    return result