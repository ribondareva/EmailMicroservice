def test_email_stats(client):
    response = client.get("/emails/stats?from=2024-01-01&to=2025-01-01")
    assert response.status_code == 200
    assert "sent" in response.json()
    assert "received" in response.json()