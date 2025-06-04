from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class EmailSendRequest(BaseModel):
    to: List[EmailStr]
    subject: str
    body: str
    is_html: Optional[bool] = False


class EmailResponse(BaseModel):
    id: int
    sender: str
    recipients: List[str]
    subject: str
    body: str
    is_sent: bool
    sent_at: datetime

    class Config:
        from_attributes = True


class EmailStatsResponse(BaseModel):
    sent: int
    received: int
