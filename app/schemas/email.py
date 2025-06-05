from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class EmailStatsResponse(BaseModel):
    sent: int
    received: int
