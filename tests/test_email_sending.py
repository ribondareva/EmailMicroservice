def test_send_email(client):
    response = client.post("/emails/send", json={
        "to": ["test@mail.local"],
        "subject": "Test",
        "body": "<b>Hello</b>"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "sent"