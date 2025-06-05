import asyncio
import smtplib

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC
from sqlalchemy.future import select
from email.mime.text import MIMEText

from app.models.email import Email
from app.core.config import settings
from app.schemas.email import EmailSendRequest, EmailResponse
from services.imap_service import IMAPService


class EmailService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.imap = IMAPService(db)

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
            sent_at=datetime.now(UTC),
        )
        self.db.add(email)
        print("Before commit:", email, flush=True)
        print("Email ID (before commit):", email.id, flush=True)

        try:
            await self.db.commit()
            print("After commit:", email, flush=True)
            print("Email ID (after commit):", email.id, flush=True)

            await self.db.refresh(email)
            print("After refresh:", email, flush=True)
            print("Email ID (after refresh):", email.id, flush=True)

        except Exception as e:
            await self.db.rollback()
            print("Ошибка при сохранении email:", e, flush=True)
            raise

        if email.id is None:
            raise ValueError("Email ID не был присвоен после коммита и рефреша")

        return EmailResponse(
            id=email.id,
            sender=email.sender,
            recipients=email.recipients.split(","),
            subject=email.subject,
            body=email.body,
            is_sent=email.is_sent,
            sent_at=email.sent_at,
        )

    def _send_email_sync(self, payload: EmailSendRequest):
        if not settings.smtp_host or not settings.smtp_port:
            print("SMTP settings not configured, skipping sending email", flush=True)
            return

        msg = MIMEText(payload.body, "html" if payload.is_html else "plain")
        msg["Subject"] = payload.subject
        msg["From"] = settings.sender_email
        msg["To"] = ", ".join(payload.to)

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            try:
                smtp.starttls()
            except Exception:
                pass
            # if settings.smtp_user and settings.smtp_password:
            #     smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.sendmail(settings.sender_email, payload.to, msg.as_string())

    async def list_emails(
            self,
            from_date=None,
            to_date=None,
            sender=None,
            recipient=None,
            subject_contains=None,
    ):
        await self.imap.fetch_emails()
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
