from fastapi.testclient import TestClient
from app.main import app

def test_websocket_connect(user_token):
    client = TestClient(app)
    with client.websocket_connect(
        f"/api/ws/notifications?token={user_token["access_token"]}"
    ):
        pass