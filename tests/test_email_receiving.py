import pytest
from unittest.mock import patch, MagicMock
from app.services.imap_service import IMAPService
from app.models.email import Email
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
@patch("imaplib.IMAP4")
async def test_fetch_emails(mock_imap, db_session: AsyncSession):
    # Настройка моков для IMAP
    mock_conn = MagicMock()
    mock_imap.return_value = mock_conn

    # Имитация успешного подключения и поиска писем
    mock_conn.select.return_value = ("OK", [b"1"])
    mock_conn.search.return_value = ("OK", [b"1 2 3"])

    # Имитация письма
    mock_conn.fetch.return_value = (
        "OK",
        [(b"1 (RFC822 {123}", b"From: test@example.com\r\nSubject: Test\r\n\r\nBody")]
    )

    # Создаем сервис с тестовой сессией БД
    service = IMAPService(db_session)
    emails = await service.fetch_emails()

    # Проверяем, что письма сохранены в БД
    assert len(emails) == 3  # 3 письма в моке
    assert isinstance(emails[0], Email)