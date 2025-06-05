from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.email import Email


class StatsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self, from_date: Optional[datetime], to_date: Optional[datetime]):
        if not from_date or not to_date:
            raise ValueError("Both from_date and to_date must be provided.")

        sent_stmt = select(func.count()).where(
            Email.sent_at >= from_date,
            Email.sent_at <= to_date,
            Email.direction == "sent"
        )
        sent_result = await self.db.execute(sent_stmt)
        sent_count = sent_result.scalar() or 0

        received_stmt = select(func.count()).where(
            Email.sent_at >= from_date,
            Email.sent_at <= to_date,
            Email.direction == "received"
        )
        received_result = await self.db.execute(received_stmt)
        received_count = received_result.scalar() or 0

        return {"sent": sent_count, "received": received_count}
