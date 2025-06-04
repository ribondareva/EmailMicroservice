import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@patch("app.services.stats_service.StatsService.get_stats", new_callable=AsyncMock)
async def test_email_stats(mock_get_stats):
    mock_get_stats.return_value = {
        "sent": 5,
        "received": 3,
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/emails/stats",
            params={
                "from_date": "2025-06-04T10:30:00",
                "to_date": "2025-06-05T10:30:00"
            }
        )
        print("Response status code:", response.status_code)
        print("Response json:", response.json())
        assert response.status_code == 200
        assert response.json() == {"sent": 5, "received": 3}
