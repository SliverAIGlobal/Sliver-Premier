import os
import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app import app
from engine import ColoringPageEngine, MetadataGenerator
from gumroad_client import GumroadPublisher

@pytest.fixture
def client():
    return TestClient(app)

def test_api_dashboard_get(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "2026 Color World" in res.text
    assert "Commercial Access Gate" in res.text

def test_api_corporate_dashboard_get(client):
    res = client.get("/corporate")
    assert res.status_code == 200
    assert "Corporate White Label" in res.text
    assert "Acme Global Corporation" in res.text

def test_api_convert_endpoint_custom_aspect_and_detail(client):
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".png", img)
    files = {"file": ("test_art.png", buf.tobytes(), "image/png")}
    data = {
        "aspect_ratio": "1:1",
        "detail_level": 0.2
    }
    res = client.post("/api/convert", files=files, data=data)
    assert res.status_code == 200
    resp = res.json()
    assert resp["success"] is True
    assert "image_data_url" in resp
    assert resp["benchmark_passed"] is True
    assert resp["dimensions"] == "400x400"
    assert len(resp["metadata"]["tags"]) == 6
    assert "junior minimal" in resp["metadata"]["tags"]
    assert resp["copyright_stamp"] == "© 2026 Color World"

def test_api_publish_endpoints(client):
    payload = {
        "name": "Magic Forest Coloring Template",
        "price_cents": 399,
        "tags": ["magic forest", "coloring page", "line art", "2026 color world", "printable template", "instant download"],
        "promo_code": "SUBSCRIBE50"
    }
    res = client.post("/api/publish", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["price"] == "$3.99"
    assert data["is_licensed"] is True

    # Bundle endpoint
    b_res = client.post("/api/publish/bundle")
    assert b_res.status_code == 200
    assert b_res.json()["price"] == "$49.99"

    # Corporate endpoint
    c_res = client.post("/api/publish/corporate")
    assert c_res.status_code == 200
    assert c_res.json()["price"] == "$5000.00"

def test_api_license_endpoints(client):
    v_res = client.post("/api/license/verify", json={"product_id": "p_101", "license_key": "KEY-123"})
    assert v_res.status_code == 200
    assert v_res.json()["success"] is True

    e_res = client.post("/api/license/enable", json={"product_id": "p_101", "license_key": "KEY-123"})
    assert e_res.status_code == 200
    assert e_res.json()["success"] is True

    d_res = client.post("/api/license/disable", json={"product_id": "p_101", "license_key": "KEY-123"})
    assert d_res.status_code == 200
    assert d_res.json()["success"] is True

def test_api_financial_endpoints(client):
    earn_res = client.get("/api/earnings?year=2025")
    assert earn_res.status_code == 200
    assert earn_res.json()["success"] is True

    pay_res = client.get("/api/payouts")
    assert pay_res.status_code == 200
    assert pay_res.json()["success"] is True
