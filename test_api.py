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

def test_api_convert_endpoint(client):
    # Create test image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".png", img)
    files = {"file": ("test_art.png", buf.tobytes(), "image/png")}
    res = client.post("/api/convert", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "image_data_url" in data
    assert data["benchmark_passed"] is True
    assert len(data["metadata"]["tags"]) == 6
    assert data["copyright_stamp"] == "© 2026 Color World"

def test_api_publish_endpoint(client):
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
    assert data["promo_code"] == "SUBSCRIBE50"
    assert data["discount"] == "50% OFF"

def test_gumroad_live_call_success():
    with patch("requests.post") as mock_post:
        # Mock product creation
        mock_product_resp = MagicMock()
        mock_product_resp.json.return_value = {
            "success": True,
            "product": {"id": "prod_12345", "short_url": "https://gumroad.com/l/prod_12345"}
        }
        # Mock promo code creation
        mock_promo_resp = MagicMock()
        mock_promo_resp.json.return_value = {"success": True}

        mock_post.side_effect = [mock_product_resp, mock_promo_resp]

        pub = GumroadPublisher(access_token="fake_token_123")
        res = pub.publish_product(name="Live Test", price_cents=399, tags=["a", "b", "c", "d", "e", "f"])

        assert res["success"] is True
        assert res["mode"] == "live"
        assert res["product_id"] == "prod_12345"
        assert res["product_url"] == "https://gumroad.com/l/prod_12345"
        assert res["price"] == "$3.99"
        assert res["is_licensed"] is True
