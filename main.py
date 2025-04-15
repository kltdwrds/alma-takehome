from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schemas import LeadCreate, LeadUpdate, LeadResponse, LeadState
from leads import create_lead, get_leads, update_lead
from emails import send_prospect_email, send_attorney_email
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "password"
    if (
        credentials.username == correct_username
        and credentials.password == correct_password
    ):
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/leads", response_model=LeadResponse)
async def create_lead_endpoint(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    lead_create = LeadCreate(first_name=first_name, last_name=last_name, email=email)
    db_lead = create_lead(db, lead_create, resume)
    send_prospect_email(lead_create.email)
    attorney_email = "attorney@example.com"
    send_attorney_email(attorney_email, db_lead)
    return db_lead


@app.get("/leads", response_model=List[LeadResponse])
def get_leads_endpoint(
    db: Session = Depends(get_db), username: str = Depends(get_current_username)
):
    leads = get_leads(db)
    return leads


@app.patch("/leads/{lead_id}", response_model=LeadResponse)
def update_lead_endpoint(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username),
):
    db_lead = update_lead(db, lead_id, lead_update)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead
