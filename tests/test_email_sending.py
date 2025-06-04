def test_send_email(client):
    response = client.post("/api/v1/emails/send", json={
        "to": ["test@example.com"],
        "subject": "Test",
        "body": "<b>Hello</b>",
        "is_html": False
    })
    data = response.json()
    assert response.status_code == 200
    assert data.get("is_sent") is True
