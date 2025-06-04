from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    sent_at = Column(DateTime, default=datetime.utcnow)
