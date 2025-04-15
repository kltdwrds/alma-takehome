from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class LeadState(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"


class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class LeadUpdate(BaseModel):
    state: LeadState


class LeadResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    resume_path: str
    state: LeadState
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
