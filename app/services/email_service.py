import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select
from email.mime.text import MIMEText
from app.models.email import Email
from app.core.config import settings
from app.schemas.email import EmailSendRequest, EmailResponse


class EmailService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def send_email(self, payload: EmailSendRequest) -> EmailResponse:
        # Отправка письма в отдельном потоке
        await asyncio.to_thread(self._send_email_sync, payload)

        email = Email(
            direction="sent",
            sender=settings.sender_email,
            recipients=",".join(payload.to),
            subject=payload.subject,
            body=payload.body,
            is_sent=True,
            sent_at=datetime.utcnow(),
        )
        self.db.add(email)

        try:
            await self.db.commit()
        except Exception as e:
            print("Ошибка при коммите:", e, flush=True)
            await self.db.rollback()
            raise

        try:
            await self.db.refresh(email)
        except Exception as e:
            print("Ошибка при рефреше:", e, flush=True)
            raise

        if email.id is None:
            raise ValueError("Email ID не был присвоен после коммита и рефреша")

        print("Email ID after commit:", email.id, flush=True)

        return EmailResponse(
            id=email.id,
            sender=email.sender,
            recipients=email.recipients.split(","),
            subject=email.subject,
            body=email.body,
            is_sent=email.is_sent,
            sent_at=email.sent_at
        )

    def _send_email_sync(self, payload: EmailSendRequest):
        import smtplib
        msg = MIMEText(payload.body, "html" if payload.is_html else "plain")
        msg["Subject"] = payload.subject
        msg["From"] = settings.sender_email
        msg["To"] = ", ".join(payload.to)

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            try:
                smtp.starttls()
            except Exception:
                pass
            if settings.smtp_user and settings.smtp_password:
                smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.sendmail(settings.sender_email, payload.to, msg.as_string())

    async def list_emails(
            self,
            from_date=None,
            to_date=None,
            sender=None,
            recipient=None,
            subject_contains=None,
    ):
        query = select(Email)

        if from_date:
            query = query.where(Email.sent_at >= from_date)
        if to_date:
            query = query.where(Email.sent_at <= to_date)
        if sender:
            query = query.where(Email.sender == sender)
        if recipient:
            query = query.where(Email.recipients.contains(recipient))
        if subject_contains:
            query = query.where(Email.subject.ilike(f"%{subject_contains}%"))

        result = await self.db.execute(query)
        emails = result.scalars().all()

        return [
            EmailResponse(
                id=email.id,
                sender=email.sender,
                recipients=email.recipients.split(","),
                subject=email.subject,
                body=email.body,
                is_sent=email.is_sent,
                sent_at=email.sent_at,
            )
            for email in emails
        ]
