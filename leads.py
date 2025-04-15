from sqlalchemy.orm import Session
from models import Lead
from schemas import LeadCreate, LeadState, LeadUpdate
from fastapi import UploadFile
import os
import uuid

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_lead(db: Session, lead: LeadCreate, resume: UploadFile):
    file_extension = resume.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(resume.file.read())
    db_lead = Lead(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        resume_path=file_path,
        state=LeadState.PENDING,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def get_leads(db: Session):
    return db.query(Lead).all()


def update_lead(db: Session, lead_id: int, lead_update: LeadUpdate):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        db_lead.state = lead_update.state
        db.commit()
        db.refresh(db_lead)
    return db_lead
