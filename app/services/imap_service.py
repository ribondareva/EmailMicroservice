import asyncio
import imaplib
import email
import os
from datetime import datetime, timezone
from typing import List
from app.models.email import Email
from sqlalchemy.ext.asyncio import AsyncSession


class IMAPService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.imap_host = os.getenv("IMAP_HOST", "localhost")
        self.imap_port = int(os.getenv("IMAP_PORT", 1143))

    def _fetch_emails_sync(self) -> List[Email]:
        emails = []
        with imaplib.IMAP4(host=self.imap_host, port=self.imap_port) as mail:
            # Попытка залогиниться пустыми, если нужно (Mailpit обычно не требует)
            try:
                mail.login("", "")
            except Exception:
                pass

            mail.select("INBOX")
            status, messages = mail.search(None, "ALL")

            if status != 'OK':
                raise RuntimeError("Failed to search emails")

            for num in messages[0].split():
                status, data = mail.fetch(num, "(RFC822)")
                if status != 'OK':
                    continue
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                email_obj = Email(
                    direction="received",
                    sender=msg["From"],
                    recipients=msg["To"],
                    subject=msg["Subject"],
                    body=self._get_email_body(msg),
                    is_sent=False,
                    sent_at=datetime.now(timezone.utc),
                )
                emails.append(email_obj)
        return emails

    async def fetch_emails(self) -> List[Email]:
        emails = await asyncio.to_thread(self._fetch_emails_sync)

        # Добавляем и коммитим в базе
        for email_obj in emails:
            self.db.add(email_obj)
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        return emails

    def _get_email_body(self, msg: email.message.Message) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return msg.get_payload(decode=True).decode()
