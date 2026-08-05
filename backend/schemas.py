from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_timestamp: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TagCreate(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: int
    name: str
    created_by: int

    class Config:
        from_attributes = True

class QueryCreate(BaseModel):
    query_name: str
    query_sql: str
    report_type: str
    tag_ids: list[int] = []

class QueryResponse(BaseModel):
    id: int
    query_name: str
    query_sql: str
    report_type: str
    created_by: int
    create_timestamp: datetime
    update_timestamp: datetime
    tags: list[TagResponse] = []

    class Config:
        from_attributes = True

class QueryUpdate(BaseModel):
    query_name: Optional[str] = None
    query_sql: Optional[str] = None
    report_type: Optional[str] = None
    tag_ids: Optional[list[int]] = None
