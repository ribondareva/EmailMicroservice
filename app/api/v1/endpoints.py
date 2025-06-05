from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional

from app.db import get_db
from app.schemas.email import EmailSendRequest, EmailResponse, EmailStatsResponse
from app.services.email_service import EmailService
from app.services.stats_service import StatsService

router = APIRouter(tags=["Emails"])


@router.post("/send", response_model=EmailResponse)
async def send_email(payload: EmailSendRequest, db: AsyncSession = Depends(get_db)):
    try:
        service = EmailService(db)
        email = await service.send_email(payload)
        return email
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[EmailResponse])
async def list_emails(
        from_date: Optional[datetime] = Query(None),
        to_date: Optional[datetime] = Query(None),
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        subject_contains: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
):
    try:
        service = EmailService(db)
        emails = await service.list_emails(
            from_date, to_date, sender, recipient, subject_contains
        )
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=EmailStatsResponse)
async def email_stats(
        from_date: Optional[datetime] = Query(None),
        to_date: Optional[datetime] = Query(None),
        db: AsyncSession = Depends(get_db)
):
    try:
        service = StatsService(db)
        stats = await service.get_stats(from_date, to_date)
        print("Stats result:", stats)
        return stats
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
