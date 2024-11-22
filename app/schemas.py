from pydantic import BaseModel, Field
from typing import List, Optional


class SpyCatCreate(BaseModel):
    name: str
    experience: int
    breed: str
    salary: float


class SalaryUpdate(BaseModel):
    salary: float


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    completed: bool = False


class MissionCreate(BaseModel):
    name: str
    targets: List[TargetCreate]
    completed: bool = False
    cat_id: Optional[int] = None
    class Config:
        orm_mode = True


class TargetUpdate(BaseModel):
    completed: Optional[bool] = Field(None, description="Mark target as complete/incomplete")
    notes: Optional[str] = Field(None, description="Update notes")