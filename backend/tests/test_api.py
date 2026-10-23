from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():assert client.get("/healthz").json()["status"]=="ok"
def test_citizen_cannot_review():
 r=client.post("/api/v1/alerts/unknown/review",json={"decision":"valid_signal","note":""},headers={"X-Demo-Role":"citizen"})
 assert r.status_code==403
