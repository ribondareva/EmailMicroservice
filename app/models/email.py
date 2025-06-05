from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    direction = Column(String, default="sent")  # sent / received
    sender = Column(String)
    recipients = Column(Text, nullable=True)
    subject = Column(String)
    body = Column(String)
    is_sent = Column(Boolean, default=True)
    sent_at = Column(TIMESTAMP(timezone=True), nullable=False)
