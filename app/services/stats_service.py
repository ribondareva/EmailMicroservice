from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.email import Email


class StatsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self, from_date, to_date):
        sent_stmt = select(Email).filter(
            Email.sent_at >= from_date,
            Email.sent_at <= to_date,
            Email.direction == "sent"
        )
        received_stmt = select(Email).filter(
            Email.sent_at >= from_date,
            Email.sent_at <= to_date,
            Email.direction == "received"
        )

        sent_result = await self.db.execute(sent_stmt)
        received_result = await self.db.execute(received_stmt)

        sent_count = len(sent_result.scalars().all())
        received_count = len(received_result.scalars().all())

        return {"sent": sent_count, "received": received_count}
